from pydantic import BaseModel, ValidationError
from enum import Enum

class RelevanceFilters(Enum):
    RELEVANT = 'R'
    RECENT = 'DD'



class TimeFilters(Enum):
    ANY = ''
    DAY = '1'
    WEEK = '1,2'
    MONTH = '1,2,3,4'


class TypeFilters(Enum):
    FULL_TIME = 'F'
    PART_TIME = 'P'
    TEMPORARY = 'T'
    CONTRACT = 'C'
    INTERNSHIP = 'I'
    VOLUNTEER = 'V'
    OTHER = 'O'


class ExperienceLevelFilters(Enum):
    INTERNSHIP = '1'
    ENTRY_LEVEL = '2'
    ASSOCIATE = '3'
    MID_SENIOR = '4'
    DIRECTOR = '5'
    EXECUTIVE = '6'


class Filters(BaseModel):
     time: TimeFilters
     job_type: TypeFilters
     relevance: RelevanceFilters
     experience: ExperienceLevelFilters

class FilterMap(BaseModel):
    time: str = 'f_TP'
    relevance: str = 'sortyBy'
    job_type: str = 'f_JT'
    experience: str = 'f_E'


     
