import os
import zipfile
import argparse

def unzip(zip_path: str, extract_dir: str):
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_dir)
    print(f"Extracted {zip_path} to {extract_dir}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Unzip AIS data')
    parser.add_argument('--zip',    required=True, help='Path to ZIP file')
    parser.add_argument('--out',    required=True, help='Extraction dir')
    args = parser.parse_args()
    unzip(args.zip, args.out)