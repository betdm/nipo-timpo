import random
import string
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"

# Function to generate a random Nitro code
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
            # Embed payload for the Discord webhook
            embed = {
                "title": "New Nitro Code!",
                "description": f"Code: {code}",
                "color": 7506394,  # Discord blue color
            }
            # Send the embed to the Discord webhook
            response = requests.post(WEBHOOK_URL, json={"embeds": [embed]})
            if response.status_code != 204:
                return jsonify({"message": "Failed to send one or more codes."}), 500

        return jsonify({"message": f"Successfully sent {count} Nitro codes!"})

    except Exception as e:
        return jsonify({"message": "An error occurred.", "error": str(e)}), 500
