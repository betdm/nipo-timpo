from flask import Flask, render_template, request, jsonify
import random
import string
import requests

app = Flask(__name__)

# Set your webhook URL here (replace with your actual webhook URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1311226714629865472/-sv_iEl2EFgvRnvYi1-aJLXQT-an_xoo-bIkP5D4w-GHJuaf_rnytTJiMfT-MRgyVy3s"

# Function to generate a random Discord Nitro code
def generate_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(16))
    return f"https://discord.gift/{code}"

# Function to send the Nitro code to the webhook
def send_code_to_webhook(code):
    embed = {
        "embeds": [
            {
                "title": "New Nitro Code!",
                "description": f"Click the link below to claim this Nitro code.",
                "color": 7506394,  # Discord blue color
                "fields": [
                    {
                        "name": "Code",
                        "value": code
                    }
                ]
            }
        ]
    }

    response = requests.post(WEBHOOK_URL, json=embed)
    if response.status_code == 204:
        return True
    else:
        return False

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate and send codes
@app.route('/generate_codes', methods=['POST'])
def generate_codes():
    try:
        count = int(request.form['count'])
        success = []
        failed = []
        
        for _ in range(count):
            code = generate_code()
            if send_code_to_webhook(code):
                success.append(code)
            else:
                failed.append(code)

        return jsonify({'status': 'success', 'success_codes': success, 'failed_codes': failed})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
