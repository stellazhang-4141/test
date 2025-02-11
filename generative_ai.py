from transformers import pipeline
import yfinance as yf
import pandas as pd

def summarize_stock_trend(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="1mo")  # 获取最近一个月的股价数据
        
        # 计算涨跌幅和趋势
        start_price = hist["Close"].iloc[0]
        end_price = hist["Close"].iloc[-1]
        change_percent = ((end_price - start_price) / start_price) * 100
        trend = "上涨" if change_percent > 0 else "下跌"
        
        # 构造描述性文本
        trend_text = (
            f"过去一个月，{stock_symbol} 的股价从 ${start_price:.2f} 变动至 ${end_price:.2f}，"
            f"整体呈现 {trend} 趋势，涨跌幅约为 {change_percent:.2f}%。"
        )
        
        summarizer = pipeline("summarization")
        summary = summarizer(trend_text, max_length=100, min_length=30, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        return f"AI 分析失败: {str(e)}"

