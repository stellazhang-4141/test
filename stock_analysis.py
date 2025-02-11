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

        # Extract key financial data, merging all relevant financial metrics
        def extract_financial_data(df, keys):
            data = {}
            for key in keys:
                if key in df.index:
                    value = df.loc[key].values[0]
                    data[key] = value if pd.notna(value) else "N/A"
                else:
                    data[key] = "N/A"
            return data

        financial_keys = [
            "Total Revenue", "Operating Income", "Net Income", "Total Assets",
            "Total Liabilities Net Minority Interest", "Total Equity Gross Minority Interest",
            "Total Cash From Operating Activities", "Total Cash From Financing Activities"
        ]

        financial_data = {**extract_financial_data(stock.financials, financial_keys),
                          **extract_financial_data(stock.balance_sheet, financial_keys),
                          **extract_financial_data(stock.cashflow, financial_keys)}
        
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
            "financial_data": financial_data,
            "key_metrics": key_metrics,
        }
        return stock_info
    except Exception as e:
        return {"error": f"Unable to retrieve data for {symbol}: {str(e)}"}

def predict_stock_trend(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="6mo")
        last_close = hist["Close"][-1]

        # Predict next 30 business days
        future_dates = pd.date_range(hist.index[-1], periods=30, freq="B")
        future_prices = [last_close * (1 + 0.001 * i) for i in range(30)]

        # Generate future stock price trend chart
        plt.figure(figsize=(10, 5))
        plt.plot(future_dates, future_prices, label="Predicted Price", color="red")
        plt.title(f"{symbol} Future Stock Price Projection")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()

        img = BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        future_plot_url = base64.b64encode(img.getvalue()).decode()

        return f"Predicted future stock price ({future_dates[-1].date()}): ${future_prices[-1]:.2f}", future_plot_url
    except Exception as e:
        return f"Prediction failed: {str(e)}", None