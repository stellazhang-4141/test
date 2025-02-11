from transformers import pipeline

def summarize_stock_trend(stock_symbol):
    news = get_stock_news(stock_symbol)  # 获取相关新闻
    summarizer = pipeline("summarization")
    summary = summarizer(news, max_length=100, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

def get_stock_news(stock_symbol):
    return f"{stock_symbol} 公司近期市场表现良好，投资者关注其财报发布。"
