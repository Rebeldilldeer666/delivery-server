import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"status": "server running"})


@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    event = request.get_json(silent=True) or {}
    print("Stripe event received:", event)
    return jsonify({"received": True}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
