import os
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load the dataset
with open('schemes.json', 'r') as file:
    schemes_data = json.load(file)

@app.route('/webhook', methods=['POST'])  # Ensure POST is allowed
def webhook():
    data = request.get_json()
    
    if not data:
        return jsonify({"fulfillmentText": "Invalid request. No JSON received."})

    policy_name = data['queryResult']['parameters'].get('policy_name', None)
    language = data['queryResult'].get('languageCode', 'en')  # Default to English

    # Find the policy in the dataset
    policy = next((scheme for scheme in schemes_data['schemes'] if scheme['policy_name'] == policy_name), None)

    if policy:
        response = {
            "fulfillmentText": f"{policy['description'].get(language, 'Information not available')}\n\n"
                               f"Eligibility: {policy['eligibility'].get(language, 'Not available')}\n"
                               f"Documents Required: {policy['documents'].get(language, 'Not available')}\n"
                               f"Benefits: {policy['benefits'].get(language, 'Not available')}"
        }
    else:
        response = {
            "fulfillmentText": f"Sorry, I don't have information about {policy_name}. Please check the official website."
        }

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Automatically detect Render's port
    app.run(host='0.0.0.0', port=port)

