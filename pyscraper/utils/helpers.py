from datetime import datetime, timedelta
from dateutil.relativedelta import *
from search.search_jobs import Search
import pandas as pd


def get_search_instance(searcher):
    """
    Creates search instance for running the search on LinkedIn.
    Keyword arguments:
    config -- pydantic model
    """
    ## create searcher model
    return Search(searcher)    ## return instantiated searcher object
    

def write_to_file(data, batch_number, file_path):
    """
    Writer list of dictionaries to csv using Pandas.
    Keyword arguments:
    data -- list, list of dictionaries to be written on file.
    batch_number -- 
    file_path -- output file path
    """
    df = pd.DataFrame(data, columns=data[0].keys())
    if batch_number > 0:
        df.to_csv(file_path, mode='a', header=False)
    else:
        df.to_csv(file_path)

def rel_time_to_absolute_datetime(relative_time_str):
    """
    Writer list of dictionaries to csv using Pandas.
    Keyword arguments:
    data -- list, list of dictionaries to be written on file.
    batch_number -- 
    file_path -- output file path
    """
    N = int(relative_time_str.split(' ')[0])
    date_n_days_ago = None
    if 'day' in relative_time_str:
        date_n_days_ago = datetime.now() - timedelta(days=N)
    elif 'week' in relative_time_str:
        date_n_days_ago = datetime.now() - relativedelta(months=-N)
    elif 'hours' in relative_time_str:
        date_n_days_ago = datetime.now() - relativedelta(hours=-N)
    elif 'month' in relative_time_str:
        date_n_days_ago = datetime.now() - relativedelta(months=-N)
    return str(date_n_days_ago).split(' ')[0]


