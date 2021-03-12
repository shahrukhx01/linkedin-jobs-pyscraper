import logging
from linkedin_jobs_pyscraper.models.extract.extractor import IdExtractor, DataExtractor
from linkedin_jobs_pyscraper.utils import helpers
from linkedin_jobs_pyscraper.models.job.job import Job
logging.basicConfig(level=logging.INFO)

class ExtractJobInfo:
    """
    Extracts relevant information from HTML markdown for Job Ids and Job detail.
    """
    def __init__(self):
        self.id_extractor = IdExtractor()
        self.data_extractor = DataExtractor()
        self.logger = logging.getLogger(__name__)
    
    def extract_job_ids(self, jobs_soup, job_ids):
        """
        Extracts Job Ids from HTML markup.
        Keyword arguments:
        jobs_soup -- bs4 response
        job_ids -- list
        """
        self.logger.info('Extracting Job IDs...')
        ## find all jobIds present in this 'jobs_soup' HTML page
        jobs = jobs_soup.findAll(self.id_extractor.job_title_element, 
                        attrs={"class": self.id_extractor.job_title_element_class})
       
        for job in jobs:  ## iterating over job elements to extract job ids   
            job_id = job[self.id_extractor.job_id_element_identifier] ## extract the jobId string from HTML
            if job_id not in job_ids:  ## insert into job_ids list of scraper already not added 
                job_ids.append('{}'.format(job_id))

        return job_ids
    
    def extract_job_data(self, job_soup, job_id):
        """
        Extracts Job detail from HTML markup.
        Keyword arguments:
        jobs_soup -- bs4 response
        job_id -- int
        """
        job_info = { "id" : int(job_id) }

        for info_element in self.data_extractor.job_data:
            data_element = job_soup.find(info_element.element , 
                                    attrs={info_element.attribute_name : info_element.element_class})
            if data_element:
                if 'date' not in info_element.name:
                    job_info[info_element.name] = data_element.text
                else:    
                    job_info[info_element.name] = helpers.rel_time_to_absolute_datetime(data_element.text)
            else:
                if 'date' in info_element.name:
                    data_element = job_soup.find(info_element.element , 
                                    attrs={info_element.attribute_name : info_element.alt_element_class})
                    if data_element:
                        job_info[info_element.name] = helpers.rel_time_to_absolute_datetime(data_element.text)
        
        job_meta_list = job_soup.find(self.data_extractor.job_meta.element,
                                attrs={self.data_extractor.job_meta.attribute_name: self.data_extractor.job_meta.element_class })            
        if  job_meta_list:
            for item in job_meta_list.findAll(self.data_extractor.job_meta.inner_element):
                    key = item.find(self.data_extractor.job_meta.inner_inner_element).text.lower()
                    key = "_".join(key.split())
                    for index, meta_data in enumerate(item.findAll(self.data_extractor.job_meta.inner_inner_inner_element)):
                        if meta_data.text:
                            if index > 0:
                                job_info['{}_{}'.format(key, index)] = meta_data.text
                            else:
                                job_info['{}'.format(key)] = meta_data.text
        
        return Job(**job_info)
