# -*- coding: UTF-8 -*-
#format python

"""
MoinMoin - Python Code

"""

import sys
import StringIO
#import cStringIO
import urllib
import traceback
from MoinMoin.action import cache
from MoinMoin.action import AttachFile
from MoinMoin.parser._ParserBase import ParserBase
from MoinMoin import caching
from MoinMoin.Page import Page
import codecs

Dependencies = ["time"]
LibPage = 'PageLibrary'

class Parser:

    def __init__(self, raw, request, **kw):
        self.pagename      = request.page.page_name
        self.request       = request
        self.formatter     = request.formatter
        self.raw           = raw
        self.args_string   = kw.get('format_args','')
        self.args          = self.args_string.split()

        #self.attpath = AttachFile.getAttachDir(request, LibPage, create=0)
        #if self.attpath not in sys.path:
        #    sys.path.append(AttachFile.getAttachDir(request, LibPage, create=0))

    ### encoding isseus

    # symptom:
    # - 1) formÀ¸·Î ¹Þ¾Æ¿Í¼­ Ã³¸®ÇÏ´Â ÇÑ±Û°ª¿¡ ´ëÇÑ ¿À·ù
    # - 2) u''·Î Ã³¸®µÇ´Â ÇÑ±Û¿¡ ´ëÇÑ ¿À·ù
    # - 3) ''·Î Ã³¸®µÇ´Â ÇÑ±Û¿¡ ´ëÇÑ ¿À·ù
    # - 4) formÃ³¸®¿Í ÇÑ±ÛÃâ·Â('')ÀÌ ¼¯¿©ÀÖ´Â °æ¿ì
    # - 5) formÃ³¸®¿Í ÇÑ±ÛÃâ·Â(u'')ÀÌ ¼¯¿©ÀÖ´Â °æ¿ì
    #
    # trying case:
    # - case 1 : StringIO
    # - case 2 : cStringIO - formµ¥ÀÌÅ¸¸¦Ã³¸®ÇÏÁö ¸øÇÔ
    # - case 4 : codecs.getwriter("utf-8")(s) Ã³¸®
    #          - http://stackoverflow.com/questions/1817695/python-how-to-get-stringio-writelines-to-accept-unicode-string
    #
    # result:
    #         | 1 | 2 | 3 | 4 | 5 |
    # -------------------------------------
    # case1   | o | o | o | x | o |
    # case2   | x | x | o | x | x |
    # case1+4 | o | o | x | o | x |
    # case2+4 | o | o | x | o | x |
    #
    # solution: case1 is better
    #
    def format(self, formatter):
        context = {}
        context["request"] = self.request
        #print 'x'*30, self.request.__hash__()

        #print self.raw.encode('cp949')
        #s = StringIO.StringIO()
        code = self.raw#u'#-*- encoding: UTF-8 -*-\n' + self.raw

        # txt = []
        # for arg in self.args:
        #     txt.append(Page(self.request, arg).get_raw_body())
        # txt = '\n'.join(txt)

        #print globals().keys()
        # print dir(self.request.request)
        # print self.request.request
        # print self.request.request.application
        # print dir(self.request.request.application)
        # print self.request.__hash__()
        # print self.request.request.__hash__()
        # print self.request.request.__dict__.keys()
        # if 'tmp' in self.request.request.__dict__:
        #     self.request.request.__dict__['tmp'] += 1
        # else:
        #     self.request.request.__dict__['tmp'] = 1
        # print self.request.request.__dict__['tmp']
        if '__shared' not in self.request.request.__dict__:
            self.request.request.__dict__['__shared'] = None
        # print self.request.request.__dict__['__shared']

        # r = self.request.request

        # from MoinMoin.web.serving import RequestHandler
        # r = RequestHandler()
        # if hasattr(r, '__shared'):
        #     tmp = r.__getattr__('__shared')
        #     r.__setattr__('__shared', tmp + 1)
        # else:
        #     r.__setattr__('__shared', 1)
        # print r.__getattr__('__shared')

        s = StringIO.StringIO()
        # s = codecs.getwriter(self.request.cfg.attachment_charset)(s) # http://stackoverflow.com/questions/1817695/python-how-to-get-stringio-writelines-to-accept-unicode-string
        sys.stdout = s


        try:
            #exec(txt + code, context)
            try:
                local_scope_dict = {'request':self.request, '__shared': self.request.request.__dict__['__shared']}
            except AttributeError:
                local_scope_dict = {'request':self.request, '__shared': None}
            exec(code) in globals(), local_scope_dict
            # self.request.query_bindvar_dict = local_scope_dict['query_bindvar_dict']
            self.request.request.__dict__['__shared'] = local_scope_dict['__shared']
            # print 'y'*30, self.request.__hash__()
            # local_scope_dict={'request':self.request}
            # exec(code) in globals(), local_scope_dict
            # self.request=local_scope_dict['request']
            # print 'y'*30, self.request.__hash__()
        except:
            from MoinMoin.parser.text_python import Parser
            Parser(code, self.request).format(formatter)
            sys.stdout.write("<pre>")
            traceback.print_exc(file=sys.stdout)
            sys.stdout.write("</pre>")
        sys.stdout = sys.__stdout__
        try:
            try:
                lines = s.getvalue()#.decode(self.request.cfg.attachment_charset)
                self.request.write(lines)
            except (UnicodeDecodeError, UnicodeEncodeError):
                print s.getvalue()
                lines = s.getvalue()
                self.request.write(lines)
        except:
            self.request.write("<pre>")
            traceback.print_exc(file=self.request)
            self.request.write("</pre>")
 
