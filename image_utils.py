import cv2
import numpy as np
import os

def calculate_image_difference(image_path1, image_path2, resize_dim=(64, 64)):
    """
    Calculates the difference between two images.
    Returns a score where 0 means identical, and higher values mean more different.
    
    Approach:
    1. Resize both images to small dimensions (e.g. 64x64) to ignore high-freq noise.
    2. Convert to grayscale.
    3. Calculate absolute difference of pixel values.
    4. Return average difference per pixel.
    """
    if not os.path.exists(image_path1) or not os.path.exists(image_path2):
        print(f"One of the images does not exist: {image_path1}, {image_path2}")
        return float('inf')

    try:
        img1 = cv2.imread(image_path1)
        img2 = cv2.imread(image_path2)
        
        if img1 is None or img2 is None:
            return float('inf')
            
        # Resize to normalize comparisons and speed up
        img1_small = cv2.resize(img1, resize_dim)
        img2_small = cv2.resize(img2, resize_dim)
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1_small, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2_small, cv2.COLOR_BGR2GRAY)
        
        # Calculate absolute difference
        diff = cv2.absdiff(gray1, gray2)
        
        # Calculate mean score (0-255)
        score = np.mean(diff)
        
        return score
        
    except Exception as e:
        print(f"Error calculating image difference: {e}")
        return float('inf')

if __name__ == "__main__":
    # Simple test
    import sys
    if len(sys.argv) >= 3:
        score = calculate_image_difference(sys.argv[1], sys.argv[2])
        print(f"Difference Score: {score}")
