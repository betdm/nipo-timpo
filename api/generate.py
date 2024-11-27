import random
import string
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1311226714629865472/-sv_iEl2EFgvRnvYi1-aJLXQT-an_xoo-bIkP5D4w-GHJuaf_rnytTJiMfT-MRgyVy3s"

def generate_code():
    characters = string.ascii_letters + string.digits
    return f"https://discord.gift/{''.join(random.choice(characters) for _ in range(16))}"

@app.route("/generate", methods=["POST"])
def generate_and_send():
    try:
        data = request.json
        count = int(data.get("count", 0))

        if count <= 0:
            return jsonify({"message": "Invalid code count provided."}), 400

        codes = [generate_code() for _ in range(count)]
        for code in codes:
            embed = {
                "title": "New Nitro Code!",
                "description": f"Code: {code}",
                "color": 7506394,
            }
            response = requests.post(WEBHOOK_URL, json={"embeds": [embed]})

            if response.status_code != 204:
                return jsonify({"message": "Failed to send one or more codes.", "error": response.text}), 500

        return jsonify({"message": f"Successfully sent {count} Nitro codes!"})

    except Exception as e:
        return jsonify({"message": "An error occurred.", "error": str(e)}), 500
