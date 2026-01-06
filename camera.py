import cv2
import os
import time

def capture_image(filepath):
    """
    Captures an image from the default camera and saves it to the specified filepath.
    Returns True if successful, False otherwise.
    """
    # Ensure directory exists
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    # Warm up camera
    time.sleep(2)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False

    ret, frame = cap.read()
    
    # Release camera immediately
    cap.release()

    if ret:
        # Resize frame to reduce VLM processing load (max dimension 1024)
        height, width = frame.shape[:2]
        max_dim = 1024
        if max(height, width) > max_dim:
            scale = max_dim / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

        cv2.imwrite(filepath, frame)
        print(f"Image saved to {filepath} ({frame.shape[1]}x{frame.shape[0]})")
        return True
    else:
        print("Error: Could not read frame.")
        return False

if __name__ == "__main__":
    # Test capture
    capture_image("test_capture.jpg")
