#-*-encoding:utf-8-*-
"""
    MoinMoin - Comment Macro

    Copyright (c) 2003 by taewook <my@tang.pe.kr>
    All rights reserved, see COPYING for details.

    Display a sequence of blog pages.

    $Id: Comment.py,v 1.1.1.1 2005/11/01 07:17:52 look Exp $
"""

import sys
import cStringIO
import re
import time
#from MoinMoin import editlog, user, config, wikiutil
from MoinMoin.Page import Page
#from MoinMoin.i18n import _


def execute(macro, args):
    try:
        arg = args.split(',')
    except AttributeError:
        arg = []

    if len(arg) > 1:
        entry_id = arg[0].strip()
        try:
            row = int(arg[1])
        except ValueError:
            row = 4

        try:
            use_custum_author = int(arg[2])
        except (ValueError, IndexError):
            use_custum_author = False
    else:
        entry_id = ''
        row = 4
        use_custum_author = False
    return _make_html(macro.request.getScriptname(), macro.formatter.page.page_name, use_custum_author, row, entry_id)


def _make_html(script_name, page_name, use_custum_author=False, row=3, entry_id=''):
    if use_custum_author:
        ret = "<table border='0'>"
        ret += "<form action='%s' method='post' name='gbook' onsubmit='return saveAuthor(\"gb_author_for_%s\", \"gb_comment_for_%s\");'>" % (
            script_name + '/' + page_name, page_name, page_name)
        ret += "<tr><td width='70%'>"
        ret += "<textarea name='comment' id='gb_comment_for_%s' style='width:95%%;' rows='%d'></textarea>" % (
            page_name, row)
        ret += "</td><td valign='bottom'><input type='text' name='custom_author' id='gb_author_for_%s' size='15' onfocus='this.value=\"\";'> <br/><input type='submit' value='comment'>" % page_name
        ret += "<input type='hidden' name='action' value='PageComment4'>"
        if use_custum_author:
            ret += "<input type='hidden' name='use_custum_author' value='%d'>" % use_custum_author
        if entry_id:
            ret += "<input type=hidden name='entry_flag_id' value='%s'>" % entry_id
        ret += "</tr></form></table>"
        ret += """
<script>
<!--
getAuthor('gb_author_for_%s');
//-->
</script>""" % page_name
    else:
        ret = "<form action='%s' method='post' name='gbook'>" % (
            script_name + '/' + page_name)
        ret += "<textarea name='comment' style='width:100%%;' rows='%d'></textarea>" % row
        ret += "<br><input type='submit' value='post'>"
        ret += "<input type='hidden' name='action' value='PageComment4'>"
        if use_custum_author:
            ret += "<input type='hidden' name='use_custum_author' value='%d'>" % use_custum_author
        if entry_id:
            ret += "<input type='hidden' name='entry_flag_id' value='%s'>" % entry_id
        ret += "</form>"
    return ret
