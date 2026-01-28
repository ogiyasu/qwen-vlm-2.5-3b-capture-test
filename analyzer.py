import ollama
import os

class ImageAnalyzer:
    def __init__(self, model_id="llava-phi3:3.8b", device=None):
        self.model_id = model_id
        # device is ignored for ollama client, but kept for compatibility
        print(f"Initialized Ollama analyzer with model: {self.model_id}")
        
    def analyze(self, image_path, prompt="Analyze this image objectively and strictly describe only what is clearly visible. Do not make assumptions, guesses, or hallucinations. If details are not clear, do not invent them.\n\nPlease output the description in the following fixed format:\n\n**1. Environment**\n- (Describe the surroundings, lighting, and location type briefly.)\n\n**2. Objects**\n- (List the main visible inanimate objects.)\n\n**3. People**\n(For each person visible, provide the following details. If no person is visible, state \"No people visible\".)\n- **Traits**: (Gender, Apparent Age Range, Hair Color)\n- **Appearance**: (Clothing Color/Type, Accessories/Glasses/Hat)\n- **Action/State**: (What they are doing, Body posture, Facial expression)\n\nKeep the descriptions concise and factual."):
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
