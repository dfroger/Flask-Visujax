from flask import get_template_attribute
from bs4 import BeautifulSoup

class RowItemCounter(object):
    creation_order = 0
    def __init__(self):
        self.creation_order = RowItemCounter.creation_order
        RowItemCounter.creation_order += 1

class BaseWidget(RowItemCounter):
    def __init__(self,prefix="sijaxvisu_"):
        self.prefix = prefix
        RowItemCounter.__init__(self)

    @property
    def id(self):
        return "{w.prefix}_{w.htmlid}".format(w=self)

class Rectangle(BaseWidget):
    def __init__(self,name,obj_response=None,ratio=1,height=100):
        self.name = name
        self.ratio = ratio
        self.height = height
        BaseWidget.__init__(self)

    def set_obj_response(self,obj_response):
        self.obj_response = obj_response

    def render_html(self):
        return '<div style="height:%ipx;border:1px solid #000;"> %s </div>' \
                % (self.height,self.label) 

    def render_js(self):
        return ''

class Label(BaseWidget):
    """Label widget"""

    def __init__(self,name,obj_response=None):
        self.name = name
        self.obj_response = obj_response
        BaseWidget.__init__(self)

    def set_obj_response(self,obj_response):
        self.obj_response = obj_response

    def set_text(self,text):
        id_ = "#%s_label" % self.name
        self.obj_response.html(id_,text)

    def render_html(self):
        return '<p> Status/iteration: <span id="%s_label"> </span> </p>' % self.name

    def render_js(self):
        return ''

class PlotReplace(BaseWidget):
    """2d plot widget"""

    def __init__(self,name,obj_response=None):
        self.name = name
        self.obj_response = obj_response
        BaseWidget.__init__(self)

    def set_obj_response(self,obj_response):
        self.obj_response = obj_response

    def replot(self,x,y):
        self.obj_response.call("window.visujax.plot.replot",[self.name,x,y])

    def render_html(self):
        figid = "visujax_plot_%s"  % self.name
        return '<div id="%s" style="height:200px;width:400px; "></div>' % figid

    def render_js(self):
        return 'visujax.plot.new_fig("%s");' % self.name

class Form(BaseWidget):
    def __init__(self,form_cls,htmlid):
        BaseWidget.__init__(self)
        self.form_cls = form_cls
        self.htmlid = htmlid
    def render_html(self):
        form = self.form_cls()
        quick_form = get_template_attribute('bootstrap/wtf.html', 'quick_form')
        html = quick_form(form,method="").unescape()
        soup = BeautifulSoup(html)
        soup.findAll('form')[0].attrs['id'] = self.htmlid
        return soup.prettify()
    def render_js(self):
        return ''

class Button(BaseWidget):
    def __init__(self,label,js_function,js_args):
        self.js_function = js_function
        self.js_args = js_args
        self.label = label
        BaseWidget.__init__(self)
    def render_html(self):
        args = ','.join( ['"%s"' % arg for arg in self.js_args] )
        return """<input class='btn btn-default' type='button' value='%s' onclick='%s(%s);'/>""" \
                % (self.label, self.js_function, args)
    def render_js(self):
        return ''
