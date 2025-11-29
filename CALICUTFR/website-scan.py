import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time
import random
import sys
import os

   # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                   >|a@@@@@@@@@|                                                
                                              }@@@@@@@@@@@@@@@@| 000M|                                          
                                          ;@@@@@@O  @@@@@@@@@@@|  j000000_                                      
                                       }@@@@@v   |@@@@@@@@@@@@@| 00J  |00000j                                   
                                     @@@@@_     @@@@@@@@@@@@@@@| 0000    ;00000^                                
                                  ;@@@@v       _@@@@@@@     >@@| 0000v      }0000_                              
                                ^@@@@_         @@@@@@@      ^O@| 00000        ;0000_                            
                                 @@@@;         @@@@@@@      ;p@| 00000         0000^                            
                                   @@@@p       >@@@@@@@^    >@@| 0000v      J0000;                              
                                     O@@@@|     M@@@@@@@@@@@@@@| 0000    >00000                                 
                                       ;@@@@@J^  }@@@@@@@@@@@@@| 00v  j00000}                                   
                                          >@@@@@@@_;@@@@@@@@@@@| ;M000000_                                      
                                              >@@@@@@@@@@@@@@@@| 00000}                                          
                                                   ^jpM@@@@@@@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|                                                
                                                            >@@|        
"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)

# --- Custom Function/Constant Placeholders ---
# Replace these with your actual implementations or remove if unnecessary.

# A simple way to handle time/logging (replace BEFORE, AFTER, etc.)
def get_current_time_log():
    return f"[{time.strftime('%H:%M:%S')}]"

# Placeholder for custom colors or logging
LOG_INFO = "[INFO]"
LOG_INPUT = "[INPUT]"
LOG_ADD = "[FOUND]"

# Title, banner, and other UI functions need to be defined
def display_title(text):
    print(f"\n{'='*50}")
    print(f"** {text} **")
    print(f"{'='*50}\n")

def get_user_agent():
    # Replace with your actual user-agent selection logic
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
    ]
    return random.choice(user_agents)

def handle_error(e):
    print(f"\n[ERROR] An error occurred: {e}", file=sys.stderr)
    # If ErrorModule did more than print, add that logic here.

# ---------------------------------------------

display_title("Website URL Scanner")

try:
    all_links = set()  # Use a set for faster lookups and automatic uniqueness
    
    user_agent = get_user_agent()
    headers = {"User-Agent": user_agent}

    def is_valid_extension(url):
        # Checks if the URL has a common web page/script extension or no extension at all
        # This function name is clearer than 'IsValidExtension'
        return re.search(r'\.(html|xhtml|php|js|css)$', url, re.IGNORECASE) or not re.search(r'\.\w+$', url)

    def extract_links(base_url, domain, tags):
        # Renamed function for Python standard snake_case
        extracted_links = []
        for tag in tags:
            # Use .get() with a default of None to avoid exceptions
            attr = tag.get('href') or tag.get('src') or tag.get('action')
            if attr:
                full_url = urljoin(base_url, attr)
                # Check for uniqueness, domain match, and valid extension
                if full_url not in all_links and domain in full_url and is_valid_extension(full_url):
                    extracted_links.append(full_url)
                    all_links.add(full_url)
        return extracted_links

    def extract_links_from_script(scripts, domain):
        # Renamed function for Python standard snake_case
        extracted_links = []
        for script in scripts:
            # Check for script content using .string or .text
            content = script.string or script.text
            if content:
                # Find common URL patterns (http/https followed by non-space characters)
                urls_in_script = re.findall(r'(https?://\S+)', content)
                for url in urls_in_script:
                    # Check for uniqueness, domain match, and valid extension
                    if url not in all_links and domain in url and is_valid_extension(url):
                        extracted_links.append(url)
                        all_links.add(url)
        return extracted_links

    def find_urls(website_url, domain):
        # Renamed function from FindSecretUrls to a more descriptive 'find_urls'
        try:
            # Added timeout for robustness
            response = requests.get(website_url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            # Handle request-specific exceptions gracefully
            print(f"{get_current_time_log()} [WARNING] Could not access {website_url}: {e}")
            return

        if response.status_code != 200:
            return
        
        # Use response.text instead of response.content for BeautifulSoup, which is generally better for HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Combine relevant tags for extracting links
        tags = soup.find_all(['a', 'link', 'script', 'img', 'iframe', 'button', 'form'])
        
        extracted_links = extract_links(website_url, domain, tags)
        
        # Look for links directly in script tags' content
        extracted_links.extend(extract_links_from_script(soup.find_all('script'), domain))
        
        for link in extracted_links:
            # Using placeholders for color/logging functions
            print(f"{get_current_time_log()} {LOG_ADD} URL: {link}")

    def crawl_website(website_url, domain):
        # Renamed from FindAllSecretUrls to 'crawl_website' for clarity
        
        # Start the initial scan
        find_urls(website_url, domain)
        
        visited_links = {website_url}  # Start with the initial URL as visited
        
        # Convert all_links to a list for iteration, but keep it a set for storage
        queue = list(all_links)
        
        while queue:
            # Pop the next link to visit
            link = queue.pop(0)
            
            # Skip if already visited
            if link in visited_links:
                continue

            # Add to visited set immediately
            visited_links.add(link)

            try:
                # Making a HEAD request is faster and doesn't download the whole page body
                # if we only need the status code.
                response = requests.head(link, headers=headers, timeout=5, allow_redirects=True)
                
                if response.status_code == 200:
                    # If the link is accessible, scan it for more URLs
                    print(f"\n{get_current_time_log()} {LOG_INFO} Scanning new page: {link}")
                    
                    # Need to use GET here to get the content for BeautifulSoup
                    find_urls(link, domain)

                    # Add newly found unique links (that are not visited) to the queue
                    newly_found = all_links - visited_links
                    queue.extend(list(newly_found))
                    
                else:
                    print(f"{get_current_time_log()} [SKIP] Cannot scan {link}. Status: {response.status_code}")

            except requests.exceptions.RequestException as e:
                # Catch specific request exceptions (timeout, connection error, etc.)
                pass # Silent pass for failed requests is common in simple scanners


    # Slow(scan_banner) would go here
    print(f"{get_current_time_log()} {LOG_INFO} Selected User-Agent: {user_agent}")
    
    website_url = input(f"{get_current_time_log()} {LOG_INPUT} Website URL -> ")
    # Censored(website_url) would go here if needed
    
    # Ensure URL has a scheme for proper parsing
    if not website_url.startswith(("https://", "http://")):
        website_url = "https://" + website_url
        
    # Extract the domain (e.g., example.com from https://www.example.com/path)
    # Using re.sub to remove the protocol, then splitting by '/' and taking the first part
    domain = re.sub(r'^https?://', '', website_url).split('/')[0]
    
    print(f"""
{get_current_time_log()} 01 Only URL
{get_current_time_log()} 02 All Website
    """)
    
    choice = input(f"{get_current_time_log()} {LOG_INPUT} Choice -> ")
    
    if choice in ['1', '01']:
        # Only scan the initial URL
        find_urls(website_url, domain)
    elif choice in ['2', '02']:
        # Crawl the entire website
        crawl_website(website_url, domain)
        
    # Continue() and Reset() would go here
    
except Exception as e:
    handle_error(e)