# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - RecentChangeSummury Macro

    This very complicated macro produces a line break.

    @copyright: 2006 HappyTk (rainyblue-gmail)
    @license: GNU GPL, see COPYING for details.
"""

import re, time, sys
from datetime import datetime
from MoinMoin.Page import Page
from MoinMoin import wikiutil
from MoinMoin.logfile import editlog
from MoinMoin.parser.text_moin_wiki import Parser as WikiParser
from MoinMoin import wikiutil


def getPageListFromLog (macro, req_year, req_week_number,comments_only):
    request = macro.request
    pages = {}
    oldyw = -1
    passed= False

    for line in editlog.EditLog(request).reverse():

        if not request.user.may.read(line.pagename):
            continue

        line.time_tuple = request.user.getTime(wikiutil.version2timestamp(line.ed_time_usecs))
        year,wn,wd = datetime.isocalendar(datetime.fromtimestamp(time.mktime(line.time_tuple)))
        yw = '%04d%02d' % (year,wn)

        if req_year > 0 and req_week_number > 0:
            if req_week_number == wn and req_year == year:
                passed = True
            elif passed and ((req_week_number < wn and req_year == year) or req_year < year):
                break #for a performance
            else:
                continue

        if not pages.has_key(yw):
            pages[yw] = {}

        if pages[yw].has_key(line.pagename):
            pages[yw][line.pagename].append(line.comment)
        else:
            pages[yw][line.pagename] = [line.comment]


    ret = []
    for yw in reversed(sorted(pages.keys())):
        if len(pages[yw].keys()) > 0:
            ret.append("WEEK%s, %s" % (yw[-2:], yw[:4]))
            for page in reversed(sorted(pages[yw].keys(), key=lambda x:len(pages[yw][x]))):
                edit_cnt = len(pages[yw][page])
                comments = filter(lambda x:len(x)>0, pages[yw][page])


                p = Page(request, page)

                if len(comments)>0 or not comments_only:
                    if p.exists():
                        ret.append(' * [[%s]] (%s)' % (page, str(edit_cnt)))
                    else:
                        ret.append(' * `%s` (%s)' % (page, str(edit_cnt)))
                    for comment in comments:
                        ret.append('  * ' + comment)
            """
            ret.append('<b>WEEK%s, %s</b>'% (yw[-2:],yw[:4]))
            ret.append('<ol>')
            for page in reversed(sorted(pages[yw].keys(), key=lambda x:len(pages[yw][x]))):
                page_link = Page(request,page).link_to(request, '%s(%d) ' % (page,len(pages[yw][page]),), css_class="include-page-link")
                comments = filter(lambda x:len(x)>0, pages[yw][page])
                if comments_only and len(comments)>0:
                    ret.append('<li>'+page_link+'</li>')
                    ret.append('<ul>')
                    for comment in comments:
                        ret.append('<li>' + comment + '</li>')
                    ret.append('</ul>')
                elif not comments_only:
                    ret.append('<li>'+page_link+'</li>')
                    ret.append('<ul>')
                    for comment in comments:
                        ret.append('<li>' + comment + '</li>')
                    ret.append('</ul>')
            ret.append('</ol>')
            """

    macro_str = "<<%s(%s)>>" % (macro.name, macro.args)
    content_str = '\n'.join(ret)
    form = u'''<form method='post'>
    <input type='hidden' name='action' value='ReplaceTagAction'>
    <input type='hidden' name='rsv' value='0'>
    <input type='hidden' name='regexp' value='0'>
    <textarea name='tag' style='display:none'>%s</textarea>
    <textarea name='txt' style='display:none'>%s</textarea>
    <input type='submit' value='   HARDCOPY TO THIS PAGE   '>
</form>
''' % (macro_str, content_str)
    return wikiutil.renderText(request, WikiParser, wikiutil.escape(content_str)) + form

def macro_RecentChangeSummury(macro, year=0, week_number=0, comments_only=False):
    
    if year == 0 and week_number == 0:
        year, week_number, wd = datetime.isocalendar(datetime.today())

    return getPageListFromLog(macro,year,week_number,comments_only)
    


