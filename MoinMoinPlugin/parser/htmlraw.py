#-*- coding: iso-8859-1 -*-
#format python
"""
    MoinMoin - HTML-RAW Parser

    @copyright: 2006 MoinMoin:AlexanderSchremmer
    @license: GNU GPL, see COPYING for details.
"""

Dependencies = []

class Parser:
    """
        Sends HTML code after filtering it.
    """

    extensions = ['.htm', '.html']
    Dependencies = Dependencies

    def __init__(self, raw, request, **kw):
        self.raw = raw
        self.request = request

    def format(self, formatter, **kw):
        """ Send the text. """
        self.request.write('<p></p>')
        self.request.write(self.raw)
        self.request.write('<div style="clear:both;"></div>')
