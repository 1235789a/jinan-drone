"""
Helper script to upload training data to Kaggle as a Dataset.
Run this on AutoDL or local machine where the data files exist.

Prerequisites:
    pip install kaggle
    # Set up ~/.kaggle/kaggle.json with your API key

Usage:
    python upload_data_to_kaggle.py --data-dir /root/jinan-drone/data/
"""

import argparse
import json
import os
import shutil
import subprocess


def create_dataset_metadata(output_dir, username="your-kaggle-username"):
    """Create dataset-metadata.json for Kaggle dataset upload."""
    metadata = {
        "title": "AI Reliability Judge Training Data",
        "id": f"{username}/ai-reliability-judge-data",
        "licenses": [{"name": "CC0-1.0"}],
    }
    with open(os.path.join(output_dir, "dataset-metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)


def validate_data(filepath):
    """Validate JSONL file format."""
    count = 0
    with open(filepath, "r") as f:
        for i, line in enumerate(f, 1):
            try:
                obj = json.loads(line.strip())
                assert "messages" in obj, f"Line {i}: missing 'messages' key"
                assert len(obj["messages"]) >= 2, f"Line {i}: need at least 2 messages"
                assert obj["messages"][0]["role"] == "user", f"Line {i}: first message must be user"
                assert obj["messages"][-1]["role"] == "assistant", f"Line {i}: last message must be assistant"
                count += 1
            except json.JSONDecodeError as e:
                print(f"ERROR Line {i}: Invalid JSON - {e}")
                return False
    print(f"  ✓ {filepath}: {count} valid samples")
    return True


def main():
    parser = argparse.ArgumentParser(description="Upload training data to Kaggle")
    parser.add_argument("--data-dir", default="/root/jinan-drone/data/", help="Directory with JSONL files")
    parser.add_argument("--kaggle-username", default="your-kaggle-username", help="Your Kaggle username")
    parser.add_argument("--skip-upload", action="store_true", help="Only validate, don't upload")
    args = parser.parse_args()

    # Validate
    print("Validating data files...")
    train_file = os.path.join(args.data_dir, "train_chat.jsonl")
    val_file = os.path.join(args.data_dir, "val_chat.jsonl")

    assert os.path.exists(train_file), f"Missing: {train_file}"
    assert os.path.exists(val_file), f"Missing: {val_file}"

    if not validate_data(train_file) or not validate_data(val_file):
        print("Data validation failed!")
        return

    if args.skip_upload:
        print("\nValidation passed! Use without --skip-upload to upload to Kaggle.")
        return

    # Prepare upload directory
    upload_dir = "/tmp/kaggle_upload"
    os.makedirs(upload_dir, exist_ok=True)
    shutil.copy2(train_file, upload_dir)
    shutil.copy2(val_file, upload_dir)
    create_dataset_metadata(upload_dir, args.kaggle_username)

    # Upload
    print("\nUploading to Kaggle...")
    result = subprocess.run(
        ["kaggle", "datasets", "create", "-p", upload_dir, "--dir-mode", "zip"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        print("\nAlternative: Push data to GitHub and pull from Kaggle notebook:")
        print("  git add data/ && git commit -m 'Add training data' && git push")
    else:
        print("✓ Dataset uploaded successfully!")


if __name__ == "__main__":
    main()
