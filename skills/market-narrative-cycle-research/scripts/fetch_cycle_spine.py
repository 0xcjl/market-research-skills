#!/usr/bin/env python3
"""Build a market cycle spine: pull daily klines, cache them, compute windows and anchors.

Usage:
    python3 fetch_cycle_spine.py --symbol BTCUSDT --start 2019-01-01 --outdir ./data

Outputs (in --outdir):
    <symbol>_daily.csv   raw daily klines: date,open,high,low,close,volume
    cycle_spine.json     period-window returns, per-window highs/lows, ATH, drawdown

Rules baked in:
  * today's bar is EXCLUDED everywhere. A daily candle stamped with its open time is still
    forming until the UTC day ends; reading it as a close makes the number unreproducible.
    The as-of date is written into the JSON.
  * period return base = the last settled close STRICTLY BEFORE the window opens.
  * period windows are bucketed into a dict keyed by period, then sorted. Never mutate a
    list you may not have appended to yet.
  * the CSV header row is left for csv.DictReader to consume. Never pre-consume it.
  * the in-progress window is flagged; its partial return is not a window return.
"""

import argparse
import calendar
import csv
import json
import os
import time
import urllib.error
import urllib.request

KLINE_URL = "https://api.binance.com/api/v3/klines"


def fetch_klines(symbol, start_ms, limit=1000, retries=3):
    """Daily klines from the public exchange endpoint, paginated forward to now.

    Response shape: [[openTime_ms, open, high, low, close, volume, closeTime_ms, ...], ...]
    """
    rows, cur = [], start_ms
    while True:
        url = f"{KLINE_URL}?symbol={symbol}&interval=1d&startTime={cur}&limit={limit}"
        batch = None
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(url, timeout=30) as r:
                    batch = json.loads(r.read())
                break
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
                if attempt == retries - 1:
                    raise
                time.sleep(2 * (attempt + 1))
        if not batch:
            break
        rows.extend(batch)
        if len(batch) < limit:
            break
        cur = batch[-1][0] + 86400000
        time.sleep(0.3)
    return rows


def write_csv(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close", "volume"])
        for k in rows:
            d = time.strftime("%Y-%m-%d", time.gmtime(k[0] / 1000))
            w.writerow([d, k[1], k[2], k[3], k[4], k[5]])


def load_close(path):
    # The header row is consumed by DictReader, not by us.
    with open(path) as f:
        return {r["date"]: float(r["close"]) for r in csv.DictReader(f)}


def window_bounds(dates):
    """Map each half-year period to its (start, calendar-end) dates."""
    periods = {}
    for d in dates:
        y, m = int(d[:4]), int(d[5:7])
        key = f"{y}H1" if m <= 6 else f"{y}H2"
        periods[key] = (f"{y}-01-01", f"{y}-06-30") if m <= 6 else (f"{y}-07-01", f"{y}-12-31")
    return periods


def build_spine(closes, today_utc):
    """Window returns on the 'base = last close strictly before window opens' rule."""
    settled = {d: v for d, v in closes.items() if d < today_utc}
    if not settled:
        raise SystemExit("no settled bars - check the symbol and start date")
    windows = []
    for key, (start, cal_end) in window_bounds(sorted(settled)).items():
        seg = {d: v for d, v in settled.items() if start <= d <= cal_end}
        if not seg:
            continue
        end = max(seg)
        prior = [d for d in settled if d < start]
        base_date = max(prior) if prior else None
        base = settled.get(base_date)
        ret = round(settled[end] / base - 1, 4) if base else None
        hi_d = max(seg, key=seg.get)
        lo_d = min(seg, key=seg.get)
        windows.append({
            "window": key,
            "start": start,
            "end": end,
            "base_date": base_date,
            "base_close": base,
            "close": settled[end],
            "return": ret,
            "in_progress": cal_end >= today_utc,
            "window_high": {"date": hi_d, "close": seg[hi_d]},
            "window_low": {"date": lo_d, "close": seg[lo_d]},
        })
    windows.sort(key=lambda w: w["window"])
    ath_date, ath = max(settled.items(), key=lambda kv: kv[1])
    last_d = max(settled)
    return windows, {
        "ath_date": ath_date,
        "ath_close": ath,
        "last_settled_date": last_d,
        "last_settled_close": settled[last_d],
        "drawdown_from_ath": round(settled[last_d] / ath - 1, 4),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="BTCUSDT")
    ap.add_argument("--start", default="2019-01-01")
    ap.add_argument("--outdir", default="data")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    start_ms = calendar.timegm(time.strptime(args.start, "%Y-%m-%d")) * 1000
    rows = fetch_klines(args.symbol, start_ms)
    if not rows:
        raise SystemExit("no klines returned - check symbol/start")
    csv_path = os.path.join(args.outdir, f"{args.symbol.lower()}_daily.csv")
    write_csv(rows, csv_path)

    today_utc = time.strftime("%Y-%m-%d", time.gmtime())
    closes = load_close(csv_path)
    windows, summary = build_spine(closes, today_utc)

    art = {
        "symbol": args.symbol,
        "as_of": summary["last_settled_date"],
        "measurement_contract": (
            "daily UTC closes from the exchange public klines endpoint; "
            "period return base = last settled close strictly before the window opens; "
            "the forming bar of the current UTC day is excluded everywhere; "
            "windows flagged in_progress are partial and their return is not a window return"
        ),
        "windows": windows,
        "summary": summary,
        "source": f"{KLINE_URL} symbol={args.symbol} interval=1d, retrieved {today_utc}",
    }
    out_json = os.path.join(args.outdir, "cycle_spine.json")
    with open(out_json, "w") as f:
        json.dump(art, f, indent=1, ensure_ascii=False)

    print(f"as-of {summary['last_settled_date']} | ATH {summary['ath_date']} "
          f"${summary['ath_close']:,.0f} | last ${summary['last_settled_close']:,.0f} "
          f"({summary['drawdown_from_ath']:.1%})")
    print(f"{'window':<9}{'end':<12}{'close':>11}{'return':>9}{'high':>12}{'low':>12}  flag")
    for w in windows:
        ret = f"{w['return']:.0%}" if w["return"] is not None else "n/a"
        print(f"{w['window']:<9}{w['end']:<12}{w['close']:>11,.0f}{ret:>9}"
              f"{w['window_high']['close']:>12,.0f}{w['window_low']['close']:>12,.0f}"
              f"  {'partial' if w['in_progress'] else ''}")
    print(f"\nwrote {csv_path}\nwrote {out_json}")


if __name__ == "__main__":
    main()
