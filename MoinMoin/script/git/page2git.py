# -*- coding: utf-8 -*-
"""
MoinMoin - wikipage2git

@copyright: 2004-2006 MoinMoin:ThomasWaldmann
@license: GNU GPL, see COPYING for details.
"""

debug = False

import codecs
import os
from MoinMoin import PageEditor, Page
from MoinMoin.script import MoinScript
from MoinMoin.action.AttachFile import _get_files, getAttachDir
from . import get_repo

class PluginScript(MoinScript):

    def __init__(self, argv, def_values):
        MoinScript.__init__(self, argv, def_values)

    def mainloop(self):
        self.init_request()
        request = self.request

        repo = get_repo(request)
        if repo is None:
            print 'repo is not exists'
            return

        # Get all existing pages in the wiki
        pagelist = request.rootpage.getPageList(user='')
        page_dir = os.path.join(request.cfg.data_dir, 'pages')

        need_to_staged = []

        # import pdb; pdb.set_trace()

        for pagename in pagelist:
            p = Page.Page(request, pagename)
            body = p.get_raw_body()

            # page
            gitfilepath = os.path.join(page_dir, p.page_name_fs + '.md')
            need_update = True
            if os.path.exists(gitfilepath):
                if codecs.open(gitfilepath, 'rb', 'utf8').read() == body:
                    need_update = False

            if need_update:

                with codecs.open(gitfilepath, 'wb', 'utf8') as f:
                    f.write(body)
                print p.page_name_fs + '.md'
                need_to_staged.append(p.page_name_fs + '.md')

            # attachments
            attach_dir = getAttachDir(request, pagename)
            files = _get_files(request, pagename)
            for filename in files:
                print os.path.join(p.page_name_fs, 'attachments', filename)
                need_to_staged.append(os.path.join(p.page_name_fs, 'attachments', filename))

        if len(need_to_staged):
            repo.stage(need_to_staged)
            repo.do_commit(message='init-with-moin(%d pages)' % len(need_to_staged))
