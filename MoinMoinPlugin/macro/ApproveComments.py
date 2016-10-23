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
#
# $Id: ApproveComments.py 43 2010-04-02 19:03:55Z hguerreiro $
#

"""
Approve Comments Macro

This macro lists the comments waiting for approval and displays the
delete and approval buttons.

Usage:
    <<ApproveComments()>>

Requirements:
    You have to create a page where the comments are stored for moderation. This
    page is defined with the configuration variable:

        comment_approval_page

    And by default has a value of:

        CommentsApproval
"""

# General imports:
from MoinMoin.Page import Page
from MoinMoin import wikiutil

import os
from datetime import datetime
import glob

from comment_utils import get_cfg, get_input, read_comment, notify_subscribers

class ApproveError(Exception): pass


class ApproveComments:
    def __init__(self, macro ):
        self.macro = macro
        self.page_name = get_cfg(macro, 'comment_approval_page',
                              'CommentsApproval')
        self.msg = []

        if self.page_name != macro.formatter.page.page_name:
            # It's mandatory to run the ApproveComments macro from the
            # comment_approval_page defined in the configuration
            return

        page = Page(macro.request,self.page_name)
        if not page.exists():
            raise ApproveError('You have to create the approval page!')
        self.approval_dir = page.getPagePath('', check_create=0)

        if macro.request.method == 'POST':
            if get_input( macro, 'do' ) == u'comment_delete':
                self.delete_comment()
            if get_input( macro, 'do' ) == u'comment_approve':
                self.approve_comment()

    def delete_comment(self):
        _ = self.macro.request.getText

        file_name = get_input( self.macro, 'file' )
        os.remove(os.path.join(self.approval_dir, file_name))
        self.msg.append(_('Comment deleted'))

    def approve_comment(self):
        _ = self.macro.request.getText

        # Source
        origin = os.path.join(self.approval_dir, get_input(self.macro, 'file'))
        comment = read_comment( origin )

        # Destination
        page = Page(self.macro.request, comment['page'] )
        if not page.exists():
            self.msg.append(_('The page this comment was written for don\'t exist any more'))
            return

        dest_dir = page.getPagePath("comments", check_create=1)
        destination = os.path.join(dest_dir,get_input(self.macro, 'file'))

        # Rename the file:
        os.rename(origin, destination)
        self.msg.append(_('Comment approved'))

        # Notify page subscribers:
        notify_subscribers(self.macro, comment)

    def render_in_page(self):

        def cmp_page_time( a, b ):
            if a['page'] < b['page']:
                return -1
            elif a['page'] > b['page']:
                return 1
            else:
                if a['time'] < b['time']:
                    return -1
                elif a['time'] > b['time']:
                    return 1
            return 0

        _ = self.macro.request.getText

        if self.page_name != self.macro.formatter.page.page_name:
            return self.macro.formatter.text(
             _('Sorry, but the  ApproveComments macro must be '
               'used on %(page_name)s page.' %
                { 'page_name': self.page_name } ))

        html = []

        if self.msg:
            html.append('<div class="comment_message"><ul>')
            for m in self.msg:
                 html.append('<li>%s</li>' % m)
            html.append('</ul></div>')

        files = glob.glob(os.path.join(self.approval_dir,'*.txt'))
        if not files:
            html.append(u'<p>%s</p>' % _("There's no comment awaiting for moderation."))
        else:
            comments = []

            # Read the comments:
            for file_name in files:
                comment = read_comment( file_name )
                comment['file_name'] = file_name
                comments.append(comment)

            # Sort the coments by page, then by time
            comments.sort(cmp_page_time)

            for comment in comments:
                html.append( u'''<div class="comment_approval">
<table>
  <tr><th colspan=2>%(intro)s %(page_name)s</th></tr>
  <tr><td>%(name)s</td><td>%(comment_name)s</td></tr>
  <tr><td>%(time)s</td><td>%(comment_time)s</td></tr>''' % {
                    'intro': _('Comment to'),
                    'page_name': comment['page'],
                    'name': _('Name:'),
                    'time': _('Time:'),
                    'comment_time': comment['time'].strftime('%Y.%m.%d %H:%M'),
                    'comment_name': comment['user_name'],
                    })
                if get_cfg(self.macro, 'comment_store_addr', False):
                    html.append(u'  <tr><td>%(remote_addr)s</td><td>%(comment_addr)s</td></tr>' % {
                    'remote_addr': _('Remote address:'),
                    'comment_addr': comment['remote_addr'],
                    })
                html.append(u'''  <tr><td colspan=2>%(comment_text)s</td></tr>
  <tr>
    <td colspan=2>
      <form method="POST" action="%(page_uri)s">
        <input type="hidden" name="do" value="comment_delete">
        <input type="submit" value="%(button_delete)s" id="delete">
        <input type="hidden" name="file" value="%(comment_file)s">
      </form>
      <form method="POST" action="%(page_uri)s">
        <input type="hidden" name="do" value="comment_approve">
        <input type="submit" value="%(button_accept)s" id="ok">
        <input type="hidden" name="file" value="%(comment_file)s">
      </form>
    </td>
  </tr>
</table>
</div><br />''' % {
                'comment_text': '<p>'.join( comment['comment'].split('\n') ),
                'comment_file': os.path.basename(comment['file_name']),
                'page_uri': self.macro.request.request.url,
                'button_delete': _('Delete'),
                'button_accept': _('Accept'),
                } )

        try:
            return self.macro.formatter.rawHTML('\n'.join(html))
        except:
            return self.macro.formatter.escapedText('')

# Macro function:
def macro_ApproveComments(macro):
    return ApproveComments(macro).render_in_page()
