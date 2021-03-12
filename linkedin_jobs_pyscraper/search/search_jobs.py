import requests
import urllib.request
from bs4 import BeautifulSoup
import logging
import time
from linkedin_jobs_pyscraper.utils import helpers
from linkedin_jobs_pyscraper.extract.extract_job_info import ExtractJobInfo
from linkedin_jobs_pyscraper.models.search.searcher import Searcher
logging.basicConfig(level=logging.INFO)


class Search:
        """
        Performs LinkedIn search based on query given.
        Keyword arguments:
        searcher -- Searcher, search configuration for specific search on LinkedIn.
        """
        def __init__(self, searcher: Searcher):
            self.searcher = searcher
            self.jobinfo_extractor = ExtractJobInfo()
            self.logger = logging.getLogger(__name__)

        def search_jobs(self):
            """
            Iterates over all search terms given in the config. 
            """
            for index, search_term in enumerate(self.searcher.search_terms):
                    
                    self.logger.info("Running for search term: [{}/{}]".format(index, len(self.searcher.search_terms)))
                    search_term = "%20".join(search_term.split())
                    self.search_jobs_ids(search_term) ## search jobs for a term
                    self.fetch_job_info() ## fetch job detail data for that term

            helpers.write_to_file(self.searcher.scraped_jobs, self.searcher.batch_num, self.searcher.output_filepath)
        
        def search_jobs_ids(self, search_term):
            """
            Fetch all HTML markup files for a given search term for number of 
            pages defined in config.
            Keyword arguments:
            search_term -- string query to be searched.
            """
            for i in range(self.searcher.search_pages_per_search_term):

                self.logger.info('Searching jobs in page {}/{}'.format(i+1, self.searcher.search_pages_per_search_term))
                url = self.searcher.search_url.format(search_term, self.searcher.location, i) # Set the URL you want to webscrape from
                response = requests.get(url)  # Connect to the URL
                jobs_soup = BeautifulSoup(response.text, "html.parser") # Parse HTML and save to BeautifulSoup object
                
                self.logger.info('Extracting Job Ids from the page')
                self.searcher.job_ids = self.jobinfo_extractor.extract_job_ids(jobs_soup, self.searcher.job_ids) ## extract job ids from the selected page

        def search_job_data(self, job_id):
            """
            Fetch  HTML markup for a given job_id.
            Keyword arguments:
            search_term -- int job_id whose HTML do be downloaded.
            """
            url = self.searcher.li_jobs_api.format(job_id)
            response = requests.get(url)  # Connect to the URL
            soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML and save to BeautifulSoup object
            return self.jobinfo_extractor.extract_job_data(soup, job_id)

        def fetch_job_info(self):
            """
            Iterate over all job HTML markups and extract job info
            """
            total_jobs = len(self.searcher.job_ids)
            while (len(self.searcher.job_ids)> 0): ## iterate until no jobs left
                
                self.logger.info('Fetching data for JOB[{}/{}]'.format((total_jobs - len(self.searcher.job_ids)), total_jobs))
                job_id = self.searcher.job_ids.pop() ## get last job in queue
                if job_id in self.searcher.scraped_job_ids:
                    self.logger.info('Skipping JobId {} already scraped...'.format(job_id))
                    continue

                job_info = self.search_job_data(job_id)   
                if job_info:
                    self.searcher.scraped_job_ids.append(job_id)
                    self.searcher.scraped_jobs.append(job_info.__dict__)
                    if len(self.searcher.scraped_jobs) >0 and len(self.searcher.scraped_jobs) % self.searcher.batch_size == 0:
                        response = helpers.write_to_file(self.searcher.scraped_jobs, self.searcher.batch_num, self.searcher.output_filepath)
                        self.searcher.batch_num += 1
                        self.searcher.scraped_jobs = list()
                        self.logger.info('Data dumped to file...')

                time.sleep(1) ## sleep for 1 seconds