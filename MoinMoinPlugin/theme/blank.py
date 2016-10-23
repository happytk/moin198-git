# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - modern theme

    @copyright: 2003-2005 Nir Soffer, Thomas Waldmann
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.theme import ThemeBase
from MoinMoin import caching
from MoinMoin.action import get_available_actions
from MoinMoin import wikiutil
from MoinMoin.Page import Page
from datetime import datetime
import random

class Theme(ThemeBase):

    name = "blank"

    _ = lambda x: x     # We don't have gettext at this moment, so we fake it
    icons = {
        # key         alt                        icon filename      w   h
        # FileAttach
        'attach':     ("%(attach_count)s",       "moin-attach.png",   16, 16),
        'info':       ("[INFO]",                 "moin-info.png",     16, 16),
        'attachimg':  (_("[ATTACH]"),            "attach.png",        32, 32),
        # RecentChanges
        'rss':        (_("[RSS]"),               "moin-rss.png",      16, 16),
        'deleted':    (_("[DELETED]"),           "moin-deleted.png",  16, 16),
        'updated':    (_("[UPDATED]"),           "moin-updated.png",  16, 16),
        'renamed':    (_("[RENAMED]"),           "moin-renamed.png",  16, 16),
        'conflict':   (_("[CONFLICT]"),          "moin-conflict.png", 16, 16),
        'new':        (_("[NEW]"),               "moin-new.png",      16, 16),
        'diffrc':     (_("[DIFF]"),              "moin-diff.png",     16, 16),
        # General
        'bottom':     (_("[BOTTOM]"),            "moin-bottom.png",   16, 16),
        'top':        (_("[TOP]"),               "moin-top.png",      16, 16),
        'www':        ("[WWW]",                  "moin-www.png",      16, 16),
        'mailto':     ("[MAILTO]",               "moin-email.png",    16, 16),
        'news':       ("[NEWS]",                 "moin-news.png",     16, 16),
        'telnet':     ("[TELNET]",               "moin-telnet.png",   16, 16),
        'ftp':        ("[FTP]",                  "moin-ftp.png",      16, 16),
        'file':       ("[FILE]",                 "moin-ftp.png",      16, 16),
        # search forms
        'searchbutton': ("[?]",                  "moin-search.png",   16, 16),
        'interwiki':  ("[%(wikitag)s]",          "moin-inter.png",    16, 16),

        # smileys (this is CONTENT, but good looking smileys depend on looking
        # adapted to the theme background color and theme style in general)
        #vvv    ==      vvv  this must be the same for GUI editor converter
        'X-(':        ("X-(",                    'angry.png',         16, 16),
        ':D':         (":D",                     'biggrin.png',       16, 16),
        '<:(':        ("<:(",                    'frown.png',         16, 16),
        ':o':         (":o",                     'redface.png',       16, 16),
        ':(':         (":(",                     'sad.png',           16, 16),
        ':)':         (":)",                     'smile.png',         16, 16),
        'B)':         ("B)",                     'smile2.png',        16, 16),
        ':))':        (":))",                    'smile3.png',        16, 16),
        ';)':         (";)",                     'smile4.png',        16, 16),
        '/!\\':       ("/!\\",                   'alert.png',         16, 16),
        '<!>':        ("<!>",                    'attention.png',     16, 16),
        '(!)':        ("(!)",                    'idea.png',          16, 16),
        ':-?':        (":-?",                    'tongue.png',        16, 16),
        ':\\':        (":\\",                    'ohwell.png',        16, 16),
        '>:>':        (">:>",                    'devil.png',         16, 16),
        '|)':         ("|)",                     'tired.png',         16, 16),
        ':-(':        (":-(",                    'sad.png',           16, 16),
        ':-)':        (":-)",                    'smile.png',         16, 16),
        'B-)':        ("B-)",                    'smile2.png',        16, 16),
        ':-))':       (":-))",                   'smile3.png',        16, 16),
        ';-)':        (";-)",                    'smile4.png',        16, 16),
        '|-)':        ("|-)",                    'tired.png',         16, 16),
        '(./)':       ("(./)",                   'checkmark.png',     16, 16),
        '{OK}':       ("{OK}",                   'thumbs-up.png',     16, 16),
        '{X}':        ("{X}",                    'icon-error.png',    16, 16),
        '{i}':        ("{i}",                    'icon-info.png',     16, 16),
        '{1}':        ("{1}",                    'prio1.png',         15, 13),
        '{2}':        ("{2}",                    'prio2.png',         15, 13),
        '{3}':        ("{3}",                    'prio3.png',         15, 13),
        '{*}':        ("{*}",                    'star_on.png',       16, 16),
        '{o}':        ("{o}",                    'star_off.png',      16, 16),
    }
    del _

    # def logo(self):
    #     """ Assemble logo with link to front page

    #     The logo contain an image and or text or any html markup the
    #     admin inserted in the config file. Everything it enclosed inside
    #     a div with id="logo".

    #     @rtype: unicode
    #     @return: logo html
    #     """
    #     page = wikiutil.getFrontPage(self.request)
    #     #text = random.choice(['#','|','+','-','~','`','^','*','=','_',';',':',',','.'])#self.request.cfg.interwikiname or 'Self'
    #     link = page.link_to(self.request, text=text, rel='nofollow')

    #     return 'Hello!'

    def msg(self, d):
        """ Assemble the msg display

        Display a message with a widget or simple strings with a clear message link.

        @param d: parameter dictionary
        @rtype: unicode
        @return: msg display html
        """
        _ = self.request.getText
        msgs = d['msg']

        result = []
        close = d['page'].link_to(self.request, text=_('Clear message'), css_class="clear-link alert-link")
        for msg, msg_class in msgs:
            try:
                result.append('%s' % msg.render())
                close = ''
            except AttributeError:
                if msg and msg_class:
                    result.append(u'<span class="%s">%s</span>' % (msg_class, msg))
                elif msg:
                    result.append(u'%s' % msg)
        if len(result)>0:
            if close != '': result.append(close)
            #return u'<div style="background-color:#efefef;padding:5px;">\n%s\n</div>\n' % '<br>\n'.join(result)
            return '''<div class="container"><div class="alert alert-danger">%s</div></div>''' % '<br>\n'.join(result)
        else:
            return u''

    def titleEditorLink(self, page):
        """ Return a link to the editor

        If the user can't edit, return a disabled edit link.

        If the user want to show both editors, it will display "Edit
        (Text)", otherwise as "Edit".
        """
        if 'edit' in self.request.cfg.actions_excluded:
            return ""

        if not (page.isWritable() and
                self.request.user.may.write(page.page_name)):
            return ""

        _ = self.request.getText
        querystr = {'action': 'edit'}

        text = _('Edit')
        querystr['editor'] = 'text'
        attrs = {'name': 'texteditlink', 'rel': 'nofollow', }

        return '<span id="titleEditorLink">[%s]</span>' % page.link_to(self.request, text=text, querystr=querystr, **attrs)

    def editorLink(self, page):
        """ Return a link to the editor

        If the user can't edit, return a disabled edit link.

        If the user want to show both editors, it will display "Edit
        (Text)", otherwise as "Edit".
        """
        if 'edit' in self.request.cfg.actions_excluded:
            return ""

        if not (page.isWritable() and
                self.request.user.may.write(page.page_name)):
            return self.disabledEdit()

        _ = self.request.getText
        querystr = {'action': 'edit'}

        text = _('Edit')
        querystr['editor'] = 'text'
        attrs = {'name': 'texteditlink', 'rel': 'nofollow', }

        return page.link_to(self.request, text=text, querystr=querystr, **attrs)

    def editbarItems(self, page):
        """ Return list of items to show on the editbar

        This is separate method to make it easy to customize the
        edtibar in sub classes.
        """
        _ = self.request.getText
        editbar_actions = []
        for editbar_item in self.request.cfg.edit_bar:
            if (editbar_item == 'Discussion' and
               (self.request.getPragma('supplementation-page', self.request.cfg.supplementation_page)
                                                   in (True, 1, 'on', '1'))):
                    editbar_actions.append(self.supplementation_page_nameLink(page))
            elif editbar_item == 'Comments':
                # we just use <a> to get same style as other links, but we add some dummy
                # link target to get correct mouseover pointer appearance. return false
                # keeps the browser away from jumping to the link target::
                editbar_actions.append('<a href="#" class="nbcomment" onClick="toggleComments();return false;">%s</a>' % _('Comments'))
            elif editbar_item == 'Edit':
                editbar_actions.append(self.editorLink(page))
            elif editbar_item == 'Info':
                editbar_actions.append(self.infoLink(page))
            #elif editbar_item == 'Subscribe':
            #    editbar_actions.append(self.subscribeLink(page))
            elif editbar_item == 'Quicklink':
                editbar_actions.append(self.quicklinkLink(page))
            elif editbar_item == 'Attachments':
                editbar_actions.append(self.attachmentsLink(page))
            elif editbar_item == 'ActionsMenu':
                editbar_actions.append(self.actionsMenu(page))
        return editbar_actions


    def editbar(self, d):
        """ Assemble the page edit bar.

        Create html on first call, then return cached html.

        @param d: parameter dictionary
        @rtype: unicode
        @return: iconbar html
        """
        page = d['page']
        if not self.shouldShowEditbar(page):
            return ''

        html = self._cache.get('editbar')
        if html is None:
            # Remove empty items and format as list. The item for showing inline comments
            # is hidden by default. It gets activated through javascript only if inline
            # comments exist on the page.
            items = []
            for item in self.editbarItems(page):
                if item:
                    if 'nbcomment' in item:
                        # hiding the complete list item is cosmetically better than just
                        # hiding the contents (e.g. for sidebar themes).
                        items.append('<span class="toggleCommentsButton" style="display:none;">%s</span>' % item)
                    else:
                        items.append('%s' % item)
            items = [item for item in items if len(item.strip())>0]
            html = u' '.join(items)
            self._cache['editbar'] = html

        return html

    def html_head(self, d):
        """ Assemble html head

        @param d: parameter dictionary
        @rtype: unicode
        @return: html head
        """
        html = [
            u'<meta name="viewport" content="user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, width=device-width" />',
            u'<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            u'<title>%(title)s - %(sitename)s</title>' % {
                'title': wikiutil.escape(d['title']),
                'sitename': wikiutil.escape(d['sitename']),
            },
            self.externalScript('common'),
            self.headscript(d), # Should move to separate .js file
            #self.guiEditorScript(d),
            self.html_stylesheets(d),
            #/moin_static195/common/js/jquery-1.8.2.min.js
            u'<script language="javascript" type="Text/javascript" src="/moin_static195/common/js/jquery-1.8.2.min.js"></script>',
            u'<script language="javascript" type="Text/javascript" src="/moin_static195/common/bootstrap/js/bootstrap.min.js"></script>',
            # u'<script language="javascript" type="Text/javascript" src="/moin_static195/common/bootstrap/js/bootstrap-dropdown.js"></script>',
            u'<link rel="stylesheet" type="text/css" charset="utf-8" href="/moin_static195/common/bootstrap/css/bootstrap.css">',
            self.rsslink(d),
            #self.universal_edit_button(d),
            ]
        return '\n'.join(html)

    def actions(self, d):

        # html = [
        #     # u'<div class="btn-group">',
        #     # u' <ul class="nav pull-right">',
        #     u''' <li class="dropdown">
        #               <a href="#" id="drop3" role="button" class="dropdown-toggle" data-toggle="dropdown">Action<b class="caret"></b></a>
        #               <ul class="dropdown-menu" role="menu" aria-labelledby="drop3">
        #                 <li role="presentation">%s</li>
        #                 <li role="presentation" class="divider"></li>
        #                 <li role="presentation">%s</li>
        #                 <li role="presentation" class="divider"></li>
        #                 %s
        #               </ul>
        #          </li>
        #       ''' % (self.editorLink(d['page']), self.availableactions(d), self.username(d)),
        #     # u'</ul></div>',
        # ]
        # return '\n'.join(html)

          # <button type="button" class="btn btn-danger">Action</button>

        return '''<!-- Split button -->
        <div class="btn-group">
          <button type="button" class="btn btn-default">%s</button>
          <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
            <span class="caret"></span>
            <span class="sr-only">Toggle Dropdown</span>
          </button>
          <ul class="dropdown-menu" role="menu">
            <li>%s</li>
            <li class="divider"></li>
            %s
          </ul>
        </div>''' % (self.editorLink(d['page']), self.availableactions(d), self.username(d))

    def searchform(self, d):
        """
        assemble HTML code for the search forms

        @param d: parameter dictionary
        @rtype: unicode
        @return: search form html
        """
        _ = self.request.getText
        form = self.request.values
        updates = {
            'search_label': _('Search:'),
            'search_value': wikiutil.escape(form.get('value', ''), 1),
            'search_full_label': _('Text'),
            'search_title_label': _('Titles'),
            'url': self.request.href(d['page'].page_name)
            }
        d.update(updates)
        html = u'''
<form id="searchform" method="get" action="%(url)s" class="navbar-form navbar-right" role="form">
<input type="hidden" name="action" value="fullsearch">
<input type="hidden" name="context" value="180">
<label for="searchinput">%(search_label)s</label>
<div class="form-group">
<input id="searchinput" type="text" name="value" value="%(search_value)s" size="20"
    onfocus="searchFocus(this)" onblur="searchBlur(this)"
    onkeyup="searchChange(this)" onchange="searchChange(this)" alt="Search"
    class="input-medium search-query form-control">
</div>
<input id="titlesearch" name="titlesearch" type="submit"
    value="%(search_title_label)s" alt="Search Titles" class="btn btn-success">
<input id="fullsearch" name="fullsearch" type="submit"
    value="%(search_full_label)s" alt="Search Full Text" class="btn btn-success">
''' % d
        # html += '\n' + self.actions(d)
        html += '''
</form>
<script type="text/javascript">
<!--// Initialize search form
var f = document.getElementById('searchform');
f.getElementsByTagName('label')[0].style.display = 'none';
var e = document.getElementById('searchinput');
searchChange(e);
searchBlur(e);
//-->
</script>
'''
        return html

    def header(self, d, **kw):
        """ Assemble wiki header

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """

        page = d['page']
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),

            u'<div class="navbar navbar-inverse navbar-fixed-top" role="navigation">',
            u'<div class="container"><div class="navbar-header">',
            u'''<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
<span class="sr-only">Toggle navigation</span>
<span class="icon-bar"></span>
<span class="icon-bar"></span>
<span class="icon-bar"></span>
</button>''',
            # self.title_with_separators(d),
            wikiutil.getFrontPage(self.request).link_to(self.request, text=self.cfg.sitename, rel='nofollow', css_class='navbar-brand'),
            u'</div>',#navbar-header
            u'<div class="navbar-collapse collapse">',
            self.navibar(d),
            self.searchform(d),
            u'</div>',#navbar-collapse
            u'</div>',#container
        #     u'''<div class="btn-group">
        # <div class="btn btn-small">
        # %s
        # </div>
        # <button class="btn btn-small dropdown-toggle" data-toggle="dropdown" href="#">
        # <span class="caret"></span>
        # </button>
        # <ul class="dropdown-menu">
        # <!-- dropdown menu links -->
        # %s
        # </ul>
        # </div>''' % (self.editorLink(d['page']), self.availableactions(d)),
        #     self.username(d),
            #self.actions(d),
            #self.interwiki(d),
            #self.titleEditorLink(page) if self.shouldShowEditbar(page) else '',
