# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Maintenance Script Package

    @copyright: 2006 MoinMoin:ThomasWaldmann
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.util import pysupport
from dulwich.repo import Repo, NotGitRepository
import os

# create a list of extension scripts from the subpackage directory
git_scripts = pysupport.getPackageModules(__file__)
modules = git_scripts

def get_repo(request):
    path = os.path.join(request.cfg.data_dir, 'pages')
    try:
        repo = Repo(path)
    except NotGitRepository:
        repo = None

    return repo
