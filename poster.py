import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def post_content(text, image_path=None):
    """
    Posts the content to the configured API.
    Also logs to file for debugging.
    """
    timestamp = datetime.now().isoformat()
    api_uri = os.getenv("API_URI")
    
    # Prepare payload matching the requested format
    # input = { 
    #   englishText: '...',
    #   occured_at: new Date().toISOString()
    # };
    payload = {
        "inputData": {
            "englishText": text,
            "occured_at": timestamp
        }
    }
    
    log_entry = {
        "timestamp": timestamp,
        "image_path": image_path,
        "content": text,
        "api_uri": api_uri,
        "status": "PENDING"
    }

    print(f"\nPosting to API: {api_uri}")
    
    try:
        if not api_uri:
             raise ValueError("API_URI not found in .env")

        response = requests.post(
            api_uri,
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=10
        )
        
        if response.ok:
            print("API Post Success!")
            try:
                print("Response:", json.dumps(response.json(), indent=2))
            except:
                print("Response:", response.text)
            log_entry["status"] = "SUCCESS"
            log_entry["response"] = response.text
        else:
            print(f"API Error: {response.status_code} {response.reason}")
            print(response.text)
            log_entry["status"] = "FAILED"
            log_entry["error"] = f"{response.status_code} {response.reason} - {response.text}"

    except Exception as e:
        print(f"Post Failed: {e}")
        log_entry["status"] = "ERROR"
        log_entry["error"] = str(e)

    # Log to file
    with open("posts_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    # Test
    post_content("This is a test analysis from semantic-camera-vlm.")
