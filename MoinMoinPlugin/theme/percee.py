# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - modern theme

    @copyright: 2003-2005 Nir Soffer, Thomas Waldmann
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.theme import ThemeBase
from MoinMoin import wikiutil
from MoinMoin.Page import Page
from datetime import datetime
import random

class Theme(ThemeBase):

    name = "percee"

    _ = lambda x: x     # We don't have gettext at this moment, so we fake it
    icons = {}
    del _

    def logo(self):
        """ Assemble logo with link to front page

        The logo contain an image and or text or any html markup the
        admin inserted in the config file. Everything it enclosed inside
        a div with id="logo".

        @rtype: unicode
        @return: logo html
        """
        #html = u''
        #page = wikiutil.getFrontPage(self.request)
        #logo = page.link_to_raw(self.request, '<img src="/FrontPage?action=AttachFile&do=get&target=logo.png" valign="bottom" alt="MoinMoin Logo">')

        # page = wikiutil.getFrontPage(self.request)
        # #text = random.choice(['#','|','+','-','~','`','^','*','=','_',';',':',',','.'])#self.request.cfg.interwikiname or 'Self'
        # text = "%02d" % datetime.today().day
        # link = page.link_to(self.request, text=text, rel='nofollow')

        # #randomcolor
        # a = map(str, range(0,9))
        # a.extend(list('abcdef'))

        # color_str = []
        # for i in range(0,6):
        #     color_str.append(random.choice(a))
        # html = u'<span id="logo" style="background-color:#%s;">%s</span>' % (''.join(color_str), link)

        return u'PER-C for UKEY MON.'

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
        close = d['page'].link_to(self.request, text=_('Clear message'), css_class="clear-link")
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
            return u'<div style="background-color:#efefef;padding:5px;">\n%s\n</div>\n' % '<br>\n'.join(result)
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
            u'<title>%(title)s - %(sitename)s</title>' % {
                'title': wikiutil.escape(d['title']),
                'sitename': wikiutil.escape(d['sitename']),
            },
            self.externalScript('common'),
            self.headscript(d), # Should move to separate .js file
            #self.guiEditorScript(d),
            self.html_stylesheets(d),
            self.rsslink(d),
            #self.universal_edit_button(d),
            ]
        return '\n'.join(html)

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

            u'<div id="header">',
            u'''
    <div id="menu" class="menu">
        <div class="logo"></div>
        <div class="topmenu">
        <div class="topmenu_text">
          <table height="60" width="900" cellspacing="0" cellpadding="0" border="0">
          <tr height="60" valign="center">
            <td height="60" width="25" valign="center"><img src="/moin_static195/percee/img/ico_line.png"></td>
            <td height="60" width="88" valign="center">TOP_DELAY_TR&nbsp;&nbsp;</td>
            <td height="60" width="25" valign="center"><img src="/moin_static195/percee/img/ico_line.png"></td>
            <td height="60" width="118" valign="center">TOP_DELAY_TR_SLOPE&nbsp;&nbsp;</td>
            <td height="60" width="25" valign="center"><img src="/moin_static195/percee/img/ico_line.png"></td>
            <td height="60" width="88" valign="center">TOP_OUT_TARGET&nbsp;&nbsp;</td>
            <td height="60" width="25" valign="center"><img src="/moin_static195/percee/img/ico_line.png"></td>
            <td height="60" width="68" valign="center">TOP_TIMEOUT&nbsp;&nbsp;</td>
            <td height="60" width="22" valign="center"><img src="/moin_static195/percee/img/ico_conf.png"></td>
            <td height="60" width="38" valign="center">SCR&nbsp;&nbsp;</td>
            <td height="60" width="22" valign="center"><img src="/moin_static195/percee/img/ico_conf.png"></td>
            <td height="60" width="38" valign="center">TR&nbsp;&nbsp;</td>
            <td height="60" width="22" valign="center"><img src="/moin_static195/percee/img/ico_conf.png"></td>
            <td height="60" width="68" valign="center">DBIO&nbsp;&nbsp;</td>
            <td height="60" width="25" valign="center"><img src="/moin_static195/percee/img/ico_pie.png"></td>
            <td height="60" width="68" valign="center">TABLE&nbsp;&nbsp;</td>
            <td height="60" width="25" valign="center"><img src="/moin_static195/percee/img/ico_conf.png"></td>
            <td height="60" width="68" valign="center">BATCH</td>
            <td width="30"></td>
          </tr>
          </table>
        </div>
        </div> 
    </div>

    <div class="menu_navi"><div class="manu_navi_text">
        <table cellspacing="0" cellpadding="0" border="0" valign="center" height="27">
          <tr height="27" valign="center">
            <td height="27" width="1100" valign="center">
''',
            self.trail(d), 
            u'''
            </td>
            <td width="60" height="27" valign="center">
              <input class="tf" cols="35" size="35">
            </td>
            <td width="36" height="27" valign="center">
              <img src="/moin_static195/percee/img/btn_srch_1.png" height="25" width="25">
            </td>
          </tr>             
         </table>
    </div></div>''',
            # Header
            # self.logo(),
            # self.navibar(d),# if self.request.user.valid else '',
            # ' | ',
            # '<input type="text"><input type="button" value="SEARCH">',
            
            #self.searchform(d),
            #u'</div>',
            #self.username(d),
            #self.interwiki(d),
            # u'<h1>',
            # self.title_with_separators(d),
            # u'</h1>',
            #self.titleEditorLink(page) if self.shouldShowEditbar(page) else '',
            # u'<hr/>',
            # self.trail(d),
            #u'<hr id="pageline">',
            #u'<div id="pageline"><hr style="display:none;"></div>',
            #self.editbar(d),
            # u'<hr/>',
            self.msg(d),
            u'</div>',
            u'<div class="mid">',
            u'<div class="content_1">',

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
            html = wikiutil.escape(d['title_text']).replace("/",":")
            return u'<span id="pagelocation">%s</span>' % html

        if d['title_text'] == d['page'].split_title():
            # just showing a page, no action
            segments = d['page_name'].split('/')
            link_text = segments[-1]
            link_title = _('Click to do a full-text search for this title')
            link_query = {'action': 'fullsearch', 'context': '180',
                          'value': 'linkto:"%s"' % d['page_name'], }
            link = d['page'].link_to(self.request, link_text,
                                     querystr=link_query, title=link_title,
                                     css_class='backlink', rel='nofollow')
            if len(segments) <= 1:
                html = link
            else:
                content = []
                curpage = ''
                for s in segments[:-1]:
                    curpage += s
                    content.append(Page(self.request,
                                        curpage).link_to(self.request, s))
                    curpage += '/'
                path_html = u'<span class="sep">:</span>'.join(content)
                html = u'<span class="pagepath">%s</span><span class="sep">:</span>%s' % (path_html, link)
        else:
            html = wikiutil.escape(d['title_text'])

        return u'<span id="pagelocation">%s</span>' % html

    def navibar(self, d):
        """ Assemble the navibar

        @param d: parameter dictionary
        @rtype: unicode
        @return: navibar html
        """
        request = self.request
        found = {} # pages we found. prevent duplicates
        items = [] # navibar items
        item = u'<span class="%s">%s</span> '
        current = d['page_name']

        # Process config navi_bar
        if request.cfg.navi_bar:
           for text in request.cfg.navi_bar:
               pagename, link = self.splitNavilink(text)
               if pagename == current:
                   cls = 'wikilink current'
               else:
                   cls = 'wikilink'
               items.append(item % (cls, link.upper()))
               found[pagename] = 1

        # Add user links to wiki links, eliminating duplicates.
        userlinks = request.user.getQuickLinks()
        for text in userlinks:
            # Split text without localization, user knows what he wants
            pagename, link = self.splitNavilink(text, localize=0)
            if not pagename in found:
                if pagename == current:
                    cls = 'userlink current'
                else:
                    cls = 'userlink'
                items.append(item % (cls, link))
                found[pagename] = 1

        # Add current page at end of local pages
        # if not current in found:
        #     title = d['page'].split_title()
        #     title = self.shortenPagename(title)
        #     link = d['page'].link_to(request, title)
        #     cls = 'current'
        #     items.append(item % (cls, link))

        # Add sister pages.
        for sistername, sisterurl in request.cfg.sistersites:
            if sistername == request.cfg.interwikiname: # it is THIS wiki
                cls = 'sisterwiki current'
                items.append(item % (cls, sistername))
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
                        items.append(item % (cls, link))

        # Assemble html
        items = u''.join(items)
        html = items
        #return u"<div id='navibar'>%s</div>" % html
        return u"%s" % html

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
<script src="/moin_static195/common/codemirror/mode/python/python.js"></script>
<script src="/moin_static195/common/js/jquery.min.js"></script>
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/default.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/night.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/neat.css">
<link rel="stylesheet" href="/moin_static195/common/codemirror/theme/elegant.css">
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
    </style>
