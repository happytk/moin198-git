# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormText Macro

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from FormField import FormField


class FormText(FormField):
    
    def __init__(self, macro, args):
        FormField.__init__(self, macro, args)
        
        self.maxlength = ""
        self.size = ""
        self.autocomplete = ""
        self.disabled = ""
        self.readonly = ""
        
    def build(self):
        FormField.build(self)
        #self.output += self._build_input("hidden", "labels[]", {'value':self.label})
        self.output += self._build_input("text", self.label, self._attribs)
    

def execute(macro, args):
    return FormText(macro, args).render()
