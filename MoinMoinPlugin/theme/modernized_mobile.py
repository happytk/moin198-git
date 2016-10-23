from MoinMoin.theme.modernized import Theme as ThemeBase
from MoinMoin import wikiutil, config
from MoinMoin.Page import Page

class Theme(ThemeBase):

    name = "modernized" # we tell that we are 'modernized', so we use its static data

    def __init__(self, request):
        ThemeBase.__init__(self, request)

        if self.request.user.mobile_preferred:
            self.is_mobile = True
        else:
            import re
            self.is_mobile = re.search(r"android.+mobile|iphone|ipod", request.http_user_agent, re.I|re.M) is not None

    # def html_head(self, d):
    #     if not self.is_mobile:
    #         return ThemeBase.html_head(self, d)

    #     html = [
    #         u'<title>%(title)s - %(sitename)s</title>' % {
    #             'title': wikiutil.escape(d['title']),
    #             'sitename': wikiutil.escape(d['sitename']),
    #         },
    #         self.html_stylesheets(d),
    #         ]
    #     return '\n'.join(html)

    def guiworks(self, page):
        if not self.is_mobile:
            return ThemeBase.guiworks(self, page)

        return False

    def username(self, d):
        """ Assemble the username / userprefs link

        @param d: parameter dictionary
        @rtype: unicode
        @return: username html
        """

        if not self.is_mobile:
            return ThemeBase.username(self, d)

        request = self.request
        _ = request.getText

        if self.request.cfg.show_interwiki:
            page = wikiutil.getFrontPage(self.request)
            text = self.request.cfg.interwikiname or 'Self'
            link = page.link_to(self.request, text=text, rel='nofollow')
            # html = u'<span id="interwiki">%s<span class="sep">: </span></span>' % link
            userlinks = [link]
        else:
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
        html = u'<div id="username">%s</div>' % userlinks_html
        return html


    def header(self, d, **kw):
        if not self.is_mobile:
            return ThemeBase.header(self, d, **kw)

        page = d['page']
        html = [
            u'<div id="header">',
            # self.logo(),
            self.username(d),
            u'<h1 id="locationline">',
            self.title_with_separators(d),
            self.titleEditorLink(page) if self.shouldShowEditbar(page) else '',
            u'</h1>',
            self.navibar(d),
            u'<div id="pageline"><hr style="display:none;"></div>',
            self.msg(d),
            # self.editbar(d),
            u'</div>',
            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)

    def editorheader(self, d, **kw):
        if not self.is_mobile:
            return ThemeBase.editorheader(self, d, **kw)

        html = [
            u'<div id="header">',
            u'<h1 id="locationline">',
            self.title_with_separators(d),
            u'</h1>',
            self.msg(d),
            u'</div>',
        ]
        return u'\n'.join(html)

    def footer(self, d, **keywords):
        if not self.is_mobile:
            return ThemeBase.footer(self, d, **keywords)

        page = d['page']
        html = [
            self.pageinfo(page),
            self.endPage(),
            # u'<div id="footer">',
            #self.credits(d),
            # self.showversion(d, **keywords),
            # u'</div>',
            ]
        return u'\n'.join(html)

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


    def send_title(self, text, **keywords):
        if not self.is_mobile:
            return ThemeBase.send_title(self, text, **keywords)

        request = self.request

        if keywords.has_key('page'):
            page = keywords['page']
            pagename = page.page_name
        else:
            pagename = keywords.get('pagename', '')
            page = Page(request, pagename)

        request.content_type = "text/html; charset=%s" % (config.charset, )

        user_head = []
        user_head.append('''<meta http-equiv="Content-Type" content="%s;charset=%s">\n''' % (page.output_mimetype, page.output_charset))
        user_head.append('<meta name="viewport" content="width=device-width, initial-scale=1.0,user-scalable=yes"/>')

        output = []
        output.append("""\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
%s
%s
%s
<style tyle='text/css'>
img.external_image {
    max-width: 100%%;
}
img.attachment {
    max-width: 100%%;
}
</style>
""" % (
            ''.join(user_head),
            self.html_head({
                'page': page,
                'title': text,
                'sitename': request.cfg.html_pagetitle or request.cfg.sitename,
                'print_mode': keywords.get('print_mode', False),
                'media': keywords.get('media', 'screen'),
            }),
            keywords.get('html_head', ''),
        ))
        output.append("</head>\n")

        bodyattr = []
        output.append('\n<body%s>\n' % ''.join(bodyattr))

        d = {
            'theme': self.name,
            'title_text': text,
            'page': page,
            'page_name': pagename or '',
            'user_name': request.user.name,
            'user_valid': request.user.valid,
            'msg': self._status,
            'editor_mode': keywords.get('editor_mode', 0),
        }
        request.themedict = d
        if keywords.get('editor_mode', 0):
            output.append(self.editorheader(d))
        else:
            output.append(self.header(d))

        request.write(''.join(output))
        self._send_title_called = True

    def send_footer(self, pagename, **keywords):
        if not self.is_mobile:
            return ThemeBase.send_footer(self, pagename, **keywords)

        request = self.request
        d = request.themedict
        request.write(self.footer(d, **keywords))

    def send_closing_html(self):
        if not self.is_mobile:
            return ThemeBase.send_closing_html(self)

        request = self.request
        d = request.themedict
        if d['editor_mode']:
            request.write('''
<script>
document.getElementById('editor-help').style.display = "none";
(function() {
    // auto grow text area
    var textarea = document.getElementById('editor-textarea'),
        timer;
    textarea.onfocus = function() {
        timer = setInterval(function() {
            var scrollHeight = textarea.scrollHeight,
                clientHeight = textarea.clientHeight;
            if(clientHeight < scrollHeight) {
                textarea.style.height = scrollHeight + 50 + 'px';
            }
        }, 100);
    };
    textarea.onblur = function() {
        clearInterval(timer);
    };
})();
</script>
''')
        request.write('</body>\n</html>\n\n')

    def recentchanges_entry(self, d):
        """
        Assemble a single recentchanges entry (table row)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges entry html
        """
        if not self.is_mobile:
            return ThemeBase.recentchanges_entry(self, d)

        _ = self.request.getText
        html = []
        html.append('<tr>\n')

        # html.append('<td class="rcicon1">%(icon_html)s</td>\n' % d)

        html.append('<td class="rcpagelink" colspan="1">%(icon_html)s %(pagelink_html)s\n<small><i>' % d)
        # if d['time_html']:
        #     html.append("%(time_html)s\n" % d)

        # html.append('<td class="rcicon2">%(info_html)s</td>\n' % d)

        # if d['editors']:
        #     html.append('<div style="float:right;">')
        #     html.append(','.join(d['editors']))
        #     html.append('</div>')
        html.append('</i></small></td>\n')

        # html.append('<td class="rccomment">')
        # if d['comments']:
        #     if d['changecount'] > 1:
        #         notfirst = 0
        #         for comment in d['comments']:
        #             html.append('%s<tt>#%02d</tt>&nbsp;%s' % (
        #                 notfirst and '<br>' or '', comment[0], comment[1]))
        #             notfirst = 1
        #     else:
        #         comment = d['comments'][0]
        #         html.append('%s' % comment[1])
        # html.append('</td>\n')

        html.append('</tr>\n')

        return ''.join(html)

    def recentchanges_daybreak(self, d):
        """
        Assemble a rc daybreak indication (table row)

        @param d: parameter dictionary
        @rtype: string
        @return: recentchanges daybreak html
        """
        if not self.is_mobile:
            return ThemeBase.recentchanges_daybreak(self, d)

        if d['bookmark_link_html']:
            set_bm = '&nbsp; %(bookmark_link_html)s' % d
        else:
            set_bm = ''
        return ('<tr class="rcdaybreak"><td colspan="%d">'
                '<strong>%s</strong>'
                '%s'
                '</td></tr>\n') % (1, d['date'], set_bm)


def execute(request):
    return Theme(request)
