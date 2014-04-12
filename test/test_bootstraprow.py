import sys
from flask import render_template, Flask

sys.path.append('..')
from bootstraprow import BootstrapRow, Column, Rectangle, Label
from prettify import prettify

app = Flask(__name__)

@app.template_filter('is_bootstrap_row')
def is_bootstrap_row(value):
    return isinstance(value,BootstrapRow)

class LabelRow(BootstrapRow):
    col = Column(twelfth=3)
    label = Label(label="label")

class MainRow(BootstrapRow):

    class NestedRow(BootstrapRow):
        col_left = Column(twelfth=6)
        right_top0 = Rectangle(label='right-top-0',ratio=0.5)

        col_right = Column(twelfth=6)
        right_top1 = Rectangle(label='right-top-1',ratio=0.5)

    left_col = Column(twelfth=3)
    left_top = Rectangle(label='left-top',ratio=0.5)
    left_bot = Rectangle(label='left-bot',ratio=0.5)

    middle_col = Column(twelfth=6)
    middle = Rectangle(label='middle',ratio=2,height=200)

    right_col = Column(twelfth=3)
    right_top = NestedRow()
    right_bot = Rectangle(label='right-bot',ratio=0.5)

row0 = LabelRow()
row1 = MainRow()

with app.test_request_context('/cols'):
    print prettify(render_template('grid-basic.html',bootstrap_rows=[row0,row1]))
