# Aggr[igator]

import jinja2
import os
from MoinMoin import wikiutil
from MoinMoin import search
from MoinMoin.Page import Page

Dependencies = ['user', 'time']

# def getPageListFromSearch (request,args):
#     # If called with empty or no argument, default to regex search for .+, the full page list.
#     needle = wikiutil.get_unicode(request, args, 'needle', u'regex:.+')

#     # With whitespace argument, return same error message as FullSearch
#     #if not needle.strip():
#     #    err = 'Please use a more selective search term instead of {{{"%s"}}}' % needle
#     #    return '<span class="error">%s</span>' % err

#     # Return a title search for needle, sorted by name.
#     try:
#         results = search.searchPages(request, needle,
#                                      titlesearch=1, case=0,
#                                      sort='page_name')
#         pages = results.hits
#         pages = map(lambda x:x.page_name, pages)
#         pages.reverse()
#     except ValueError:
#         # same error as in MoinMoin/action/fullsearch.py, keep it that way!
#         """
#         ret = ''.join([macro.formatter.text('<<PageList('),
#                       _('Your search query {{{"%s"}}} is invalid. Please refer to '
#                         'HelpOnSearching for more information.', wiki=True,
#                         percent=True) % wikiutil.escape(needle),
#                       macro.formatter.text(')>>')])
#         """
#         pages = []
#     return pages

import re
import humanize
from datetime import datetime, timedelta

# >>> humanize.naturalday(datetime.datetime.now())
# 'today'
# >>> humanize.naturalday(datetime.datetime.now() - datetime.timedelta(days=1))
# 'yesterday'
# >>> humanize.naturalday(datetime.date(2007, 6, 5))
# 'Jun 05'
# >>> humanize.naturaldate(datetime.date(2007, 6, 5))
# 'Jun 05 2007'
# >>> humanize.naturaltime(datetime.datetime.now() - datetime.timedelta(seconds=1))
# 'a second ago'
# >>> humanize.naturaltime(datetime.datetime.now() - datetime.timedelta(seconds=3600))
# 'an hour ago'

def humanized(d):
    try:
        if (datetime.now() - d) < timedelta(days=1):
            return humanize.naturaltime(d)
        else:
            return humanize.naturaldate(d)
    except:
        return 'error-humanized_date'

def macro_Aggr(macro, middleware_name, count=10):

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Aggr.html')
    template = jinja2.Template(open(path, 'r').read().decode('utf8'))

    x = macro.request.storage[middleware_name].list_pages(macro.request)
    x.sort()
    x.reverse()

    try:
        paging = int(macro.request.values.get('p',1))
    except ValueError:
        paging = 1

    last_page = int(len(x)/count) + 1
    if paging > last_page:
        paging = last_page

    if not hasattr(macro.request, "_Include_backto"):
        macro.request._Include_backto = macro.request.formatter.page.page_name
    # macro.request.href(macro.request.formatter.page.page_name)

    x = x[(paging-1)*count:paging*count]

    def _rendering(page):
        output = macro.request.redirectedOutput(page.send_page_content, macro.request, page.get_raw_body(), format=page.pi['format'], do_cache=False)
        return output
    _with_timestamp = re.compile('.*/[0-9]+')
    x = [Page(macro.request, pagename) for pagename in x if macro.request.user.may.read(pagename)]
    x = [{'output': _rendering(page), \
          'page': page, \
          'pagename': page.page_name, \
          'created_at': humanized(datetime.fromtimestamp(int(page.page_name.split('/')[1]))) \
                            if _with_timestamp.match(page.page_name) else page.last_modified() \
          } for page in x]

    return template.render(pages=x, request=macro.request, paging=paging, last_page=last_page)
