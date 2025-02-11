from flask import Flask, render_template, request
from stock_analysis import get_stock_info, predict_stock_price
from generative_ai import summarize_stock_trend

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    stock_data = None
    prediction = None
    summary = None

    if request.method == "POST":
        stock_symbol = request.form.get("stock_symbol").upper()
        stock_data = get_stock_info(stock_symbol)
        prediction = predict_stock_price(stock_symbol)
        summary = summarize_stock_trend(stock_symbol)

    return render_template("search.html", stock_data=stock_data, prediction=prediction, summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
