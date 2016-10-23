# -*- coding: utf-8 -*-

import os
import json
from MoinMoin import search, wikiutil
from MoinMoin.log import logging
from MoinMoin.logfile import editlog
from MoinMoin.Page import Page
from MoinMoin.macro.RecentChanges import logchain
from .attachf import get_attachments, getAttachUrl, getAttachDir


"""

easy_attach에서 쉽게 첨부파일이나 페이지링크를 붙일 수 있도록 도와주는 datapump
return type은 json


"""


PAGE_COUNT = 10

def _page_search(request, pagename, include_self=False):
    # XXX error handling!
    try:
        raise Exception('Redis')
    except:
        searchresult = search.searchPages(request, 't:"%s"' % pagename)

    pages = [p.page_name for p in searchresult.hits]
    pages.sort()
    if include_self:
        pages[0:0] = [pagename]
    return pages

def _page_attachments(request, pagename, link_with_pagename=False):
    attach_dir = getAttachDir(request, pagename)
    files = get_attachments(pagename, request, attach_dir)
    for file in files:
        if file['ext'] in ('.mp3', '.jpg', '.gif', '.png'):
            bracket_typ = ('{{', '}}')
        else:
            bracket_typ = ('[[', ']]')
        efile = wikiutil.escape(file['file'])
        if link_with_pagename:
            name = '%sattachment:%s/%s%s' % (bracket_typ[0], pagename, efile, bracket_typ[1],)
            file['pagename'] = pagename
        else:
            name = '%sattachment:%s%s' % (bracket_typ[0], efile, bracket_typ[1],)
        file['id'] = name
        file['text'] = name
        file['src'] = getAttachUrl(pagename, file['file'], request)
    return files

def execute(pagename, request):
    # page = Page(request,pagename)
    # return page.send_page(content_only=1)

    # list of wiki pages
    typ = request.values.get('typ', 'name')
    page = int(request.values.get('page', 1))

    # logging.error(typ)
    if typ == 'name':
        name = request.values.get("name", "")
        include_self = int(request.values.get('self', 0))
        # logging.error(name)
        if name:
            pages = _page_search(request, name, include_self)
            pages = [Page(request, p) for p in pages]
            pages = [{'id':'[[%s]]' % p.page_name, 'text': p.page_name} for p in pages if p.exists()]
        else:
            pages = []
        # logging.error(pages)
        request.write(json.dumps({'items':pages[(page-1)*PAGE_COUNT:page*PAGE_COUNT], 'more':len(pages)>page*PAGE_COUNT}))
    elif typ == 'attachment':
        """
        단일페이지에서 첨부파일을 찾고 싶을 때
        """
        pagename = request.values.get("pagename", pagename)
        if pagename:
            atts = _page_attachments(request, pagename)
        else:
            atts = []
        request.write(json.dumps({'items':atts[(page-1)*PAGE_COUNT:page*PAGE_COUNT], 'more':len(atts)>page*PAGE_COUNT}))
    elif typ == 'attachments':
        """
        여러개의 페이지에서 첨부파일목록을 받고 싶을때
        """
        name = request.values.get("name", "")
        atts = []
        if name:
            pagenames = _page_search(request, name)
            for pagename in pagenames:
                atts.extend(_page_attachments(request, pagename, link_with_pagename=True))
                if len(atts) > page*PAGE_COUNT:
                    break
        request.write(json.dumps({'items':atts[(page-1)*PAGE_COUNT:page*PAGE_COUNT], 'more':len(atts)>page*PAGE_COUNT}))
    elif typ == 'recentchanges':
        log = editlog.EditLog(request)
        pages = []
        more = False
        for line in logchain(request, log.reverse()):
            if not request.user.may.read(line.pagename):
                continue
            if line.pagename not in pages:
                pages.append(line.pagename)
            if len(pages) > page*PAGE_COUNT:
                more=True
                break

        # wrapping to Page object
        pages = [Page(request, p) for p in pages]

        # make dict
        pages = [{'id':'[[%s]]' % p.page_name, 'text': p._get_adpt().text()} for p in pages]

        # flush
        request.write(json.dumps({'items':pages[(page-1)*PAGE_COUNT:page*PAGE_COUNT], 'more':more}))
    elif typ == 'dayone_entries_by_tag':
        pass
    return ''