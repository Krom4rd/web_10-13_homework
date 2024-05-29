from django.test import TestCase
from models import Author
from connect_mongo import authors_from_mongodb
def authors_seeds():
    data = authors_from_mongodb()

    Author.objects.create(**data)

if __name__=="__main__":
    authors_seeds()



