# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormSubmit Macro

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.security.textcha import TextCha

from FormField import FormField


class FormSubmit(FormField):
    
    def __init__(self, macro, args):
        FormField.__init__(self, macro, args)
        
        self.value = ""
        self.size = ""
        
    def parse_args(self):
        FormField.parse_args(self)
        self.value = self.label
        
    def build(self):
        self.output += TextCha(self.request).render()
        self.output += self._build_input("submit", None, {'value': self.value})
    

def execute(macro, args):
    return FormSubmit(macro, args).render()
