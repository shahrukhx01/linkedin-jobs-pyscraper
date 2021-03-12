import time
from datetime import datetime
import pandas as pd
from utils import helpers
from urllib.parse import urlencode, quote_plus
import logging
from models.search.searcher import Searcher
logging.basicConfig(level=logging.INFO)

class LinkedInJobsPyScraper:
    """
    Scrapes public job postings from LinkedIn.
    """
    def __init__(self, searcher, query="", config_path=None):
        """
        Initializes scraper's configurations
        """
        self.searcher = searcher
        self.logger = logging.getLogger(__name__) ## get logger for logging system state
    

    def start(self):
        """
        Starts Scraping public job postings from LinkedIn based on search and filter criteria.
        """
        search = helpers.get_search_instance(self.searcher)  ## create search instance
        search.search_jobs() ## search jobs


def main():
    searcher = Searcher(
        search_pages_per_search_term = 4,
        search_terms = ['data analyst', 'data scientist'],
        batch_size = 5,
        output_filepath = 'out.csv',
        )

    scraper = LinkedInJobsPyScraper(searcher= searcher) 
    scraper.start()

if __name__ == "__main__":
    main()