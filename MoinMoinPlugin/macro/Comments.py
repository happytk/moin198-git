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
# $Id: Comments.py 47 2010-04-02 23:00:39Z hguerreiro $
#

"""
Comments Macro

This macro display the comments page.
It collects the comments files and displays its content.

Usage:
    <<Comments([page_name])>>
"""

# General imports:
import os
import glob

# MoinMoin imports
from MoinMoin.Page import Page

# Utils
from comment_utils import *

# Auxiliary functions:

def comment_html(request, comment):
    _ = request.getText
    return '''<table>
    <tr><td>%(name)s</td><td>%(comment_name)s</td></tr>
    <tr><td>%(time)s</td><td>%(comment_time)s</td></tr>
    <tr><td colspan=2>%(comment_text)s</td></tr>
    </table>''' % {
    'name': _('Name:'),
    'comment_name': comment['user_name'],
    'time': _('Time:'),
    'comment_time': comment['time'].strftime('%Y.%m.%d %H:%M'),
    'comment_text': '<p>'.join( comment['comment'].split('\n') ),
    }

def navbar(request, page_number, max_pages, page_uri):
    _ = request.getText

    if max_pages == 1:
        return ''

    html = ['<div class="navbar">']
    if page_number > 1:
        html.append('<div class="prevcmt">')
        html.append('<a href="%s">%s</a>&nbsp;&nbsp;' %
                (page_uri,_('|&lt;')))
        html.append('<a href="%s?page_number=%d">%s</a>&nbsp;&nbsp;' %
                (page_uri,page_number-1,_('&lt;&lt;')))
        html.append('</div>')

    if page_number < max_pages:
        html.append('<div class="nextcmt">')
        html.append('<a href="%s?page_number=%d">%s</a>&nbsp;&nbsp;' %
                (page_uri,page_number+1,_('&gt;&gt;')))
        html.append('<a href="%s?page_number=%d">%s</a>&nbsp;&nbsp;' %
                (page_uri,max_pages,_('&gt;|')))
        html.append('</div>')

    html.append('</div>')

    return '\n'.join(html)

def macro_Comments(macro, page_name=u''):
    '''
    Usage:

        <<Comments(page_name)>>
        Shows the comments of page 'page_name'
    or
        <<Comments()>>
        Shows the page of the current page.
    '''
    _ = macro.request.getText
    request = macro.request
    formatter = macro.formatter


    # By default show the comments for the current page
    if page_name == u'':
        page_name = macro.formatter.page.page_name

    # Get the configuration:
    page = Page(request, page_name )
    comments_dir = page.getPagePath("comments", check_create=1)

    # Get the page_name comment list
    files = glob.glob(os.path.join(comments_dir,'*.txt'))
    files.sort()

    # Compose the comments markup
    html = [u'<a name="comment_section"></a>']
    if not files:
        html.append(u'<p>%s</p>' % _('There are no comments'))
    else:
        # Pagination
        cmt_per_page = get_cfg_int(macro, 'comment_cmt_per_page',50)

        if cmt_per_page:
            page_uri = request.url.split('?')[0]

            number_messages = len(files)
            if number_messages % cmt_per_page:
                offset = 1
            else:
                offset = 0
            max_pages = number_messages / cmt_per_page + offset
            try:
                page_number = get_input_int(macro, 'page_number', 1 )
            except ValueError:
                page_number = 1
            if page_number > max_pages:
                page_number = max_pages
            elif page_number < 1:
                page_number = 1

            first = (page_number - 1) * cmt_per_page
            last  = first + cmt_per_page

            files = files[first:last]

        # Get the comments contents
        comments = [ read_comment(Xi) for Xi in files]

        for comment in comments:
            html.append( u"%s" % comment_html(request, comment ) )

        if cmt_per_page:
            html.append(navbar(request, page_number, max_pages, page_uri))

    try:
        return formatter.rawHTML('\n'.join(html))
    except:
        return formatter.escapedText('')
