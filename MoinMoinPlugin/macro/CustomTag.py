# -*- coding: utf-8 -*-
"""
    MoinMoin - CustomTag Macro

    This very complicated macro produces a line break.

    @copyright: 2006 HappyTk (rainyblue-gmail)
    @license: GNU GPL, see COPYING for details.
"""

import re, time, sys, datetime, urllib, cgi
from MoinMoin.Page import Page
from MoinMoin import wikiutil
from MoinMoin.logfile import editlog
from MoinMoin import search
from MoinMoin.parser.text_moin_wiki import Parser as WikiParser


_MAX_DAYS = 30

def getPageListFromSearch (request,args):
    # If called with empty or no argument, default to regex search for .+, the full page list.
    needle = wikiutil.get_unicode(request, args, 'needle', u'regex:.+')

    # With whitespace argument, return same error message as FullSearch
    #if not needle.strip():
    #    err = 'Please use a more selective search term instead of {{{"%s"}}}' % needle
    #    return '<span class="error">%s</span>' % err

    # Return a title search for needle, sorted by name.
    try:
        results = search.searchPages(request, needle,
                                     titlesearch=1, case=0,
                                     sort='page_name')
        pages = results.hits#pageList(macro.request, macro.formatter, paging=False)
        pages = map(lambda x:x.page_name, pages)
    except ValueError:
        # same error as in MoinMoin/action/fullsearch.py, keep it that way!
        """
        ret = ''.join([macro.formatter.text('<<PageList('),
                      _('Your search query {{{"%s"}}} is invalid. Please refer to '
                        'HelpOnSearching for more information.', wiki=True,
                        percent=True) % wikiutil.escape(needle),
                      macro.formatter.text(')>>')])
        """
        pages = []
    return pages


def getPageListFromLog (request):
    this_day = request.user.getTime(time.time())[0:3]
    log = editlog.EditLog(request)
    pages = {}
    pagelist = []
    ignore_pages = {}
    day_count = 0

    for line in log.reverse():
        if not request.user.may.read(line.pagename):
            continue

        line.time_tuple = request.user.getTime(wikiutil.version2timestamp(line.ed_time_usecs))
        day = line.time_tuple[0:3]

        if ((this_day != day or (not _MAX_DAYS))) and len(pages) > 0:
            # new day or bookmark reached: print out stuff
            this_day = day
            for page in pages:
                ignore_pages[page] = None

            for page in pages.values():
                pagelist.append(page[0].pagename)

            pages = {}
            day_count += 1
            if _MAX_DAYS and (day_count >= _MAX_DAYS):
                break

        elif this_day != day:
            # new day but no changes
            this_day = day

        if ignore_pages.has_key(line.pagename):
            continue

        # end listing by default if user has a bookmark and we reached it
        if not _MAX_DAYS:
            break

        if pages.has_key(line.pagename):
            pages[line.pagename].append(line)
        else:
            pages[line.pagename] = [line]
    else:
        if len(pages) > 0:
            for page in pages.values():
                pagelist.append(page[0].pagename)
    return pagelist


def getIndentationLevel(line):
    spacecount = 0
    for c in line:
        if c == " ":
            spacecount += 1
        else:
            break
    return spacecount

