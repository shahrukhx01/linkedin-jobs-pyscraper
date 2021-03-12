from pydantic import BaseModel

class Searcher(BaseModel):
    """
    Search model for storing search configuration.
    Keyword arguments:
    search_pages_per_search_term -- Number of paginations to be processed per search term.
    search_terms -- list of search keywords to be searched.
    batch_size -- number of data points after which to checkpoint data to file
    output_filepath -- path to csv file on disk
    """
    search_url : str = 'https://www.linkedin.com/jobs/search?keywords={}&location={}&trk=public_jobs_jobs-search-bar_search-submit&f_TP=1&redirect=false&position=1&pageNum={}'
    search_pages_per_search_term : int
    search_terms : list
    location: str = ''
    batch_size: int
    output_filepath: str = 'out.csv'
    batch_num: int = 0
    li_jobs_api: str = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    job_ids: list = list()
    scraped_job_ids: list = list()
    scraped_jobs: list = list()