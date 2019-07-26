from google.appengine.api import search

from flask import url_for

faker

def create_index_and_document():
    index = search.Index(name="Books")
    fields = [
            search.TextField(name='Author', 