#             u'''<div class="btn-group">
#   <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
#     Action
#     <span class="caret"></span>
#   </a>
#   <ul class="dropdown-menu">
#     <!-- dropdown menu links -->
#     <li><a href="#">helloworld</a></li>
#     <li><a href="#">helloworld</a></li>
#     <li><a href="#">helloworld</a></li>
#   </ul>
# </div>''',
            # self.editbar(d),
            # u'<div class="row-fluid">',
            # u'<div class="span3">a</div>',
            # u'<div class="span9">',
            # u'</div>',
            # u'</div>',
            u'</div>',#navbar
            self.trail(d),
            #u'<hr id="pageline">',
            #u'<div id="pageline"><hr style="display:none;"></div>',
            # u'</div>',
            # u'<div class="bs-old-docs">',
            # u'<div class="container">',
            # u'<h3>',
            # self.title_with_separators(d),
            # u'</h3>',
            # u'<div class="container">',
            # u'</div>',
            u'<div class="page-header container"><h1>',
            self.title_with_separators(d),
            u'<small><span style="float:right; vertical-align:bottom;">',
            self.actions(d),
            u'</span></small>',
            u'</h1></div>',
            self.msg(d),
            # u'</div>',
            # u'</div>',

            u'<div class="container">',
            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),

            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)

    def title_with_separators(self, d):
        """ Assemble the title using slashes, not <ul>

        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        #_ = self.request.getText
        #html = wikiutil.escape(d['title_text']).replace("/",":")
        #return u'<span id="pagelocation">%s</span>' % html

        """ Assemble the title using slashes, not <ul>

        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        _ = self.request.getText
        if not self.request.user.valid:
            html = u'<span class="navbar-brand">%s</span>' % wikiutil.escape(d['title_text'])
            return html

        if d['title_text'] == d['page'].split_title():
            # just showing a page, no action
            segments = d['page_name'].split('/')
            link_text = segments[-1]
            link_title = _('Click to do a full-text search for this title')
            link_query = {'action': 'fullsearch', 'context': '180',
                          'value': 'linkto:"%s"' % d['page_name'], }
            link = d['page'].link_to(self.request, link_text,
                                     querystr=link_query, title=link_title, rel='nofollow')
            if len(segments) <= 1:
                html = link
            else:
                content = []
                curpage = ''
                for s in segments[:-1]:
                    curpage += s
                    content.append(Page(self.request,
                                        curpage).link_to(self.request, s, css_class=''))
                    curpage += '/'
                path_html = u'/'.join(content)
                html = u'<span class="pagepath">%s</span>/%s' % (path_html, link)
        else:
            html = wikiutil.escape(d['title_text'])

        # return u'<span id="pagelocation">%s</span>' % html
        # return u'<span class="navbar-brand">%s</span>' % html
        return html

    def navibar(self, d):
        """ Assemble the navibar

        @param d: parameter dictionary
        @rtype: unicode
        @return: navibar html
        """
        request = self.request
        found = {} # pages we found. prevent duplicates
        items = [] # navibar items
        item = u'<li class="%s">%s</li> '
        current = d['page_name']
        current_link = ''
        # Process config navi_bar
        if request.cfg.navi_bar:
           for text in request.cfg.navi_bar:
               pagename, link = self.splitNavilink(text)
               if pagename == current:
                   cls = 'wikilink active'
                   current_link = link
               else:
                   cls = 'wikilink'
               # items.append(item % (cls, link))
               items.append((cls, link))
               found[pagename] = 1

        # # Add user links to wiki links, eliminating duplicates.
        # userlinks = request.user.getQuickLinks()
        # for text in userlinks:
        #     # Split text without localization, user knows what he wants
        #     pagename, link = self.splitNavilink(text, localize=0)
        #     if not pagename in found:
        #         if pagename == current:
        #             cls = 'userlink active'
        #             current_link = link
        #         else:
        #             cls = 'userlink'
        #         # items.append(item % (cls, link))
        #         items.append((cls, link))
        #         found[pagename] = 1

        # Add current page at end of local pages
        # if not current in found:
        #     title = d['page'].split_title()
        #     title = self.shortenPagename(title)
        #     link = d['page'].link_to(request, title)
        #     cls = 'active'
        #     current_link = link
        #     # items.append(item % (cls, link))
        #     items.append((cls, link))

        # Add sister pages.
        for sistername, sisterurl in request.cfg.sistersites:
            if sistername == request.cfg.interwikiname: # it is THIS wiki
                cls = 'sisterwiki active'
                # items.append(item % (cls, sistername))
                items.append((cls, sistername))
            else:
                # TODO optimize performance
                cache = caching.CacheEntry(request, 'sisters', sistername, 'farm', use_pickle=True)
                if cache.exists():
                    data = cache.content()
                    sisterpages = data['sisterpages']
                    if current in sisterpages:
                        cls = 'sisterwiki'
                        url = sisterpages[current]
                        link = request.formatter.url(1, url) + \
                               request.formatter.text(sistername) +\
                               request.formatter.url(0)
                        # items.append(item % (cls, link))
                        items.append((cls, link))

        # Assemble html
        # first_item = items[0]

        items = map(lambda x:item % (x[0], x[1]), items)
        html = [
            # u'<div>',
            # u' <ul class="nav pull-right">',
            u'''<ul class='nav navbar-nav'>''',
            # item % (first_item[0], first_item[1]) if first_item[1] != current_link else '',
            # wikiutil.getFrontPage(self.request).page_name != current else '',
    #wikiutil.getFrontPage(self.request).link_to(self.request, text=self.request.cfg.interwikiname, rel='nofollow')
    #     #text = random.choice(['#','|','+','-','~','`','^','*','=','_',';',':',',','.'])#self.request.cfg.interwikiname or 'Self'
    #     link = page.link_to(self.request, text=text, rel='nofollow')


            # u''' <li class="dropdown">
            #           <a href="#" id="drop3" role="button" class="dropdown-toggle" data-toggle="dropdown"><b class="caret"></b></a>
            #           <ul class="dropdown-menu" role="menu" aria-labelledby="drop3">
            #             %s
            #           </ul>
            #      </li>
            #   ''' % (u''.join(items)),
            # self.actions(d),
            u''.join(items),
            u'''</ul>''',
        ]
        return u'\n'.join(html)
        # return u"<ul class='nav navbar-nav'>%s\n%s\n%s</ul>" % (first_item, html[0], self.actions(d))
        #return u"%s" % html

        # html = [
        #     u"""<div class='nav navbar-nav'>""",
        #     u'<div class="btn-group">',
        #     u'<a type="button" class="btn btn-danger %s">%s</button>' % (first_item[0], first_item[1]),
        #     u'''<button type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown">
        #     <span class="caret"></span>
        #     <span class="sr-only">Toggle Dropdown</span>
        #   </button>''',
        #     u'<ul class="dropdown-menu" role="menu">%s</ul>' % 
        #     u'</div>',
        #     u'</div>',
        # ]
        # return u'\n'.join(html)

    def availableactions(self, d):
        """
        assemble HTML code for the available actions

        @param d: parameter dictionary
        @rtype: string
        @return: available actions html
        """
        request = self.request
        _ = request.getText
        rev = d['rev']
        html = []
        page = d['page']
        available = get_available_actions(request.cfg, page, request.user)
        if available:
            available = list(available)
            available.sort()
            for action in available:
                # Always add spaces: AttachFile -> Attach File
                # XXX do not make a page object just for split_title
                #title = Page(request, action).split_title(force=1)
                title = action
                # Use translated version if available
                title = _(title)
                querystr = {'action': action}
                if rev:
                    querystr['rev'] = str(rev)
                link = page.link_to(request, text=title, querystr=querystr, rel='nofollow')
                html.append('<li>%s</li>' % link)

        title = _("DeleteCache")
        link = page.link_to(request, text=title, querystr={'action': 'refresh'}, rel='nofollow')

        cache = caching.CacheEntry(request, page, page.getFormatterName(), scope='item')
        date = request.user.getFormattedDateTime(cache.mtime())
        # deletecache = u'<p>%s %s</p>' % (link, _('(cached %s)') % date)

        html.append('<li>%s</li>' % link)
        # html = deletecache + u'<p>%s %s</p>\n' % (_('Or try one of these actions:'),
                                       # u', '.join(html))
        return '\n'.join(html)

    def editorheader(self, d, **kw):
        """ Assemble wiki header for editor

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),
            u'''
<script src="/moin_static195/common/codemirror/lib/codemirror.js"></script>
<link rel="stylesheet" href="/moin_static195/common/codemirror/lib/codemirror.css">

<script src="/moin_static195/common/codemirror/mode/clike/clike.js"></script>
<script src="/moin_static195/common/codemirror/mode/clojure/clojure.js"></script>
<script src="/moin_static195/common/codemirror/mode/css/css.js"></script>
<script src="/moin_static195/common/codemirror/mode/diff/diff.js"></script>
<script src="/moin_static195/common/codemirror/mode/groovy/groovy.js"></script>
<script src="/moin_static195/common/codemirror/mode/haskell/haskell.js"></script>
<script src="/moin_static195/common/codemirror/mode/haxe/haxe.js"></script>
<script src="/moin_static195/common/codemirror/mode/htmlembedded/htmlembedded.js"></script>
<script src="/moin_static195/common/codemirror/mode/htmlmixed/htmlmixed.js"></script>
<script src="/moin_static195/common/codemirror/mode/javascript/javascript.js"></script>
<script src="/moin_static195/common/codemirror/mode/jinja2/jinja2.js"></script>
<script src="/moin_static195/common/codemirror/mode/less/less.js"></script>
<script src="/moin_static195/common/codemirror/mode/markdown/markdown.js"></script>
<script src="/moin_static195/common/codemirror/mode/sql/sql.js"></script>
<script src="/moin_static195/common/codemirror/mode/properties/properties.js"></script>
<script src="/moin_static195/common/codemirror/mode/python/python.js"></script>
<script src="/moin_static195/common/codemirror/mode/r/r.js"></script>
<script src="/moin_static195/common/codemirror/mode/shell/shell.js"></script>
<script src="/moin_static195/common/codemirror/mode/tiddlywiki/tiddlywiki.js"></script>
<script src="/moin_static195/common/codemirror/mode/tiki/tiki.js"></script>
<script src="/moin_static195/common/codemirror/mode/vb/vb.js"></script>
<script src="/moin_static195/common/codemirror/mode/vbscript/vbscript.js"></script>
<script src="/moin_static195/common/codemirror/mode/xml/xml.js"></script>

<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/3024-day.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/3024-night.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/ambiance-mobile.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/ambiance.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/base16-dark.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/base16-light.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/blackboard.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/cobalt.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/eclipse.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/elegant.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/erlang-dark.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/lesser-dark.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/mbo.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/midnight.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/monokai.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/neat.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/night.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/paraiso-dark.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/paraiso-light.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/pastel-on-dark.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/rubyblue.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/solarized.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/the-matrix.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/tomorrow-night-eighties.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/twilight.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/vibrant-ink.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/xq-dark.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/xq-light.css">
<style type="text/css">
        .CodeMirror {border-top: 1px solid black; border-bottom: 1px solid black;}
        .fullscreen {
            display: block;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 9999;
            margin: 0;
            padding: 0;
            border: 0px solid #BBBBBB;
            opacity: 1;
        }
        body { padding: 0; }
    </style>
<script src="/moin_static195/common/js/codemirror_run.js"></script>
<script type="text/javascript">
<!--
document.body.onload = function() {
    codemirror_run(document);
}
//-->
</script>
            ''', #if self.request.user.valid and self.request.user.name else u'',
            # Header
            u'<div id="header">',
            u'<div class="container">',
            u'<h1 id="locationline">',
            self.title_with_separators(d),
            u'</h1>',
            u'</div>',
            u'</div>',
            self.msg(d),

            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),

            u'<div class="container">',
            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)

    def footer(self, d, **keywords):
        """ Assemble wiki footer

        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        page = d['page']
        html = [
            # End of page
            self.endPage(),
            u'</div>', # container

            # u'<div id="footer">',
            # u'#',
            # self.username(d),
            # u'|',
            # self.pageinfo(page), 
            # self.searchform(d),
            # u'</div>',
            self.emit_custom_html(self.cfg.page_footer1),

            #u'<div id="c2wikifooter" style="float:right; display:none;" align="right"><small>',
            #u'<div id="header" style="float:right;">',
            #u'</div>',
            #self.editbar(d),
            # Pre footer custom html (not recommended!)

            # Footer
            #u'<div id="footer">',
            #self.navibar(d) if (page.isWritable() and
            #    self.request.user.may.write(page.page_name)) else '',
            #self.username(d) if (page.isWritable() and
            #    self.request.user.may.write(page.page_name)) else '',
            #u'</small></div>',

            #self.credits(d),
            #self.showversion(d, **keywords),
            #u'</div>',
            # u'''<div id="footer">
            #   <div class="container">
            #     <p class="text-muted">Place sticky footer content here.</p>
            #   </div>
            # </div>''',
            # Post footer custom html
            self.emit_custom_html(self.cfg.page_footer2),
            ]
        return u'\n'.join(html)


    def pageinfo(self, page):
        """ Return html fragment with page meta data

        Since page information uses translated text, it uses the ui
        language and direction. It looks strange sometimes, but
        translated text using page direction looks worse.

        @param page: current page
        @rtype: unicode
        @return: page last edit information
        """
        _ = self.request.getText
        html = ''
        if self.shouldShowPageinfo(page):
            info = page.lastEditInfo()
            if info:
                if info['editor']:
                    info = _("last edited %(time)s by %(editor)s") % info
                else:
                    info = _("last modified %(time)s") % info
                #pagename = page.page_name
                #if self.request.cfg.show_interwiki:
                #    pagename = "%s: %s" % (self.request.cfg.interwikiname, pagename)
                #info = "%s  (%s)" % (wikiutil.escape(pagename), info)
                #html = '<span id="pageinfo" class="info"%(lang)s>%(info)s</span>\n' % {
                #    'lang': self.ui_lang_attr(),
                #    'info': info
                #    }
                html = info
        return html

    def username(self, d):
        """ Assemble the username / userprefs link

        @param d: parameter dictionary
        @rtype: unicode
        @return: username html
        """
        request = self.request
        _ = request.getText

        userlinks = []

        text = ''
        # Add username/homepage link for registered users. We don't care
        # if it exists, the user can create it.
        if request.user.valid and request.user.name:
            interwiki = wikiutil.getInterwikiHomePage(request)
            name = request.user.name
            aliasname = request.user.aliasname
            if not aliasname:
                aliasname = name
            title = "%s @ %s" % (aliasname, interwiki[0])
            # link to (interwiki) user homepage
            homelink = (request.formatter.interwikilink(1, title=title, id="userhome", generated=True, *interwiki) +
                        request.formatter.text(name) +
                        request.formatter.interwikilink(0, title=title, id="userhome", *interwiki))
            userlinks.append(homelink)
            # link to userprefs action
            if 'userprefs' not in self.request.cfg.actions_excluded:
                userlinks.append(d['page'].link_to(request, text=_('Settings'),
                                               querystr={'action': 'userprefs'}, id='userprefs', rel='nofollow'))
            text = name

        if request.user.valid:
            if request.user.auth_method in request.cfg.auth_can_logout:
                userlinks.append(d['page'].link_to(request, text=_('Logout'),
                                                   querystr={'action': 'logout', 'logout': 'logout'}, id='logout', rel='nofollow'))
        else:
            query = {'action': 'login'}
            # special direct-login link if the auth methods want no input
            if request.cfg.auth_login_inputs == ['special_no_input']:
                query['login'] = '1'
            if request.cfg.auth_have_login:
                userlinks.append(d['page'].link_to(request, text=_("Login"),
                                                   querystr=query, id='login', rel='nofollow'))

            text = _("Login")

        if len(userlinks) > 0:
            userlinks_html = u'</li><li role="presentation">'.join(userlinks)
            return '<li>%s</li>' % userlinks_html
        else:
            return ''
        #html = u'<div id="username">%s</div>' % userlinks_html

        # html = [
        #     # u'<div>',
        #     u'''<ul class="nav pull-right">
        #             <li id="fat-menu" class="dropdown">
        #               <a href="#" id="drop3" role="button" class="dropdown-toggle" data-toggle="dropdown">%s<b class="caret"></b></a>
        #               <ul class="dropdown-menu" role="menu" aria-labelledby="drop3">
        #                 <li role="presentation">%s</li>
        #               </ul>
        #             </li>
        #           </ul>''' % (text, userlinks_html),
        #     # u'</div>',
        # ]
        # return '\n'.join(html)

    def trail(self, d):
        """ Assemble page trail

        @param d: parameter dictionary
        @rtype: unicode
        @return: trail html
        """
        request = self.request
        user = request.user
        html = ''

        found = {} # pages we found. prevent duplicates
        items = [] # navibar items
        item = u'<li class="%s">%s</li> '
        current = d['page_name']
        current_link = ''
        # Process config navi_bar
        # if request.cfg.navi_bar:
        #    for text in request.cfg.navi_bar:
        #        pagename, link = self.splitNavilink(text)
        #        if pagename == current:
        #            cls = 'wikilink active'
        #            current_link = link
        #        else:
        #            cls = 'wikilink'
        #        items.append(item % (cls, link))
        #        # items.append((cls, link))
        #        found[pagename] = 1

        # item = u'<li class="%s"><span class="label label-primary">&nbsp;</span> %s</li> '
        # Add user links to wiki links, eliminating duplicates.
        userlinks = request.user.getQuickLinks()
        items.append('<span class="glyphicon glyphicon-star"></span>')
        for text in userlinks:
            # Split text without localization, user knows what he wants
            pagename, link = self.splitNavilink(text, localize=0)
            if not pagename in found:
                if pagename == current:
                    cls = 'userlink active'
                    current_link = link
                else:
                    cls = 'userlink'
                items.append(item % (cls, link))
                # items.append((cls, link))
                found[pagename] = 1
        items.append('<span class="glyphicon glyphicon-signal"></span>')
        if not user.valid or user.show_page_trail:
            trail = user.getTrail()
            if trail:
                # items = []
                for pagename in trail:
                    try:
                        interwiki, page = wikiutil.split_interwiki(pagename)
                        if interwiki != request.cfg.interwikiname and interwiki != 'Self':
                            link = (self.request.formatter.interwikilink(True, interwiki, page) +
                                    self.shortenPagename(page) +
                                    self.request.formatter.interwikilink(False, interwiki, page))
                            items.append('<li>%s</li>' % link)
                            continue
                        else:
                            pagename = page

                    except ValueError:
                        pass
                    page = Page(request, pagename)
                    title = page.split_title()
                    title = self.shortenPagename(title)
                    link = page.link_to(request, title)
                    items.append('<li>%s</li>' % link)
                # html = u'''%s''' % (' <span class="divider">/</span> '.join(items))
                ###
                ###<li><a href="#">Library</a> <span class="divider">/</span></li>
                ###<li class="active">Data</li>

                #html = u'<div id="pagetrail">%s</div>' % u'<span class="sep"> &raquo; </span>'.join(items)
        html = u'''<div style='background-color:#f5f5f5; text-align:center;'><small>
        <ul class="breadcrumb">%s</ul></small></div>''' % ('\n'.join(items))

        return html

    # # RecentChanges ######################################################

    # def recentchanges_entry(self, d):
    #     """
    #     Assemble a single recentchanges entry (table row)

    #     @param d: parameter dictionary
    #     @rtype: string
    #     @return: recentchanges entry html
    #     """
    #     _ = self.request.getText
    #     html = []
    #     html.append('<li>\n')
    #     html.append('<small>%(icon_html)s</small> ' % d)
    #     #html.append('<small>%(info_html)s</small> ' % d)
    #     html.append('%(pagelink_html)s\n' % d)
    #     if d['time_html']:
    #         html.append("(%(time_html)s) " % d)

    #     if d['editors']:
    #         html.append(', '.join(d['editors']))

    #     if d['comments']:
    #         if d['changecount'] > 0:
    #             for comment in d['comments']:
    #                 html.append('<br/>#%02d&nbsp;%s' % (
    #                     comment[0], comment[1]))
    #         else:
    #             comment = d['comments'][0]
    #             html.append('%s' % comment[1])
    #     html.append('</li>\n')

    #     return ''.join(html)

    # def recentchanges_daybreak(self, d):
    #     """
    #     Assemble a rc daybreak indication (table row)

    #     @param d: parameter dictionary
    #     @rtype: string
    #     @return: recentchanges daybreak html
    #     """
    #     if d['bookmark_link_html']:
    #         set_bm = '&nbsp; %(bookmark_link_html)s' % d
    #     else:
    #         set_bm = ''
    #     return ('</ul><strong>%s</strong>'
    #             '%s'
    #             '\n<ul/>') % (d['date'], set_bm)

    # def recentchanges_header(self, d):
    #     """
    #     Assemble the recentchanges header (intro + open table)

    #     @param d: parameter dictionary
    #     @rtype: string
    #     @return: recentchanges header html
    #     """
    #     _ = self.request.getText

    #     # Should use user interface language and direction
    #     html = '<div class="recentchanges"%s>\n' % self.ui_lang_attr()
    #     html += '<div>\n'
    #     #page = d['page']
    #     #if self.shouldUseRSS(page):
    #     #    link = [
    #     #        u'<div class="rcrss">',
    #     #        self.request.formatter.url(1, self.rsshref(page)),
    #     #        self.request.formatter.rawHTML(self.make_icon("rss")),
    #     #        self.request.formatter.url(0),
    #     #        u'</div>',
    #     #        ]
    #     #    html += ''.join(link)
    #     html += '<p>'
    #     # Add day selector
    #     if d['rc_days']:
    #         days = []
    #         for day in d['rc_days']:
    #             if day == d['rc_max_days']:
    #                 days.append('<strong>%d</strong>' % day)
    #             else:
    #                 days.append(
    #                     wikiutil.link_tag(self.request,
    #                         '%s?max_days=%d' % (d['q_page_name'], day),
    #                         str(day),
    #                         self.request.formatter, rel='nofollow'))
    #         days = ' | '.join(days)
    #         html += (_("Show %s days.") % (days, ))

    #     if d['rc_update_bookmark']:
    #         html += " %(rc_update_bookmark)s %(rc_curr_bookmark)s" % d

    #     html += '</p>\n</div>\n'

    #     html += '<ul>\n'
    #     return html

    # def recentchanges_footer(self, d):
    #     """
    #     Assemble the recentchanges footer (close table)

    #     @param d: parameter dictionary
    #     @rtype: string
    #     @return: recentchanges footer html
    #     """
    #     #_ = self.request.getText
    #     html = ''
    #     html += '</ul>\n'
    #     #if d['rc_msg']:
    #     #    html += "<br>%(rc_msg)s\n" % d
    #     #html += '</div>\n'
    #     return html

def execute(request):
    """
    Generate and return a theme object

    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)

