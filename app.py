from flask import Flask, render_template
import pandas as pd
import requests
import os

app = Flask(__name__)

# API Key (Replace with your actual API key from RapidAPI)
API_KEY = "your_api_key_here"
url = "https://uk-supermarkets-product-pricing.p.rapidapi.com/supermarkets"

# Fetch price data
def get_prices():
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "uk-supermarkets-product-pricing.p.rapidapi.com"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

@app.route("/")
def home():
    data = get_prices()
    if not data:
        return "<h2>Failed to load price data.</h2>"

    items = []
    for store in data:
        for product in store['products']:
            items.append({"Store": store['name'], "Product": product['name'], "Price": f"£{product['price']}"})

    df = pd.DataFrame(items)
    return render_template("dashboard.html", tables=[df.to_html(classes='table table-striped')])

if __name__ == "__main__":
    app.run(debug=True)
