from widgets import RowItemCounter

from collections import OrderedDict

class Column(RowItemCounter):
    def __init__(self,twelfth=None):
        RowItemCounter.__init__(self)
        self.twelfth = twelfth
        self._items = OrderedDict()
        self.divclass = "col-sm-%i" % self.twelfth
    def append(self,name,value):
        """element is either a Widget or a (nested) Row"""
        self._items[name] = value
        setattr(self,name,self._items[name])
    @property
    def items(self):
        return self._items.values()
    @property
    def items_dict(self):
        return self._items
    def __repr__(self):
        return "<Column>"
    def __str__(self):
        return "<Column>"
    def __iter__(self):
        for name,value in self._items.iteritems():
            yield name, value

class BootstrapRowBase(RowItemCounter):

    def __init__(self):
        RowItemCounter.__init__(self)

    @property
    def columns_dict(self):
        return self._columns

    @property
    def columns(self):
        return self._columns.values()

class MyMetaClass(type):
    """
    Data structure
    V self._columns = {<col_name>:<col_instance>, ...}
    
    Accessor
    V self.columns_dict  -> {<col_name>:col_instance, ...}
    V self.widgets_dict  -> {<widget_name>:<widget_instance>, ...}
    V self.<col_name>    -> col_instance
    V self.<widget_name> -> widget_instance
    """

    def __init__(cls, clsname, bases, attrs):
        type.__init__(cls, clsname, bases, attrs)

    def __new__(cls, clsname, bases,dct):

        def is_row_item(value):
            return isinstance(v,RowItemCounter) or \
                   isinstance(v,BootstrapRowBase)

        _columns = OrderedDict()
        # Get row items from Row attributes.
        items = OrderedDict(sorted( 
            [(k,v) for k,v in dct.iteritems() if is_row_item(v)],
            key = lambda t: dct[t[0]].creation_order))
        
        # Check for overrided Row attributes.
        creation_orders = [-1] + [ w.creation_order for w in items.values() ]
        for i in range(1,len(creation_orders)):
            if creation_orders[i] != creation_orders[i-1]+1:
                pass
                #print "Warning: row element number %i is missing" % (i-1)

        # Compute column index in items.
        cols_idx = [idx for idx,item in enumerate(items.values()) if isinstance(item,Column)]
        if len(cols_idx) == 0:
            return type.__new__(cls, clsname, bases, dct)

        if cols_idx[0] != 0:
            raise ValueError, "First item must be a Column"

        # Check for empty columns
        for i in range( len(cols_idx)-1 ):
            if cols_idx[i] + 1 == cols_idx[i+1]:
                raise ValueError, "Column %i is empty." % i
        if cols_idx[-1] == len(items)-1:
            raise ValueError, "Column %i is empty." % len(items)

        cols_idx.append( len(items) )

        for icol in range( len(cols_idx)-1 ):
            colname = items.keys()[cols_idx[icol]]
            col = items[colname]
            i0 = cols_idx[icol]+1
            i1 = cols_idx[icol+1]
            for name in items.keys()[i0:i1]:
                col.append(name,items[name])
            _columns[colname] = col

        # Add access methods.
        dct['_columns'] = _columns
        _widgets = OrderedDict()
        for name,col in _columns.iteritems():
            dct['name'] = property(lambda self: col)
            for wname,widget in col:
                #widget.id = wname
                dct[wname] = widget
                _widgets[wname] = widget
        dct['widgets_dict'] = property(lambda self: _widgets)
        dct['widgets'] = property(lambda self: _widgets.values())

        return type.__new__(cls, clsname, bases, dct)

class BootstrapRow(BootstrapRowBase):
    __metaclass__ = MyMetaClass

class Content(object):
    def __init__(self,*rows):
        self.rows = rows

    def __iter__(self):
        for row in self.rows:
            yield row
