# -*- coding: utf-8 -*-
"""
    Moniker theme for MoinMoin wiki
    
    Theme code largely based on modernized, with inspiration and help by 
    Roger Haase's FixedLeft theme (code for converting the dropdown menu into javascript).

    @copyright: 2010 Rick Vanderveer
    @license: GNU GPL
    
"""

from MoinMoin.theme import ThemeBase
from MoinMoin.action import get_available_actions
from MoinMoin import wikiutil
from MoinMoin.Page import Page

class Theme(ThemeBase):

    name = "moniker"  # Rick: I call it 'moniker' so that I can use the same CSS folder regardless of which I'm testing.

    _ = lambda x: x     # We don't have gettext at this moment, so we fake it
    icons = {
        # key         alt                        icon filename      w   h
        # file mime types for AttachTable.py macro:
        'unknown':      ("unknown type",               "filetype-unknown.png", 24, 24),
        '.doc':         ("Word file",                  "filetype-doc.png",     24, 24),
        '.docx':        ("Word file",                  "filetype-doc.png",     24, 24),
        '.xls':         ("Excel file",                 "filetype-xls.png",     24, 24),
        '.xlsx':        ("Excel file",                 "filetype-xls.png",     24, 24),
        '.ppt':         ("PowerPoint file",            "filetype-ppt.png",     24, 24),
        '.mov':         ("mov file",                   "filetype-mov.png",     24, 24),
        '.txt':         ("txt file",                   "filetype-doc.png",     24, 24),
        '.pdf':         ("pdf file",                   "filetype-pdf.png",     24, 24), 
        '.swf':         ("Flash file",                 "filetype-swf.png",     24, 24),
        '.png':         ("Graphic file",               "filetype-image.png",   24, 24),
        '.zip':         ("zip file",                   "filetype-zip.png",     24, 24),
        '.bmp':         ("Graphic file",               "filetype-image.png",   24, 24),
        '.jpg':         ("Graphic file",               "filetype-image.png",   24, 24),
        '.gif':         ("Graphic file",               "filetype-image.png",   24, 24),
        '.wmv':         ("Graphic file",               "filetype-media.png",   24, 24),
        '.wma':         ("Graphic file",               "filetype-media.png",   24, 24),
        '.mp3':         ("Graphic file",               "filetype-media.png",   24, 24),
        # AttachTable toggle controls
        #'table-null':   ("null  table control image",  "table-null.png",      16, 16),
        #'table-close':  ("close table control image",  "table-null.png",      16, 16),
        #'table-open':   ("open table control image",   "table-null.png",      16, 16),
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
        # 'interwiki':  ("[%(wikitag)s]",          "moin-inter.png",    16, 16),

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
    def header(self, d, **kw):
        """ Assemble wiki header

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),
            self.username(d),
            # '<div id="header">%s</div>' % self.logo(), 
            u'<div id="header"><div id="logo">%s %s</div></div>' % (wikiutil.getFrontPage(self.request).link_to_raw(self.request, 'PineTri'),  u'오라클모니터링/튜닝도구'),

            # Start of left panels. 
            u'<div id="sidebar">',

            self.menubarpanel(d),

            # Rick: rebuild below so we can put a cute little box around it:  self.navibar(d),
            self.navibarpanel(d),

            # Rick: rebuild below so we can put a cute little box around it:  self.searchform(d),
            self.searchpanel(d),

            # Rick: rebuild below so we can put a cute little box around it:  self.trail(d),
            self.trailpanel(d),
            
            # Rick: rebuild below so we can put a cute little box around it:  self.navibar(d),
            self.editbarpanel(d),
            u'</div>',

            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),

            # Start of page
            self.msg(d),
            self.startPage(),
            self.title_with_separators(d),
        ]
        return u'\n'.join(html)

# Rick:  copied code from Roger Haase's FixedLeft theme, but then whacked out most of it because all I really want is just to load my little javascript.  This augments to the __init__.py def html_head
    def html_head(self, d):
        """ Assemble html head
        
        modifications to ThemeBase method:
            - Add javascript source file 
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted header
        """
        head = ThemeBase.html_head(self, d)
        head += u'\n<script type="text/javascript" src="%s/%s/js/actionmenuoptions.js"></script>' % (self.cfg.url_prefix_static, self.name)
        return head


#
#   Rick:  Let's build us some panels!
#   We're going to wrap a cute little HTML box around each bar so we can dress it in CSS.
#        

    def menubarpanel(self, d):
        """ Create page actions panel . 
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted actions panel
        """
        _ = self.request.getText
        html = [
            u'<div class="sidepanel"><h1>%s</h1>' % ( _("Main Menu")),
            self.menubar(d),
            u'</div>',
            ]
        return u''.join(html) 

# Rick: Remember to customize this box by editing the edit_bar entry in your farmconfig/wikiconfig.py file!
# ## Rick This is a basic, no-frills (no hiding) panel
    def navibarpanel(self, d):
        """ Create page actions panel . 
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted actions panel
        """
        _ = self.request.getText
        html = [
            u'<div class="sidepanel"><h1>%s</h1>' % ( _("Quick Links")),
            self.navibar(d),
            u'</div>',
            ]
        return u''.join(html) 

        
# Rick: Borrowing code from Roger Haase's FixedLeft theme so that the searchbox buttons will wrap: 
    def searchpanel(self,d):
        """Create search panel.
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted search panel
        """
        _ = self.request.getText
        html = [
            u'<div class="sidepanel"><h1>%s</h1>' % (_("Search")),
            self.searchform(d),
            u'</div>',
            ]
        return u''.join(html)


    def trailpanel(self, d):
        """ Create page trail panel.

        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted page trail panle
        """
        _ = self.request.getText
        trail = self.trail(d)
        if trail:
            html = [
                u'<div class="sidepanel"><h1>%s</h1>' % ( _("Recently Viewed")),
                trail,
                u'</div>',
                ]
        else:
            html = []
        return u''.join(html)


    def trail(self, d):
        """ Assemble page trail
        from modernized (not __init__.py):

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
                html = u'<div class="pagetrail">%s</div>' % u'<span class="sep"> &darr; </span> <br>'.join(items)
        return html



    # if the the user is not allowed to edit (i.e. not logged in), then don't display at all.
    def editbarpanel(self, d):
        """ Create page actions panel . 
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted actions panel
        """
        _ = self.request.getText
        if self.shouldShowEditbar(d['page']) and \
          self.request.user.valid and self.request.user.name:
            html = [
                u'<div class="sidepanel"><h1>%s</h1>' % ( _("Page Tools")),
                self.editbar(d),
                u'</div>',
                ]
            return u''.join(html)
        return ''


    # Rick: We get to re-write this whole def all so we can convert the actions menu a drop-down list.
    # original code block copied out of Roger Haase's FixedLeft theme: he added baseurl to make things work properly 
    # with javascript, then we re-write the HTML end with our own javascript.
    
    # Don't forget you can control what appears in this listed in this menu by controlling the Actions_excluded option.
    # Paste the following into your farmconfig.py/wikiconfig.py file and comment out items you -DO- want to list:
    """    
    actions_excluded = [
            'raw',
            #'print',
            'RenderAsDocbook',
            #'refresh',
            'SpellCheck',
            'LikePages',
            #'LocalSiteMap',
            #'RenamePage',
            'CopyPage',
            'DeletePage',
            'MyPages',
            #'SubscribeUser',
            'Despam',
            'revert',
            'PackagePages',
            'SyncPages',
            'Load',
            'Save',
            ]
    """

    def actionsMenu(self, page):
        """ Create actions menu list and items data dict

        The menu will contain the same items always, but items that are
        not available will be disabled (some broken browsers will let
        you select disabled options though).

        The menu should give best user experience for javascript
        enabled browsers, and acceptable behavior for those who prefer
        not to use Javascript.

        TODO: Move actionsMenuInit() into body onload - requires that the theme will render body,
              it is currently done in wikiutil/page.


        @param page: current page, Page object
        @rtype: unicode
        @return: actions menu html fragment
        """
        request = self.request
        _ = request.getText
        rev = request.rev
        # rev was a hidden input within the more actions form
        # alternative will be to append it to anchor urls
        if rev: 
            revision = '&amp;rev=%s' % rev
        else:
            revision = ''

        menu = [
            'raw',
            'print',
            'RenderAsDocbook',
            'refresh',
            #'__separator__',
            'SpellCheck',
            'LikePages',
            'LocalSiteMap',
            #'__separator__',
            'RenamePage',
            'CopyPage',
            'DeletePage',
            #'__separator__',
            'MyPages',
            'SubscribeUser',
            #'__separator__',
            'Despam',
            'revert',
            'PackagePages',
            'SyncPages',
            ]

        titles = {
            # action: menu title
            '__title__': _("More Actions:"),
            # Rick: Set separator to blank, as that looks better in our drop down menu:
            '__separator__': _(''),
            'raw': _('Raw Text'),
            'print': _('Print View'),
            'refresh': _('Delete Cache'),
            'SpellCheck': _('Check Spelling'), # rename action!
            'RenamePage': _('Rename Page'),
            'CopyPage': _('Copy Page'),
            'DeletePage': _('Delete Page'),
            'LikePages': _('Like Pages'),
            'LocalSiteMap': _('Local Site Map'),
            'MyPages': _('My Pages'),
            'SubscribeUser': _('Subscribe User'),
            'Despam': _('Remove Spam'),
            'revert': _('revert to this revision'),
            'PackagePages': _('Package Pages'),
            'RenderAsDocbook': _('Render as Docbook'),
            'SyncPages': _('Sync Pages'),
            }

        options = []
        #original:  option = '<option value="%(action)s"%(disabled)s>%(title)s</option>'
        
        option = '<li><a href="%(baseurl)s?action=%(action)s%(revision)s">%(title)s</a></li>'
        disabledOption = '<li class="disabled">%(title)s</li>'
     
        # class="disabled" is a workaround for browsers that ignore
        # "disabled", e.g IE, Safari
        # for XHTML: data['disabled'] = ' disabled="disabled"'
        disabled = ' disabled class="disabled"'
        # @@@ is this best way to form link to current page?  Had trouble with subpages replicating parent page name in url
        #  baseurl is full url as used here
        baseurl = self.request.getScriptname() + '/' + wikiutil.quoteWikinameURL(page.page_name) 


        # Format standard actions
        available = get_available_actions(request.cfg, page, request.user)
        for action in menu:
            data = {'action': action, 'disabled': '', 'title': titles[action], 'baseurl': baseurl, 'revision': revision,}
            # removes excluded actions from the more actions menu
            if action in request.cfg.actions_excluded:
                continue

            # Enable delete cache only if page can use caching
            if action == 'refresh':
                if not page.canUseCache():
                    data['action'] = 'show'
                    data['disabled'] = disabled

            # revert action enabled only if user can revert
            if action == 'revert' and not request.user.may.revert(page.page_name):
                data['action'] = 'show'
                data['disabled'] = disabled

            # SubscribeUser action enabled only if user has admin rights
            if action == 'SubscribeUser' and not request.user.may.admin(page.page_name):
                data['action'] = 'show'
                data['disabled'] = disabled

            # PackagePages action only if user has write rights
            if action == 'PackagePages' and not request.user.may.write(page.page_name):
                data['action'] = 'show'
                data['disabled'] = disabled

            # Despam action enabled only for superusers
            if action == 'Despam' and not request.user.isSuperUser():
                data['action'] = 'show'
                data['disabled'] = disabled

            # Special menu items. Without javascript, executing will
            # just return to the page.
            if action.startswith('__'):
                data['action'] = 'show'

            # Actions which are not available for this wiki, user or page
            if (action == '__separator__' or
                (action[0].isupper() and not action in available)):
                data['disabled'] = disabled


            #~ options.append(option % data) # @@@
            if data['disabled']:
                options.append(disabledOption % data)
            else:
                options.append(option % data)

        # Add custom actions not in the standard menu, except for
        # some actions like AttachFile (we have them on top level)
        more = [item for item in available if not item in titles and not item in ('AttachFile', )]
        more.sort()
        if more:
            # Add separator
            #~ separator = option % {'action': 'show', 'disabled': disabled,  # @@@
                                  #~ 'title': titles['__separator__'], 'baseurl': baseurl,} # @@@ deleted by last fix
                                  #~ 'title': titles['__separator__'], 'baseurl': baseurl, 'revision': revision,} # @@@
            separator = disabledOption % {'action': 'show', 'disabled': disabled,
                                  'title': titles['__separator__'], 'baseurl': baseurl,} 

            options.append(separator)
            # Add more actions (all enabled)
            for action in more:
                data = {'action': action, 'disabled': '', 'baseurl': baseurl, 'revision': revision,}
                # Always add spaces: AttachFile -> Attach File
                # XXX do not create page just for using split_title -
                # creating pages for non-existent does 2 storage lookups
                #title = Page(request, action).split_title(force=1)
                title = action
                # Use translated version if available
                data['title'] = _(title)
                options.append(option % data)

        data = {
            'label': titles['__title__'],
            'options': '\n'.join(options),
            'rev_field': rev and '<input type="hidden" name="rev" value="%d">' % rev or '',
            'do_button': _("Do"),
            'baseurl': self.request.getScriptname(),
            'pagename_quoted': wikiutil.quoteWikinameURL(page.page_name),
            }
        html = '''
<div class="togglelink" id="togglelink" onclick="toggleMenu('menu1')">[ more options ]</div>
<div id="menu1">
<ul>
%(options)s
</ul>
</div>
''' % data

        return html


    def menubar(self, d):
        return Page(self.request, 'PineTriMainMenuBar').get_raw_body()
#         return '''<ul id="navibar"><li>
#             <div class="togglelink" id="togglelink_m" onclick="toggleMenuWithTitle(this, '-monitoring', '+monitoring', 'menu_m')">+monitoring</div>
# <div id="menu_m">
# <ul>
# <li><a href='/rtchart/view/ukyp'>UKYP</li>
# <li><a href='/rtchart/view/nukyp1'>NON-UKEY(grp1)</li>
# <li><a href='/rtchart/view/nukyp1'>NON-UKEY(grp2)</li>
# <li><a href='/rtchart/view/b2b'>B2B</li>
# </ul>
# </div></li>
# <li><a href='/wiki/SqlIntegrityChecker'>SqlIntegrityChecker</a></li>
# </ul>'''



# Rick:  We get to copy this in from __init__.py so that we can comment out the current page link.
    def navibar(self, d):
        """ Assemble the navibar

        @param d: parameter dictionary
        @rtype: unicode<li>…</li>
        @return: navibar html
        """
        request = self.request
        found = {} # pages we found. prevent duplicates
        items = [] # navibar items
        item = u'<li class="%s">%s</li>'
        current = d['page_name']

        # Process config navi_bar
        if request.cfg.navi_bar:
            for text in request.cfg.navi_bar:
                pagename, link = self.splitNavilink(text)
                if pagename == current:
                    cls = 'wikilink current'
                else:
                    cls = 'wikilink'
                items.append(item % (cls, link))
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

        # Rick:  This.  This gets commented out to hide "current page" from navibar links.
        """
        # Add current page at end of local pages
        if not current in found:
            title = d['page'].split_title()
            title = self.shortenPagename(title)
            link = d['page'].link_to(request, title)
            cls = 'current'
            items.append(item % (cls, link))
        """

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
        html = u'''
        <ul id="navibar">
        %s
        </ul>
''' % items
        return html



# Rick: Pasted in <div id="searchbuttons"> (don't forget the extra </div>) to break onto two lines.  Also removed the extra size="20" so that we can make it pretty.
    def searchform(self, d):
        """
        assemble HTML code for the search forms

        @param d: parameter dictionary
        @rtype: unicode
        @return: search form html
        """
        _ = self.request.getText
        form = self.request.form
        updates = {
            # Rick - commented out because we don't need it. We wrap this in the panel above: 
            #'search_label': _('Search:'),
            'search_value': wikiutil.escape(form.get('value', [''])[0], 1),
            'search_full_label': _('Text'),
            'search_title_label': _('Titles'),
            'baseurl': self.request.getScriptname(),
            'pagename_quoted': wikiutil.quoteWikinameURL(d['page'].page_name),
            }
        d.update(updates)
# Rick - paste this in below if you want a needless field label. 
# <label for="searchinput">%(search_label)s</label>
# Rick - I also whack the 'size' from input id because that belongs in CSS.
        html = u'''
<form id="searchform" method="get" action="%(baseurl)s/%(pagename_quoted)s">
<div>
<input type="hidden" name="action" value="fullsearch">
<input type="hidden" name="context" value="180">

<input id="searchinput" type="text" name="value" value="%(search_value)s" 
    onfocus="searchFocus(this)" onblur="searchBlur(this)"
    onkeyup="searchChange(this)" onchange="searchChange(this)" alt="this">
    <div id="searchbuttons">
    <input id="titlesearch" name="titlesearch" type="submit"
    value="%(search_title_label)s" alt="Search Titles">
<input id="fullsearch" name="fullsearch" type="submit"
    value="%(search_full_label)s" alt="Search Full Text">
</div>
</div>
</form>
<script type="text/javascript">
// Initialize search form
// var f = document.getElementById('searchform');
// f.getElementsByTagName('label')[0].style.display = 'none';
var e = document.getElementById('searchinput');
e.value = "";
searchChange(e);
searchBlur(e);
</script>
''' % d
        return html


# Rick:  Here we comment out the code that does the "linkto:" code because it's too easy to accidently click in our theme.
# Rick:  Use the WhatLinksToThis.py macro available on http://moinmo.in/MacroMarket
    def title_with_separators(self, d):
        """ Assemble the title using slashes, not <ul>

        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        # _ = self.request.getText
        # if d['title_text'] == d['page'].split_title():
        #     # just showing a page, no action
        #     segments = d['page_name'].split('/')
        #     link_text = segments[-1]
        #     link_title = _('Click to do a full-text search for this title')
        #     # Rick: commented out the below line:
        #     #link_query = {'action': 'fullsearch', 'context': '180', 'value': 'linkto:"%s"' % d['page_name'], }
            
        #     # Rick: We also delete 'querystr=link_query, title=link_title,' from this section:
        #     link = d['page'].link_to(self.request, link_text, css_class='backlink', rel='nofollow')
        #     if len(segments) <= 1:
        #         html = link
        #     else:
        #         content = []
        #         curpage = ''
        #         for s in segments[:-1]:
        #             curpage += s
        #             content.append(Page(self.request,
        #                                 curpage).link_to(self.request, s))
        #             curpage += '/'
        #         path_html = u'<span class="sep"> / </span>'.join(content)
        #         # Rick: original: html = u'<span class="pagepath"> return to %s</span><span class="sep"> < </span>%s' % (path_html, link)
        #         html = u'<span class="pagepath">%s</span><span class="sep"> / </span>%s' % (path_html, link)
        # else:
        #     html = wikiutil.escape(d['title_text'])
        # return u'<span id="pagelocation">location: %s</span>' % html
        return u''
        
# Rick:  This is experimental feature for creating auto-backlinks.  Basically identical to title_with_separators, except that it hides the current page.  The backlink is only displayed on non-root pages (like subpages).  Nothing fancy, just a new link description combined with CSS display:none tag.
    def auto_backlink(self, d):
        """ Assemble the title using slashes, not <ul>

        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        _ = self.request.getText
        if d['title_text'] == d['page'].split_title():
            # just showing a page, no action
            segments = d['page_name'].split('/')
            link_text = segments[-1]
            link_title = _('Click to do a full-text search for this title')
            # Rick: commented out the below line:
            #link_query = {'action': 'fullsearch', 'context': '180', 'value': 'linkto:"%s"' % d['page_name'], }
            
            # Rick: We also delete 'querystr=link_query, title=link_title,' from this section:
            link = d['page'].link_to(self.request, link_text, css_class='backlink', rel='nofollow')
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
                path_html = u'<span class="sep"> / </span>'.join(content)
                # Rick: original: html = u'<span class="pagepath"> return to %s</span><span class="sep"> < </span>%s' % (path_html, link)
                html = u'<span class="pagepath_autobacklink">parent: %s</span><span class="sep"> / </span>' % (path_html)
        else:
            html = wikiutil.escape(d['title_text'])
        return u'<span id="pagelocation_autobacklink">%s</span>' % html




# Rick:  I copy this in from __init__.py so that I can change the last bit for CSS:
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
                userlinks.append(d['page'].link_to(request, text=_('settings'),
                                               querystr={'action': 'userprefs'}, id='userprefs', rel='nofollow'))

        if request.user.valid:
            if request.user.auth_method in request.cfg.auth_can_logout:
                userlinks.append(d['page'].link_to(request, text=_('logout'),
                                                   querystr={'action': 'logout', 'logout': 'logout'}, id='logout', rel='nofollow'))
        else:
            query = {'action': 'login'}
            # special direct-login link if the auth methods want no input
            if request.cfg.auth_login_inputs == ['special_no_input']:
                query['login'] = '1'
            if request.cfg.auth_have_login:
                userlinks.append(d['page'].link_to(request, text=_("please sign in"),
                                                   querystr=query, id='login', rel='nofollow'))

        # Rick added this to get the welcome in there:
        userlinks_html = u' | '.join(userlinks)
        html = u'<div id="username">welcome: %s</div>' % userlinks_html
        return html



# Rick: here we copy in the maxPagenameLength from __init__.py so that we can shorten it so that it fits in our panels.
# Rick; effects "Recently Viewed" as well as "quick links".  (original value: 25).
    def maxPagenameLength(self):
        """ Return maximum length for shortened page names """
        return 21



#
#   Rick:  Let's re-write some def Links so that we can make them human-readable!
#   This entire section is untouched code-wise, except to just change the "text=_('something descriptive')," 
#

    # originally 'Info'
    def infoLink(self, page):
        """ Return link to page information """
        if 'info' in self.request.cfg.actions_excluded:
            return ""
        _ = self.request.getText
        return page.link_to(self.request,
                            text=_('page history'),
                            querystr={'action': 'info'}, rel='nofollow')


    # originally 'Attachments'
    def attachmentsLink(self, page):
        """ Return link to page attachments """
        if 'AttachFile' in self.request.cfg.actions_excluded:
            return ""
        _ = self.request.getText
        return page.link_to(self.request,
                            text=_('upload & manage files'),
                            querystr={'action': 'AttachFile'}, rel='nofollow')


    # originally 'Immutable Page'
    def disabledEdit(self):
        """ Return a disabled edit link """
        _ = self.request.getText
        return ('<span class="disabled">%s</span>'
                % _('Page Locked'))


    # originally 'Subscribe' and 'Unsubscribe'
    def subscribeLink(self, page):
        """ Return subscribe/unsubscribe link to valid users

        @rtype: unicode
        @return: subscribe or unsubscribe link
        """
        if not ((self.cfg.mail_enabled or self.cfg.jabber_enabled) and self.request.user.valid):
            return ''
        _ = self.request.getText
        if self.request.user.isSubscribedTo([page.page_name]):
            action, text = 'unsubscribe', _("stop email updates")
        else:
            action, text = 'subscribe', _("email me changes")
        if action in self.request.cfg.actions_excluded:
            return ""
        return page.link_to(self.request, text=text, querystr={'action': action}, rel='nofollow')


    # originally 'Add Link' and 'Remove Link'
    def quicklinkLink(self, page):
        """ Return add/remove quicklink link

        @rtype: unicode
        @return: link to add or remove a quicklink
        """
        if not self.request.user.valid:
            return ''

        _ = self.request.getText
        if self.request.user.isQuickLinkedTo([page.page_name]):
            action, text = 'quickunlink', _("remove from quicklinks")
        else:
            action, text = 'quicklink', _("add to quicklinks")
        if action in self.request.cfg.actions_excluded:
            return ""
        return page.link_to(self.request, text=text, querystr={'action': action}, css_class='nbquicklink', rel='nofollow')



    # originally 'Edit'
    # P.S. not going to bother copying in "def guiEditorScript" because we set "editor_ui = 'theonepreferred'" in the farmconfig.py.
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

        guiworks = self.guiworks(page)
        if self.showBothEditLinks() and guiworks:
        # Rick: This.
            text = _('Edit (Text)')
            querystr['editor'] = 'text'
            attrs = {'name': 'texteditlink', 'rel': 'nofollow', }
        else:
        # Rick: And this.
            text = _('edit this page')
            if guiworks:
                # 'textonly' will be upgraded dynamically to 'guipossible' by JS
                querystr['editor'] = 'textonly'
                attrs = {'name': 'editlink', 'rel': 'nofollow', }
            else:
                querystr['editor'] = 'text'
                attrs = {'name': 'texteditlink', 'rel': 'nofollow', }

        return page.link_to(self.request, text=text, querystr=querystr, **attrs)


#
#   End def link re-writes.
#

#
#   Rick: The rest of these are carried over from Modernized, and are unmodified:
#


    def editorheader(self, d, **kw):
        """ Assemble wiki header for editor

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),

            # Header
            u'<div id="header">',
            u'<h1 id="locationline">',
            self.title(d),
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
            # self.pageinfo(page),
            self.endPage(),

            # Pre footer custom html (not recommended!)
            self.emit_custom_html(self.cfg.page_footer1),

            # Footer
            u'<div id="footer">',
            # self.credits(d),
            self.showversion(d, **keywords),
            u'</div>',

            # Post footer custom html
            self.emit_custom_html(self.cfg.page_footer2),
            ]
        return u'\n'.join(html)



    def title(self, d):
        """ Assemble the title (now using breadcrumbs)

        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        _ = self.request.getText
        content = []
        if d['title_text'] == d['page'].split_title(): # just showing a page, no action
            curpage = ''
            segments = d['page_name'].split('/') # was: title_text
            for s in segments[:-1]:
                curpage += s
                content.append(Page(self.request, curpage).link_to(self.request, s))
                curpage += '/'
            link_text = segments[-1]
            link_title = _('Click to do a full-text search for this title')
            link_query = {
                'action': 'fullsearch',
                'value': 'linkto:"%s"' % d['page_name'],
                'context': '180',
            }
            # we dont use d['title_link'] any more, but make it ourselves:
            link = d['page'].link_to(self.request, link_text, querystr=link_query, title=link_title, css_class='backlink', rel='nofollow')
            content.append(link)
        else:
            content.append(wikiutil.escape(d['title_text']))

        location_html = u'<span class="sep">/</span>'.join(content)
        html = u'<span id="pagelocation">%s</span>' % location_html
        return html



    def interwiki(self, d):
        """ Assemble the interwiki name display, linking to page_front_page

        @param d: parameter dictionary
        @rtype: string
        @return: interwiki html
        """
        if self.request.cfg.show_interwiki:
            page = wikiutil.getFrontPage(self.request)
            text = self.request.cfg.interwikiname or 'Self'
            link = page.link_to(self.request, text=text, rel='nofollow')
            html = u'<span id="interwiki">%s<span class="sep">: </span></span>' % link
        else:
            html = u''
        return html

def execute(request):
    """
    Generate and return a theme object

    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)

