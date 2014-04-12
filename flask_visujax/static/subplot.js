/* Stores jqplot figures instances */
var subplot_figs = {};

/* Store result of subplotForm2js */
var subplotJs = {};

/* Stores function to obtain x-array */
var subplotGetDataX = {};

/* Stores function to obtain y-array */
var subplotGetDataY = {};

/* Create empty jqplot figures, for latter data update and plot */
function populateSubplotFigs(subplotName, nrows, ncols, ncurves) {
    subplot_figs[subplotName] = [];

    var datacurves = [];
    for (var icurve=0 ; icurve<ncurves ; icurve++) {
        datacurves.push([undefined]);
    }

    var row;
    var fig;
    var opt = {title:'no title', legend:{show:true}, seriesDefaults:{show:true} };
    for (var irow=0 ; irow<nrows ; irow++) {
        row = [];
        for (var icol= 0 ; icol<ncols ; icol++) {
            name = 'subplot_placeholder_' + irow + '_' + icol;
            fig = $.jqplot(name,datacurves,opt)
            row.push(fig);
        }
        subplot_figs[subplotName].push(row);
    }
}

function zip(a,b) {
    var zipped = [];
    for (var i = 0 ; i < a.length ; i++) {
        zipped[i] = [a[i],b[i]];
    }
    return zipped;
}

function cartProd(paramArray) {
  function addTo(curr, args) {
    var i, copy, 
        rest = args.slice(1),
        last = !rest.length,
        result = [];
    for (i = 0; i < args[0].length; i++) {
      copy = curr.slice();
      copy.push(args[0][i]);
      if (last) {
        result.push(copy);
      } else {
        result = result.concat(addTo(copy, rest));
      }
    }
    return result;
  }
  return addTo([], Array.prototype.slice.call(arguments));
}

/* Trigged when submit button of subplot Form is clicked */
function onSubplotFormSubmit(subplotFormId) {
    // Parse form data.
    var d = subplotForm2js(subplotFormId);
    // Report form errors.
    var error_report_items = $("#velocitySubplotForm ul").empty();
    $.each(d.errors, function(idx,error_string) {
        error_report_items.append('<li>'+error_string+'</li>');
    });
    var error_report = $("#velocitySubplotForm [name=error_report]");
    if (d.errors.length > 0) {
        error_report.show();
    }
    else {
        // Add parse data in global dictionary.
        error_report.hide();
        subplotJs[d.name] = d;
        console.log("ready to plot!");
    }
    return false;
}

function updateSubplot(name) {
    d = subplotJs[name];
    x = subplotGetDataX[name]()
    figs = subplot_figs[name]

    // Clear figures.
    console.log("clear figures");
    var irow, icol, icurve;
    for (irow=0 ; irow<d.maxRows ; irow++) {
        for (icol=0 ; icol<d.maxCols ; icol++) {
            for (icurve=0 ; icurve<d.maxCurves ; icurve++) {
                figs[irow][icol].series[icurve].data = [[undefined]];
                figs[irow][icol].series[icurve].show = false;
            }
            figs[irow][icol].replot({resetAxes:true});
        }
    }

    // Iterate on rows.
    console.log("plot curves");
    params = {};
    $.each(d.rows, function(irow,rowParamValue) {
        params[d.rowParamName] = rowParamValue;
        // Iterate on columns.
        $.each(d.cols, function(icol,colParamValue) {
            params[d.colParamName] = colParamValue;
            // Iterate on curves.
            $.each(d.curveParamCartProd, function(icurve,curveParamSet) {
                $.extend(params,curveParamSet);
                var y = subplotGetDataY[d.name](params)
                figs[irow][icol].series[icurve].data = zip(x,y);
                figs[irow][icol].series[icurve].show = true;
                figs[irow][icol].series[icurve].label = d.curveLabels[icurve];
            });
            var t = d.rowParamName+rowParamValue+'_'+d.colParamName+colParamValue;
            figs[irow][icol].title.text = t;
            figs[irow][icol].replot({resetAxes:true});
        });
    });

    return false;
};


/* Convert subplot form data to well-ordened JavaScript structure */
function subplotForm2js(subplotFormId) {

    // Parse using form2js, see https://github.com/maxatwork/form2js
    var formData = form2js(subplotFormId);

    // Read HTML hidden fields.
    var maxCols = formData['_maxCols'];
    var maxRows = formData['_maxRows'];
    var maxCurves = formData['_maxCurves'];
    var rowParamName = formData['_row'];
    var colParamName = formData['_col'];
    var allParamNames = formData['_allParamNames'];
    var name = formData['_name'];

    var errors = [];

    // Every param is required.
    $.each(allParamNames, function(indx,name) {
        if (! (name in formData)) {
            errors.push(name + " is required.");
        }
    });

    // Construct rows, check its length.
    var rows;
    if (rowParamName in formData) { // Otherwise, an error is already set by (0) or (1).
        rows = formData[rowParamName];
        if (rows.length > maxRows) {
            errors.push("Maximum row's items is " + maxRows + 
            ", but got " + rows.length + " items.");
        };
    } else {
        rows = undefined;
    }

    // Construct cols, check its length.
    var cols;
    if (colParamName in formData) { // Otherwise, an error is already set by (0) or (1).
        cols = formData[colParamName];
        if (cols.length > maxCols) {
            errors.push("Maximum column's items is " + maxCols + 
            ", but got " + cols.length + " items.");
        };
    } else {
        cols = undefined;
    }

    // Check row and column are different.
    if (rowParamName == colParamName) {
        errors.push("Column and row must be different.");
    }

    // Construct curves, and check number of curves of curves per fig does not
    // exceed maximum.
    var curves = {};
    if (errors.length == 0) {
        ncurves = 1;
        $.each(allParamNames, function(idx,name) {
            if (name==rowParamName || name==colParamName || name[0]=='_') return true;
            curves[name] = formData[name]
            ncurves *= formData[name].length;
        });
        if (ncurves > maxCurves) {
            errors.push("Too much curves (" + ncurves +
                ") to plot. Maximum is " + maxCurves + ".");
        }
    }

    // [ [a0,a1,...], [b0,b1,...], ...]
    var curveParamValuesList = [];
    var curveParamCartProdNames = [];
    for (curveParamName in curves) {
        curveParamCartProdNames.push(curveParamName);
        curveParamValuesList.push( curves[curveParamName] );
    }
    // [ [a0,b0,...], [a0,b1,...], ... ]
    curveParamCartProdList = cartProd.apply(this,curveParamValuesList);

    curveLabels = [];
    curveParamCartProd = [];
    $.each(curveParamCartProdList, function(icurve,curveParamSetList) {
        var label = "";
        var curveParamSet = {};
        $.each(curveParamCartProdNames , function(iCurveParam,curveParamName) {
            curveParamSet[curveParamName] = curveParamSetList[iCurveParam];
            label += curveParamName + curveParamSetList[iCurveParam] + "_";
        });
        curveLabels.push(label);
        curveParamCartProd.push(curveParamSet);
    });

    return {
        name : name, // string

        rowParamName : rowParamName, // string
        rows : rows, // array
        maxRows : maxRows, // int

        colParamName : colParamName,
        cols : cols, // array
        maxCols : maxCols, // int

        curves : curves, // {'curveParamName': [curveParamValue,...], ...}
        curveLabels : curveLabels, // ['label0', 'label1', ...]
        curveParamCartProd : curveParamCartProd, // [{'A':a0,'B':b0,...}, {'A':a0,'B':b1,...},]
        maxCurves : maxCurves, // int

        errors : errors // array of string
    }
}
