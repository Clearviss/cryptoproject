import ccxt
from flask import Flask, request, jsonify
from flask_cors import CORS

# Inicjalizacja aplikacji Flask
app = Flask(__name__)
CORS(app)  # Dodanie wsparcia dla CORS, aby frontend mógł się komunikować z backendem

# Inicjalizacja Binance API za pomocą ccxt
exchange = ccxt.binance({
    'enableRateLimit': True  # Włączenie automatycznego zarządzania limitami API
})

# Prosty portfel (przykład)
portfolio = {
    "BTC": 0.1,  # 0.1 BTC
    "ETH": 2.0,  # 2 ETH
    "ADA": 500   # 500 ADA
}

# Funkcja do pobierania ceny z Binance
def fetch_price(symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']  # Zwraca ostatnią cenę
    except Exception as e:
        print(f"Error fetching price for {symbol}: {str(e)}")
        return None

# Endpoint do pobierania portfolio
@app.route("/portfolio", methods=["GET"])
def get_portfolio():
    total_value = 0
    portfolio_values = []

    try:
        for symbol, amount in portfolio.items():
            # Pobieranie ceny z Binance
            price = fetch_price(f"{symbol}/USDT")
            if price is None:
                return jsonify({"error": f"Could not fetch price for {symbol}"}), 500
            value = price * amount
            total_value += value
            portfolio_values.append({
                "symbol": symbol,
                "amount": amount,
                "price": price,
                "value": value
            })

        return jsonify({
            "portfolio": portfolio_values,
            "total_value_usdt": total_value
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Endpoint do dodawania kryptowalut do portfela
@app.route("/add", methods=["POST"])
def add_to_portfolio():
    data = request.json
    symbol = data.get("symbol").upper()
    amount = data.get("amount")

    if not symbol or not amount:
        return jsonify({"error": "Symbol and amount are required"}), 400

    # Dodawanie nowego symbolu lub zwiększanie ilości istniejącego
    portfolio[symbol] = portfolio.get(symbol, 0) + amount
    return jsonify({"message": f"Added {amount} {symbol} to your portfolio"})

# Endpoint do usuwania kryptowalut z portfela
@app.route("/remove", methods=["POST"])
def remove_from_portfolio():
    data = request.json
    symbol = data.get("symbol").upper()
    amount = data.get("amount")

    if not symbol or not amount:
        return jsonify({"error": "Symbol and amount are required"}), 400

    if symbol in portfolio:
        # Usuwanie lub zmniejszanie ilości kryptowaluty
        portfolio[symbol] -= amount
        if portfolio[symbol] <= 0:
            del portfolio[symbol]  # Usuwanie kryptowaluty, jeśli ilość wynosi 0 lub mniej
        return jsonify({"message": f"Removed {amount} {symbol} from your portfolio"})
    else:
        return jsonify({"error": f"{symbol} not found in portfolio"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Uruchomienie aplikacji na porcie 5000

