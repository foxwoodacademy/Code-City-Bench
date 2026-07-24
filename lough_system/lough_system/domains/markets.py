"""Market movement and investment trend analysis events."""

DOMAIN = "markets"
DESCRIPTION = "Market flux, volatility, trend, and risk signal analysis."

EVENTS = {
    "price_tick": "markets.price.tick",
    "volatility_shift": "markets.volatility.shift",
    "trend_signal": "markets.trend.signal",
    "risk_alert": "markets.risk.alert",
}

PERSONA = {
    "name": "Market Trend Analyst",
    "prompt_template": (
        "Given these market and system events, identify the strongest trend, "
        "volatility, or risk signal. Do not provide financial advice; describe "
        "observable evidence and uncertainty. Respond in one sentence."
    ),
    "location": "analyst.markets",
    "source": "analyst_markets",
    "event_key": "trend_signal",
}