def findtext_by_re (request, task_re, re_exp, rpl_text, page):
    result = []
    sublines = []

    lines = page.getlines()
    lvl = 0
    include = False

    for line_index in range(0,len(lines)):

        line = lines[line_index]

        # 하위컨텐츠는 모두 집어넣는다.
        line_lvl = getIndentationLevel(line)
        if include == True and lvl < line_lvl:
            sublines.append(' ' * (line_lvl - lvl + 1) + line.lstrip())
            #tasklines.append(line)
        else:

            #하위컨텐츠를 모두 넣고 indentation이 감소해 마무리지어야 할때
            if include:

                editlinkform = {}
                editlinkform['action'] = 'edit'
                editlinkform['srev'] = page.current_rev()
                pageedit_link = page.link_to(request,text=page.page_name,querystr=urllib.urlencode(editlinkform))
                # editlinkform['startline'] = headline_index+1
                # editlinkform['endline'] = line_index
                # lineedit_link = page.link_to(request,text='lineedit',querystr=urllib.urlencode(editlinkform))

                edit_link = "(<<HTML(%s)>>)" % (pageedit_link)

                # if rpl_text != "" and rpl_text != None:
                #     donelinkform = {}
                #     donelinkform['action'] = 'CustomTagAction'
                #     donelinkform['srev'] = page.current_rev()
                #     donelinkform['editline'] = headline_index
                #     donelinkform['reg'] = re_exp
                #     donelinkform['rpl_text'] = rpl_text
                #     done_link = page.link_to(request,text=rpl_text,querystr=urllib.urlencode(donelinkform))
                #     done_link = "(<<HTML(%s)>>)" % (done_link)
                # else:
                #     done_link = ""

                # headline의 indentaion은 무조건 1로 설정
                headline = ' ' + headline.lstrip()
                if headline.startswith(' 1.'):
                    headline = ' * ' + headline[3:]
                if not headline.startswith(' * '):
                    headline = ' * ' + headline
                if headline.startswith(' * ToDo:'):
                    headline = ' * [[%s]]:%s' % (page.page_name, headline[8:])

                # headline_withlink = '%s %s%s' % (headline, done_link,edit_link)
                headline_withlink = '%s %s' % (headline, edit_link)
                result.append(headline_withlink)
                result.extend(sublines)

                sublines = []
                headline= ""
                headline_index = -1
                include = False

            m = task_re.match(line)
            if m != None:
                #마지막에 처리하기 위해 headline에 잠시 넣어두고 하위컨텐츠 수집시작
                headline = line
                #수정페이지링크를 위해 index임시저장
                headline_index = line_index
                #이 indentation level보다 작은 라인은 모두 수집한다.
                lvl = getIndentationLevel(line)
                #다음라인부터 검색하기 위해 flag변경
                include = True
            else:

                lvl = 0


    if len(result)>0:
        #macro.request.write(page.link_to(macro.request, '%s ' % (pagename,), css_class="include-page-link"))
        #page.set_raw_body('\n'.join(result),1)
        #page.send_page(content_only=1)
        pass
    return '\n'.join(result)

def find_by_re (request, formatter, re_exp, rpl_text, search):

    ret = []

    if not hasattr(request, "_Include_backto"):
        request._Include_backto = formatter.page.page_name

    if search == None:
        pages = getPageListFromLog(request)
        ret.append('Results from recent-log(%d pages):' % len(pages))
    else:
        pages = getPageListFromSearch(request,search)
        ret.append('Results from searching by __%s__(%d pages):' % (search, len(pages)))

    task_re = re.compile(re_exp, re.UNICODE|re.DOTALL)

    for pagename in pages:

        if pagename == formatter.page.page_name: continue

        page = Page(request, pagename)
        if not page.exists(): continue

        ret.append(findtext_by_re(request, task_re, re_exp, rpl_text, page))

    return wikiutil.renderText(request, WikiParser, '\n'.join(ret))#wikiutil.escape('\n'.join(ret)))

#from advancedsearch.py (macro)
def form_get(request, name, default='', escaped=False):
    """ Fetches a form field

    @param request: current request
    @param name: name of the field
    @param default: value if not present (default: '')
    @param escaped: if True, escape value so it can be used for html generation (default: False)
    """
    value = request.values.get(name, default)
    if escaped:
        value = wikiutil.escape(value, quote=True)
    return value


def macro_CustomTag(macro, exp, rpl_text, needle=u'', search_form=False):

    if exp is None or exp == '':
        return u'<pre>%s</pre>' % cgi.escape(u'''
검색tag는 반드시 입력해야합니다.

Arguments:
 - exp : 검색expression, 필수
 - rpl_text : 교체될text, 옵션
 - needle : 검색대상, 옵션 (전체의 경우 .*)
 - search_form : needle검색창을 넣기 (기본값:false)

Example:
 - <<CustomTagMacro(exp)>> #exp를 RecentChanges에서 검색
 - <<CustomTagMacro(exp,rpl_text)>> #exp를 RecentChanges에서 검색, rpl_text로 대체할 것임
 - <<CustomTagMacro(exp,rpl_text,needle)>> #exp를 needle기준으로 검색, rpl_text로 대체할 것임

Etc:
 - 호출하는 페이지의 내용은 검색되지 않습니다.
''')


    #매크로에서지정한값이 있더라도 needle을 폼으로 지정했다면 그게 우선권
    if macro.request.values.has_key('needle'):
        needle = form_get(macro.request, 'needle', '')

    ## case for being no needle from macro argument
    if needle is None or needle == '':
        _MAX_DAYS = 7
        needle = None

    action = form_get(macro.request, 'action', '')
    if action != 'raw' and action != 'print' and search_form:
        html = [
            u'<form method="get" action="">',
            #u'<div>',
            u'''<input type="text" name="needle" size="25" value="%s"><input type="submit" value="SEARCH">''' % (needle or ""),
            #u'</div>',
            u'</form>',
            ]

        macro.request.write(u'\n'.join(html))


    return find_by_re(macro.request, macro.formatter, exp, rpl_text, needle)#r"^(\s)+\*\sTODO:\s(?!\-\-\().*")

