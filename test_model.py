import ollama
import os

def test_model(model_id, image_path):
    print(f"Testing model: {model_id} with image: {image_path}")
    
    if not os.path.exists(image_path):
        print("Image not found.")
        return

    try:
        response = ollama.chat(
            model=model_id,
            messages=[{
                'role': 'user',
                'content': 'Describe this image.',
                'images': [image_path]
            }]
        )
        print("Success! Response:")
        print(response['message']['content'])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_model("gemma3:4b", "test_capture.jpg")
