from flask import Flask, request

from google.appengine.api import search


app=Flask(__name__)

@app.route('/')
def index():
    return "Search API module"


@app.route('/createDocument/{}')
def createDocument(documentName):


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)

