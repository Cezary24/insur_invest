import os
import json
import requests
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")

def send_gemini_request(prompt, pdf_path):
    api_key = load_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
    
    request_payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {
                        "mime_type": "application/pdf",
                        "data": pdf_data.decode("latin1")  # Encoding workaround for binary data
                    }}
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(request_payload))
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

# Example usage
if __name__ == "__main__":
    prompt_text = "Summarize the contents of this PDF file."
    pdf_file_path = "example.pdf"
    response = send_gemini_request(prompt_text, pdf_file_path)
    print(response)
