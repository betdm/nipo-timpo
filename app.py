from flask import Flask, render_template_string, request, jsonify
import random
import string
import requests

app = Flask(__name__)

# Set your webhook URL here (replace with your actual webhook URL)
WEBHOOK_URL = "YOUR_WEBHOOK_URL"

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

# HTML content as a string
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discord Nitro Code Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            text-align: center;
            padding: 20px;
        }
        h1 {
            color: #7289da;
        }
        button {
            background-color: #7289da;
            color: white;
            border: none;
            padding: 10px 20px;
            margin-top: 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background-color: #5b6eae;
        }
        input {
            padding: 10px;
            margin: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        #output {
            margin-top: 20px;
            text-align: left;
            display: inline-block;
            max-width: 80%;
        }
        .valid {
            color: green;
        }
        .invalid {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Nitro Code Generator</h1>
    <p>Specify how many codes to generate.</p>
    <input type="number" id="codeCount" placeholder="Enter number of codes" min="1">
    <button onclick="generateCodes()">Generate Codes</button>
    <div id="output"></div>

    <script>
        function generateCodes() {
            var count = document.getElementById('codeCount').value;
            var outputDiv = document.getElementById('output');
            outputDiv.innerHTML = '';  // Clear previous output

            if (!count || count <= 0) {
                outputDiv.innerHTML = '<p>Please enter a valid number of codes.</p>';
                return;
            }

            // Sending the count of codes to the Flask backend
            var formData = new FormData();
            formData.append('count', count);

            fetch('/generate_codes', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    outputDiv.innerHTML = '<h3>Generated Codes:</h3>';
                    data.success_codes.forEach(function(code) {
                        var p = document.createElement('p');
                        p.textContent = `Success: ${code}`;
                        outputDiv.appendChild(p);
                    });

                    if (data.failed_codes.length > 0) {
                        outputDiv.innerHTML += '<h3>Failed Codes:</h3>';
                        data.failed_codes.forEach(function(code) {
                            var p = document.createElement('p');
                            p.textContent = `Failed: ${code}`;
                            outputDiv.appendChild(p);
                        });
                    }
                } else {
                    outputDiv.innerHTML = `<p>Error: ${data.message}</p>`;
                }
            })
            .catch(error => {
                outputDiv.innerHTML = `<p>Error: ${error}</p>`;
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_content)

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
