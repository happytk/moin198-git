# -*- coding: utf-8 -*-
"""
MoinMoin - do global changes to all pages in a wiki.

@copyright: 2004-2006 MoinMoin:ThomasWaldmann
@license: GNU GPL, see COPYING for details.
"""
import os
import shutil

from MoinMoin.script import MoinScript
from dulwich.repo import Repo, NotGitRepository

class PluginScript(MoinScript):

    def __init__(self, argv, def_values):
        MoinScript.__init__(self, argv, def_values)

    def mainloop(self):

        self.init_request()
        request = self.request

        while True:
            n = raw_input('THIS CANNOT BE RECOVERED! DO YOU REALLY WANT TO DELETE GIT-REPO? (y/*) ')
            if n.lower() == 'y':
                break
            else:
                continue

        page_dir = os.path.join(request.cfg.data_dir, 'pages')
        try:
            repo = Repo(page_dir)
        except NotGitRepository:
            print 'Repo is not exists'
            return

        # delete *.md
        for filename in os.listdir(page_dir):
            if filename.endswith('.md') and os.path.exists(os.path.join(page_dir, filename)):
                os.remove(os.path.join(page_dir, filename))
                print 'deleted', filename
        # delete .git
        filepath = os.path.join(page_dir, '.git')
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)
            print 'deleted', '.git'
        elif os.path.exists(filepath):
            os.remove(filepath)
            print 'deleted', '.git'

        # delete .gitignore
        filepath = os.path.join(page_dir, '.gitignore')
        if os.path.exists(filepath):
            os.remove(filepath)
            print 'deleted', '.gitignore'

        # delete ../pages.git
        filepath = os.path.join(request.cfg.data_dir, 'pages.git')
        # os.remove(os.path.join(request.cfg.data_dir, 'pages.git'))
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)
            print 'deleted', 'pages.git'

