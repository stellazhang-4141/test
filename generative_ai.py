from transformers import pipeline
import yfinance as yf
import pandas as pd

def summarize_stock_trend(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="1mo")  # Get the past one month stock data
        
        # Calculate price change and trend
        start_price = hist["Close"].iloc[0]
        end_price = hist["Close"].iloc[-1]
        change_percent = ((end_price - start_price) / start_price) * 100
        trend = "upward" if change_percent > 0 else "downward"
        
        # Calculate highest and lowest prices
        max_price = hist["Close"].max()
        min_price = hist["Close"].min()
        max_date = hist["Close"].idxmax().date()
        min_date = hist["Close"].idxmin().date()
        
        # Calculate average daily volatility
        daily_changes = hist["Close"].pct_change().dropna() * 100
        avg_daily_change = daily_changes.abs().mean()
        
        # Construct detailed descriptive text
        trend_text = (
            f"In the past month, {stock_symbol}'s stock price changed from ${start_price:.2f} to ${end_price:.2f}, "
            f"showing an overall {trend} trend with a percentage change of approximately {change_percent:.2f}%.\n"
            f"The highest price was on {max_date} at ${max_price:.2f}, while the lowest price was on {min_date} at ${min_price:.2f}.\n"
            f"The average daily price fluctuation was around {avg_daily_change:.2f}%."
        )
        
        summarizer = pipeline("summarization")
        summary = summarizer(trend_text, max_length=150, min_length=50, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        return f"AI analysis failed: {str(e)}"
