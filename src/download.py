import os
import requests
from tqdm import tqdm
import argparse

DOWNLOAD_DIR = 'data/downloads'

def download_file(url: str, download_dir: str = DOWNLOAD_DIR) -> str:
    os.makedirs(download_dir, exist_ok=True)
    filename = os.path.join(download_dir, url.split('/')[-1])
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total = int(response.headers.get('content-length', 0))
        with open(filename, 'wb') as f, tqdm(
            total=total, unit='B', unit_scale=True, desc=filename, ncols=80
        ) as pbar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    print(f"Downloaded to {filename}")
    return filename

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download AIS ZIP')
    parser.add_argument('--url', required=True, help='ZIP file URL')
    parser.add_argument('--out', default=DOWNLOAD_DIR,
                        help='Download directory')
    args = parser.parse_args()
    download_file(args.url, args.out)