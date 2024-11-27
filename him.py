import discord
import random
import string
import asyncio

# Set your webhook URL here
WEBHOOK_URL = "YOUR_WEBHOOK_URL"

# Create an instance of a client to interact with Discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Function to generate a random Discord Nitro code
def generate_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(16))
    return f"https://discord.gift/{code}"

# Function to send the Nitro code to the webhook with an "Accept" button
async def send_code_to_webhook(code):
    embed = discord.Embed(
        title="New Nitro Code!",
        description=f"Click the button below to accept this Nitro code.",
        color=0x7289DA  # Discord blue color
    )
    embed.add_field(name="Code", value=code)

    # Button for accepting the Nitro code
    components = [
        discord.ui.Button(
            label="Accept Code", 
            style=discord.ButtonStyle.url, 
            url=code
        )
    ]

    # Send the embed with the button to the webhook
    webhook = discord.Webhook.from_url(WEBHOOK_URL, adapter=discord.RequestsWebhookAdapter())
    await webhook.send(embed=embed, components=components)

# Function to generate and send multiple codes
async def generate_and_send_codes(count=5):
    for _ in range(count):
        code = generate_code()
        await send_code_to_webhook(code)
        await asyncio.sleep(1)  # Small delay between sending codes

# Run the bot
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    # Generate and send 10 Nitro codes to the webhook
    await generate_and_send_codes(count=10)

    # Close the bot after sending the codes
    await client.close()

# Start the bot with your bot token
client.run('YOUR_BOT_TOKEN')
