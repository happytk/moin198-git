# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormSelect Macro

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from FormField import FormField


class FormSelect(FormField):
            
    def __init__(self, macro, args):
        FormField.__init__(self, macro, args)
        
        self.list = ()
        self.size = ""
        self.multiple = ""
        self.disabled = ""
        
    def parse_args(self):
        FormField.parse_args(self)
        self.list = self._main
        self.list.pop(0)
        
    def build(self):
        FormField.build(self)
        #self.output += self._build_input("hidden", "labels[]", {'value':self.label})
        self.output += "<select name=\"%(label)s\" %(attribs)s>\n" % {'label': self.label, 'attribs': self._attribs}
        self.output += "<option value=\"\"></option>\n"
        for item in self.list:
            self.output += "<option value=\"%(item)s\">%(item)s</option>\n" % {'item': item}
        self.output += "</select>\n"
    

def execute(macro, args):
    return FormSelect(macro, args).render()
