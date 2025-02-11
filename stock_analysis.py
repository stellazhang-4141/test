import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1y")
        
        # Generate stock price trend chart (1 year)
        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist["Close"], label="Stock Price", color="blue")
        plt.title(f"{symbol} Stock Price Trend (1 Year)")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        
        img = BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        # Generate last month stock price trend chart
        hist_month = stock.history(period="1mo")
        plt.figure(figsize=(10, 5))
        plt.plot(hist_month.index, hist_month["Close"], label="Stock Price (1 Month)", color="green")
        plt.title(f"{symbol} Stock Price Trend (1 Month)")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        
        img_month = BytesIO()
        plt.savefig(img_month, format="png")
        img_month.seek(0)
        plot_url_month = base64.b64encode(img_month.getvalue()).decode()

        # Extract key financial data
        financials = stock.financials.iloc[:, :1]  # Latest financial data
        balance_sheet = stock.balance_sheet.iloc[:, :1]  # Latest balance sheet data
        cashflow = stock.cashflow.iloc[:, :1]  # Latest cashflow data
        
        key_metrics = {
            "Market Cap": stock.info.get("marketCap", "N/A"),
            "P/B Ratio": stock.info.get("priceToBook", "N/A"),
            "P/E Ratio": stock.info.get("trailingPE", "N/A"),
            "EPS": stock.info.get("trailingEps", "N/A"),
        }

        stock_info = {
            "name": stock.info.get("longName", "Unknown"),
            "symbol": symbol,
            "price": stock.history(period="1d")["Close"][0],
            "plot_url": plot_url,
            "plot_url_month": plot_url_month,
            "financials": financials.to_html(),
            "balance_sheet": balance_sheet.to_html(),
            "cashflow": cashflow.to_html(),
            "key_metrics": key_metrics,
        }
        return stock_info
    except Exception as e:
        return {"error": f"Unable to retrieve data for {symbol}: {str(e)}"}
