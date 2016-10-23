# -*- coding: iso-8859-1 -*-
from MoinMoin.Page import Page
from MoinMoin.wikiutil import importPlugin

def execute(pagename, request):

    arena = request.values.get('arena', 'Page.py')
    if arena == 'Page.py':
        arena = Page(request, pagename)
    key = request.values.get('key', 'text_html')

    # Remove cache entry (if exists), and send the page
    from MoinMoin import caching
    caching.CacheEntry(request, arena, key, scope='item').remove()
    caching.CacheEntry(request, arena, "pagelinks", scope='item').remove()
    
    page = arena
    text = page.get_raw_body()

    parser = importPlugin(request.cfg, 'parser', 'pythonruntime', 'Parser')

    parser(text, request).format(request.formatter)
    return ''
