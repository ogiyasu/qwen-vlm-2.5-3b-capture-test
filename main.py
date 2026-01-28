import time
import argparse
import os
from camera import capture_image
from analyzer import ImageAnalyzer
from poster import post_content
from image_utils import calculate_image_difference

def cleanup_old_images(directory, retention_seconds):
    """
    Deletes images in the specified directory that are older than retention_seconds.
    Assumes filenames are in the format 'capture_{timestamp}.jpg'.
    """
    current_time = time.time()
    
    if not os.path.exists(directory):
        return

    for filename in os.listdir(directory):
        if filename.startswith("capture_") and filename.endswith(".jpg"):
            try:
                parts = filename.split('_')
                if len(parts) >= 2:
                    timestamp_part = parts[1].split('.')[0]
                    file_timestamp = int(timestamp_part)
                    
                    if current_time - file_timestamp > retention_seconds:
                        filepath = os.path.join(directory, filename)
                        os.remove(filepath)
                        print(f"Deleted old file: {filename}")
            except Exception:
                pass

def main():
    parser = argparse.ArgumentParser(description="Semantic Camera VLM")
    parser.add_argument("--interval", type=int, default=3, help="Interval in seconds between captures")
    parser.add_argument("--output_dir", type=str, default="captures", help="Directory to save captured images")
    parser.add_argument("--model", type=str, default="llava-phi3:3.8b", help="Model ID to use (Ollama)")
    parser.add_argument("--device", type=str, default=None, help="Device to run model on (cpu, cuda, mps)")
    parser.add_argument("--retention", type=int, default=48*3600, help="Image retention period in seconds (default: 48 hours)")
    parser.add_argument("--diff-threshold", type=float, default=10.0, help="Difference threshold to skip analysis (lower = more sensitive)")
    
    args = parser.parse_args()
    
    # 1. Initialize Analyzer
    print("Initializing Analyzer (this may take a while to download/load the model)...")
    try:
        analyzer = ImageAnalyzer(model_id=args.model, device=args.device)
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to initialize analyzer. {e}")
        return

    # 2. Main Loop
    print(f"Starting loop with interval {args.interval}s. Saving to '{args.output_dir}'")
    print(f"Image retention policy: {args.retention} seconds")
    print(f"Change detection threshold: {args.diff_threshold}")
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        
    last_image_path = None

    try:
        while True:
            timestamp = int(time.time())
            filename = f"capture_{timestamp}.jpg"
            filepath = os.path.join(args.output_dir, filename)
            
            print(f"\n--- Cycle Start: {time.ctime(timestamp)} ---")
            
            # Capture
            if capture_image(filepath):
                # Check for changes if we have a previous image
                skip_analysis = False
                if last_image_path and os.path.exists(last_image_path):
                    diff_score = calculate_image_difference(last_image_path, filepath)
                    print(f"Difference score: {diff_score:.2f} (Threshold: {args.diff_threshold})")
                    
                    if diff_score < args.diff_threshold:
                        print("Change is below threshold. Skipping analysis.")
                        skip_analysis = True
                
                if not skip_analysis:
                    # Analyze
                    print("Analyzing image...")
                    description = analyzer.analyze(filepath)
                    print(f"Analysis Result:\n{description}")
                    # Post
                    post_content(description, filepath)
                
                # Update last image path
                last_image_path = filepath
                
                # Cleanup old images
                cleanup_old_images(args.output_dir, args.retention)
            else:
                print("Skipping analysis due to capture failure.")
                
            print(f"Sleeping for {args.interval} seconds...")
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\nStopping loop.")

if __name__ == "__main__":
    main()
