# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormTextarea Macro

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from FormField import FormField


class FormTextarea(FormField):
    
    def __init__(self, macro, args):
        FormField.__init__(self, macro, args)
        
        self.rows = ""
        self.cols = ""
        self.disabled = ""
        self.readonly = ""
        
    def build(self):
        FormField.build(self)
        #self.output += self._build_input("hidden", "labels[]", {'value':self.label})
        self.output += "<textarea name=\"%(label)s\" %(attribs)s></textarea>" % {
            'attribs': self._build_attribs(self._attribs), 'label': self.label}
    

def execute(macro, args):
    return FormTextarea(macro, args).render()
