from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load the dataset
with open('schemes.json', 'r') as file:
    schemes_data = json.load(file)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    policy_name = data['queryResult']['parameters']['policy_name']
    language = data['queryResult']['languageCode']

    # Find the policy in the dataset
    policy = next((scheme for scheme in schemes_data['schemes'] if scheme['policy_name'] == policy_name), None)

    if policy:
        response = {
            "fulfillmentText": f"{policy['description'][language]}\n\n"
                               f"Eligibility: {policy['eligibility'][language]}\n"
                               f"Documents Required: {policy['documents'][language]}\n"
                               f"Benefits: {policy['benefits'][language]}"
        }
    else:
        response = {
            "fulfillmentText": f"Sorry, I don't have information about {policy_name}. Please check the official website for details."
        }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
