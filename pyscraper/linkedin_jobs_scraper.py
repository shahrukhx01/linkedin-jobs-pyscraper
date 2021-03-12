import time
from datetime import datetime
import pandas as pd
from utils import helpers
from urllib.parse import urlencode, quote_plus
import logging
from models.search.searcher import Searcher
from models.filters import filters
logging.basicConfig(level=logging.INFO)

class LinkedInJobsPyScraper:
    """
    Scrapes public job postings from LinkedIn.
    """
    def __init__(self, searcher, filters, query="", config_path=None):
        """
        Initializes scraper's configurations
        """
        self.searcher = searcher
        self.filters = filters
        self.logger = logging.getLogger(__name__) ## get logger for logging system state

    def start(self):
        """
        Starts Scraping public job postings from LinkedIn based on search and filter criteria.
        """
        search = helpers.get_search_instance(self.searcher, self.filters)  ## create search instance
        search.search_jobs() ## search jobs

def main():
    ## create searach query with configurations
    searcher = Searcher(
        search_pages_per_search_term = 4,
        search_terms = ['data analyst', 'data scientist'],
        batch_size = 5,
        output_filepath = 'out.csv',
        location = 'Germany'
        )

    search_filter = filters.Filters(
        experience= filters.ExperienceLevelFilters.INTERNSHIP,
        job_type= filters.TypeFilters.INTERNSHIP,
        relevance= filters.RelevanceFilters.RECENT,
        time= filters.TimeFilters.MONTH
        )
    scraper = LinkedInJobsPyScraper(searcher= searcher, filters=search_filter) 
    scraper.start()

if __name__ == "__main__":
    main()