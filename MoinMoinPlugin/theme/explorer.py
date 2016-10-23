# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - explorer theme
    
    @copyright: 2007, 2008 Wolfgang Fischer
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.theme import ThemeBase
from MoinMoin import version

is_moin_1_6 = version.release.startswith('1.6')

# Debugging
# import pdb, time
# pdb.set_trace()

class Theme(ThemeBase):
    from MoinMoin.action import AttachFile
    from MoinMoin import i18n, wikiutil, version
    from MoinMoin.Page import Page

    name = 'explorer'
    

    # ========================================
    # Toolbars and UI text definition
    # ========================================
    # fake _ function to get gettext recognize those texts:
    _ = lambda x: x

    ui_text = { 'splitbar_title' : _('Drag to resize. Double click to show or hide tree.') }

    toolbar_lists = [
        ['home', 'recentchanges', 'separator', 'login', 'mypages', 'separator', 'showcomments', 'quicklink', 'subscribe', 'subscribeuser', 'separator', 'edit', 'renamepage', 'copypage', 'load', 'save', 'deletepage', 'separator', 'attachfile', 'spellcheck', 'diff', 'info', 'revert', 'format xml', 'renderasdocbook', 'print', 'raw', 'refresh', 'separator', 'help', 'separator', 'find', 'likepages', 'localsitemap', 'separator', 'despam', 'packagepages', 'syncpages', 'separator', 'searchform'],
    ]


    buttons = {
        # key               page, query dict
        'separator':       ("", {}, ""),
        'searchform':      ("", {}, ""),
        'home':            ("%(page_front_page)s", {}),
        'recentchanges':   ("RecentChanges", {}),
        'login':           ("", {'action': 'login'}),
        'login direct':    ("", {'action': 'login', 'login': '1'}),
        'logout':          ("", {'action': 'logout', 'logout': 'logout'}),
        'userprefs':       ("", {'action': 'userprefs'}),
        'mypages':         ("", {'action': 'MyPages'}),
        'showcomments':    ("", {}),
        'hidecomments':    ("", {}),
        'quicklink':       ("", {'action': 'quicklink'}),
        'quickunlink':     ("", {'action': 'quickunlink'}),
        'subscribe':       ("", {'action': 'subscribe'}),
        'unsubscribe':     ("", {'action': 'unsubscribe'}),
        'subscribeuser':   ("", {'action': 'SubscribeUser'}),
        'edit text':       ("", {'action': 'edit', 'editor': 'text'}),
        'edit gui':        ("", {'action': 'edit', 'editor': 'gui'}),
        'renamepage':      ("", {'action': 'RenamePage'}),
        'copypage':        ("", {'action': 'CopyPage'}),
        'load':            ("", {'action': 'Load'}),
        'save':            ("", {'action': 'Save'}),
        'deletepage':      ("", {'action': 'DeletePage'}),
        'attachfile':      ("", {'action': 'AttachFile'}),
        'spellcheck':      ("", {'action': 'SpellCheck'}),
        'diff':            ("", {'action': 'diff', 'rev': ''}),
        'info':            ("", {'action': 'info'}),
        'revert':          ("", {'action': 'revert', 'rev': ''}),
        'format xml':      ("", {'action': 'format', 'mimetype': 'text/xml'}),
        'renderasdocbook': ("", {'action': 'RenderAsDocbook'}),
        'print':           ("", {'action': 'print', 'rev': ''}),
        'raw':             ("", {'action': 'raw', 'rev': ''}),
        'refresh':         ("", {'action': 'refresh'}),
        'help':            ("%(page_help_contents)s", {}),
        'find':            ("%(page_find_page)s", {}),
        'likepages':       ("", {'action': 'LikePages'}),
        'localsitemap':    ("", {'action': 'LocalSiteMap'}),
        'despam':          ("", {'action': 'Despam'}),
        'packagepages':    ("", {'action': 'PackagePages'}),
        'syncpages':       ("", {'action': 'SyncPages'}),
        }


    icons_update = {
        # key         alt                        icon filename              w   h
        # ------------------------------------------------------------------------
        # toolbars
        'home':                (_("Home"),                "home.png",                16, 16),
        'recentchanges':       (_("RecentChanges"),       "recentchanges.png",       16, 16),
        'login':               (_("Login"),               "login.png",               16, 16),
        'login_direct':        (_("Login"),               "login.png",               16, 16),
        'logout':              (_("Logout"),              "login.png",               16, 16),
        'userprefs':           (_("Preferences"),         "userprefs.png",           16, 16),
        'mypages':             (_("My Pages"),            "mypages.png",             16, 16),
        'showcomments':        (_("Comments"),            "comments.png",            16, 16),
        'hidecomments':        (_("Comments"),            "comments.png",            16, 16),
        'quicklink':           (_("Add Link"),            "quicklink.png",           16, 16),
        'quickunlink':         (_("Remove Link"),         "quicklink.png",           16, 16),
        'subscribe':           (_("Subscribe"),           "subscribe.png",           16, 16),
        'unsubscribe':         (_("Unsubscribe"),         "subscribe.png",           16, 16),
        'subscribeuser':       (_("Subscribe User"),      "subscribeuser.png",       16, 16),
        'edit':                (_("Edit"),                "edit text.png",           16, 16),
        'edit text':           (_("Edit (Text)"),         "edit text.png",           16, 16),
        'edit text disabled':  (_("Edit (Text)"),         "edit text disabled.png",  16, 16),
        'edit gui':            (_("Edit (GUI)"),          "edit gui.png",            16, 16),
        'edit gui disabled':   (_("Edit (GUI)"),          "edit gui disabled.png",   16, 16),
        'renamepage':          (_("Rename Page"),         "renamepage.png",          16, 16),
        'renamepage disabled': (_("Rename Page"),         "renamepage disabled.png", 16, 16),
        'copypage':            (_("Copy Page"),           "copypage.png",            16, 16),
        'copypage disabled':   (_("Copy Page"),           "copypage disabled.png",   16, 16),
        'load':                (_("Load Page"),           "load.png",                16, 16),
        'load disabled':       (_("Load Page"),           "load disabled.png",       16, 16),
        'save':                (_("Save Page"),           "save.png",                16, 16),
        'save disabled':       (_("Save Page"),           "save disabled.png",       16, 16),
        'deletepage':          (_("Delete Page"),         "deletepage.png",          16, 16),
        'deletepage disabled': (_("Delete Page"),         "deletepage disabled.png", 16, 16),
        'attachfile':          (_("Attachments"),         "attachfile.png",          16, 16),
        'spellcheck':          (_("Check Spelling"),      "spellcheck.png",          16, 16),
        'diff':                (_("Diffs"),               "diff.png",                16, 16),
        'info':                (_("Info"),                "info.png",                16, 16),
        'revert':              (_('Revert to this revision'),  "revert.png",         16, 16),
        'format xml':          (_("XML"),                 "format xml.png",          16, 16),
        'renderasdocbook':     (_("Render as Docbook"),   "renderasdocbook.png",     16, 16),
        'print':               (_("Print View"),          "print.png",               16, 16),
        'raw':                 (_("Raw Text"),            "raw.png",                 16, 16),
        'refresh':             (_("Delete Cache"),        "refresh.png",             16, 16),
        'help':                ("%(page_help_contents)s", "help.png",                16, 16),
        'find':                ("%(page_find_page)s",     "find.png",                16, 16),
        'likepages':           (_("Like Pages"),          "likepages.png",           16, 16),
        'localsitemap':        (_("Local Site Map"),      "localsitemap.png",        16, 16),
        'despam':              (_("Remove Spam"),         "despam.png",              16, 16),
        'packagepages':        (_("Package Pages"),       "packagepages.png",        16, 16),
        'syncpages':           (_('Sync Pages'),          "syncpages.png",           16, 16),
        'view':                (_("View"),                "view.png",                16, 16),
        'up':                  (_("Up"),                  "up.png",                  16, 16),
        # RecentChanges
        'deleted':    (_("[DELETED]"),  "deletepage.png", 16, 16),
        'updated':    (_("[UPDATED]"),  "edit text.png",  16, 16),
        'renamed':    (_("[RENAMED]"),  "renamepage.png", 16, 16),
        'conflict':   (_("[CONFLICT]"), "conflict.png",   16, 16),
        'new':        (_("[NEW]"),      "new.png",        16, 16),
        'diffrc':     (_("[DIFF]"),     "diff.png",       16, 16),
        }
   
    del _


    def __init__(self, request):
        """ Initialize the explorer theme
        
        @param request: the request object
        """
        ThemeBase.__init__(self, request)
        # Get the cookie
        if is_moin_1_6:  # Moin 1.6
            self.cookie = request.parse_cookie()
        else:  # Moin 1.7
            self.cookie = request.cookie
        # Add them especific icons
        self.icons.update(self.icons_update)
        # Get module name of the theme
        self.module_name = module_name = __name__.rsplit('.', 1)[1]
        cfg = self.cfg
        # Determine if theme should be displayed in site mode or desktop mode
        # Default: desktop mode <=> request is from localhost
        self.site_mode = getattr(cfg, '%s_site_mode' % module_name, not request.http_host.startswith('localhost'))
        # Get admin configured toolbars
        self.toolbar_lists = getattr(cfg, '%s_toolbars' % module_name, self.toolbar_lists)
        # Get admin configured toolbars position
        self.toolbars_in_header = getattr(cfg, '%s_toolbars_in_header' % module_name, not self.site_mode)
        # Get admin configured buttons removed from toolbar
        self.buttons_remove = getattr(cfg, '%s_buttons_remove' % module_name, [])
        # Get admin configured default tree width
        self.default_sidebar_width = getattr(cfg, '%s_default_sidebar_width' % module_name, "20em")
        # Get admin configured page_header status
        # Default: show page header <=> theme is in desktop mode
        self.page_header = getattr(cfg, '%s_page_header' % module_name, not self.site_mode)
        # Get admin configured attachments status
        # Default: show attachments <=> theme is in desktop mode
        self.attachments = getattr(cfg, '%s_attachments' % module_name, not self.site_mode)
        if not self.site_mode:
            # Add additional stylesheet for desktop mode
            self.stylesheets += (('screen', 'desktop'),)


    def header(self, d, **kw):
        """ Assemble the wiki header
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        self.page = d['page']
        self.page_name = d['page_name']
        module_name = self.module_name
        # Init the wiki tree
        self.wiki_tree = WikiTree(self, self.page_name)

        # Initialize default settings
        self.sidebar_width, main_height, page_content_height = self.default_sidebar_width, "auto", "auto"

        # Apply setings from cookie
        if self.cookie:
            if self.cookie.has_key('%s_hide_sidebar' % module_name):
                self.sidebar_width = "0px"
            elif self.cookie.has_key('%s_sidebar_width' % module_name):
                self.sidebar_width = self.cookie['%s_sidebar_width' % module_name].value
            if self.cookie.has_key('%s_main_height' % module_name):
                main_height = self.cookie['%s_main_height' % module_name].value
            if self.cookie.has_key('%s_page_content_height' % module_name):
                page_content_height = self.cookie['%s_page_content_height' % module_name].value

        is_ltr = self.i18n.getDirection(self.request.lang) == "ltr"

        header_html = page_header_html = page_header_html = []
        page_title_html = attachment_html = u''
        if self.site_mode:
            # Build site header
            header_html = [
                u'<div id="header">',
                u'<div></div>',  # IE Fix: Logo and searchform float over the header
                self.logo(),
                u'<span id="searchform_container">',  # IE 6 Fix: To enable searchform to float
                self.searchform(d),
                u'</span>',
                self.username(d),
                u'<div style="clear:both;"></div>',  # IE Fix: Navibar tabs move at hover
                self.navibar(d),
                u'</div>',
                u'<div id="pageline"><hr style="display:none;"></div>',
            ]
        if self.attachments:
            # Build attachment list
            attachment_html = self.attachment_list()
        if self.page_header:
            # Build wiki page header
            page_header_html = [
                u'<div id="page_header">',
                self.wiki_tree.page_summary_html(),
                self.wiki_tree.page_categories_html(),
                self.interwiki(d),
                self.title(d),
                self.page_header_info(self.page),
                u'<div class="bottom"></div>'
                u'</div>',  # page_header
            ]
        else:
            # Build wiki page title
            page_title_html = [
                u'<div id="page_title">',
                self.interwiki(d),
                self.title(d),
                u'</div>',  # page_title
            ]

        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),
            u'',
            u'\n'.join(header_html),
            self.trail(d),
            [u'', self.toolbars(d)][self.toolbars_in_header],
            u'',
            # u'<div id="main" style="height:%s;">' % main_height,
            u'<div id="main">',
            u'',
            u'<div id="page_area">',
            u'',
            [self.toolbars(d), u''][self.toolbars_in_header],
            u'\n'.join(page_header_html),
            u'',
            # u'<div id="page_content" style="height:%s;">' % page_content_height,
            u'<div id="content_area" style="height:auto;"><div id="page_content">',
            self.msg(d),
            attachment_html,
            u'\n'.join(page_title_html),

            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),
            
            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)
        
        
    def editorheader(self, d, **kw):
        """ Assemble wiki header for editor
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        return self.header(d, **kw)

        
    def footer(self, d, **keywords):
        """ Assemble wiki footer
        
        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        # Uncomment to display the cookie (for test purpose)
        # cookie = ['<li>%s</li>' % self.cookie[i] for i in self.cookie]
        wiki_tree_html = self.wiki_tree.tree_html()
        _ = self.ui_text
        pageinfo_html = [self.pageinfo(self.page), u''][self.page_header]
        html = [
            pageinfo_html,
            # End of page
            self.endPage(),
            
            # Pre footer custom html (not recommended!)
            self.emit_custom_html(self.cfg.page_footer1),

            u'</div>',  # page_content
            u'</div>',  # content_area
            u'</div>',  # page
            u'',
            u'<div id="splitbar" title="%s"></div>' % _['splitbar_title'],
            u'',
            u'<div id="sidebar" style="width:%s;">' % self.sidebar_width,
            wiki_tree_html,
            u'</div>',  # sidebar
            u'</div>',  # main
            u'',
            # Footer
            u'<div id="footer">',
            self.wiki_tree.summary_html,
            self.credits(d),
            self.showversion(d, **keywords),
            # Uncomment to display the cookie (for test purpose)
            # u'<ul id="cookie">\n%s\n</ul>\n' % ''.join(cookie),
            u'</div>',
            u'',
            # Post footer custom html
            self.emit_custom_html(self.cfg.page_footer2),
            ]
        return u'\n'.join(html)


    
    # =============================
    # Iconbar
    # =============================

    def toolbars(self, d):
        """
        Assemble the iconbar
        
        @param d: parameter dictionary
        @rtype: string
        @return: toolbar html
        """
        request = self.request
        # available_actions = request.getAvailableActions(self.page)
        actions_excluded = request.cfg.actions_excluded
        toolbar = []
        for toolbar_list in self.toolbar_lists:
            toolbar.append('<div id="iconbar">')
            toolbar.append('<ul class="iconbar">')
            
            for icon in toolbar_list:
                if icon in self.buttons_remove:
                    pass
                elif icon == "separator":
                    if toolbar[-1] != '<ul class="iconbar">':
                        toolbar.append('</ul>')
                        toolbar.append('<ul class="iconbar">')
                elif icon == "home" and self.site_mode:
                    # Don't include the home icon in site mode
                    pass
                elif icon == "edit":
                    toolbar.append(self.editor_link(d))
                elif icon == "rename":
                    if (self.page.isWritable()
                        and self.request.user.may.read(self.page_name)
                        and self.request.user.may.write(self.page_name)
                        and self.request.user.may.delete(self.page_name)):
                        toolbar.append('<li>%s</li>' % self.make_iconlink(icon, d))
                    else:
                        toolbar.append('<li>%s</li>' % self.make_icon('rename disabled', d))
                elif icon == "delete":
                    if (self.page.isWritable()
                        and self.request.user.may.delete(self.page_name)):
                        toolbar.append('<li>%s</li>' % self.make_iconlink(icon, d))
                    else:
                        toolbar.append('<li>%s</li>' % self.make_icon('delete disabled', d))
                elif icon == "copy":
                    if self.request.user.may.read(self.page_name):
                        toolbar.append('<li>%s</li>' % self.make_iconlink(icon, d))
                    else:
                        toolbar.append('<li>%s</li>' % self.make_icon('copy disabled', d))
                elif icon == "load":
                    if self.request.user.may.read(self.page_name):
                        toolbar.append('<li>%s</li>' % self.make_iconlink(icon, d))
                    else:
                        toolbar.append('<li>%s</li>' % self.make_icon('load disabled', d))
                elif icon == "save":
                    if self.request.user.may.read(self.page_name):
                        toolbar.append('<li>%s</li>' % self.make_iconlink(icon, d))
                    else:
                        toolbar.append('<li>%s</li>' % self.make_icon('save disabled', d))
                elif icon == "login":
                    if not self.site_mode:
                        if request.user.valid and request.user.name:
                            toolbar.append('<li>%s&nbsp;</li>' % self.username_link(d))
                        if is_moin_1_6:  # Moin 1.6
                            if self.cfg.show_login:
                                if request.user.valid:
                                    toolbar.append('<li class="ib_selected">%s</li>' % self.make_iconlink("logout", d))
                                    toolbar.append('<li>%s</li>' % self.make_iconlink("userprefs", d))
                                else:
                                    toolbar.append('<li>%s</li>' % self.make_iconlink(icon, d))
                        else:  # Moin 1.7
                            if request.user.valid:
                                if request.user.auth_method in request.cfg.auth_can_logout:
                                    toolbar.append('<li class="ib_selected">%s</li>' % self.make_iconlink("logout", d))
                                    toolbar.append('<li>%s</li>' % self.make_iconlink("userprefs", d))
                            elif request.cfg.auth_have_login:
                                # special direct-login button if the auth methods want no input
                                if request.cfg.auth_login_inputs == ['special_no_input']:
                                    toolbar.append('<li>%s</li>' % self.make_iconlink('login direct', d))
                                else:
                                    toolbar.append('<li>%s</li>' % self.make_iconlink(icon, d))
                elif icon == "quicklink" and request.user.valid:
                    # Only display for logged in users
                    toolbar.append('<li%s>%s</li>' % [('', self.make_iconlink(icon, d)), (' class="ib_selected"', self.make_iconlink("quickunlink", d))][request.user.isQuickLinkedTo([self.page_name])])
                elif icon == "showcomments":
                    toolbar.append('<li%s><a href="#" onClick="toggle_comments(this);return false;">%s</a></li>' % [('', self.make_icon(icon, d)), (' class="ib_selected"', self.make_icon("hidecomments", d))][self.request.user.show_comments])
                elif icon == "subscribe" and self.cfg.mail_enabled:
                    toolbar.append('<li%s>%s</li>' % [('', self.make_iconlink(icon, d)), (' class="ib_selected"', self.make_iconlink("unsubscribe", d))][self.request.user.isSubscribedTo([self.page_name])])
                elif icon == "searchform":
                    if not self.site_mode:
                        toolbar.append('<li>%s</li>' % self.searchform(d))
                elif icon == "Despam" and not request.user.isSuperUser():
                    pass
                else:
                    page_name, querystr = self.buttons[icon]
                    if not (self.site_mode and page_name and self.cfg.navi_bar and ((page_name % d) in self.cfg.navi_bar)):
                        toolbar.append('<li>%s</li>' % self.make_iconlink(icon, d))
            toolbar.append('</ul></div>\n')
        return ''.join(toolbar)

        
    def editor_link(self, d):
        """ Return links to the editor if the user can edit
        """
        page = self.page
        enabled = page.isWritable() and self.request.user.may.write(page.page_name)
        guiworks = self.guiworks(page)
        editor = self.editor_to_show()
        if editor == 'freechoice' and guiworks:
            if enabled:
                return '<li>%s</li><li>%s</li>' % (self.make_iconlink('edit gui', d), self.make_iconlink('edit text', d))
            else:
                return '<li>%s</li><li>%s</li>' % (self.make_icon('edit gui disabled', d), self.make_icon('edit text disabled', d))
        else:
            if enabled:
                icon = ['edit text', 'edit gui'][editor == 'gui' and guiworks]
                return '<li>%s</li>' % self.make_iconlink(icon, d)
            else:
                icon = ['edit text disabled', 'edit gui disabled'][editor == 'gui' and guiworks]
                return '<li>%s</li>' % self.make_icon(icon, d)


    def editor_to_show(self):
        """ Returns the editor to show
        depending on global or user configuration
        
        @return: 'freechoice', 'gui' or 'text'
        """
        cfg = self.cfg
        user = self.request.user
        if cfg.editor_force:
            editor = cfg.editor_ui
            if editor == 'theonepreferred':
                editor = cfg.editor_default
        else:
            editor = user.editor_ui
            if editor == '<default>':
                editor = cfg.editor_ui
                if editor == 'theonepreferred':
                    editor = user.editor_default
                    if editor == '<default>':
                        editor = cfg.editor_default
            elif editor == 'theonepreferred':
                editor = user.editor_default
                if editor == '<default>':
                    editor = cfg.editor_default
        return editor

                    
    def username_link(self, d):
        """ Assemble the username link
        
        Based on username function in MoinMoin/theme/__init__.py module
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: username html
        """
        request = self.request

        homelink = u''
        # Add username/homepage link for registered users. We don't care
        # if it exists, the user can create it.
        if request.user.valid and request.user.name:
            interwiki = self.wikiutil.getInterwikiHomePage(request)
            name = request.user.name
            aliasname = request.user.aliasname
            if not aliasname:
                aliasname = name
            title = "%s @ %s" % (aliasname, interwiki[0])
            # link to (interwiki) user homepage
            homelink = (request.formatter.interwikilink(1, title=title, id="userhome", generated=True, *interwiki) +
                        request.formatter.text(name) +
                        request.formatter.interwikilink(0, title=title, id="userhome", *interwiki))
        return homelink

        
    def make_iconlink(self, which, d):
        """
        Make a link with an icon

        @param which: icon id (dictionary key)
        @param d: parameter dictionary
        @rtype: string
        @return: html link tag
        """
        qs = {}
        # MOD querystr, title, icon = self.cfg.page_icons_table[which]
        page_name, querystr = self.buttons[which]
        qs.update(querystr) # do not modify the querystr dict in the buttons table!
        # d['icon-alt-text'] = d['title'] = title % d
        # d['i18ntitle'] = self.request.getText(d['title'])
        img_src = self.make_icon(which, d)
        if 'rev' in qs:
            qs['rev'] = str(d['rev'])
        attrs = {'rel': 'nofollow', }
        page = d['page']
        if page_name:
            page = self.Page(self.request, page_name % d)
        else:
            page = self.page
        return page.link_to_raw(self.request, text=img_src, querystr=qs, **attrs)



    # =============================
    # Page Area
    # =============================

    def page_header_info(self, page):
        """ Return html fragment with page meta data

        Based on pageinfo function.
        
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
                    info = _("last edited %(time)s by %(editor)s", formatted=False) % info
                else:
                    info = _("last modified %(time)s", formatted=False) % info
                html = '<p id="page_header_info"%(lang)s>%(info)s, page size: %(size)s</p>' % {
                    'lang': self.ui_lang_attr(),
                    'info': info,
                    'size': self.wiki_tree.human_readable_size(page.size())
                    }
        return html


    def attachment_list(self):
        html = self.AttachFile._build_filelist(self.request, self.page_name, showheader=0, readonly=0)
        if html:
            html = u'<div id="attachments">\n%s\n</div>' % html
        return html



    # ========================================
    # Include explorer.js
    # ========================================

    def externalScript(self, name):
        # Overwritten from ThemeBase
        """ Format external script html """
        # modified to supply an additional script file
        return '%s\n<script type="text/javascript" src="%s/explorer/js/explorer.js"></script>' % (ThemeBase.externalScript(self, name), self.cfg.url_prefix_static)


