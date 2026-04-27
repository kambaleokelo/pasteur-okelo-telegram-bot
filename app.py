# ============================================================
# 🥷 PASTEUR OKELO - TradingView → Telegram Bridge
# Déploiement Render.com (Python Flask)
# ============================================================

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ============================================================
# 🔐 CONFIGURATION
# Mets ces variables dans Render Environment Variables
# ============================================================

TOKEN = os.getenv("TOKEN", "REMPLACE_PAR_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "REMPLACE_PAR_CHANNEL_ID")

TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ============================================================
# 📩 ENVOI TELEGRAM
# ============================================================

def send_telegram_message(message):
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        r = requests.post(TELEGRAM_URL, json=payload, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# ============================================================
# 🏠 TEST PAGE
# ============================================================

@app.route("/", methods=["GET"])
def home():
    return "🥷 PASTEUR OKELO BOT TELEGRAM BRIDGE ACTIF"

# ============================================================
# 📈 WEBHOOK TRADINGVIEW
# ============================================================

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json if request.is_json else request.form.to_dict()

    pair   = data.get("pair", "UNKNOWN")
    signal = data.get("signal", "SIGNAL")
    price  = data.get("price", "0")
    time_  = data.get("time", "NOW")

    message = f"""
🥷 <b>PASTEUR OKELO ELITE IA</b>

📊 Paire : <b>{pair}</b>
📈 Signal : <b>{signal}</b>
💰 Prix : <b>{price}</b>
⏰ Heure : <b>{time_}</b>

🔥 Bonne discipline = Victoire
"""

    result = send_telegram_message(message)

    return jsonify({
        "status": "success",
        "telegram": result
    })

# ============================================================
# 🚀 START SERVER
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)