from flask import Flask, render_template, request
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
def index():
    return "hello"


@app.route('/bokeh')
def bokeh_handler():
    from bokeh.plotting import figure
    from bokeh.resources import CDN
    from bokeh.embed import file_html

    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    p.line(x, y, legend="Temp.", line_width=2)

    html = file_html(p, CDN, "my plot")

    return html


@sockets.route('/socket')
def my_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
