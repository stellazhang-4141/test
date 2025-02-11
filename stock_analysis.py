import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1y")

        # 生成股价趋势图
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
    except Exception as e:
        return {"error": f"无法获取 {symbol} 的数据: {str(e)}"}

def predict_stock_trend(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="6mo")
        last_close = hist["Close"][-1]
        
        # 未来股价预测（使用简单趋势线估计）
        future_price = last_close * 1.02  # 未来股价的简单估计
        future_date = pd.date_range(hist.index[-1], periods=30, freq='B')
        future_prices = [last_close * (1 + 0.0008 * i) for i in range(30)]

        # 生成未来股价趋势图
        plt.figure(figsize=(10, 5))
        plt.plot(future_date, future_prices, label="Future Price", color="red")
        plt.title(f"{symbol} Future Stock Price Projection")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        
        img = BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        future_plot_url = base64.b64encode(img.getvalue()).decode()

        return f"预计未来股价 ({future_date[-1].date()}): {future_price:.2f} USD", future_plot_url
    except Exception as e:
        return f"预测失败: {str(e)}", None

