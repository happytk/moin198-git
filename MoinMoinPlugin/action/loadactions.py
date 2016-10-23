# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - loadactions Action
    
    Triggers multiple actions at once.
    Actions are defined in actions[] CGI parameter, 
    where actions[] is array of action names.

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.action import ActionBase
from MoinMoin.action import getHandler

from submitbase import SubmitError


def execute(pagename, request):
    for action in request.form.getlist("actions[]"):
        handler = getHandler(request, action)
        try:
            if handler:
                handler(pagename, request)
        except SubmitError:
            # Stop executing next actions if there is an error
            break
