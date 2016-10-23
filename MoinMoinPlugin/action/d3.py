## page was renamed from __moinext/parser/d3
# -*- coding: iso-8859-1 -*-
#format python
from MoinMoin.Page import Page
from MoinMoin.wikiutil import importPlugin

def execute(pagename, request):

    arena = request.values.get('arena', 'Page.py')
    if arena == 'Page.py':
        arena = Page(request, pagename)

    page = arena
    text = page.get_raw_body()
    lines = text.split('\n')
    for idx, line in enumerate(lines):
        if not line.startswith('#'):
            text = '\n'.join(lines[idx:])
            break

    # lines = [line for line in lines if not line.startswith('#')]
    # text = '\n'.join(lines)

    request.write('''<html><head>''')
    request.write('<script type="text/javascript" src="/moin_static195/common/js/d3.min.js"></script>')
    #request.write('<script type="text/javascript" src="http://localhost:8090/moin_static195/common/bootstrap/js/bootstrap.js"></script>')
    # request.write('<link rel="stylesheet" type="text/css" href="/moin_static195/common/bootstrap/css/bootstrap.css">')
    request.write('</head><body>')
    request.write(text)
    request.write('''</body></html>''')
    return ''
