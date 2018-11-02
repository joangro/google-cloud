from flask import Flask, request

app = Flask(__name__)


@app.route('/basic_handler', methods=['POST'])
def basicHandler():
    '''Test that payload works'''
    payload = request.get_data(as_text=True) or '(empty payload)'
    print('Received task with payload: '+payload)
    return 'Payload received: '+payload

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)

