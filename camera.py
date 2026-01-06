import cv2
import os
import time

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def capture_image(filepath):
    """
    Captures an image using GStreamer (CSI) or V4L2 (USB) and saves it.
    Returns True if successful, False otherwise.
    """
    # Ensure directory exists
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # 1. Try GStreamer Pipeline (CSI Camera)
    print("Attempting to open CSI camera via GStreamer...")
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    
    success = False
    if cap.isOpened():
        # Warm up/Check if it actually works
        # Sometimes GStreamer opens but fails to read if no camera is present
        print("GStreamer pipeline opened. Testing read...")
        for _ in range(5): # warm up for a few frames
            ret, frame = cap.read()
            if ret:
                success = True
                break
            time.sleep(0.1)
        
        if not success:
             print("GStreamer opened but failed to read frames.")
             cap.release()
    
    if not success:
        print("Falling back to USB Camera (V4L2)...")
        cap = cv2.VideoCapture(0)
        # Warm up
        time.sleep(2)

    if not cap.isOpened():
        print("Error: Could not open any camera.")
        return False

    if not success: # if we fell back to V4L2, we need to read a frame
        ret, frame = cap.read()
    
    cap.release()

    if ret and frame is not None:
        # Resize if necessary to keep VLM load low
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
        print("Error: Could not read frame from any source.")
        return False

if __name__ == "__main__":
    # Test capture
    print(cv2.getBuildInformation())
    capture_image("test_capture.jpg")
