import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse

def get_scrappable_urls(urls):
    scrappable_urls = []
    robots_cache = {}  # Cache to store parsed robots.txt for each domain
    
    for url in urls:
        try:
            # Parse the domain from the URL
            domain = urlparse(url).netloc
            
            # Check if the domain's robots.txt is already in the cache
            if domain not in robots_cache:
                # Construct the robots.txt URL
                robots_url = urljoin(f"https://{domain}", "/robots.txt")
                
                # Fetch the robots.txt file
                response = requests.get(robots_url, timeout=5)
                
                if response.status_code == 200:
                    # Parse and store the robots.txt in the cache
                    rp = RobotFileParser()
                    rp.parse(response.text.splitlines())
                    robots_cache[domain] = rp
                else:
                    # If robots.txt doesn't exist, mark the domain as non-scrappable
                    robots_cache[domain] = None
            
            # Check if the domain is scrappable using cached robots.txt
            rp = robots_cache[domain]
            if rp and rp.can_fetch("*", url):
                scrappable_urls.append(url)
        except Exception as e:
            # If any error occurs, skip the URL
            continue

    return scrappable_urls

# Example usage
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://google.com",
    "https://google.com/search",
    "https://nonexistent-website.com"
]
scrappable = get_scrappable_urls(urls)
print("Scrappable URLs:", scrappable)