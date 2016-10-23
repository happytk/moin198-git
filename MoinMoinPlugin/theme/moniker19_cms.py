# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - moniker_cms theme
    (based entirely on modernized_cms)

    @copyright: 2009 MoinMoin:ThomasWaldmann
    @license: GNU GPL, see COPYING for details.
"""

from moniker19 import Theme as ThemeBase



class Theme(ThemeBase):

    name = "moniker" # we tell that we are 'moniker', so we use its static data

    def onlyloggedin(method):
        """ decorator that returns empty string for not logged-in users,
            otherwise it calls the decorated method
        """
        return lambda self, *args, **kwargs: (
            self.request.user.valid and self.request.user.name and method(self, *args, **kwargs)
            or
            ''
            )


# Rick: Borrowing code from Roger Haase's FixedLeft theme so that the searchbox buttons will wrap: 
    def searchpanel(self,d):
        """Create search panel.
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: formatted search panel
        """
        _ = self.request.getText
        html = [
            u'<div class="sidepanel"><h1>%s</h1>' % (_("Search Site")),
            self.searchform(d),
            u'</div>',
            ]
        return u''.join(html)




# Rick:  Comment out the parts you do or don't want to show.  Hint: username.
    interwiki = onlyloggedin(ThemeBase.interwiki)
    title = onlyloggedin(ThemeBase.title)
    #username = onlyloggedin(ThemeBase.username)
    pageinfo = onlyloggedin(ThemeBase.pageinfo)
    title_with_separators = onlyloggedin(ThemeBase.title_with_separators)
    editbarpanel = onlyloggedin(ThemeBase.editbarpanel)


def execute(request):
    return Theme(request)

