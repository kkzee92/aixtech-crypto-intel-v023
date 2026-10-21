# Asset-class strategy notes (v0.23)

Research heuristics with Ichimoku proxy, ADX-like strength, RSI divergence, adaptive multi-TF volume-delta, and anomaly overlays. Not forecasts.

Regime: trend / range / stress. Volatility tier: low/normal/high. Anomaly score includes kurtosis, volume-price divergence. Correlation proxy for portfolio gates.

## Major

Hypothesis: Liquid majors trend with Ichimoku + ADX + Supertrend + Keltner + multi-EMA alignment outside stress/high anomaly/RSI divergence, low correlation.
Entry: Ichimoku up, ADX > 0.4, Supertrend up, price above Keltner mid, positive MACD, StochRSI not stretched, positive volume-delta, no RSI div, corr < 0.8.
Invalidation: Stress, high anomaly, RSI divergence, or Supertrend flip.
Horizon: 8/20 bars. Cap 8%. Cost 8 bps.

## Large-cap alt

Hypothesis: Breakouts need volume-delta confirmation, multi-TF momentum, ADX, and Keltner outside stress.
Entry: Close above prior high and Keltner upper, volume-delta > threshold, multi-period momentum positive, ADX support.
Cap 4%. Cost 14 bps.

## Stablecoin

Hypothesis: Statistical multi-metric peg deviation (z, consecutive, skew, kurtosis).
Alerts only. Size zero.

## DeFi

Hypothesis: Trend only in calm non-stress with Ichimoku, Supertrend, Keltner support, ADX, low anomaly.
Cap 2%. Cost 22 bps.

## Meme

Hypothesis: Qualified bursts with volume-delta consistency, StochRSI filter, RSI not extreme.
Hard 3-bar horizon. Cap 0.5%. Cost 45 bps.

## L2

Hypothesis: Multi-period relative strength with volume-delta, ADX, and correlation vs non-stress benchmark.
Cap 3%. Cost 16 bps.

## RWA

Hypothesis: Slow Ichimoku/Keltner trend; halt on adaptive gap or stress; ADX confirmation.
Cap 2%. Cost 12 bps.

## Perpetual

Hypothesis: Negative funding with contained drift, Supertrend/Ichimoku alignment, low anomaly.
Cap 2%. Cost 10 bps.

Out of scope: live orders, trade keys, future return claims.
