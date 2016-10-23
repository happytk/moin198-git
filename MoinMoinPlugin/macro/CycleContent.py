# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Cylce Content Macro

    Selects a pagename from CycleContent or a given page and cycles
    it by the refresh rate given on the page e.g. #refresh 5 ExamplePage
    For an attachment from a cycled page of name MyPage use an absolute
    name for the attachment e.g. {{attachment:MyPage/image.png}}

    Usage:
        <<CycleContent()>>
        <<CycleContent(CycleContent)>>

    Comments:
        It will look for list delimiters on the page in question.
        It will ignore anything that is not in an "*" list.

    @copyright: 2002-2004 Juergen Hermann <jh@web.de>
                2009 MoinMoin:ReimarBauer
    @license: GNU GPL, see COPYING for details.

    Based on RandomQuote
    Originally written by Thomas Waldmann.
    Gustavo Niemeyer added wiki markup parsing of the quotes.

"""
from MoinMoin.action import cache
from MoinMoin.Page import Page

Dependencies = ["time"]

def macro_CycleContent(macro, pagename=u'CycleContent'):
    """
    Macro for cycling content of other pages on the page where it is called from.
    That also can be used for slide shows and also without a refresh rate
    because each request cycles.

    @param pagename: the pagename for the list to cycle through.
    """
    request = macro.request
    _ = request.getText

    if request.user.may.read(pagename):
        page = Page(request, pagename)
        raw = page.get_raw_body()
    else:
        raw = ""

    username = request.user.name or 'Anonymous'
    # this selects lines looking like a list item
    quotes = raw.splitlines()
    quotes = [quote.strip() for quote in quotes]
    quotes = [quote[2:] for quote in quotes if quote.startswith('* ')]
    if not quotes:
        return (macro.formatter.highlight(1) +
                _('No quotes on %(pagename)s.') % {'pagename': pagename} +
                macro.formatter.highlight(0))

    content_type = 'text/plain'
    key = '%s_%s_%s_CycleContent' % (content_type.replace('/', '_'),
                                     pagename, username)
    if not cache.exists(request, key):
        index = 0
        cache.put(request, key, str(index + 1), content_type=content_type)
    else:
        # may be I want a cache.get method
        index = int(cache._get_datafile(request, key).read()) + 1
        if index + 1 > len(quotes):
            cache.put(request, key, '0', content_type=content_type)
            index = 0
        else:
            cache.put(request, key, str(index), content_type=content_type)

    quote = quotes[index]
    if quote.startswith('[[') and quote.endswith(']]'):
        quote = quote[2:-2]
    page.set_raw_body(Page(request, quote).get_raw_body(), 1)
    quote = request.redirectedOutput(page.send_page,
                                     content_only=1, content_id="CycleContent")

    return quote

