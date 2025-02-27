import os
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load the dataset
with open('schemes.json', 'r', encoding="utf-8") as file:
    schemes_data = json.load(file)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"fulfillmentText": "Invalid request. No JSON received."})

    query_text = data['queryResult']['queryText'].lower()  # User's query
    policy_name = data['queryResult']['parameters'].get('policy_name', None)
    language = data['queryResult'].get('languageCode', 'en')  # Default to English

    # Find the policy in the dataset
    policy = next((scheme for scheme in schemes_data['schemes'] if scheme['policy_name'].lower() == policy_name.lower()), None)

    if policy:
        # Detect what the user is asking
        if "eligibility" in query_text or "eligible" in query_text:
            response_text = f"Eligibility criteria for {policy['policy_name']}: {policy['eligibility'].get(language, 'Not available')}"
        elif "document" in query_text or "required document" in query_text:
            response_text = f"Required documents for {policy['policy_name']}: {policy['documents'].get(language, 'Not available')}"
        elif "benefit" in query_text:
            response_text = f"Benefits of {policy['policy_name']}: {policy['benefits'].get(language, 'Not available')}"
        else:
            # Default full response if no specific query is detected
            response_text = (
                f"{policy['policy_name']} is a government scheme. {policy['description'].get(language, 'Information not available')}\n\n"
                f"Eligibility: {policy['eligibility'].get(language, 'Not available')}\n"
                f"Documents Required: {policy['documents'].get(language, 'Not available')}\n"
                f"Benefits: {policy['benefits'].get(language, 'Not available')}"
            )
    else:
        response_text = f"Sorry, I don't have information about {policy_name}. Please check the official website."

    return jsonify({"fulfillmentText": response_text})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Automatically detect Render's port
    app.run(host='0.0.0.0', port=port)

