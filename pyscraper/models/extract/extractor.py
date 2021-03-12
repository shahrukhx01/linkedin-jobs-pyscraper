from pydantic import BaseModel

class Extractor(BaseModel):
    job_title_element = 'li'
    job_title_element_class = 'result-card job-result-card result-card--with-hover-state'
    job_id_element_identifier = 'data-id'