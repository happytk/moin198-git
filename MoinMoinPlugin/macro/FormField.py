# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormField Macro

    Base stuff for field macros. All form fields should 
    be derived from FormField class.

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin import wikiutil

from FormBase import FormBase, FormValidationError


class FormField(FormBase):
    
    def __init__(self, macro, args):
        FormBase.__init__(self, macro, args)
        
        self.label = ""
        self.width = ""
        self.height = ""
        
        #if not hasattr(self.request, "fieldindex"):
        #    self.request.fieldindex = 0
        #else:
        #    self.request.fieldindex += 1    
        #self.index = str(self.request.fieldindex)
        
    def parse_args(self):
        FormBase.parse_args(self)
        self.label = self._main[0]
        
    def validate(self):
        FormBase.validate(self)
        if not self.label:
            self.msg = self._("Field label is not defined")
            raise FormValidationError(self.msg)

    def build(self):
        if not hasattr(self.request, "labels"):
            self.request.labels = []
            self.request.labels.append(self.label)
        else:
            if self.request.labels.count(self.label) == 0:
                self.request.labels.append(self.label)
            
        #self.output += self._build_input("hidden", self.label+"_index", {'value':self.index})
