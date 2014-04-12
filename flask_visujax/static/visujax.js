var visujax = {


    /*======================================================================*/
    /*=========================== common methods ===========================*/
    /*======================================================================*/


    timeout_sijax: function(callback_name,milliseconds) {
        setTimeout(function(){Sijax.request(callback_name)},milliseconds);
    },

    SijaxClick: function(callback_name) {
        Sijax.request(callback_name);
        return false;
    },

    SijaxForm: function(callback_name,formId) {
        var formData = form2js(formId);
        console.log(formData);
        Sijax.request(callback_name,[formData]);
    },

    data: {},

    UpdateData: function(datanew) {
        for (var key in datanew) {
            visujax.data[key] = datanew[key];
        }
    },

    zip: function(a,b) {
        var zipped = [];
        for (var i = 0 ; i < a.length ; i++) {
            zipped[i] = [a[i],b[i]];
        }
        return zipped;
    },

    /*======================================================================*/
    /*============================= plot plugin ============================*/
    /*======================================================================*/


    plot: {
        figs: {},

        new_fig: function(name) {
            var figid = 'visujax_plot_' + name;
            visujax.plot.figs[figid] = $.jqplot(figid,  [[[0, -1],[6.5,1]]]);
        },

        clear: function(name) {
            var figid = 'visujax_plot_' + name;
            visujax.plot.figs[figid].series[0].data=[[undefined]];
            visujax.plot.figs[figid].replot({resetAxes:false});
        },

        replot: function(name,xid,yid) {
            console.log("replot",name,xid,yid);
            var figid = 'visujax_plot_' + name;
            var fig = visujax.plot.figs[figid];
            var x = visujax.data[xid];
            var y = visujax.data[yid];
            fig.series[0].data = visujax.zip(x,y);
            fig.replot({resetAxes:false});
        },
    }

};
