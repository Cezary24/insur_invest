import os
import json
import base64
import requests
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")

def send_gemini_request(prompt, pdf_path):
    api_key = load_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # Read and encode PDF file as base64
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = base64.b64encode(pdf_file.read()).decode('utf-8')
    
    request_payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {
                        "mime_type": "application/pdf",
                        "data": pdf_data
                    }}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,  # Lower temperature for more consistent output
            "topP": 0.8,
            "topK": 40
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=request_payload)
        response.raise_for_status()  # Raise exception for bad status codes
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        error_message = f"API request failed: {str(e)}"
        if hasattr(e.response, 'json'):
            try:
                error_details = e.response.json()
                error_message = f"API error: {error_details.get('error', {}).get('message', str(e))}"
            except json.JSONDecodeError:
                pass
        return {"error": error_message}

# Example usage
if __name__ == "__main__":
    from prompt import PROMPT
    prompt_text = PROMPT
    pdf_file_path = "../../example_data/Allianz.pdf"
    response = send_gemini_request(prompt_text, pdf_file_path)
    print(json.dumps(response, indent=2))