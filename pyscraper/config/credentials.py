import os
## mongo credentials from environment variables
credentials = {
'mongo_username': os.environ['MONGO_LINKEDIN_USERNAME'],
'mongo_password': os.environ['MONGO_LINKEDIN_PASSWORD']
}