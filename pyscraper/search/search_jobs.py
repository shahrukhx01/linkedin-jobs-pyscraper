import logging
from extract.extract_job_info import ExtractJobInfo
from linkedin_jobs_scraper import LinkedInJobsPyScraper


class Search:
        def __init__(self, search_url, search_terms, total_search_pages):
            self.search_url = search_url
            self.total_search_pages = total_search_pages
            self.search_terms = search_terms
            self.total_search_terms = len(search_terms)
            self.logger = logging.getLogger(__name__)
        
        def search_jobs(self):
            for index, search_term in enumerate(scraper.scraper_config['search_terms']):
                    self.logger.info("RUNNING FOR SEARCH TERM: [{}/{}]".format(index, total_search_terms))
                    search_term = "%20".join(search_term.split())
                    self.search_jobs_ids(search_term)
        
        def search_jobs_ids(self, search_term):
            for i in range(self.scraper_config['total_search_pages']):
                # Set the URL you want to webscrape from
                url = self.search_url.format(search_term, i)

                self.logger.info('Searching jobs in page {}/{}'.format(i+1, self.scraper_config['total_search_pages']))
                # Connect to the URL
                response = requests.get(url)

                # Parse HTML and save to BeautifulSoup object
                jobs_soup = BeautifulSoup(response.text, "html.parser")
                
                self.logger.info('Extracting Job Ids from the page')
                ## extract job ids from the selected page
                self.extract_job_ids(jobs_soup)

        def get_job_data(self, job_id):
            url = self.scraper_config['li_jobs_api'].format(job_id)
            # Connect to the URL
            response = requests.get(url)

            # Parse HTML and save to BeautifulSoup object
            soup = BeautifulSoup(response.text, "html.parser")