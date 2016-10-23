# -*- coding: iso-8859-1 -*-

from MoinMoin.Page import Page

def execute(pagename, request):
    page = Page(request,pagename)
    return page.send_page(content_only=1)