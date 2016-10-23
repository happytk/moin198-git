# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormCheckbox Macro

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from FormField import FormField


class FormCheckbox(FormField):
    
    def __init__(self, macro, args):
        FormField.__init__(self, macro, args)
        
        self.true = self._("True")
        self.false = self._("False")
        self.checked = ""
        self.size = ""
        
    def parse_args(self):
        FormField.parse_args(self)
        length = len(self._main)
        if length == 2:
            self.true = self._main[1]
        elif length == 3:
            self.true = self._main[1]
            self.false = self._main[2]
        
    def build(self):
        FormField.build(self)
        self.output += """
        <script type=\"text/javascript\">
        function checkbox(box, input)
        {
            if(box.checked==false)
            {
                input.value = "%(false)s"
            }
            else
            {
                input.value = "%(true)s"
            }
        }
        </script>
        """ % {'true': self.true, 'false': self.false}
        inputId = self.label
        checkboxId = self.label + "box"
        
        self._attribs["id"] = checkboxId
        self._attribs["onclick"] = "checkbox(document.getElementById('" + checkboxId + "'), document.getElementById('" + inputId + "'))"
        
        self.output += self._build_input("hidden", self.label, {'id': inputId, 'value': self.false})
        self.output += self._build_input("checkbox", None, self._attribs)


def execute(macro, args):
    return FormCheckbox(macro, args).render()
