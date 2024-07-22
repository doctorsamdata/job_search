import unittest
from unittest.mock import patch, Mock
import requests
from main import ContentScraper, BuzzCounter

class TestContentScraper(unittest.TestCase):
    
    def setUp(self):
        self.url = 'http://example.com'
        self.scraper = ContentScraper(self.url)
    
    def test_initialization(self):
        self.assertEqual(self.scraper.url, self.url)
        self.assertEqual(self.scraper.text, "")
    
    @patch('requests.get')
    def test_fetch_and_convert(self, mock_get):
        mock_response = Mock()
        mock_response.content = b'<html><body>Test content</body></html>'
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        self.scraper.fetch_and_convert()
        self.assertEqual(self.scraper.get_text(), 'Test content')
    
    @patch('requests.get')
    def test_fetch_and_convert_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Error")
        with patch('builtins.print') as mock_print:
            self.scraper.fetch_and_convert()
            mock_print.assert_called_with("Error fetching URL: Error")
    
    def test_remove_text(self):
        self.scraper.text = 'This is a test. Het Rijk hecht waarde aan een diverse en inclusieve organisatie.'
        self.scraper.remove_text("Het Rijk hecht waarde aan een diverse en inclusieve organisatie.")
        self.assertEqual(self.scraper.get_text(), 'This is a test.')
    
    def test_no_text_removal(self):
        self.scraper.text = 'This is a test.'
        self.scraper.remove_text("Nonexistent text")
        self.assertEqual(self.scraper.get_text(), 'This is a test.')

class TestBuzzCounter(unittest.TestCase):

    def setUp(self):
        self.buzzwords = ['innovation', 'synergy']
        self.counter = BuzzCounter(self.buzzwords)
    
    def test_initialization(self):
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 0, 'synergy': 0})
    
    def test_count_buzzwords(self):
        text = 'Innovation and synergy are key. Innovation drives success.'
        self.counter.count_buzzwords(text)
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 2, 'synergy': 1})
    
    def test_case_insensitivity(self):
        text = 'Innovation INNOVATION'
        self.counter.count_buzzwords(text)
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 2, 'synergy': 0})
    
    def test_no_buzzwords(self):
        text = 'There are no matching words here.'
        self.counter.count_buzzwords(text)
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 0, 'synergy': 0})
    
    def test_empty_text(self):
        text = ''
        self.counter.count_buzzwords(text)
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 0, 'synergy': 0})

if __name__ == "__main__":
    unittest.main()