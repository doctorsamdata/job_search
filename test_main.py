import unittest
from unittest.mock import patch, Mock
import requests
from main import ContentScraper, BuzzCounter, WageExtractor

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
        mock_response.content = b'<html><body>Test/content-with-hyphens</body></html>'
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        self.scraper.fetch_and_convert()
        self.assertEqual(self.scraper.get_text(), 'Test content with hyphens')
    
    @patch('requests.get')
    def test_fetch_and_convert_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Error")
        with patch('builtins.print') as mock_print:
            self.scraper.fetch_and_convert()
            mock_print.assert_called_with("Error fetching URL: Error")
    
    def test_remove_text(self):
        self.scraper.text = 'This is a test. Stel gerust je vraag Meer informatie over deze vacature'
        self.scraper.remove_text("Stel gerust je vraag Meer informatie over deze vacature")
        self.assertEqual(self.scraper.get_text(), 'This is a test.')
    
    def test_no_text_removal(self):
        self.scraper.text = 'This is a test.'
        self.scraper.remove_text("Nonexistent text")
        self.assertEqual(self.scraper.get_text(), 'This is a test.')

    def test_replace_chars(self):
        self.scraper.text = 'This/is-a/test'
        self.scraper.replace_chars()
        self.assertEqual(self.scraper.get_text(), 'This is a test')

class TestBuzzCounter(unittest.TestCase):

    def setUp(self):
        self.buzzwords = ['innovation', 'synergy', 'git']
        self.counter = BuzzCounter(self.buzzwords)
    
    def test_initialization(self):
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 0, 'synergy': 0, 'git': 0})
    
    def test_count_buzzwords(self):
        text = 'Innovation and synergy are key. Innovation drives success.'
        self.counter.count_buzzwords(text)
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 2, 'synergy': 1, 'git': 0})
    
    def test_case_insensitivity(self):
        text = 'Innovation INNOVATION'
        self.counter.count_buzzwords(text)
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 2, 'synergy': 0, 'git': 0})
    
    def test_no_buzzwords(self):
        text = 'There are no matching words here.'
        self.counter.count_buzzwords(text)
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 0, 'synergy': 0, 'git': 0})
    
    def test_empty_text(self):
        text = ''
        self.counter.count_buzzwords(text)
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 0, 'synergy': 0, 'git': 0})

    def test_partial_buzzwords(self):
        text = 'GitHub uses Git as a version control system.'
        self.counter.count_buzzwords(text)
        self.assertEqual(self.counter.get_buzzword_counts(), {'innovation': 0, 'synergy': 0, 'git': 2})

class TestWageExtractor(unittest.TestCase):

    def setUp(self):
        self.wage_extractor = WageExtractor()
    
    def test_extract_wages(self):
        text = ('€ 5.212,- en € 7.747\n'
                'minimaal €5.008,- en maximaal €6.777,- bruto per maand\n'
                'tot €7.300,-\n'
                '€4.691   €6.907 (bruto)\n'
                '€4.691 €6.907 (bruto)\n'
                'Min €4.691–Max. €6.907 (bruto)')
        
        expected_wages = [
            '€ 5.212,-', '€ 7.747', '€5.008,-', '€6.777,-',
            '€7.300,-', '€4.691', '€6.907', '€4.691', '€6.907',
            '€4.691', '€6.907'
        ]
        
        extracted_wages = self.wage_extractor.extract_wages(text)
        self.assertEqual(extracted_wages, expected_wages)
    
    def test_extract_no_wages(self):
        text = 'There are no wages mentioned in this text.'
        self.assertEqual(self.wage_extractor.extract_wages(text), [])

if __name__ == "__main__":
    unittest.main()