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
# $Id: comment_utils.py 49 2010-04-03 00:04:09Z hguerreiro $
#

"""
Utility functions to use with the comments macros.
"""

##
# Imports
##

import pickle
from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.mail import sendmail

##
# Functions
##

def read_comment( file_name ):
    f = open(file_name, 'r')
    comment = pickle.load(f)
    f.close()
    return comment

def write_comment( file_name, comment ):
    f = open(file_name, 'wb')
    pickle.dump(comment, f )
    f.close()

def get_input( macro, arg_name, default = ''  ):
    '''
    Reads a form field and returns default if the field is missing
    '''
    if arg_name in macro.request.values:
        return wikiutil.escape(macro.request.values[arg_name])
    else:
        return default

def get_input_int( macro, arg_name, default = 0  ):
    try:
        return int(get_input( macro, arg_name, default ))
    except ValueError:
        return 0

def get_cfg( macro, key, default = None ):
    '''
    Reads a configuration value and returns a default if it doesn't exist.
    '''
    try:
        return macro.request.cfg[key]
    except AttributeError:
        return default

def get_cfg_int( macro, key, default = 0 ):
    try:
        return int(get_cfg( macro, key, default ))
    except ValueError:
        return default

def notify_subscribers(macro, comment):
    '''Notify page subscribers'''
    subscribed_notify = get_cfg(macro, 'comment_subscribed_notify', False)
    if not subscribed_notify:
        return

    request = macro.request
    _ = macro.request.getText
    page = Page(request, comment['page'])
    subscribers = page.getSubscribers(request)

    mailing_list = []
    for lang in subscribers.keys():
        for person in subscribers[lang]:
            mailing_list.append(person)

    if mailing_list:
        sendmail.sendmail( request, mailing_list,
        _('New comment was posted in page %(page)s' % comment),
        _('New comment was posted in page:\n\nPage: %(page)s\nFrom: %(user_name)s\nMessage:\n\n%(comment)s\n\n--' %
        comment ))