#!/usr/bin/env python

class Param:
    def __init__(self,name, name_human, values, col=False,row=False):
        self.name = name
        self.name_human = name_human
        self.values = values
        self.col = col
        self.row = row

class Subplot:
    def __init__(self,name,nrows,ncols,ncurves,nchoices,params):
        self.name = name
        self.nrows = nrows
        self.ncols = ncols
        self.ncurves = ncurves
        self.nchoices = nchoices
        self.params = params

        rows = []
        cols = []

        for param in params:
            if len(param.values) > nchoices:
                raise ValueError, "Param %r has %i values, but " \
                "maximum allowed is %i." % (
                param.name, len(param.values), nchoices)
            if param.row:
                rows.append(param.name)
            if param.col:
                cols.append(param.name)

        if len(rows) == 0:
            raise ValueError, "No parameters has the row flag"
        elif len(rows) > 1:
            raise ValueError, "More than one parameter with the row flag: %r" % rows

        if len(cols) == 0:
            raise ValueError, "No parameters has the col flag"
        elif len(cols) > 1:
            raise ValueError, "More than one parameter with the col flag: %r" % cols


