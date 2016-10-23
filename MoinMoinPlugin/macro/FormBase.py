# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormBase Macro

    Base stuff for all form macros.
    Macro generates HTML form elements in following sequence:
    - parse_args   parse defined parameters
    - validate     validate correct definition of parameters  
    - build        build HTML element and stores it into self.output

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin import wikiutil


class FormBase(object):

    debug = False
    
    def __init__(self, macro, args):
        self.macro = macro
        self.request = macro.request
        self._ = self.request.getText
        self.module = self.__module__.split(".").pop()
        self.args = args
        
        self.msg = ""
        self.output = ""
        
        # Macro parameters
        self._main = {}  # Main parameters
        self._attribs = {}  # in FormField macros used as HTML tag attributes
        self._params = {}  # Additional parameters

    def parse_args(self):
        """ Parse parameters into specific macro properties """
        self._main, self._attribs, self._params = wikiutil.parse_quoted_separated(self.args)    
    
    def validate(self):
        """ Validates macro parameters """
        for name, value in self._attribs.iteritems():
            if not hasattr(self, name):
                self.msg = self._("Invalid attribute [%(attr)s] specified in macro [%(mod)s]" % {
                                  'attr': name, 'mod': self.module})
                raise FormValidationError(self.msg)
    
    def build(self):
        """ Build HTML element """
        raise NotImplementedError
    
    def render(self):
        """ Executes core methods: parse_args, validate, build 
        
        Returns output as HTML element or error message.
        """
        if not self.debug:
            try:
                self.parse_args()
                self.validate()
                self.build()
            except FormValidationError:
                return self.msg
            except Exception, e:
                # TODO: Log exception
                self.output = self._("Error - %s") % e
                            
            return self.output
        
        else:
            try:
                self.parse_args()
                self.validate()
                self.build()
            except FormValidationError:
                return self.msg
            
            return self.output

    def _build_attribs(self, attribs):
        """ Converts HTML element attributes from dictionary to string """
        attrstr = ""
        for name, value in attribs.iteritems():
            if value:
                attrstr += "%(name)s=\"%(value)s\" " % {'name': name, 'value': value}
            
        return attrstr
    
    def _build_input(self, type, name, args):
        """ Builds HTML input element """
        attrs = self._build_attribs(args)
        if name is None:
            input = "<input type=\"%(type)s\" %(attrs)s/>\n" % {'type': type, 'attrs': attrs}
        else:
            input = "<input type=\"%(type)s\" name=\"%(name)s\" %(attrs)s/>\n" % {
                'type': type, 'name': name, 'attrs': attrs}
        return input


class FormValidationError(Exception):
    """ Exception raised for errors during validation """
