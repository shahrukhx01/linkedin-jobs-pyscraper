import logging
import yaml
from scraper.exceptions.exception import InvalidConfigurationException
from datetime import datetime, timedelta
from dateutil.relativedelta import *
#from elasticsearch import Elasticsearch 
from scraper.config.credentials import credentials
import json
import pymongo

def read_config(config_path):
    if not config_path:
        config_path = 'scraper/config/scraper_config.yaml'

    with open(r'{}'.format(config_path)) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        scraper_config = yaml.load(file, Loader=yaml.FullLoader)
        print(credentials)
    return (scraper_config, credentials)

def get_logger():
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(name='LinkedIn Jobs Scraper')

def write_to_file(data, file_path):
    with open(file_path,'a+') as f:
        f.write('{}\n'.format(data))

def read_from_file(file_path):
    with open(file_path,'r') as f:
        return [job_id.rstrip('\n') for job_id in f.readlines()] ## preprocess job_ids

def get_mongo_client(scraper_config, credentials):
    mongo_collection = None
    try:
        mongo_client = pymongo.MongoClient(scraper_config['mongo_connect_url'].format(credentials['mongo_username'], credentials['mongo_password'], scraper_config['mongo_db']))
        mongo_db = mongo_client[scraper_config['mongo_db']]
        mongo_collection = mongo_db[scraper_config['mongo_collection']]
    except Exception as e:
        print(e)
    
    return mongo_collection 



def rel_time_to_absolute_datetime(relative_time_str):
    N = int(relative_time_str.split(' ')[0])
    date_n_days_ago = None
    if 'day' in relative_time_str:
        date_n_days_ago = datetime.now() - timedelta(days=N)
    elif 'week' in relative_time_str:
        date_n_days_ago = datetime.now() - relativedelta(months=-N)
    elif 'month' in relative_time_str:
        date_n_days_ago = datetime.now() - relativedelta(months=-N)

    return str(date_n_days_ago).split(' ')[0]

def write_to_es(index_name, data, es_client):
   str_data = json.dumps(data)
   print(data)
   try:
       res = es_client.exists(index=index_name, id=data['_id'])
       es_client.index(index=index_name, id=data['_id'], body=json.loads(str_data))
   except  Exception as e: print(e)


def write_to_mongo(mongo_collection, data):
    response = None
    try:
        response = mongo_collection.insert_one(data)
    except:
        response = "Job already has been crawled."
    return response
        

