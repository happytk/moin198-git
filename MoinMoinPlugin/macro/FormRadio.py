# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormRadio Macro

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from FormField import FormField


class FormRadio(FormField):
    
    def __init(self, macro, args):
        FormField.__init__(self, macro, args)
        
        self.value = ""
        self.checked = ""
        self.size = ""
        
    def parse_args(self):
        FormField.parse_args(self)
        
        self.value = self._main[1]
        
    def validate(self):
        FormField.validate(self)
        if not self.value:
            self.msg = self._("Field value is not defined")
            raise FormValidationError(self.msg)     
            
    def build(self):
        FormField.build(self)
        self._attribs["value"] = self.value
        self._attribs["checked"] = "checked"
        #self.output += self._build_input("hidden", "labels[]", {'value':self.label})
        self.output += self._build_input("radio", self.label, self._attribs)
    

def execute(macro, args):
    return FormRadio(macro, args).render()
