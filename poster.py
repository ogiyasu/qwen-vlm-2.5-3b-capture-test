import json
from datetime import datetime

def post_content(text, image_path=None):
    """
    Mock function to 'post' the content.
    For now, it prints the content to the console and logs to a file.
    """
    timestamp = datetime.now().isoformat()
    
    output = {
        "timestamp": timestamp,
        "image_path": image_path,
        "content": text
    }
    
    # Print to console (User Interface)
    print("\n" + "="*30)
    print(f"FAILED TO POST (Mock implementation):")
    print(f"Time: {timestamp}")
    print(f"Image: {image_path}")
    print(f"Analysis: {text}")
    print("="*30 + "\n")
    
    # Log to file
    with open("posts_log.jsonl", "a") as f:
        f.write(json.dumps(output) + "\n")

if __name__ == "__main__":
    post_content("This is a test analysis.", "test.jpg")
