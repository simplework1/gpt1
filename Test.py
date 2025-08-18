import pandas as pd
import requests
from goose3 import Goose
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# custom headers (pretend to be a browser)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0 Safari/537.36"
}

def fetch_content(url, retries=2, timeout=10):
    """Fetch article content using requests + Goose with retries."""
    g = Goose()
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=timeout)
            if resp.status_code == 200:
                article = g.extract(raw_html=resp.text, url=url)
                if article.cleaned_text:
                    return article.cleaned_text
        except Exception as e:
            if attempt < retries:
                time.sleep(1)  # wait before retry
            else:
                return None
    return None

def add_content_column(df, url_column="link", max_workers=30, retries=2):
    """Takes a dataframe, extracts content from URLs, and adds a 'content' column."""
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(fetch_content, row[url_column], retries): idx
            for idx, row in df.iterrows()
        }

        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception:
                results[idx] = None

    df["content"] = df.index.map(results.get)
    return df