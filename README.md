# AIxTech crypto intel v0.23: paper-only trading information system

Advanced research harness for automated cryptocurrency **information** and paper strategy evaluation.
Builds on [zeekiankok92/aixtech-crypto-intel](https://github.com/zeekiankok92/aixtech-crypto-intel) and prior enhanced versions under kkzee92 (v0.22 and earlier).

It does not place live orders, does not store exchange secrets, and is not financial advice.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![version](https://img.shields.io/badge/version-0.23.0-blue)
![mode](https://img.shields.io/badge/execution-paper%20only-orange)
![Licence](https://img.shields.io/badge/licence-MIT-green)

## Enhancements in v0.23

- Ichimoku cloud proxy (tenkan/kijun) and ADX-like trend strength for confirmation on majors, DeFi, RWA, L2.
- RSI divergence detection and multi-timeframe momentum consistency filters.
- Portfolio-level correlation proxy between asset classes for concentration risk.
- Refined anomaly scoring with volume-price divergence and kurtosis.
- Expanded secret redaction: BIP39 seed phrase proxies, more private key formats, AWS/GitHub/JWT patterns.
- Strengthened zero-trust: simulated lineage encryption, isolation anomaly, data residency checks.
- Updated architecture and strategy docs with per-class refinements.

## What it does

- Eight asset classes with refined multi-factor research rules including Ichimoku/ADX.
- Multi-scale regime + volatility tier + advanced anomaly scoring + correlation gates.
- Signals with EMA, MACD, Bollinger/Keltner, Supertrend, Ichimoku, StochRSI, volume-delta, RSI divergence, then multi-gate risk.
- Paper-only backtests with class costs; enhanced hash-chained audit with encrypted lineage simulation.
- Synthetic candles only. No network by default.

| Asset class | Enhanced research rule (v0.23) | Risk cap | Cost |
|---|---|---|---|
| Major | Multi-EMA + Ichimoku + ADX + Supertrend + Keltner + MACD + StochRSI + volume-delta + no RSI div; stand aside stress/high-vol/anomaly | 8% | 8 bps |
| Large-cap alt | Volume-delta confirmed breakout with multi-TF momentum + Keltner + ADX | 4% | 14 bps |
| Stablecoin | Adaptive peg + multi-stat (z, consecutive, skew, kurtosis) alerts only | 0% | n/a |
| DeFi | Calm multi-scale + Ichimoku + Supertrend + Keltner + low anomaly + ADX | 2% | 22 bps |
| Meme | Qualified burst with volume-delta, StochRSI not extreme, consistency, RSI filter | 0.5% | 45 bps |
| L2 | Multi-period RS + relative volume-delta + correlation vs non-stress benchmark + ADX | 3% | 16 bps |
| RWA | Slow Ichimoku/Keltner low-vol trend; adaptive gap halt + ADX | 2% | 12 bps |
| Perpetual | Funding carry with adaptive drift, Supertrend/Ichimoku alignment, low anomaly | 2% | 10 bps |

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/make_fixtures.py
PYTHONPATH=src python -m crypto_intel scan fixtures/candles_synthetic.json
```

## Controls

Paper-only. No live credentials. Class caps, adaptive confidence and sizing, kill switch, drawdown, statistical anomaly + correlation gates, hash-chained audit with lineage, expanded redaction (incl. BIP39), PDPA tripwire, gitleaks. Zero-trust research design with simulated encryption.

## Honesty

No live exchange connector. Scores describe synthetic fixtures. Not investment, legal, or compliance advice. Research only.
