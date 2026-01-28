import os
import cv2
import numpy as np
import time
from image_utils import calculate_image_difference

def create_test_images():
    # Base image: Solid gray
    base = np.full((100, 100, 3), 128, dtype=np.uint8)
    cv2.imwrite("test_base.jpg", base)
    
    # Identical image
    cv2.imwrite("test_same.jpg", base)
    
    # Slightly different (brightness change)
    slightly_diff = np.full((100, 100, 3), 135, dtype=np.uint8) # +7 brightness
    cv2.imwrite("test_slight.jpg", slightly_diff)
    
    # Different (white noise)
    noise = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    cv2.imwrite("test_diff.jpg", noise)
    
    print("Test images created.")

def run_test():
    create_test_images()
    
    # 1. Identical
    score1 = calculate_image_difference("test_base.jpg", "test_same.jpg")
    print(f"Base vs Same: {score1} (Expected ~0)")
    
    # 2. Slight difference
    score2 = calculate_image_difference("test_base.jpg", "test_slight.jpg")
    print(f"Base vs Slight: {score2} (Expected small value, e.g. < 10)")
    
    # 3. Completely different
    score3 = calculate_image_difference("test_base.jpg", "test_diff.jpg")
    print(f"Base vs Different: {score3} (Expected large value)")
    
    # Cleanup
    for f in ["test_base.jpg", "test_same.jpg", "test_slight.jpg", "test_diff.jpg"]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    run_test()
