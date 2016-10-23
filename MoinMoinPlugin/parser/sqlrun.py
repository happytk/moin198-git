# -*- coding: UTF-8 -*-
#format python
#sqlrun parser
from __future__ import absolute_import
from MoinMoin.parser._ParserBase import ParserBase
from datetime import timedelta, datetime
import traceback
import sys

from MoinMoin import log
logging = log.getLogger(__name__)

Dependencies = ["time"]
Available_options = ['async', 'sync', 'share_result',
                    # 'show_header', 'hide_header', 
                    # 'show_sql', 'hide_sql',
                    'show_table', 'hide_table', 
                    'show_chart', 'hide_chart'
                    # ,'show_toolbox', 'hide_toolbox'
                    ]

class Parser:

    def __init__(self, raw, request, **kw):
        self.pagename      = request.page.page_name
        self.request       = request
        self.args_string   = kw.get('format_args','')
        self.args          = self.args_string.split()
        self.fetch         = True
        self.dbname        = ''
        self.params        = {}
        self.query         = raw
        # self.chart_script  = ''
        self.__shared      = self.request.request.__dict__['__shared'] if '__shared' in self.request.request.__dict__ else {}
        self.options       = []
        # self.option_show_sql = True
        # self.option_show_chart = False
        self.option_show_table = True
        # self.option_show_toolbox = True
        # self.option_show_info = True
        self.option_share_result = False
        self.option_async = True

    def validate(self):

        # IMPORT HERE for dynamic env-check
        from easy_sqlrun.tasks import sql

        # dbname
        self.dbname = self.args[0]

        # option check
        self.options = self.args[1:]
        delta = set(self.options) - set(Available_options)
        if len(delta) > 0:
            raise Exception('Unknown options - %s. All available_options are %s' % (','.join(delta), ','.join(Available_options)))

        # self.option_show_chart = 'show_chart' in self.options and 'hide_chart' not in self.options
        self.option_show_table = 'hide' not in self.options
        # self.option_show_sql = 'show_sql' in self.options and 'hide_sql' not in self.options
        # self.option_show_toolbox = 'show_toolbox' in self.options and 'hide_toolbox' not in self.options
        # self.option_show_info = self.option_show_toolbox
        self.option_share_result = 'share_result' in self.options
        self.option_async = 'sync' not in self.options


        # bindvar check
        param_keys = sql.checkBindVars(self.query)
        self.params = {}
        for k in param_keys:
            v = self.request.values.get(k)
            if v is not None:
                self.params[k] = v
            else:
                try:
                    qbd = self.request.request.__dict__['__shared']
                    if type(qbd) == type({}):
                        self.params[k] = qbd[k]
                    else:
                        raise AttributeError()
                except (AttributeError, KeyError):
                    #if not self.params.has_key(i):
                    self.params[k] = ''
                    pass #raise Exception('error - failed to bind \'%s\'' % k)

    def format(self, formatter):
        if len(self.args) <= 0:
            from MoinMoin.wikiutil import importPlugin
            sqlparser = importPlugin(self.request.cfg, 'parser', 'sql', 'Parser')
            sqlparser(self.query, self.request).format(formatter)
        else:
            try:
                self.validate()
                self.__run_n_format(formatter)
            except Exception as inst:
                from MoinMoin.wikiutil import importPlugin
                sqlparser = importPlugin(self.request.cfg, 'parser', 'sql', 'Parser')
                sqlparser(self.query, self.request).format(formatter)

                self.request.write(u'<pre>%s</pre>' % str(inst))

                import traceback, sys
                traceback.print_exc(file=sys.stdout)


    def __run_n_format(self, formatter):

        # IMPORT HERE for dynamic environment check
        from easysr.tasks import sql, html_table, html_chart

        # create
        s = sql(self.query, self.params)
        # sr = sqlrun(self.dbname, s)

        if self.option_async:
            task_id = 'sqlrun-' + s.uid
            data = s.rrun(str(self.dbname), task_id=task_id)
            # data = sr.run_async(task_id)
        else:
            # data = sr.run_sync()
            data = s.rrun(str(self.dbname), sync=True)

        if self.option_share_result:
            self.request.request.__dict__['__shared'] = data

        if self.option_show_table:
            table = html_table(data)
            # table.show_toolbox = self.option_show_toolbox
            # table.show_sql = self.option_show_sql
            # table.show_info = self.option_show_info
            self.request.write(table.format())

        # if self.option_show_chart:
        #     chart = html_chart(data)
        #     # chart.custom_script = self.chart_script
        #     # chart.show_toolbox = self.option_show_toolbox
        #     # chart.show_sql = self.option_show_sql
        #     # chart.show_info = self.option_show_info
        #     self.request.write(chart.format())
