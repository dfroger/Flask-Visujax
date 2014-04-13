from flask import Blueprint

from widgets import *
from response import *
from bootstraprow import Column, BootstrapRow, Content

class Visujax(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        @app.template_filter('is_bootstrap_row')
        def is_bootstrap_row(value):
            print 'is_bootstrap_row'
            return isinstance(value,BootstrapRow)

        blueprint = Blueprint(
            'visujax',
            __name__,
            template_folder = 'templates',
            static_folder = 'static',
            static_url_path = app.static_url_path + '/visujax'
        )

        app.register_blueprint(blueprint)
