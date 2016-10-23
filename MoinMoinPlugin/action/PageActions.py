# -*- coding: iso-8859-1 -*-

'''
This is copied from Mandarin or Solinoid themes. It is by FixedLeft when
Icon Bar is used and the More Actions icon is clicked.
'''

import re
from MoinMoin import config, wikiutil
from MoinMoin.Page import Page
from MoinMoin import version

# Ripped from the LikePages action
def execute(pagename, request):
    _ = request.getText
    from MoinMoin.formatter.text_html import Formatter
    request.formatter = Formatter(request)

    try:
        request.emit_http_headers()
    except AttributeError:
        try:
            request.http_headers()
        except AttributeError:
            pass

    # This action generate data using the user language
    request.setContentLanguage(request.lang)
    try:
        send_title = request.theme.send_title
        send_title(_('Actions for %s') % pagename, page_name=pagename)
    except AttributeError:
        wikiutil.send_title(request, _('Actions for %s') % pagename, pagename=pagename)

    # Start content - IMPORTANT - without content div, there is no
    # direction support!
    request.write(request.formatter.startContent("content"))

    # Just list the actions
    request.write(availableactions(request))

    # End content and send footer
    request.write(request.formatter.endContent())
    try:
        request.theme.send_footer(pagename)
    except AttributeError:
        wikiutil.send_footer(request, pagename)

# Make a link to action
def actionlink(request, action, title, comment=''):
    page = request.page
    _ = request.getText
    # Always add spaces: AttachFile -> Attach File
    # XXX TODO do not make a page object just for split_title
    title = Page(request, title).split_title()
    # Use translated version if available
    title = _(title, formatted=False)
    params = '%s?action=%s' % (page.page_name, action)
    if action == 'RenamePage':
        params += '&subpages_checked=1'
    link = wikiutil.link_tag(request, params, _(title))
    return u''.join([ u'<li>', link, comment, u'</li>' ])


# Rippped from the theme code
def availableactions(request):
    page = request.page
    _ = request.getText
    html = ''
    links = []
    try:
        available = request.getAvailableActions(page) # Moin 1.8
    except AttributeError:
        from MoinMoin.action import get_available_actions
        available = get_available_actions(request.cfg, page, request.user) # Moin 1.9

    for action in available:
        links.append(actionlink(request, action, action))
    if page.isWritable() and request.user.may.write(page.page_name):
        links.append(actionlink(request, 'edit', 'EditText'))
    if request.user.valid and request.user.email:
        action = ("Subscribe", "Unsubscribe")[request.user.isSubscribedTo([page.page_name])]
        links.append(actionlink(request, 'subscribe', action))
    if request.user.valid:
        links.append(actionlink(request, 'userform&logout=logout', 'Logout'))
    links.append(actionlink(request, 'print', 'PrintView'))
    links.append(actionlink(request, 'raw', 'ViewRawText'))
    links.append(actionlink(request, 'refresh', 'DeleteCache'))
    html = u'<ul>%s</ul>' % u''.join(links)
    return html
