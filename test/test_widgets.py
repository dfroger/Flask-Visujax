import sys
import os
from flask import render_template, Flask, g
from flask_bootstrap import Bootstrap
import sijax
import flask_sijax

sys.path.append('..')
from widgets import Label, PlotReplace
from bootstraprow import BootstrapRow, Column, Rectangle
from prettify import prettify
from sijaxutil import NumserveResponse

sijax_path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax')

app = Flask(__name__)
app.config['SIJAX_STATIC_PATH'] = sijax_path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)
Bootstrap(app)

@app.template_filter('is_bootstrap_row')
def is_bootstrap_row(value):
    return isinstance(value,BootstrapRow)

class Response(sijax.response.BaseResponse):
    def __init__(self,*args,**kwargs):
        sijax.response.BaseResponse.__init__(self,*args,**kwargs)
        self.status = Label('status',self)
        self.time = Label('time',self)
        self.plot = PlotReplace('y',self)

class LabelRow(BootstrapRow):
    col = Column(twelfth=3)
label = Label(text="label")

class MainRow(BootstrapRow):
    left_col = Column(twelfth=3)
    left = Rectangle(label='left',ratio=0.5,height=200)

    middle_col = Column(twelfth=6)
    middle = Rectangle(label='middle',ratio=2,height=200)

    right_col = Column(twelfth=3)
    right = Rectangle(label='right',ratio=0.5,height=200)

class Handler(object):

    @staticmethod
    def run(resp):
        m.start()
        resp.plot.replace_x(m.x())
        resp.status.set_text('running')
        resp.call("timeout_sijax",['update',250])

    @staticmethod
    def update(resp):
        resp.time.set_text("%.2f" % m.time())
        resp.plot.y.replace(m.y())
        resp.plot.replot()
        if m.is_alive():
            resp.call("timeout_sijax",["update",250])
        else:
            if m.stopped():
                resp.status.set_text("stopped!")
            else:
                resp.status.set_text("complete!")

    @staticmethod
    def stop(resp):
        m.stop()

    @staticmethod
    def clear(resp):
        resp.call("figclear")
        resp.time.set_text("")

@flask_sijax.route(app,"/")
def index():
    if g.sijax.is_sijax_request:
        sijax.register_object(Handler,response_class=NumserveResponse)
        return g.sijax.process_request()
    return prettify(render_template('test_widgets.html',bootstrap_rows=[row0,row1]))

if __name__ == "__main__":
    row0 = LabelRow()
    row1 = MainRow()
    m = Master()
    app.run(debug=True)
