import time
import argparse
import os
from camera import capture_image
from analyzer import ImageAnalyzer
from poster import post_content

def main():
    parser = argparse.ArgumentParser(description="Semantic Camera VLM")
    parser.add_argument("--interval", type=int, default=10, help="Interval in seconds between captures")
    parser.add_argument("--output_dir", type=str, default="captures", help="Directory to save captured images")
    parser.add_argument("--model", type=str, default="llava-phi3:3.8b", help="Model ID to use (Ollama)")
    parser.add_argument("--device", type=str, default=None, help="Device to run model on (cpu, cuda, mps)")
    
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
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        
    try:
        while True:
            timestamp = int(time.time())
            filename = f"capture_{timestamp}.jpg"
            filepath = os.path.join(args.output_dir, filename)
            
            print(f"\n--- Cycle Start: {time.ctime(timestamp)} ---")
            
            # Capture
            if capture_image(filepath):
                # Analyze
                print("Analyzing image...")
                description = analyzer.analyze(filepath)
                print(f"Analysis Result:\n{description}")
                # Post
                post_content(description, filepath)
            else:
                print("Skipping analysis due to capture failure.")
                
            print(f"Sleeping for {args.interval} seconds...")
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\nStopping loop.")

if __name__ == "__main__":
    main()
