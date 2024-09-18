import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

def query_gpt4(payload):
    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    return None


def get_gpt4_response(prompt, context):
    if not isinstance(prompt, str):
        prompt = str(prompt)
    if not isinstance(context, str):
        context = str(context)

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000
    }

    response = query_gpt4(payload)
    if response and 'choices' in response and len(response['choices']) > 0:
        return response['choices'][0]['message']['content']
    return "Error: Could not get a response from GPT-4."