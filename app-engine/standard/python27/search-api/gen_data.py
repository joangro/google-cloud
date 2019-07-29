from google.appengine.api import search
from datetime import datetime
from flask import url_for
from faker import Faker
import time


fake = Faker()


'''
The next two functions are used to create Documents and generate fake data
'''
def create_index_and_document():
    '''
    Called from the '/gendata' handler, it creates documents and puts them into the "Book" index. 
    It fills every document identity with random data from the "faker" library.
    '''
    data_gen = document_data_generator()

    for author, text, date, num in data_gen:

        date_fmt=datetime.strptime(date, '%Y-%M-%d')

        index = search.Index(name="Books")

        fields = [
            search.TextField(name='Author', value=author),
            search.DateField(name='Date', value=date_fmt),
            search.TextField(name='Text', value=text), 
            search.NumberField(name='Price', value=num) 
            ]

        document = search.Document(doc_id=fake.ean(length=13), fields=fields)

        index.put(document)

        time.sleep(0.05)

def document_data_generator(iters=10000):
    '''
    Generator to create the random data by either calling the "faker" module or the standard "random" library.
    '''
    for _ in range(iters):

        import random

        yield  fake.name(), fake.sentence(), fake.date(), random.randint(2, 50)


'''
[BATCH INSERT] The next two functions are used to create Documents and generate fake data, like the previous one, but using batching to not stress as much the Search API
'''
def batch_create_index_and_document():
    '''
    As indicated by the documentation (https://cloud.google.com/appengine/docs/standard/python/search/best_practices#batch_indexput_and_indexdelete_calls), it's possible to batch insert
    documents up to 200 at a time. This is implemented here.
    '''
    data_gen = batch_document_data_generator()

    documents = []

    index = search.Index(name="Books")
    
    for counter, data in enumerate(data_gen):
        if counter%200 == 0:
            index.put(documents)
            documents = []
            time.sleep(2)

        date_fmt=datetime.strptime(data['date'], '%Y-%M-%d')


        fields = [
            search.TextField(name='Author', value=data['author']),
            search.DateField(name='Date', value=date_fmt),
            search.TextField(name='Text', value=data['sentence']), 
            search.NumberField(name='Price', value=data['price']) 
            ]

        document = search.Document(doc_id=fake.ean(length=13), fields=fields)

        documents.append(document)

def batch_document_data_generator(iters=10000):
    '''
    Generator to create the random data by either calling the "faker" module or the standard "random" library.
    '''
    for _ in range(iters):

        import random

        yield  {'author':   fake.name(), 
                'sentence': fake.sentence(), 
                'date':     fake.date(), 
                'price':    random.randint(2, 50)}

'''
The next two functions are used to add random properties to each document on the "Books" index
'''
def create_property():

    data_gen = create_property_generator()

    for property in data_gen():
        pass

def create_property_generator():
    pass

