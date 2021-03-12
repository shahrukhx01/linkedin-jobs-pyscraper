from models.extract.extractor import Extractor
from linkedin_jobs_scraper import LinkedInJobsPyScraper

class ExtractJobInfo:
    def __init__(self):
        self.extractor = Extractor()
        self.logger = logging.getLogger(__name__)
    
    def extract_job_ids(self, jobs_soup):
        self.logger.info('Extracting Job IDs...')

        ## find all jobIds present in this 'jobs_soup' HTML page
        jobs = jobs_soup.findAll(self.extractor.job_title_element, 
                        attrs={"class": self.extractor.job_title_element_class})

        ## iterating over job elements to extract job ids   
        for job in jobs:
            ## extract the jobId string from HTML
            job_id = job[self.extractor.job_id_element_identifier]
            
            ## insert into job_ids list of scraper already not added 
            if job_id not LinkedInJobsPyScraper.job_ids:
                LinkedInJobsPyScraper.job_ids.append('{}'.format())        