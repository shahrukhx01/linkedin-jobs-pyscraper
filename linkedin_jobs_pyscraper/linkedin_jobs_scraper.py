import time
from datetime import datetime
import pandas as pd
from linkedin_jobs_pyscraper.utils import helpers
from urllib.parse import urlencode, quote_plus
import logging
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
