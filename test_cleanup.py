import os
import time
import shutil
import tempfile
from pathlib import Path

def cleanup_old_images(directory, retention_seconds):
    """
    Deletes images in the specified directory that are older than retention_seconds.
    Assumes filenames are in the format 'capture_{timestamp}.jpg'.
    """
    print(f"Running cleanup on {directory} (retention: {retention_seconds}s)")
    current_time = time.time()
    count = 0
    
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return 0

    for filename in os.listdir(directory):
        if filename.startswith("capture_") and filename.endswith(".jpg"):
            try:
                # Extract timestamp from filename
                # format: capture_{timestamp}.jpg
                timestamp_str = filename.replace("capture_", "").replace(".jpg", "")
                file_timestamp = int(timestamp_str)
                
                # Check age
                if current_time - file_timestamp > retention_seconds:
                    filepath = os.path.join(directory, filename)
                    os.remove(filepath)
                    print(f"Deleted old file: {filename}")
                    count += 1
            except ValueError:
                print(f"Skipping file with invalid timestamp format: {filename}")
                continue
            except Exception as e:
                print(f"Error deleting {filename}: {e}")
                continue
                
    return count

def test_cleanup_logic():
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temp dir: {temp_dir}")
        
        current_time = int(time.time())
        retention_period = 48 * 3600  # 48 hours
        
        # 1. Create a file that is NEW (should NOT be deleted)
        # e.g., 1 hour old
        new_timestamp = current_time - 3600
        new_file = os.path.join(temp_dir, f"capture_{new_timestamp}.jpg")
        with open(new_file, 'w') as f:
            f.write("dummy data")
            
        # 2. Create a file that is OLD (SHOULD be deleted)
        # e.g., 49 hours old
        old_timestamp = current_time - (49 * 3600)
        old_file = os.path.join(temp_dir, f"capture_{old_timestamp}.jpg")
        with open(old_file, 'w') as f:
            f.write("dummy data")

        # 3. Create a file with WRONG format (should NOT be deleted)
        wrong_file = os.path.join(temp_dir, "other_image.jpg")
        with open(wrong_file, 'w') as f:
            f.write("dummy data")
            
        print("Files created.")
        print(os.listdir(temp_dir))
        
        # Run cleanup
        deleted_count = cleanup_old_images(temp_dir, retention_period)
        
        # Verify
        remaining_files = os.listdir(temp_dir)
        print(f"Remaining files: {remaining_files}")
        
        assert deleted_count == 1, f"Expected 1 file deleted, got {deleted_count}"
        assert f"capture_{new_timestamp}.jpg" in remaining_files, "New file should remain"
        assert f"capture_{old_timestamp}.jpg" not in remaining_files, "Old file should be deleted"
        assert "other_image.jpg" in remaining_files, "Wrong format file should remain"
        
        print("\nTEST PASSED: Cleanup logic works as expected.")

if __name__ == "__main__":
    test_cleanup_logic()
