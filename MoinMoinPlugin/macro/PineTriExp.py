# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - PineTriExp
    show the chart from pinetri-export-data

    @license: GNU GPL, see COPYING for details.
"""


Dependencies = ["page"]

def macro_PineTriExp(macro, ym, uid, width=None, height=None):
    result = '''
<div id="chart_''' + ym + "" + uid + '''"></div>
<div style="clear:both;"></div>
<script type="text/javascript" src="/static/js/d3.min.js"></script>
<script type="text/javascript" src="/static/js/ptreev2.js"></script>
<script>
    var ym = "''' + ym + '''";
    var uid = "''' + uid + '''";
    var static_to = function(selection) {

        var dat = selection[0][0].__data__;
        d3.json('/histchart/export/_entry/' + dat.ym + '/' + dat.uid + '.json', function(result) {
            // console.log(result);
            var cfg = result.cfg;
            cfg.data_columns.forEach(function(d) {
                d.title = dat.title;
            });'''
    if width:
        result += '''
            cfg.width = ''' + str(width) + ''';
        '''
    if height:
        result += '''
            cfg.height = ''' + str(height) + ''';
        '''
    result += '''

            var refchart = d3.ptreev2.refchart(cfg);
            var datasets = result.dat;
            datasets.forEach(function(ds) {
                // ds.values.forEach(function(d) {
                //  d._tid = d3.ptreev2.std_dt_fmt.parse(d._tid);
                // });
                refchart.data_update(ds);
                refchart.chart(selection);
            });
        });
    };
    var divobj = d3.select("#chart_''' + ym + "" + uid + '''")
                    // .append('div')
                    //.insert('div', ":first-child")
                    //.attr('id', 'chart_' + g_chart_idx)
                    // .datum(chart)
                    // .call(chart.chart)
                    ;
    // chart.chart(d3.select('#chart_' + g_chart_idx));
    // d3.select('#chart_add_to').append('option').attr('value', 'chart_' + g_chart_idx).text('chart_' + g_chart_idx);
    divobj.datum({'ym':ym, 'uid':uid, 'title':ym + '-' + uid}).call(static_to);
</script>
'''
    return result