def execute(request):
    """
    Generate and return a theme object
        
    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)



class WikiNode:
    """
    A WikiNode is an object representing a page (resp. category)
    or an attachment and has the following attributes:
        display_name  : displayed name of the node
        type          : node type (0 = category, 1 = page or 2 = attachment)
        exists        : flag indicating that a node exists
        url           : url of the node
        html          : html code representing the node
        parents       : list of parents of the node
        size          : size of the node
        subnodes_size : size of all sub pages and attachments
        categories    : list of sub categories of the category
        pages         : list of pages in this category or subpages of page
        attachments   : list of attachments of the node
        may_read      :
    """
    import re
    
    url = ''
    html = ''
    summary_html = ''
    categories_html = ''
    exists = False
    size = 0
    subnodes_size = 0
    
    
    def __init__(self, request, name, id, is_attachment=False):
        """ Init the wiki node

        @param request: the request object
        @param name: string
        @param is_attachment: boolean
        """
        self.name = name
        self.display_name = name
        self.id = id
        self.parents, self.categories, self.pages, self.attachments = [], [], [], []
        self.subnodes = [ self.categories, self.pages, self.attachments ]
        self.may_read = { }
        if is_attachment:
            self.type = 2  # attachment
        else:  # Identify the node type
            match_object = self.re.match(request.cfg.cache.page_category_regex, name)
            if match_object:
                self.type = 0  # category
                if is_moin_1_6:  # Moin 1.6
                    # On categories remove the key string identifying a category (default 'Category')
                    if match_object.lastindex:
                        self.display_name = match_object.group(1).lstrip()
                else:  # Moin 1.7
                    # Extract the key of the category to be dispalyed only
                    if match_object.groupdict().has_key('key'):
                        self.display_name = match_object.groupdict()['key'].lstrip()
            else:
                self.type = 1  # page


    def add_sub_node(self, node):
        """ Add a sub node of the given type
        """
        node.parents.append(self.name)
        self.subnodes[node.type].append(node.name)
        self.subnodes_size += node.size


    def remove_sub_node(self, node):
        """ Remove a sub node
        """
        node.parents.remove(self.name)
        self.subnodes[node.type].remove(node.name)
        self.subnodes_size -= node.size


    def reset(self):
        self.exists = False
        self.html = ''
        self.size = 0



class WikiTree:
    """
    The wiki tree represents the tree of all pages (resp. categories) and
    attachments of the wiki. It has the following attributes:
        wiki_tree   : a dictionary of WikiNodes { node_name : node, ... }
        root        : name of the root category
        orphaned    : name of the orphaned category
        underlay    : name of the underlay category
        root_category, orphaned_category, underlay_category
        type_counts : list of total counts of categories, pages and attachments
        total_size  : total size of all nodes
        
    These are cached in the meta cache server object and are updated on changes.
    """
    import thread, math, os, cPickle, Cookie
    from MoinMoin.action import AttachFile
    from MoinMoin import wikiutil, config, caching
    from MoinMoin.Page import Page
    
    release = '1.0.3'

    # fake _ function to get gettext recognize those texts:
    _ = lambda x: x
    ui_text = {
        # used in node_description
        'categories' :   _('categories'),
        'pages' :        _('pages'),
        'attachments' :  _('attachments'),
        'size' :         _('size'),
        }
    del _
    
    touched = set([])  # Nodes changed since last tree update


    def __init__(self, theme, page_name):
        """ Inits the wiki tree structure and wiki tree info
            or loads it from cache
        """
        self.request = request = theme.request
        self.page_name = page_name

        # Define image tags for node icons
        self.node_icon_html = [
            u'<img src="%s">' % theme.img_url('category.png'),
            u'<img src="%s">' % theme.img_url('page.png'),
            u'<img src="%s">' % theme.img_url('attachment.png'),
            u'<img src="%s">' % theme.img_url('category missing.png'),
            u'<img src="%s">' % theme.img_url('page missing.png'),
            ]
        self.expand_icon_url = theme.img_url('toggle1.png')
        self.collapse_icon_url = theme.img_url('toggle0.png')
        
        self.categories_formatter = CategoriesFormatter(request, store_pagelinks=1)

        # Get cached lock on wiki tree
        self.lock = request.cfg.cache.meta.getItem(request, u'', u'wiki_tree_lock')
        if not self.lock:  # If lock doesn't exist build one
            self.lock = self.thread.allocate_lock()
            request.cfg.cache.meta.putItem(request, u'', u'wiki_tree_lock', self.lock)
        # Get cached wiki tree
        self.cache = request.cfg.cache.meta.getItem(request, u'', u'wiki_tree')
        if not self.cache and self.lock.acquire(0):
            # Only enter if lock can be acquired immediately without waiting
            # (i.e. only the first one enters, others wait in the else clause)
            # No cached tree exists: Set lock and build tree.
            try:
                # Special categories of the wiki tree (generally these should be a categories) 
                cfg = request.cfg
                self.root = getattr(cfg, 'wiki_tree_root', u'')
                self.orphaned = getattr(cfg, 'wiki_tree_orphaned', self.root)
                self.underlay = getattr(cfg, 'wiki_tree_underlay', u'CategoryUnderlay')
                disk_cache = self.caching.CacheEntry(request, '', 'wiki_tree', 'wiki')
                # Check if there's a cached wiki tree
                if disk_cache.exists():
                    version, self.cache = self.cPickle.loads(disk_cache.content())
                    if version == self.release and self.cache[4:7] == [self.root, self.orphaned, self.underlay]:
                        # Only use cached data if it corresponds to the wiki_tree version
                        # This avoids errors when data structure changes
                        request.cfg.cache.meta.putItem(request, u'', u'wiki_tree', self.cache)
                        self.load_cache_data(self.cache)
                        self.refresh()
                        self.write_disk_cache(self.cache)

                if not getattr(self, 'wiki_tree', False):
                    self.build()
            finally:
                self.lock.release()
        else:
            self.cache = None
            self.lock.acquire()
            try:
                # Get wiki tree data from cache.
                if not self.cache:
                    self.cache = self.request.cfg.cache.meta.getItem(self.request, u'', u'wiki_tree')
                    self.load_cache_data(self.cache)
                self.refresh()
            finally:
                self.lock.release()


    def load_cache_data(self, cache):
        self.log_pos, self.total_size, self.summary_html, self.type_counts, self.root, self.orphaned, self.underlay, self.root_category, self.orphaned_category, self.underlay_category, self.wiki_tree = cache


    def build_cache_data(self):
        return [
            self.log_pos, self.total_size, self.summary_html, self.type_counts,
            self.root, self.orphaned, self.underlay,
            self.root_category, self.orphaned_category, self.underlay_category,
            self.wiki_tree
        ]
        
        
    def write_disk_cache(self, cache):
        # Cache the wiki tree to disk
        disk_cache = self.caching.CacheEntry(self.request, '', 'wiki_tree', 'wiki')
        data = self.cPickle.dumps([self.release, cache])
        disk_cache.update(data)

        
    def refresh(self):
        """ Refresh the wiki nodes changed
            if anything has changed in the wiki, we see it
            in the edit-log and update the wiki_tree accordingly
        """
        self.log_pos = self.cache[0]
        self.total_size = self.cache[1]
        self.summary_html = self.cache[2]
        elog = self.request.editlog
        old_pos = self.log_pos
        new_pos, items = elog.news(old_pos)
        if self.request.action == 'refresh':
            page_name = self.page_name
            if page_name not in items:
                items.append(page_name)
            page = self.Page(self.request, page_name, formatter=self.categories_formatter)
            parent_categories = self.categories_formatter.getCategories(page, update_cache=True)
            if page_name == self.root and self.request.user.isSuperUser():
                self.build()
                return

        if items:
            items = set(items)  # Convert to set
            for item in items:
                self.remove_page(item)
            for item in items:
                self.add_page(item)
            self.finalize_touched()
        self.log_pos = new_pos  # important to do this at the end -
                                # avoids threading race conditions
        self.cache[0] = self.log_pos
        self.cache[1] = self.total_size
        self.cache[2] = self.summary_html


    def build(self):
        """ Builds the wiki tree structure and wiki tree info
        """
        self.wiki_tree = { }
        self.type_counts = [ 0, 0, 0 ]
        self.total_size = 0

        self.root_category = self.get_assured_node(self.root)
        # if self.orphaned:
        self.orphaned_category = self.get_assured_node(self.orphaned)
        # if self.underlay:
        self.underlay_category = self.get_assured_node(self.underlay)

        # print '>>>>>> Start Build WikiTree: ', time.clock()
        page_list = self.request.rootpage.getPageList(exists=0, user='')
        # print '>>>>>> End Build PageList: ', time.clock()
        # Add all pages from the wiki
        for page_name in page_list:
            self.add_page(page_name)
        # print '>>>>>> Finish Build WikiTree: ', time.clock()
        self.finalize_touched()
        
        self.log_pos, items = self.request.editlog.news(None)  # ToDo: Optimize. Only need end position
        self.cache = self.build_cache_data()
        self.request.cfg.cache.meta.putItem(self.request, u'', u'wiki_tree', self.cache)
        self.write_disk_cache(self.cache)


        
    def add_page(self, page_name):
        """ Add a page to the wiki tree
        """
        request = self.request
        page = self.Page(request, page_name, formatter=self.categories_formatter)
        if page.exists():
            node = self.get_assured_node(page_name)
            node.exists = True
            node.size = page.size()
            node.url = page.url(request, relative=False)
            self.type_counts[node.type] += 1
            self.total_size += node.size

            # Add attachments to the wiki tree
            attachments = self.get_attachment_dict(page_name)
            for (attachment_name, attachment_info) in attachments.iteritems():
                attachment_key = page_name + '/' + attachment_name
                attachment_node = self.get_assured_node(attachment_key, is_attachment=True)
                attachment_node.display_name = attachment_name
                attachment_node.exists = True
                attachment_node.size = attachment_info[0]
                attachment_node.url = attachment_info[1]
                self.add_to_parent(attachment_node, page_name, node)
                self.type_counts[2] += 1
                self.total_size += attachment_node.size
                self.touched.add(attachment_key)

            pos = page_name.rfind('/')
            if pos > 0:  # page is subpage
                node.display_name = page_name[pos+1:]
                self.add_to_parent(node, page_name[:pos])
            else:
                # Add the page to the categories it belongs to
                parent_categories = self.categories_formatter.getCategories(page)
                if self.underlay_category and page.isUnderlayPage():
                    parent_categories.append(self.underlay)
                for parent_category in parent_categories:
                    self.add_to_parent(node, parent_category)

            self.touched.add(page_name)


    def get_assured_node(self, node_name, is_attachment=False):
        """ Get a wiki node with the specified name.
        If the node doesn't exist it is created.
        """
        if node_name in self.wiki_tree:
            node = self.wiki_tree[node_name]
        else:
            node = WikiNode(self.request, node_name, self.wikiutil.url_quote('%s_node' % node_name, ''), is_attachment=is_attachment)
            self.wiki_tree[node_name] = node
            self.touched.add(node_name)
        return node


    def add_to_parent(self, node, parent_name, parent = None):
        """ Add a node to a parent node
        """
        if not parent:
            parent = self.get_assured_node(parent_name)
        parent.add_sub_node(node)
        self.touched.add(parent_name)


    def get_attachment_dict(self, page_name):
        """ Returns a dict of attachments

        The structure of the dictionary is:
        { file_name : [file_size, get_url], ... }
        
        @param page_name:
        @rtype: attachments dictionary
        @return: attachments dictionary
        """
        attach_dir = self.AttachFile.getAttachDir(self.request, page_name)
        files = self.AttachFile._get_files(self.request, page_name)
        attachments = {}
        for file in files:
            fsize = float(self.os.stat(self.os.path.join(attach_dir,file).encode(self.config.charset))[6])
            get_url = self.AttachFile.getAttachUrl(page_name, file, self.request, escaped=1)
            attachments[file] = [fsize, get_url]
        return attachments


    def remove_page(self, page_name):
        """ Remove a node from the wiki tree
        """
        if page_name in self.wiki_tree:
            node = self.wiki_tree[page_name]
            self.type_counts[node.type] -= 1
            self.total_size -= node.size

            while node.attachments:
                self.remove_page(node.attachments[0])

            while node.parents:
                self.remove_from_parent(node, node.parents[0])

            if node.categories or node.pages or (page_name in [self.root, self.orphaned, self.underlay]):
                node.reset()
                self.touched.add(page_name)
            else:
                del self.wiki_tree[page_name]


    def remove_from_parent(self, node, parent_name):
        """ Remove a node from the parent node
        """
        parent = self.wiki_tree[parent_name]
        parent.remove_sub_node(node)
        if parent.exists or parent.categories or parent.pages or (node.name in [self.root, self.orphaned, self.underlay]):
            self.touched.add(parent_name)
        else:
            self.remove_page(parent_name)


    def finalize_touched(self):
        """ Calculate totals, prepare the html code for each node
        that has changed (these nodes are stored in the touched set)
        """
        first_step_touched = self.touched
        self.touched = set([])
        for node_name in first_step_touched:
            self.finalize_node(node_name)
        second_step_touched = self.touched
        self.touched = set([])
        for node_name in second_step_touched:
            self.finalize_node(node_name)
        # Build a description of the wiki (counters and size)
        _ = self.ui_text
        self.summary_html =  u'<ul id="wiki_summary"><li>%i&nbsp;%s<li>%i&nbsp;%s<li>%i&nbsp;%s<li>%s:&nbsp;%s</ul>' % (
                    self.type_counts[1], _['pages'],
                    self.type_counts[0], _['categories'],
                    self.type_counts[2], _['attachments'],
                    _['size'], self.human_readable_size(self.total_size))


    def finalize_node(self, node_name):
        """ Finalize the wiki tree node
        
        Calculates the totals and the html code for the node.
        
        @param node name:
        @param path: list of nodes up to this one
        """
        if node_name in self.wiki_tree:
            request = self.request

            node = self.wiki_tree[node_name]
            parents = node.parents

            # Sort sub nodes
            node.categories.sort()
            node.pages.sort()
            node.attachments.sort()
            if not node.exists:
                # Page represented by node doesn't exist
                node.url = '%s/%s' % (request.getScriptname(), self.wikiutil.quoteWikinameURL(node_name))
                if node_name != self.orphaned and not parents:
                    # Add page to category orphaned
                    self.add_to_parent(node, self.orphaned)
            if not parents and node_name != self.root:
                # Page is orphaned but not root, add it to orphaned category
                self.add_to_parent(node, self.orphaned)
                if node_name == self.orphaned:
                    # If orphaned category is orphaned add it to root
                    self.add_to_parent(node, self.root)
            # Get list of parents the page belongs to
            if node_name.find('/') == -1 and parents:
                items = [u'<ul id="parents">']
                for parent in parents:
                    if parent != self.root or parent != self.orphaned:
                        page = self.Page(request, parent)
                        title = page.split_title()
                        link = page.link_to(request, title)
                        items.append('<li>%s</li>' % link)
                items.append(u'</ul>')
                node.categories_html = '\n'.join(items)

            # Build the html code for the link
            categories_count = len(node.categories)
            pages_count = len(node.pages)
            attachments_count = len(node.attachments)
            total_size = node.subnodes_size + node.size
            node.summary_html = u'<ul id="page_summary"><li>%s</ul>' % self.description('', categories_count, pages_count, attachments_count, total_size, separator=u'<li>')
            title = self.description(node_name, categories_count, pages_count,attachments_count, total_size)
            icon_type = [node.type + 3, node.type][node.exists]
            html = u'%s<a class="node" href="%s" title="%s">%s</a>' % (self.node_icon_html[icon_type], node.url, title, node.display_name)
            if node.categories or node.pages or node.attachments:
                # ToDo: make this nicer
                node.html = u'<li><img id="%s" class="toggle" alt="%%(alt)s" src="%%(src)s" onclick="toggle_node(event)">%s' % (node.id.replace('%', '%%'), html.replace('%', '%%'))
            else:
                node.html = u'<li class="leaf">%s' % html


    def description(self, name, categories_count, pages_count,attachments_count, size, separator = u', '):
        """ Return a description of the node
        
        The description contains information about the size and
        counters of the sub tree of the node
        
        @param node: 
        @param separator: separator unicode string
        @rtype: unicode
        @return: html describing the sub tree
        """
        if name:
            name = u'%s: ' % name
        description = name
        _ = self.ui_text
        description = u'%s%i&nbsp;%s%s%i&nbsp;%s%s%i&nbsp;%s%s%s:&nbsp;%s' % (
                description,
                pages_count, _['pages'], separator,
                categories_count, _['categories'], separator,
                attachments_count, _['attachments'], separator,
                _['size'], self.human_readable_size(size))
        return description


    def human_readable_size(self, size):
        """ Return the size normalized with unit
        
        @param size: integer denoting a file size
        @rtype: unicode
        @return: html describing the file size
        """
        if size == 0:
            return u'0&nbsp;Bytes'
        file_size_name = [u'Bytes', u'KB', u'MB', u'GB', u'TB', u'PB', u'EB', u'ZB', u'YB']
        i = int(self.math.log(size, 1024))
        if i:
            return u'%.2f&nbsp;%s' % (round(size/pow(1024, i), 2), file_size_name[i])
        else:
            return u'%i&nbsp;Bytes' % size
    


    # =============================
    # UI
    # =============================
    def page_summary_html(self):
        if not self.page_name in self.wiki_tree:
            return ""
        return self.wiki_tree[self.page_name].summary_html


    def page_categories_html(self):
        if not self.page_name in self.wiki_tree:
            return ""
        return self.wiki_tree[self.page_name].categories_html


    def tree_html(self):
        """ Returns wiki tree html code
        """
        request = self.request
        self.user_may_read = request.user.may.read
        self.userid = request.user.id
        self.acl_caching = getattr(request.cfg, 'wiki_tree_acl_caching', True)
        # Get the cookie of the request
        if is_moin_1_6:  # Moin 1.6
            self.cookie = request.parse_cookie()
        else:  # Moin 1.7
            self.cookie = request.cookie
        if not self.cookie:
            self.cookie = self.Cookie.SimpleCookie()
        
        if self.wiki_tree.has_key(self.page_name):
            self.expand_parents(self.page_name, [])
        
        self.expand_subtree = ''
        if self.cookie.has_key('expand_subtree'):
            self.expand_subtree = self.cookie['expand_subtree'].value
            self.cookie[self.expand_subtree] = 1
        return self.subtree_html(self.root)


    def subtree_html(self, node_name, path=None, display_all=False):
        """ Return wiki sub tree html code with the specified node as root

        The path contains the path of nodes from the root to the current node.
        
        @param node_name: root of the sub tree
        @param path: list of nodes up to this one
        @rtype: unicode
        @return: wiki tree html
        """
        node = self.wiki_tree[node_name]
        if node.exists:
            if self.acl_caching:
                if self.userid in node.may_read:
                    may_read = node.may_read[self.userid]
                else:
                    may_read = self.user_may_read(node_name)
                    node.may_read[self.userid] = may_read
            else:
                may_read = self.user_may_read(node_name)
            if not may_read:
                return u''

        items = []
        html = node.html
        if node_name == self.page_name:
            html = html.replace('class="node"', 'id="node_selected"')
        sub_nodes = node.categories + node.pages + node.attachments
        if not sub_nodes:
            if path:  #  root node is not diplayed
                items = [html]
        else:
            id = node.id
            display_subtree = id in self.cookie or display_all or not path
            if path:  #  root node is not diplayed
                if display_subtree:
                    toggle_icon_url = self.collapse_icon_url
                    toggle_icon_alt = "[-]"
                else:
                    toggle_icon_url = self.expand_icon_url
                    toggle_icon_alt = "[+]"
                items = [html % {'alt' : toggle_icon_alt, 'src' : toggle_icon_url}]
            if display_subtree:
                if not path:
                    path = [node_name]
                else:
                    path.append(node_name)
                path.append(node_name)
                display_all = display_all or id == self.expand_subtree
                items.append(u'<ul class="wiki_tree">')
                for sub_node_name in sub_nodes:
                    if sub_node_name not in path:  # don't allow recursion
                        items.append(self.subtree_html(sub_node_name, path, display_all))
                items.append(u'</ul>')
        return u'\n'.join(items)


    def expand_parents(self, node_name, path=None):
        """ Expands the parent nodes up to the given node

        The path contains the path of nodes from the current node
        toward the root.
        This is used to avoid recursion in the wiki tree.
        
        @param node_name: root of the sub tree
        @param path: list of nodes from this one to the current page
        @rtype: unicode
        @return: wiki tree html
        """
        if node_name == self.root:  # root node reached
            return True
        node = self.wiki_tree[node_name]
        id = node.id
        if id in path:  # stop on recursion
            return False
        if path:
            path.append(id)
        else:
            path = [id]
        is_path_to_root = False
        for parent_name in node.parents:
            if self.expand_parents(parent_name, path):
                self.cookie[id] = 'X'
                is_path_to_root = True
                break
        return is_path_to_root



from MoinMoin.formatter import FormatterBase
    
class CategoriesFormatter(FormatterBase):
    """
        categories Formatter
        @copyright: 2007, 2008 Wolfgang Fischer

        based on pagelinks formatter
        @copyright: 2005 Nir Soffer <nirs@freeshell.org>
        @license: GNU GPL, see COPYING for details.
    """
    """ Collect categories and format nothing :-) """

    def __init__(self, request, **kw):
        FormatterBase.__init__(self, request, **kw)
        import re
        self.page_category_regex = re.compile(request.cfg.page_category_regex, re.UNICODE)

        
    def pagelink(self, on, pagename='', page=None, **kw):
        if self.page_category_regex.search(pagename):
            FormatterBase.pagelink(self, on, pagename, page, **kw)
        return self.null()


    def getCategories(self, page, update_cache=False):
        """ Get a list of the links on this page.
        Based on getPageLinks function in Page module

        @page page: the page object
        @rtype: list
        @return: category names this page belongs to
        """
        request = self.request
        if page:
            self.setPage(page)
        page = self.page
        if page.exists():
            from MoinMoin import caching
            cache = caching.CacheEntry(request, page, 'categories', scope='item', do_locking=False, use_pickle=True)
            if update_cache or cache.needsUpdate(page._text_filename()):
                links = self.parseCategories()
                cache.update(links)
            else:
                try:
                    links = cache.content()
                except caching.CacheError:
                    links = self.parseCategories()
                    cache.update(links)
        else:
            links = []
        return links


    def parseCategories(self):
        """ Parse categories by formatting with a categories formatter 
        [Based on parsePageLinks function in Page module]

        This is a old hack to get the pagelinks by rendering the page
        with send_page. We can remove this hack after factoring
        send_page and send_page_content into small reuseable methods.
        
        More efficient now by using special pagelinks formatter and
        redirecting possible output into null file.
        """
        request = self.request
        page = self.page
        pagename = page.page_name

        request.clock.start('parseCategories')

        class Null:
            def write(self, data):
                pass

        request.redirect(Null())
        try:
            self.pagelinks = []
            pi = page.pi
            page.send_page_content(request, page.data,
                                   format=pi['format'],
                                   format_args=pi['formatargs'],
                                   do_cache=1,
                                   start_line=pi['lines'])
        finally:
            request.redirect()
            # if hasattr(request, '_fmt_hd_counters'):
            #    del request._fmt_hd_counters
            request.clock.stop('parseCategories')
        return self.pagelinks

        
    def null(self, *args, **kw):
        return ''
        
    def macro(self, macro_obj, name, args, markup=None):
        return ''
        
    # All these must be overriden here because they raise
    # NotImplementedError!@#! or return html?! in the base class.
    set_highlight_re = rawHTML = url = image = smiley = text = null
    strong = emphasis = underline = highlight = sup = sub = strike = null
    code = preformatted = small = big = code_area = code_line = null
    code_token = linebreak = paragraph = rule = icon = null
    number_list = bullet_list = listitem = definition_list = null
    definition_term = definition_desc = heading = table = null
    table_row = table_cell = attachment_link = attachment_image = attachment_drawing = null
    transclusion = transclusion_param = null
