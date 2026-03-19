import pandas as pd

def detect_regime(df, i, config):
    trend_ma = config["trend_ma"]
    atr_window = config["atr_window"]

    # Calculate indicators
    ma = df['close'].rolling(trend_ma).mean()
    atr = (df['high'] - df['low']).rolling(atr_window).mean()

    # Avoid early rows
    if i < trend_ma:
        return "range"

    # Regime logic
    if df['close'].iloc[i] > ma.iloc[i]:
        return "trend"

    elif atr.iloc[i] > atr.quantile(0.7):
        return "volatile"

    elif atr.iloc[i] < atr.quantile(0.3):
        return "low_vol"

    else:
        return "range"