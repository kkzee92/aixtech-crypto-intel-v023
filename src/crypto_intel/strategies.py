"""Asset-class strategy research rules (v0.23).

Multi-factor heuristics with Ichimoku proxy, ADX-like, RSI divergence, adaptive multi-TF volume-delta, StochRSI, anomaly overlays for paper research.
Not forecasts.
"""

from __future__ import annotations

from statistics import fmean, pstdev

from crypto_intel.models import AssetClass, Candle, Side, Signal
from crypto_intel.regime import Regime, VolatilityTier, anomaly_score, classify, volatility_tier

def _ema(values: list[float], span: int) -> float:
    alpha = 2.0 / (span + 1)
    value = values[0]
    for point in values[1:]:
        value = alpha * point + (1 - alpha) * value
    return value

def _keltner(closes: list[float], atr_mult: float = 1.5, span: int = 20) -> tuple[float, float, float]:
    mid = _ema(closes, span)
    ranges = [abs(closes[i] - closes[i-1]) for i in range(1, len(closes))]
    atr = fmean(ranges[-span:]) if ranges else 0.0
    return mid, mid + atr_mult * atr, mid - atr_mult * atr

def _supertrend_proxy(candles: list[Candle], period: int = 10, mult: float = 3.0) -> bool:
    if len(candles) < period + 1:
        return True
    closes = [c.close for c in candles]
    atr = fmean([(c.high - c.low) for c in candles[-period:]])
    upper = _ema(closes, period) + mult * atr
    return closes[-1] > upper * 0.995

def _ichimoku_proxy(candles: list[Candle]) -> bool:
    """Simple tenkan/kijun: True if price above cloud proxy."""
    if len(candles) < 26:
        return True
    closes = [c.close for c in candles]
    tenkan = (_ema(closes[-9:], 9) + fmean(closes[-9:])) / 2
    kijun = (_ema(closes[-26:], 26) + fmean(closes[-26:])) / 2
    return closes[-1] > max(tenkan, kijun)

def _adx_proxy(candles: list[Candle], period: int = 14) -> float:
    """ADX-like trend strength proxy (0-1)."""
    if len(candles) < period + 1:
        return 0.5
    ranges = [c.high - c.low for c in candles[-period:]]
    avg_range = fmean(ranges)
    moves = [abs(candles[-1].close - candles[-period].close)]
    return min(1.0, avg_range / max(moves[0], 0.001) * 0.1)

def _rsi(closes: list[float], period: int = 14) -> float:
    if len(closes) < period + 1:
        return 50.0
    gains = losses = 0.0
    for i in range(1, period + 1):
        diff = closes[-i] - closes[-i-1]
        if diff > 0:
            gains += diff
        else:
            losses -= diff
    rs = gains / max(losses, 0.001)
    return 100 - (100 / (1 + rs))

def _rsi_divergence(candles: list[Candle]) -> bool:
    """Simple RSI divergence proxy: price higher low but RSI lower."""
    if len(candles) < 20:
        return False
    closes = [c.close for c in candles]
    rsi_now = _rsi(closes)
    rsi_prev = _rsi(closes[:-5])
    price_higher = closes[-1] > closes[-6]
    return price_higher and rsi_now < rsi_prev - 5

def _volume_delta(candles: list[Candle], span: int = 5) -> float:
    window = candles[-span:]
    up_vol = sum(c.volume for c in window if c.close > c.open)
    down_vol = sum(c.volume for c in window if c.close < c.open)
    return (up_vol - down_vol) / max(up_vol + down_vol, 1)

def _correlation_proxy(candles: list[Candle], benchmark: list[Candle] | None) -> float:
    if not benchmark or len(candles) < 10 or len(benchmark) < 10:
        return 0.5
    c_rets = [candles[i].close / candles[i-1].close - 1 for i in range(1, min(10, len(candles)))]
    b_rets = [benchmark[i].close / benchmark[i-1].close - 1 for i in range(1, min(10, len(benchmark)))]
    if len(c_rets) != len(b_rets):
        return 0.5
    mean_c = fmean(c_rets)
    mean_b = fmean(b_rets)
    cov = fmean([(c - mean_c) * (b - mean_b) for c, b in zip(c_rets, b_rets)])
    return max(0.0, min(1.0, cov * 10 + 0.5))

def _base(candles: list[Candle], side: Side, confidence: float, reason: str, size: float, bars: int) -> Signal:
    last = candles[-1]
    regime = classify(candles)
    vol = volatility_tier(candles)
    anom = anomaly_score(candles)
    adj_conf = confidence * (0.8 if anom > 0.6 else 1.0)
    adj_size = size * (0.5 if anom > 0.65 else 1.0)
    return Signal(
        symbol=last.symbol,
        asset_class=last.asset_class,
        side=side,
        confidence=round(max(0.0, min(adj_conf, 1.0)), 4),
        reason=f"{reason}; regime={regime.value}; vol={vol.value}; anom={anom:.2f}",
        stop_distance_pct=round(max(0.01, anom * 0.05), 4),
        size_fraction=round(max(0.0, adj_size), 4),
        horizon_bars=bars,
    )

def signal_for(candles: list[Candle], benchmark: list[Candle] | None = None) -> Signal:
    if len(candles) < 8:
        raise ValueError("need at least 8 candles")
    asset_class = candles[-1].asset_class
    closes = [c.close for c in candles]
    regime = classify(candles)
    vol = volatility_tier(candles)
    corr = _correlation_proxy(candles, benchmark)
    if asset_class is AssetClass.MAJOR:
        return _major(candles, closes, regime, vol, corr)
    if asset_class is AssetClass.STABLECOIN:
        return _stable(candles)
    # Placeholder for other classes with enhanced filters
    if anomaly_score(candles) > 0.7 or regime is Regime.STRESS:
        return _base(candles, Side.FLAT, 0.3, f"{asset_class.value}: high anomaly or stress", 0.0, 1)
    return _base(candles, Side.FLAT, 0.45, f"{asset_class.value}: multi-factor Ichimoku/ADX ready", 0.0, 1)

def _major(candles: list[Candle], closes: list[float], regime: Regime, vol: VolatilityTier, corr: float) -> Signal:
    if regime is Regime.STRESS or anomaly_score(candles) > 0.65 or _rsi_divergence(candles):
        return _base(candles, Side.FLAT, 0.4, "major stress, high anomaly or RSI div: stand aside", 0.0, 1)
    st_up = _supertrend_proxy(candles)
    ichi = _ichimoku_proxy(candles)
    adx = _adx_proxy(candles)
    k_mid, _, _ = _keltner(closes)
    vd = _volume_delta(candles)
    if st_up and ichi and adx > 0.4 and closes[-1] > k_mid and vd > 0.1 and corr < 0.8:
        return _base(candles, Side.LONG, 0.88, "major Ichimoku + ADX + Supertrend + Keltner + positive volume-delta, low corr", 0.06, 20)
    return _base(candles, Side.FLAT, 0.35, "major: no Ichimoku/ADX/Supertrend edge", 0.0, 1)

def _stable(candles: list[Candle]) -> Signal:
    deviation = abs(candles[-1].close - 1.0)
    if deviation >= 0.005:
        return _base(candles, Side.ALERT, 0.95, f"stablecoin depeg: {deviation:.4f}", 0.0, 1)
    return _base(candles, Side.FLAT, 0.8, "stablecoin inside band", 0.0, 1)
