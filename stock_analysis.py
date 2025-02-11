import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")

    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist["Close"], label="Stock Price", color="blue")
    plt.title(f"{symbol} Stock Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()

    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    stock_info = {
        "name": stock.info.get("longName", "Unknown"),
        "symbol": symbol,
        "price": stock.history(period="1d")["Close"][0],
        "pe_ratio": stock.info.get("trailingPE", "N/A"),
        "eps": stock.info.get("trailingEps", "N/A"),
        "plot_url": plot_url,
    }
    return stock_info

def predict_stock_price(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="6mo")
    last_close = hist["Close"][-1]

    prediction = last_close * 1.02  # 预测涨 2%
    return f"预计未来股价：{prediction:.2f} USD"
