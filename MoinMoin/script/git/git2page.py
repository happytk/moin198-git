# -*- coding: utf-8 -*-
"""
MoinMoin - do global changes to all pages in a wiki.

@copyright: 2004-2006 MoinMoin:ThomasWaldmann
@license: GNU GPL, see COPYING for details.
"""

debug = False

import codecs
import os

from MoinMoin import PageEditor
from MoinMoin.script import MoinScript
from MoinMoin.wikiutil import unquoteWikiname

class PluginScript(MoinScript):

    def __init__(self, argv, def_values):
        MoinScript.__init__(self, argv, def_values)

    def mainloop(self):

        self.init_request()
        request = self.request

        # Get all existing pages in the wiki
        # pagelist = request.rootpage.getPageList(user='')
        page_dir = os.path.join(request.cfg.data_dir, 'pages')
        pagelist = os.listdir(page_dir)
        for pagename_fs in pagelist:
            if not pagename_fs.endswith('.md'):
                continue

            pagename = unquoteWikiname(pagename_fs[:-3])

            p = PageEditor.PageEditor(request, pagename, do_editor_backup=0)
            origtext = p.get_raw_body()

            gitfilepath = os.path.join(page_dir, pagename_fs)
            gittext = codecs.open(gitfilepath, 'rb', 'utf8').read()
            gittext = gittext.replace(u'\r', u'')
            if gittext != origtext:
                # import pdb; pdb.set_trace()
                print "Writing %s ..." % repr(pagename_fs)
                p._write_file(gittext)

