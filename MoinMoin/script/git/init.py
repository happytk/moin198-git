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
from dulwich.repo import Repo, NotGitRepository

class PluginScript(MoinScript):

    def __init__(self, argv, def_values):
        MoinScript.__init__(self, argv, def_values)


    def migrate_repo(self, repo, page_dir):

        request = self.request

        # move the directory
        source_dir = os.path.join(page_dir, '.git')
        dest_dir = os.path.join(request.cfg.data_dir, 'pages.git')
        os.rename(source_dir, dest_dir)

        # create git file
        gitfile_path = source_dir
        with file(gitfile_path, 'w') as f:
            f.write('gitdir: ' + dest_dir)


    def make_config(self, repo, page_dir):
        # config
        with file(os.path.join(page_dir, '.git', 'config'), 'w') as f:
            f.write('''[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
    ignorecase = true
    precomposeunicode = true
    quotepath = false
[receive]
    denyCurrentBranch = updateInstead
''')

    def make_gitignore(self, repo, page_dir):
        # make .gitignore
        with file(os.path.join(page_dir, '.gitignore'), 'w') as f:
            f.write('''current
edit-log
edit-lock
synctags
tags
cache/
revisions/

# systempage
MissingPage/
BadContent/''')

        repo.stage(['.gitignore'])
        repo.do_commit(message='init with gitignore')

    def mainloop(self):

        self.init_request()
        request = self.request

        page_dir = os.path.join(request.cfg.data_dir, 'pages')
        try:
            repo = Repo(page_dir)
            print 'Repo already exists.'
            return
        except NotGitRepository:
            repo = Repo.init(page_dir)

        self.make_config(repo, page_dir)
        self.make_gitignore(repo, page_dir)
        self.migrate_repo(repo, page_dir)


