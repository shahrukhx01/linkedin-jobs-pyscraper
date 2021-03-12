import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import time
import pandas as pd
from scraper.utils.helpers import *
from urllib.parse import urlencode, quote_plus



class LinkedInJobsScraper:
    def __init__(self, num_jobs, query, config_path=None):

        self.num_jobs = num_jobs
        self.query = query
        self.job_ids = [] ## list for holding per page job ids
        
        self.scraper_config, self.credentials = read_config(config_path) ## loading configuration
        self.scraper_logger = get_logger() ## get logger for logging system state
       
        
        ## connecting to mongo db cloud
        self.mongo_collection = get_mongo_client(self.scraper_config, self.credentials)

        #self.es_client = Elasticsearch(hosts=self.scraper_config['es_host'])
                                        
    
    def search_jobs_ids(self, search_term):
        for i in range(self.scraper_config['total_search_pages']):
            # Set the URL you want to webscrape from
            url = self.scraper_config['search_url'].format(search_term,i)

            self.scraper_logger.info('Searching jobs in page {}/{}'.format(i+1, self.scraper_config['total_search_pages']))
            # Connect to the URL
            response = requests.get(url)

            # Parse HTML and save to BeautifulSoup object
            soup = BeautifulSoup(response.text, "html.parser")
            
            self.scraper_logger.info('Extracting Job Ids from the page')

            ## extract job ids from the selected page
            self.extract_job_ids(soup)

            if len(self.job_ids) > 0:
                self.scraper_logger.info('Found {} new jobs'.format(len(self.job_ids)))
                self.fetch_job_info()
            else:
                self.scraper_logger.info('Found {} new jobs'.format(len(self.job_ids)))
            

    def extract_job_ids(self, soup):
        jobs = soup.findAll(self.scraper_config['job_title_element'], 
                        attrs={"class":self.scraper_config['job_title_element_class']})

        ## iterating over job elements to extract job ids
        for job in jobs:
            self.job_ids.append('{}'.format(job[self.scraper_config['job_id_element_identifier']]))


    def get_job_data(self, job_id):
        url = self.scraper_config['li_jobs_api'].format(job_id)
        # Connect to the URL
        response = requests.get(url)

        # Parse HTML and save to BeautifulSoup object
        soup = BeautifulSoup(response.text, "html.parser")
        job_info = {}
        ## find jd section
        job_info['_id'] = job_id
        if soup.find("h2",attrs={"class":self.scraper_config['job_title_class']}):
            job_info['job_title'] = soup.find("h2",attrs={"class":self.scraper_config['job_title_class']}).text
        else:
            job_info['job_title'] = '<NOT_GIVEN>'
        
        if soup.find("section",attrs={"class":"description"}):
            job_info['description'] = soup.find("section",attrs={"class":"description"}).text
        else:
            job_info['description'] = '<NOT_GIVEN>'

        if soup.find("span",attrs={"class":self.scraper_config['job_location_class']}):
            job_info['location'] = soup.find("span",attrs={"class":self.scraper_config['job_location_class']}).text
        else:
            job_info['location'] = '<NOT_GIVEN>'

        if soup.find("a",attrs={"class":self.scraper_config['employer_name_class']}):
            job_info['employer_name'] = soup.find("a",attrs={"class":self.scraper_config['employer_name_class']}).text
        else:
            job_info['employer_name'] = '<NOT_GIVEN>'
        if soup.find("span",attrs={"class":self.scraper_config['job_date_class']}):
            job_info['date_posted'] = rel_time_to_absolute_datetime(soup.find("span",attrs={"class":self.scraper_config['job_date_class']}).text)
        else:
            job_info['date_posted'] = '<NOT_GIVEN>'
        
        job_meta_ul = soup.find("ul",attrs={"class": self.scraper_config['job_meta_info_class'] })

        if soup.find("span",attrs={"class": self.scraper_config['n_applicants_class'] }):
            job_info['n_applicants'] = int(soup.find("span",attrs={"class": self.scraper_config['n_applicants_class'] }).text.split(' ')[0])  
        else:
            job_info['n_applicants'] = 0
        if  job_meta_ul:
            for item in job_meta_ul.findAll('li'):
                    key = item.find('h3').text.lower()
                    for index, meta_data in enumerate(item.findAll('span')):
                        if meta_data.text:
                            job_info['{}_{}'.format(key, index)] = meta_data.text

        return job_info
    
    def fetch_job_info(self):
        total_jobs = len(self.job_ids)
        while (len(self.job_ids)>0): ## iterate until no jobs left
            self.scraper_logger.info('Fetching data for JOB[{}/{}]'.format((total_jobs - len(self.job_ids)), total_jobs))
            job_id = self.job_ids.pop() ## get last job in queue
            job_info = self.get_job_data(job_id)
                
            if job_info:
                ## TODO: update status and dump to ES
                self.scraper_logger.info('dumping to mongo')
                #write_to_es(self.scraper_config['es_index'], job_info, self.es_client)
                response = write_to_mongo(self.mongo_collection, job_info)
                self.scraper_logger.info('[MongoDB] for new row insert: {}'.format(response))

            time.sleep(1) ## sleep for 1 seconds
            
