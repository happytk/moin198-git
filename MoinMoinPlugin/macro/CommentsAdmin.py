# -*- coding: utf-8 -*-

# Moin-comments - Blog like comments in MoinMoin
# Copyright (C) 2009 José Lopes

## This file is part of Moin-comments.
##
## Moin-comments is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Moin-comments is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Moin-comments.  If not, see <http://www.gnu.org/licenses/>.

#
# José Lopes <jose.lopes@paxjulia.com>
# Helder Guerreiro <helder@paxjulia.com>
#
# $Id: CommentsAdmin.py 30 2009-09-18 23:22:40Z hguerreiro $
#

"""
Comments Administration Macro
"""
# General imports:
import os
import glob

# MoinMoin imports:
from MoinMoin import user, wikiutil
from MoinMoin.Page import Page

from comment_utils import *

class ApproveError(Exception): pass

def macro_CommentsAdmin(macro):
    '''
    This macro adds an administration functionality to the comments feature.
    It can be place anywhere, like for instance the wiki menu, and if the
    user is a SuperUser he will see the link to the comments approval page,
    with the total of comments waiting for approval.

    Usage:
        <<CommentsAdmin>>
    '''
    request = macro.request
    formatter = macro.formatter
    _ = macro.request.getText

    # Configuration:
    page_name = unicode(get_cfg(macro, 'comment_approval_page',
        'CommentsApproval'))
    page = Page(request,page_name)

    if not page.exists():
        raise ApproveError('You have to create the approval page! (%s)' % (
                page_name))
    approval_dir = page.getPagePath('', check_create=0)
    approval_url = wikiutil.quoteWikinameURL(page_name)

    if request.user.isSuperUser():
        # Get the number of comments waiting for approval
        files = glob.glob('%s/*.txt' % approval_dir)
        total_waiting = len(files)

        html = u'<a href="%s">%s (%s)</a>' % (
            approval_url, _('Pending Comments'), total_waiting)
    else:
        html = u''

    try:
        return formatter.rawHTML(html)
    except:
        return formatter.escapedText('')


