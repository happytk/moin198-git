# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormHeader Macro

    Generates form header with some additional parameters.

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.Page import Page

from FormBase import FormBase, FormValidationError


class FormHeader(FormBase):
     
    def parse_args(self):
        FormBase.parse_args(self)
        
        self.action = ""
        self.actions = ()

        length = len(self._main)
        
        if length > 1:
            self.action = "loadactions"
            self.actions = self._main
        elif length == 1:
            self.action = self._main[0]

        self.targetfile = self._attribs.get('targetfile', '')
        self.targetemail = self._attribs.get('targetemail', '')
        self.targetpage = self._attribs.get('targetpage', '')
        
    def validate(self):
        FormBase.validate(self)    
        if not self.action:
            self.msg = self._("No action was specified in macro [%(macro)s]" % {'macro': self.module})
            raise FormValidationError(self.msg)
        
    def build(self):
        self.output += "<form enctype=\"multipart/form-data\" action=\"\" method=\"post\">\n"
        self.output += self._build_input("hidden", "doit", {'value': "Do it"})
        self.output += self._build_input("hidden", "action", {'value': self.action})
        
        if self.actions:
            for action in self.actions:
                self.output += self._build_input("hidden", "actions[]", {'value': action})
        
        if self.targetfile:
            self.output += self._build_input("hidden", "targetfile", {'value': self.targetfile})
            
        if self.targetemail:
            self.output += self._build_input("hidden", "targetemail", {'value': self.targetemail})
            
        if self.targetpage:
            page = Page(self.request, self.targetpage)
            if page.isStandardPage(False):
                self.output += self._build_input("hidden", "targetpage", {'value': self.targetpage})
            else:
                self.output += self._("Targetpage [%(targetpage)s] does not exists" % {'targetpage': self.targetpage})

        
def execute(macro, args):
    return FormHeader(macro, args).render()  
