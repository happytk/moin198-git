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
# $Id: AddComment.py 42 2010-04-02 18:29:13Z hguerreiro $
#


"""
Add Comment Macro

This macro places the comment form on the page.

Usage:
    <<AddComment(Add a Comment title, Add button label)>>
"""

# MoinMoin imports:
from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.mail import sendmail
from MoinMoin.datastruct.backends import GroupDoesNotExistError

from datetime import datetime
from random import choice
from string import letters, digits

import os
import uuid

from comment_utils import get_cfg, get_input, write_comment, notify_subscribers

# Auxiliary class:
class AddComment:
    def __init__(self, macro ):
        self.macro = macro
        self.page = macro.request.page
        self.user = macro.request.user
        self.page_name = macro.formatter.page.page_name

        self.msg = ''
        self.reset_comment()
        self.errors = []

        try:
            passpartout_group = macro.request.groups[
                get_cfg(macro, 'comment_passpartout_group', 'PasspartoutGroup' )]

            if self.user.name in passpartout_group:
                passpartout = True
            else:
                passpartout = False
        except GroupDoesNotExistError:
            passpartout = False

        self.passpartout = passpartout
        self.moderate = get_cfg(macro, 'comment_moderate', True) and not passpartout

        if macro.request.method == 'POST':
            self.save_comment()

    def reset_comment(self):
        '''Resets the comment dict to default a value'''
        self.comment = {
                'user_name' : self.user.name,
                'comment': '',
                'email': '',
                }

    def get_comment(self):
        self.comment = {
            'user_name' : get_input(self.macro, 'user_name'),
            'comment': get_input(self.macro, 'comment'),
            'email': get_input(self.macro, 'email'),
            }

    def errors_check(self):
        """
        Check the form for errors.
        """
        _ = self.macro.request.getText

        errors = []

        if not self.comment['user_name']:
            errors.append( _('You must enter your name.') )
        if len(self.comment['user_name']) > 128:
            errors.append( _('Please use a shorter name.') )
        if not self.comment['comment']:
            errors.append( _('You have yet to write your comment.') )
        if len(self.comment['comment']) > 10240:
            errors.append( _('Maximum number of characters is 10240.'))

        if ( get_cfg(self.macro, 'comment_recaptcha', False) and not self.passpartout
            and not self.captcha.is_valid):
            errors.append( _("I'm not sure you're human! Please fill in the captcha."))

        return errors

    def save_comment( self ):
        _ = self.macro.request.getText

        if get_input(self.macro, 'do' ) != u'comment_add':
            # This is not a comment post do nothing
            return

        if get_cfg(self.macro, 'comment_recaptcha', False ) and not self.passpartout:
            import captcha
            self.captcha = captcha.submit (
                get_input(self.macro, 'recaptcha_challenge_field'),
                get_input(self.macro, 'recaptcha_response_field'),
                get_cfg(self.macro, 'comment_recaptcha_private_key'),
                self.macro.request.remote_addr )

        self.get_comment()
        self.errors = self.errors_check()

        if not self.errors: # Save the comment
            # Find out where to save the comment:
            if self.moderate:
                # This commet will be added to the moderation queue
                page = Page(self.macro.request,
                    get_cfg(self.macro, 'comment_approval_page', 'CommentsApproval'))
                comment_dir = page.getPagePath('', check_create=0)
            else:
                # The comment will be immediately posted
                page = Page(self.macro.request,self.page_name)
                comment_dir = page.getPagePath('comments', check_create=1)

            # Compose the comment structure and write it
            now = datetime.now()
            # random_str =  ''.join([choice(letters + digits) for i in range(20)])
            random_str = str(uuid.uuid1()).replace('-', '')
            comment_file = '%s-%s.txt' % (now.strftime("%s"), random_str)
            file_name = os.path.join(comment_dir, comment_file)

            comment = self.comment
            comment['page'] = self.page_name
            comment['time'] = now
            if get_cfg(self.macro, 'comment_store_addr', False):
                comment['remote_addr'] = self.macro.request.remote_addr

            if self.moderate:
                self.msg = _('Your comment awaits moderation. Thank you.')
            else:
                self.msg = _('Your comment has been posted. Thank you.')

            write_comment( file_name, comment )

            if self.moderate:
                # If we have defined a list of moderators to notify and this user is
                # moderated then a message is sent to the moderator list
                moderators = get_cfg(self.macro, 'comment_moderators', None)
                if moderators:
                    sendmail.sendmail( self.macro.request, moderators.split(','),
                    _('New comment awaits moderation for page %(page)s' % self.comment ),
                    _('New comment awaits moderation:\n\nPage: %(page)s\nFrom: %(user_name)s\nMessage:\n\n%(comment)s\n\n--' %
                        self.comment ))
            else:
                # Send notification to page subscribers if the page
                notify_subscribers(self.macro, self.comment)

            # clean up the fields to display
            self.reset_comment()

    def renderInPage(self):
        """
        Render comments form in page context.
        """
        _ = self.macro.request.getText
        html = u'''<div class="comments_form">
        <form method="POST" action="%(page_uri)s">
        <input type="hidden" name="do" value="comment_add">
        <table>''' % { 'page_uri': self.macro.request.request.url }

        html += '''
            <tr>
                <td colspan=2 id="center_cell"><b>%(header)s</b></td>
            </tr>
            <tr>
                <th>%(name_label)s</th>
                <td>
                    <input type="text" id="name" maxlength=128 name="user_name"
                           value="%(user_name)s">
                </td>
            </tr>
            <tr>
                <th>%(comment_label)s</th>
                <td>
                    <textarea name="comment">%(comment)s</textarea>
                </td>
            </tr>
            ''' % {
            'page_name': self.page_name,
            'user_name': self.comment['user_name'],
            'comment':   self.comment['comment'],
            'header': _('Comment this page'),
            'name_label': _('Name:'),
            'comment_label': _('Comment:')  }

        if self.msg:
            html += u'<tr><td colspan = 2><div id="comment_message">'
            html += u'<p>%s</p>' % self.msg
            html += u'</div></td></tr>'

        if self.errors:
            html += u'<tr><td colspan = 2><div id="comment_error">'
            if len(self.errors) > 1:
                html += u'<p>%s</p><ul>'  % _('Your comment has errors:')
            else:
                html += u'<p>%s</p><ul>'  % _('Your comment has one error:')
            for error in self.errors:
                html += u'<li>%s</li>' % error
            html += u'</ul></div></td></tr>'

        if get_cfg(self.macro, 'comment_recaptcha', False) and not self.passpartout:
            import captcha
            html += u"""
            <tr>
                <th>%(recaptcha_label)s</th>
                <td>%(recaptcha)s</td>
            </tr>""" % {
            'recaptcha' : captcha.displayhtml(
                                get_cfg(self.macro, 'comment_recaptcha_public_key')),
            'recaptcha_label': _('Are you human?') }

        html += """
             <tr>
                <td colspan=2 id="center_cell"><input type="submit" value="%(label)s">
                </td>
            </tr>
        </table></form></div>""" % { 'label': _('Send comment') }

        try:
            return self.macro.formatter.rawHTML(html)
        except:
            return self.macro.formatter.escapedText('')


# Macro function:
def macro_AddComment(macro):
    return AddComment(macro).renderInPage()
