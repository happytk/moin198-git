# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FormFooter Macro

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from FormBase import FormBase


class FormFooter(FormBase):
        
    def build(self):
        self.output += self._build_input("hidden", "labels", {'value':';'.join(self.request.labels)})
        self.output += "</form>\n"


def execute(macro, args):
    return FormFooter(macro, args).render()  
