from transformers import pipeline

def summarize_stock_trend(stock_symbol):
    try:
        news = get_stock_news(stock_symbol)  # 获取股票相关新闻
        summarizer = pipeline("summarization")
        summary = summarizer(news, max_length=100, min_length=30, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        return f"AI 分析失败: {str(e)}"

def get_stock_news(stock_symbol):
    # 模拟新闻数据，实际项目中可接入 API
    return f"{stock_symbol} 公司近期市场表现良好，投资者关注其财报发布。"

