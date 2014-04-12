import os

from flask import Flask, render_template, g
from flask_bootstrap import Bootstrap
from flask_wtf import Form as FlaskForm
import sijax
import flask_sijax
import flask_visujax
from wtforms import Form, IntegerField
from werkzeug import MultiDict
from wtforms.validators import DataRequired
# include Form from wtforms instead of flask_wtf, in order to
# pass 'form_data' received from Ajax, instead of the normal Flask
# object comming form Post, that flask_wtf automatically passed.

from flask_visujax import BootstrapRow, Column, Content, Label, \
    PlotReplace, Button, BaseResponse
from flask_visujax import Form as WidgetForm
from util import Master
from prettify import prettify

path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax')

app = Flask(__name__)
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
app.config['WTF_CSRF_ENABLED'] = False
app.config['WTF_CSRF_SECRET_KEY'] = 'a random string'
flask_sijax.Sijax(app)
flask_visujax.Visujax(app)
Bootstrap(app)

@app.template_filter('is_bootstrap_row')
def is_bootstrap_row(value):
    return isinstance(value,BootstrapRow)

class ControlForm(Form):
    number = IntegerField('Number of seconds', validators=[DataRequired()])

class Response(BaseResponse):

    def __init__(self,*args,**kwargs):
        BaseResponse.__init__(self,*args,**kwargs)
        self.status = Label('status',self)
        self.time = Label('time',self)
        self.plot = PlotReplace('foo',self)

class Handler(object):

    @staticmethod
    def run(resp,form_data):
        form = ControlForm(MultiDict(form_data))
        if not form.validate():
            resp.status.set_text("Number of seconds missing!")
            return
        m.nseconds = form.number.data
        m.start()
        resp.update_data(x=m.x())
        resp.status.set_text('running')
        resp.timeout('update',250)

    @staticmethod
    def update(resp):
        resp.time.set_text("%.2f" % m.time())
        resp.update_data(y=m.y())
        resp.plot.replot('x','y')
        if m.is_alive():
            resp.timeout("update",250)
        else:
            if m.stopped():
                resp.status.set_text("stopped!")
            else:
                resp.status.set_text("complete!")

    @staticmethod
    def stop(resp):
        m.stop()

class ControlFlaskForm(FlaskForm):
    number = IntegerField('Number of seconds', validators=[DataRequired()])

class StatusRow(BootstrapRow):
    col = Column(twelfth=12)
    status = Label('status')

class TimeRow(BootstrapRow):
    col = Column(twelfth=12)
    time = Label('time')

class MainRow(BootstrapRow):
    left_col = Column(twelfth=6)
    chart = PlotReplace("foo")

    right_col = Column(twelfth=6)
    form = WidgetForm(ControlFlaskForm,'visujax_form_control')
    run = Button('Run','visujax.SijaxForm',['run','visujax_form_control'])
    clear = Button('Clear','visujax.plot.clear',['foo'])
    stop = Button('Stop','visujax.SijaxClick',['stop'])

@flask_sijax.route(app,'/')
def home():
    if g.sijax.is_sijax_request:
        g.sijax.register_object(Handler, response_class=Response)
        return g.sijax.process_request()
    return prettify(render_template('visujax/content.html',content=content))

if __name__ == "__main__":
    content = Content(StatusRow(), TimeRow(), MainRow())
    m = Master()
    app.run(debug=True)
