from flask import Flask, request

app = Flask(__name__)


@app.route('/example_task_handler', methods=['POST'])
def basic_handler():
    '''Test that payload works'''
    payload = request.get_data(as_text=True) or '(empty payload)'
    print('Received task with payload: '+payload)
    return 'Payload received: '+payload

@app.route('/')
def rootHandler():
    return 'hi from cloud'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

