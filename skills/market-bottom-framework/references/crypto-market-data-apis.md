# Crypto Tail-Risk Data Sources

What actually prices a crypto black swan, what each source can and cannot answer, and the
one API quirk that silently truncates every history you fetch with it.

Companion to SKILL.md §3 (mechanism classes) and the load-bearing assertion in §8.

## Deribit public API — the only source of crypto tail pricing

Base: `https://www.deribit.com/api/v2/public/`

| Endpoint | Gives | Answers |
|---|---|---|
| `get_volatility_index_data?currency=BTC&start_timestamp=&end_timestamp=&resolution=3600` | DVOL — the implied volatility of the options surface, one point per bar | how the options market prices *volatility* now vs its own history |
| `get_book_summary_by_currency?currency=BTC&kind=option` | per-instrument open interest, mark price, greeks | where open interest is concentrated; the strike structure the market actually pays for |
| `get_instruments?currency=BTC&kind=option` | instrument list with expiry and strike | the contract universe behind the above |

### The window quirk — the one that silently eats your history

**A response is capped at 1000 points, and when the requested range is wider than the cap,
the API returns the LAST 1000 points of the range, not the first.** A single
"give me everything" request therefore yields a full-looking array that silently begins
only a few years ago — it reads as complete data and is not.

Two traps around it:

- The response carries a continuation timestamp, but **advancing it does not move the
  window** — the next request returns the same last-1000 slice. The array appears to grow
  while holding no new observations. Advance `start_timestamp` past the last returned
  point instead, and re-check that the returned points are genuinely new.
- Testing with a recent window hides the problem: a short range fits inside the cap, so
  the first request looks correct.

**Fix: chunk by calendar year.** Each yearly window is ~365 daily points, comfortably
under the cap, and the windows tile the full history with no gap. Then:

1. Dedupe by timestamp, keeping the **last** value for a repeated stamp, and sort
   ascending.
2. Assert the resulting series has no duplicate timestamps, no downward step, and no
   gap larger than a few days — a wrong window shows up as a gap, not an error.
3. **Assert the chunking is load-bearing:** the artifact's earliest observation must be
   EARLIER than the earliest point a single unchunked request returns. Without this
   assertion the fix can regress silently, leaving a short but perfectly well-formed
   series that every other check accepts.

Keep the window unit in the artifact, not only in the prose — see SKILL.md §1.

### Reading DVOL correctly

- **Percentile of its own history, not level across assets.** DVOL's normal range depends
  on the asset's volatility regime and on how much history you have; a reading of "58"
  means something only against that series' own distribution. Compute the percentile over
  the longest history available and report the comparison window.
- **A spike is not the same as tail pricing.** DVOL rising measures the options market
  repricing volatility; it does not measure the probability of a specific mechanism
  event. A tail report needs both: the implied-vol reading for *how the market prices
  risk now*, and a separate base rate for *how often the mechanism has fired*.
- **Seal the last bar.** The final daily bar may still be forming; use the last settled
  day, and apply the same as-of rule across every panel.

## Prediction markets — paths, not mechanisms

Prediction markets price **outcome paths**: "BTC below $X", "ETH above $Y", rate and
policy paths. They are excellent evidence for macro/transmission inputs and for price-path
scenarios.

They are almost silent on **mechanism-class** risk — depeg, exploit, exchange or custodian
insolvency, bridge failure. Tag-filtering a crypto category returns a large universe of
price-path contracts and essentially nothing about mechanism failure.

So: a mechanism-class tail report cannot source its probabilities from a prediction-market
query. Build them from a **base-rate table**:

| Field | Meaning |
|---|---|
| mechanism class | the failure type itself (depeg / exploit / insolvency / bridge / custody) |
| event date | the settlement date, not the announcement date |
| denominator | the exposure at risk over the same span (assets-years, bridges-years, custodians-years) |
| loss severity | measured in the affected asset, not in the announcing headline |
| survivor note | assets/bridges/custodians that failed without ever being in the sample |

The denominator is the part that is usually missing, and it is the part that decides
whether the base rate can be compared to any other market's history at all.

Filter mechanics, parameter names, and the coverage caveat:
`research/polymarket`.

## Other crypto stress indicators (flow, not probability)

Funding rates, futures basis, open interest in perps, and liquidation prints describe
**positioning and flow pressure**. They are legitimate environment-gate and
leading-condition layers in the framework. They are not probabilities of a mechanism
event, and labelling them as such is the most common overclaim in a crypto tail report.

When a percentile is quoted from these, name the window unit explicitly (observation
count vs calendar days) and carry the unit in the artifact.

## Pitfalls

| Pitfall | Guard |
|---|---|
| One wide history request treated as full history | chunk by year; assert coverage exceeds the unchunked window |
| Continuation timestamp believed to advance the window | verify the returned points are new; advance `start_timestamp` instead |
| Recent-window test used to validate the fetch | test with the oldest window, not the newest |
| DVOL level compared across assets | percentile within the asset's own longest history |
| Implied vol read as the probability of a mechanism event | keep the two in separate layers of the framework |
| Prediction-market odds used for mechanism-class tail risk | build a base-rate table instead; market odds only for paths |
| Base rate quoted without a denominator | state events per exposure-year, and the survivor note |
| Last (still-forming) bar read as a settled close | seal every series to the last settled bar, one as-of rule throughout |