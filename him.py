import random
import string
import requests
import time

# Set your webhook URL here (replace with your actual webhook URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1311226714629865472/-sv_iEl2EFgvRnvYi1-aJLXQT-an_xoo-bIkP5D4w-GHJuaf_rnytTJiMfT-MRgyVy3s"

# Function to generate a random Discord Nitro code
def generate_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(16))
    return f"https://discord.gift/{code}"

# Function to check if a Nitro code is valid (API call)
def check_nitro_code(code):
    code_id = code.split("/")[-1]
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code_id}?with_application=false&with_subscription_plan=true"
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("uses") == 0:
            return True  # Valid and unused code
    return False  # Invalid or used code

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

    # Send the embed with the code to the webhook
    response = requests.post(WEBHOOK_URL, json=embed)
    if response.status_code == 204:
        print(f"Successfully sent Nitro code to webhook: {code}")
    else:
        print(f"Failed to send code: {code}, Status Code: {response.status_code}")

# Function to generate and send multiple codes
def generate_and_send_codes(count=5):
    for _ in range(count):
        code = generate_code()

        # Check if the code is valid before sending (optional)
        if check_nitro_code(code):
            send_code_to_webhook(code)
        else:
            print(f"Invalid code: {code}")

        time.sleep(1)  # Small delay between sending codes

# Start generating and sending codes
generate_and_send_codes(count=10)  # Generate and send 10 codes
