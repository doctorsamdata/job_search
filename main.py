import re, requests
from bs4 import BeautifulSoup
from collections import Counter

class ContentScraper:
    def __init__(self, url):
        self.url = url
        self.text = ""

    def fetch_and_convert(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            self.text = ' '.join(soup.stripped_strings)
            self.remove_text("Het Rijk hecht waarde aan een diverse en inclusieve organisatie.")
            self.replace_chars()
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")

    def remove_text(self, remove_text):
        if remove_text in self.text:
            self.text = self.text.split(remove_text)[0].rstrip()

    def replace_chars(self):
        self.text = self.text.replace('/', ' ').replace('-', ' ')

    def get_text(self):
        return self.text
    
class BuzzCounter:
    def __init__(self, buzzwords):
        self.buzzwords = buzzwords
        self.buzzword_counts = Counter({buzzword: 0 for buzzword in buzzwords})

    def count_buzzwords(self, text):
        text = text.lower()
        for buzzword in self.buzzwords:
            # Use a regular expression to find all occurrences of the buzzword, even as part of other words
            pattern = re.compile(re.escape(buzzword), re.IGNORECASE)
            matches = pattern.findall(text)
            self.buzzword_counts[buzzword] += len(matches)

    def get_buzzword_counts(self):
        return dict(self.buzzword_counts)
    
# Example usage
url = "https://www.werkenbijdeoverheid.nl/vacatures/forensisch-data-scientist-uit-het-veiligheidsdomein-NFI-2024-0064?baanplein_id=01487-155551330261&utm_campaign=2024-07-11&utm_source=job-mailing&utm_medium=email"
buzzwords = ["data", "scientist", "veiligheid", "GitHub", "ai ", "machine learning", "python", "doctoraal"]

# Scrape
scraper = ContentScraper(url)
scraper.fetch_and_convert()
text = scraper.get_text()
print(f"Scraped text: {text[:100]}...")  # Print first 100 characters of the scraped text
print(f"Scraped text: {text}...")

# Count buzzwords
buzz_counter = BuzzCounter(buzzwords)
buzz_counter.count_buzzwords(text)
buzzword_counts = buzz_counter.get_buzzword_counts()
print(f"Buzzword Counts: {buzzword_counts}")