from linkedin_jobs_pyscraper.models.search.searcher import Searcher
from linkedin_jobs_pyscraper.models.filters import filters
from linkedin_jobs_pyscraper.linkedin_jobs_scraper import LinkedInJobsPyScraper
def main():
    ## create searach query with configurations
    searcher = Searcher(
        search_pages_per_search_term = 4,
        search_terms = ['data analyst', 'data scientist'],
        batch_size = 5,
        output_filepath = 'out.csv',
        location = 'Germany'
        )

    search_filter = filters.Filters(
        experience= filters.ExperienceLevelFilters.INTERNSHIP,
        job_type= filters.TypeFilters.INTERNSHIP,
        relevance= filters.RelevanceFilters.RECENT,
        time= filters.TimeFilters.MONTH
        )
    scraper = LinkedInJobsPyScraper(searcher= searcher, filters=search_filter) 
    scraper.start()

if __name__ == "__main__":
    main()