import re, requests
from bs4 import BeautifulSoup
from collections import Counter
from ordered_set import OrderedSet

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
            self.remove_text("Stel gerust je vraag Meer informatie over deze vacature")
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
    def __init__(self, technical_buzzwords, personal_buzzwords, working_buzzwords):
        self.technical_buzzwords = technical_buzzwords
        self.personal_buzzwords = personal_buzzwords
        self.working_buzzwords = working_buzzwords
        self.buzzword_counts = Counter({buzzword: 0 for buzzword in 
                                        technical_buzzwords + personal_buzzwords + working_buzzwords})

    def count_buzzwords(self, text):
        text = text.lower()
        for buzzword in self.buzzword_counts:
            # Use a regular expression to find all occurrences of the buzzword, even as part of other words
            pattern = re.compile(re.escape(buzzword), re.IGNORECASE)
            matches = pattern.findall(text)
            self.buzzword_counts[buzzword] += len(matches)

    def get_buzzword_counts(self):
        return dict(self.buzzword_counts)
    
    def get_category_counts(self):
        technical_counts = {buzzword: self.buzzword_counts[buzzword] for buzzword in self.technical_buzzwords}
        personal_counts = {buzzword: self.buzzword_counts[buzzword] for buzzword in self.personal_buzzwords}
        working_counts = {buzzword: self.buzzword_counts[buzzword] for buzzword in self.working_buzzwords}
        return {
            'technical': technical_counts,
            'personal': personal_counts,
            'working': working_counts
        }
    
    def get_non_zero_category_counts(self):
        category_counts = self.get_category_counts()
        non_zero_counts = {
            'technical': sum(1 for count in category_counts['technical'].values() if count > 0),
            'personal': sum(1 for count in category_counts['personal'].values() if count > 0),
            'working': sum(1 for count in category_counts['working'].values() if count > 0)
        }
        return non_zero_counts
    
class WageExtractor:
    def extract_wages(self, text):
        # Regular expression to match various wage formats in euros
        pattern = re.compile(
            r'€\s?\d{1,2}\.\d{3},?-?|€\d{1,2}\.\d{3}-|€\d{4}|€\s?\d{1,2}\.\d{3}\s?\–\s?€\d{1,2}\.\d{3}',
            re.IGNORECASE
        )
        wages = pattern.findall(text)
        return self.get_unique_wages(wages)
    
    def get_unique_wages(self, wages):
        # Return only unique wages
        return list(OrderedSet(wages))
    
# Example usage
url = "https://www.example.com/vacancy"
technical_buzzwords = ["python", "machine learning", "GitHub"]
personal_buzzwords = ["team", "analyti", "universit"]
working_buzzwords = ["team", "innovat", "agile"]

# Scrape
scraper = ContentScraper(url)
scraper.fetch_and_convert()
text = scraper.get_text()
print(f"Scraped text: {text[:100]}...")  # Print first 100 characters of the scraped text

# Count buzzwords
buzz_counter = BuzzCounter(technical_buzzwords, personal_buzzwords, working_buzzwords)
buzz_counter.count_buzzwords(text)
buzzword_counts = buzz_counter.get_category_counts()
nonzero_counts = buzz_counter.get_non_zero_category_counts()
print(f"Buzzword counts: {buzzword_counts}")
print(f"Non-zero counts: {nonzero_counts}")

# Check wage
wage_extractor = WageExtractor()
wages = wage_extractor.extract_wages(text)
print(f"Extracted wages: {wages}")