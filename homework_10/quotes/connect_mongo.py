from pymongo import MongoClient
from homework_10.settings import BASE_DIR
import environ

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')


client = MongoClient(host=env("MONGO_CLIENT"))
db = client[env('MONGO_DB_NAME')]
# Mongo connect

def authors_from_mongodb():
    '''
    returns a list of dictionaries with such padding:
    [{'full_name':type(str), 'born_date':type(datetime), 'born_location':type(str), 'description':type(str)},...]
    data from mongodb
    '''

    collection = db['authors']

    mongodb_data = collection.find()
    result = []
    for item in mongodb_data:
        result.append({'full_name': item.get('fullname'),
                       'born_date': item.get('born_date'),
                       'born_location': item.get('born_location'),
                       'description': item.get('description')
                       })
    return result


def quotes_from_mongodb():
    '''
    returns a list of dictionaries with such padding:
    [{''author': type(str),', tags: type(list), quote: type(str)...]
    data from mongodb
    '''

    collection = db['quote']
    mongodb_data_quotes = collection.find()
    collection = db['authors']
    mongodb_data_authors = collection.find()
    result = []
    for item in mongodb_data_quotes:
        for author in mongodb_data_authors:
            if author.get('_id') == item.get('author'):
                author_fullname = author.get('fullname')
        result.append({
                        'author': author_fullname,
                        'tags': item.get('tags'),
                        'quote': item.get('quote')
                        })
    return result
