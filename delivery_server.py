import os
from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCT_LINKS = {
    "prompt_pack": "https://yourdomain.com/prompt_pack.zip",
    "side_hustle": "https://yourdomain.com/side_hustle.pdf",
}


@app.route("/")
def home():
    return jsonify({"status": "server running"})


@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    data = request.get_json(silent=True) or {}

    customer_email = (
        data.get("data", {})
        .get("object", {})
        .get("customer_details", {})
        .get("email")
    )

    product_id = (
        data.get("data", {})
        .get("object", {})
        .get("metadata", {})
        .get("product", "prompt_pack")
    )

    download_link = PRODUCT_LINKS.get(product_id)

    return jsonify({
        "status": "stripe webhook received",
        "customer_email": customer_email,
        "product_id": product_id,
        "download_link": download_link,
    })


@app.route("/webhook/digistore", methods=["POST"])
def digistore_webhook():
    buyer_email = request.form.get("buyer_email")
    product_id = request.form.get("product_id", "prompt_pack")
    download_link = PRODUCT_LINKS.get(product_id)

    return jsonify({
        "status": "digistore webhook received",
        "buyer_email": buyer_email,
        "product_id": product_id,
        "download_link": download_link,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
