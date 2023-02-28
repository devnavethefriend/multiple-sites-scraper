# Import requirements
import requests
from bs4 import BeautifulSoup
import re

# Assign a list of target websites to scrape
target_sites = ['https://examplesite1.com', 'https://examplesite2.com']

# Function that extracts the title & text content from a webpage
def extract_text(url):
    # Add error handling method
    try:
        # Take URL as input & retrieve page content
        page = requests.get(url)
        # Initiate soup instance to parse & access page content
        soup = BeautifulSoup(page.content, 'html.parser')
        # Get the page title
        title = soup.title.string.strip()
        # Get the page texts, using <p> tags in this case
        texts = '\n'.join([p.text.strip() for p in soup.find_all('p')])
        # Return extracted title & texts
        return title, texts
    except:
        # Return 'None' if error occurs
        return None, None

# Function to create a .txt file of a website
def create_txt_file(site):
    # Error handling
    try:
        # Get the sitemap for the website
        sitemap_url = site + '/sitemap.xml'
        # Retrieve page content of the sitemap
        sitemap = requests.get(sitemap_url)
        # Initiate soup instance to parse & access sitemap content
        soup = BeautifulSoup(sitemap.content, 'xml')
        # Find all the URLs in the sitemap
        urls = [loc.text for loc in soup.find_all('loc')]
        # Get the texts for each URL & write it to a .txt file
        for url in urls:
            title, texts = extract_text(url)
            if title and texts:
                filename = re.sub('[^0-9a-zA-Z]+', '_', title) + '.txt'
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(texts)
    except:
        # Display an error message incase of an error
        print(f"Error occured while creating .txt files for {site}")

# Generate a .txt file for each target site
for site in target_sites:
    create_txt_file(site)