<script src="/moin_static195/common/js/codemirror_run.js"></script>
<script type="text/javascript">
<!--
document.body.onload = function() {
    codemirror_run(document);
}
//-->
</script>
            ''' if self.request.user.valid and self.request.user.name else u'',
            # Header
            u'<div id="header">',
            u'<h1 id="locationline">',
            self.title_with_separators(d),
            u'</h1>',
            self.msg(d),
            u'</div>',

            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),

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
            u'</div></div>',
            u'<div id="footer">',
            # u'#',
            # self.username(d),
            # u'|',
            # self.pageinfo(page), 
            # self.searchform(d),
            u'</div>',
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

        userlinks_html = u'<span class="sep"> | </span>'.join(userlinks)
        #html = u'<div id="username">%s</div>' % userlinks_html
        return userlinks_html

    def trail(self, d):
        """ Assemble page trail

        @param d: parameter dictionary
        @rtype: unicode
        @return: trail html
        """
        request = self.request
        user = request.user
        html = ''
        if not user.valid or user.show_page_trail:
            trail = user.getTrail()
            if trail:
                items = []
                for pagename in trail:
                    try:
                        interwiki, page = wikiutil.split_interwiki(pagename)
                        if interwiki != request.cfg.interwikiname and interwiki != 'Self':
                            link = (self.request.formatter.interwikilink(True, interwiki, page) +
                                    self.shortenPagename(page) +
                                    self.request.formatter.interwikilink(False, interwiki, page))
                            items.append(link)
                            continue
                        else:
                            pagename = page

                    except ValueError:
                        pass
                    page = Page(request, pagename)
                    title = page.split_title()
                    title = self.shortenPagename(title)
                    link = page.link_to(request, title)
                    items.append(link)
                html = u' <img src="/moin_static195/percee/img/arrow_1.png"> '.join(items)
        return html

    # RecentChanges ######################################################

    def recentchanges_entry(self, d):
        """
        Assemble a single recentchanges entry (table row)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges entry html
        """
        _ = self.request.getText
        html = []
        html.append('<li>\n')
        html.append('<small>%(icon_html)s</small> ' % d)
        #html.append('<small>%(info_html)s</small> ' % d)
        html.append('%(pagelink_html)s\n' % d)
        if d['time_html']:
            html.append("(%(time_html)s) " % d)

        if d['editors']:
            html.append(', '.join(d['editors']))

        if d['comments']:
            if d['changecount'] > 0:
                for comment in d['comments']:
                    html.append('<br/>#%02d&nbsp;%s' % (
                        comment[0], comment[1]))
            else:
                comment = d['comments'][0]
                html.append('%s' % comment[1])
        html.append('</li>\n')

        return ''.join(html)

    def recentchanges_daybreak(self, d):
        """
        Assemble a rc daybreak indication (table row)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges daybreak html
        """
        if d['bookmark_link_html']:
            set_bm = '&nbsp; %(bookmark_link_html)s' % d
        else:
            set_bm = ''
        return ('</ul><strong>%s</strong>'
                '%s'
                '\n<ul/>') % (d['date'], set_bm)

    def recentchanges_header(self, d):
        """
        Assemble the recentchanges header (intro + open table)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges header html
        """
        _ = self.request.getText

        # Should use user interface language and direction
        html = '<div class="recentchanges"%s>\n' % self.ui_lang_attr()
        html += '<div>\n'
        #page = d['page']
        #if self.shouldUseRSS(page):
        #    link = [
        #        u'<div class="rcrss">',
        #        self.request.formatter.url(1, self.rsshref(page)),
        #        self.request.formatter.rawHTML(self.make_icon("rss")),
        #        self.request.formatter.url(0),
        #        u'</div>',
        #        ]
        #    html += ''.join(link)
        html += '<p>'
        # Add day selector
        if d['rc_days']:
            days = []
            for day in d['rc_days']:
                if day == d['rc_max_days']:
                    days.append('<strong>%d</strong>' % day)
                else:
                    days.append(
                        wikiutil.link_tag(self.request,
                            '%s?max_days=%d' % (d['q_page_name'], day),
                            str(day),
                            self.request.formatter, rel='nofollow'))
            days = ' | '.join(days)
            html += (_("Show %s days.") % (days, ))

        if d['rc_update_bookmark']:
            html += " %(rc_update_bookmark)s %(rc_curr_bookmark)s" % d

        html += '</p>\n</div>\n'

        html += '<ul>\n'
        return html

    def recentchanges_footer(self, d):
        """
        Assemble the recentchanges footer (close table)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges footer html
        """
        #_ = self.request.getText
        html = ''
        html += '</ul>\n'
        #if d['rc_msg']:
        #    html += "<br>%(rc_msg)s\n" % d
        #html += '</div>\n'
        return html

def execute(request):
    """
    Generate and return a theme object

    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)

