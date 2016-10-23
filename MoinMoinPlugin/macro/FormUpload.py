# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormUpload Macro

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from FormField import FormField


class FormUpload(FormField):
    
    def __init__(self, macro, args):
        FormField.__init__(self, macro, args)
        
        self.size = ""
                
    def parse_args(self):
        FormField.parse_args(self)
        
    def build(self):
        FormField.build(self)
        self.output += self._build_input("hidden", "uploadlabel", {'value': self.label})
        self.output += self._build_input("file", "file", self._attribs)
    

def execute(macro, args):
    return FormUpload(macro, args).render()
