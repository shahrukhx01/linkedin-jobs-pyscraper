from pydantic import BaseModel
from datetime import datetime

class Job(BaseModel):
    id: int
    job_title: str = '<NOT_GIVEN>'
    description: str = '<NOT_GIVEN>'
    location: str = '<NOT_GIVEN>'
    employer: str = '<NOT_GIVEN>'
    date_posted: str = str(datetime.now()).split(' ')[0]
    n_applicants: str = '0'
    industries: str = ''
    industries_1: str = ''
    industries_2: str = ''
    employment_type: str = ''
    job_function: str = ''
    job_function_1: str = ''
    seniority_level: str = ''
