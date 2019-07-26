from google.appengine.api import search
from datetime import datetime
from faker import Faker

from flask import url_for

fake = Faker()

def create_index_and_document():

    data_gen = document_data_generator()

    for author, text, date, num in data_gen:

        date_fmt=datetime.strptime(date, '%Y-%M-%d')

        index = search.Index(name="Books")

        fields = [
            search.TextField(name='Author', value=author),
            search.DateField(name='Date', value=date_fmt),
            search.TextField(name='Text', value=text), 
            search.TextField(name='Author', value=str(num)) 
            ]

        document = search.Document(doc_id=fake.ean(length=13), fields=fields)

        index.put(document)

def document_data_generator(iters=10000):

    for _ in range(iters):

        import random

        yield  fake.name(), fake.sentence(), fake.date(), random.randint(2, 50)


