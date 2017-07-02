from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
from bokeh.themes import Theme
import yaml
import random
from tornado.ioloop import IOLoop
from BFXLight.client import Client
import datetime

io_loop = IOLoop.current()

theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """))

def make_document(doc):
    source = ColumnDataSource({'x': [], 'y': []})
    client = Client()

    def update():
        data = client.pubticker("ethusd")
        new = {'x': [datetime.datetime.utcfromtimestamp(data['timestamp'])],
               'y': [data['last_price']],
               }
        source.stream(new)

    doc.add_periodic_callback(update, 500)

    fig = figure(title='Streaming Ticker Data!', sizing_mode='scale_height',
                 x_axis_type='datetime',
                 y_axis_label='Price (USD)',
                 # output_backend="webgl",
                 )
    fig.line(source=source, x='x', y='y')

    doc.title = "Now with live updating!"
    doc.theme = theme
    doc.add_root(fig)


apps = {'/': Application(FunctionHandler(make_document))}

server = Server(apps, port=5006)
server.start()

def main():
    print('Opening BFXLight dashboard application on http://localhost:5006/')
    io_loop.add_callback(server.show, "/")
    io_loop.start()

if __name__ == '__main__':
    main()
