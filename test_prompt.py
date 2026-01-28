import ollama
import os

def test_prompt(model_id, image_path, prompt):
    print(f"\n--- Testing Prompt ---\nModel: {model_id}\nImage: {image_path}\nPrompt:\n{prompt}\n----------------------\n")
    
    if not os.path.exists(image_path):
        print("Image not found.")
        return

    try:
        response = ollama.chat(
            model=model_id,
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_path]
            }],
            options={
                'temperature': 0.1, # Lower temperature for more factual/deterministic output
                'num_ctx': 2048
            }
        )
        print("Response:\n")
        print(response['message']['content'])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Proposed new prompt
    NEW_PROMPT = """
Analyze this image objectively and strictly describe only what is clearly visible. Do not make assumptions, guesses, or hallucinations. If details are not clear, do not invent them.

Please output the description in the following fixed format:

**1. Environment**
- (Describe the surroundings, lighting, and location type briefly.)

**2. Objects**
- (List the main visible inanimate objects.)

**3. People**
(For each person visible, provide the following details. If no person is visible, state "No people visible".)
- **Traits**: (Gender, Apparent Age Range, Hair Color)
- **Appearance**: (Clothing Color/Type, Accessories/Glasses/Hat)
- **Action/State**: (What they are doing, Body posture, Facial expression)

Keep the descriptions concise and factual.
"""
    test_prompt("llava-phi3:3.8b", "test_capture.jpg", NEW_PROMPT)
