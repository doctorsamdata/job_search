# Job description analysis

## Overview
This repository contains the Pythonisation of my job search. It includes tools for scraping job descriptions, counting specific buzzwords, and extracting unique wage values. 

## Folder structure
The project directory structure is as follows:

```
job_search/
│
├── main.py # Main script with the implementation of ContentScraper, BuzzCounter, and WageExtractor classes
├── test_main.py # Unit tests for the functionality in main.py
├── report.qmd # Quarto Markdown file for generating reports
├── requirements.txt # List of Python dependencies
├── styles.css # Custom CSS for styling the Quarto report if using html
 ```

## Setup
1. **Clone the repository**:

    ```
    cd job_search
    git clone https://github.com/doctorsamdata/job_search.git
    ```

2. **Install dependencies**:

    ```
    pip install -r requirements.txt
    ```

## Running the application
To run the application, execute:

```
python main.py
```

## Usage
In main.py, you can find some lines to run the file with example usage.

## Example input paramaters

```
url = "https://www.example.com/vacancy"
technical_buzzwords = ["python", "machine learning", "GitHub"]
personal_buzzwords = ["team", "analyst", "university"]
working_buzzwords = ["team", "innovative", "agile"]
```

### ContentScraper
Use the `ContentScraper` class to fetch and process job description text from a URL.

```
from main import ContentScraper

scraper = ContentScraper(url)
scraper.fetch_and_convert()
text = scraper.get_text()
```

### BuzzCounter
Use the BuzzCounter class to count buzzwords.

```
from main import BuzzCounter

technical_buzzwords = ["python", "machine learning", "GitHub"]
personal_buzzwords = ["team", "analyst", "university", "stakeholder"]
working_buzzwords = ["team", "innovative", "agile"]

buzz_counter = BuzzCounter(technical_buzzwords, personal_buzzwords, working_buzzwords)
buzz_counter.count_buzzwords(text)
buzzword_counts = buzz_counter.get_category_counts()
nonzero_counts = buzz_counter.get_non_zero_category_counts()
```

### Extract wages

Use the WageExtractor class to extract wages.

```
from main import WageExtractor

wage_extractor = WageExtractor()
wages = wage_extractor.extract_wages(text)
```