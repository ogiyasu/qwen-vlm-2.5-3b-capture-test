import ollama
import os

class ImageAnalyzer:
    def __init__(self, model_id="llava-phi3:3.8b", device=None):
        self.model_id = model_id
        # device is ignored for ollama client, but kept for compatibility
        print(f"Initialized Ollama analyzer with model: {self.model_id}")
        
    def analyze(self, image_path, prompt="Describe the people in the image. Focus on: sex, age, hairstyle, facial expression, action, what they are holding, and clothing. Be concrete and avoid guesses. Output in 5 bullet points: Expression / Action / Holding / Clothing / Person traits (gender / age range / hairstyle):"):
        if not os.path.exists(image_path):
            return f"Error: Image file not found at {image_path}"
            
        try:
            print(f"Sending request to Ollama ({self.model_id})...")
            response = ollama.chat(
                model=self.model_id,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [image_path]
                }],
                options={
                    'num_ctx': 1024  # Further reduce context to 1024 for speed/stability
                }
            )
            return response['message']['content']
            
        except Exception as e:
            return f"Error during analysis: {e}. Ensure 'ollama serve' is running and model is pulled."

if __name__ == "__main__":
    # Test
    analyzer = ImageAnalyzer()
    test_image = "test_capture.jpg"
    if os.path.exists(test_image):
        print(f"Testing analysis on {test_image}...")
        result = analyzer.analyze(test_image)
        print("Analysis Result:")
        print(result)
    else:
        print(f"Analyzer ready. Run 'ollama pull {analyzer.model_id}' first. No {test_image} found to test.")
