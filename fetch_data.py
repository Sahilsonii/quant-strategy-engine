import yfinance as yf
import pandas as pd

# Download data
df = yf.download("BTC-USD", period="6mo", interval="1d")

# Clean data
df = df.dropna()
df.columns = [col[0].lower() if isinstance(col, tuple) else col.lower() for col in df.columns]

# Save
df.to_csv("data/ohlc_clean.csv")

print("✅ Data saved successfully!")