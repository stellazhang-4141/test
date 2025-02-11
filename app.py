from flask import Flask, render_template, request
from stock_analysis import get_stock_info, predict_stock_trend
from generative_ai import summarize_stock_trend

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    stock_data = None
    prediction = None
    trend_summary = None
    future_trend_plot = None
    
    if request.method == "POST":
        stock_symbol = request.form.get("stock_symbol").upper()
        stock_data = get_stock_info(stock_symbol)
        prediction, future_trend_plot = predict_stock_trend(stock_symbol)
        trend_summary = summarize_stock_trend(stock_symbol)

    return render_template("search.html", stock_data=stock_data, prediction=prediction, trend_summary=trend_summary, future_trend_plot=future_trend_plot)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

