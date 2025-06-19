import os
import re
import sys
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def is_dataset_link(url: str) -> bool:
    """Return True if the URL looks like a downloadable dataset."""
    dataset_extensions = (".csv", ".zip", ".xls", ".xlsx", ".json")
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in dataset_extensions)


def download_file(url: str, output_dir: str):
    """Download a single file to the output directory."""
    local_name = os.path.join(output_dir, os.path.basename(urlparse(url).path))
    print(f"Downloading {url} -> {local_name}")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(local_name, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def scrape_datasets(start_url: str, output_dir: str):
    """Find and download dataset links from a webpage."""
    print(f"Fetching {start_url}")
    resp = requests.get(start_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    links = [urljoin(start_url, href) for href in links]
    dataset_links = [link for link in links if is_dataset_link(link)]

    if not dataset_links:
        print("No dataset links found on the page.")
        return

    os.makedirs(output_dir, exist_ok=True)
    for link in dataset_links:
        try:
            download_file(link, output_dir)
        except Exception as exc:
            print(f"Failed to download {link}: {exc}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python aiddata_scraper.py <start_url> <output_dir>")
        print("Example: python aiddata_scraper.py https://www.aiddata.org/ data")
        sys.exit(1)
    start_url = sys.argv[1]
    output_dir = sys.argv[2]
    scrape_datasets(start_url, output_dir)
