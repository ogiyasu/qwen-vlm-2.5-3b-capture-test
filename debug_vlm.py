import ollama
import os

model = "llava-phi3:3.8b"

print(f"Testing text-only on {model}...")
try:
    res = ollama.chat(model=model, messages=[{'role':'user', 'content':'hello'}])
    print("Text-only success:", res['message']['content'])
except Exception as e:
    print("Text-only failed:", e)

print(f"\nTesting with simple image on {model}...")
# Create tiny image
import cv2
import numpy as np
img = np.zeros((64, 64, 3), np.uint8)
cv2.imwrite("tiny.jpg", img)

try:
    res = ollama.chat(
        model=model, 
        messages=[{'role':'user', 'content':'describe this', 'images': ['tiny.jpg']}],
        options={'num_ctx': 1024}
    )
    print("Tiny image success:", res['message']['content'])
except Exception as e:
    print("Tiny image failed:", e)
