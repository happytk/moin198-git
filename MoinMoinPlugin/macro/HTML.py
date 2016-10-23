# -*- coding: iso-8859-1 -*-
"""
    HTML Macro

    @copyright: 2009 happytk
    @license: GNU GPL, see COPYING for details.
"""

Dependencies = ["language"]

import urllib
from MoinMoin.packages import unpackLine

def execute(macro, args):
    """ Return a translation of args, or args as is """
    return args