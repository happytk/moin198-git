# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - submitattachment Action

    Attach file into standard MoinMoin attachment folder or defined in
    targetpage CGI parameter.
    
    If attachment with same name already exists, numeric index
    is added to new attachment. (file_1.txt, file_2.txt, ...)
    
    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.action import AttachFile

from submitbase import SubmitBase, SubmitValidationError


def execute(pagename, request):
    submitattachment(pagename, request).render()


class submitattachment(SubmitBase):
    
    def rewrite_filename(self, filename):
        """ Rewrites filename if there already exists attachment with the same name
        """
        attachFile = filename
        i = 0 
        while AttachFile.exists(self.request, self.targetpage, attachFile):
            attachFile = self.attachFile
            attachFileSplit = attachFile.split(".", 2)
            ext = attachFileSplit.pop()
            name = '.'.join(attachFileSplit)
            attachFile = "%(name)s_%(index)d.%(extension)s" % {'name': name, 'index': i, 'extension': ext}
            i += 1
            
        filename = attachFile
        
        return filename
            
    def validate(self):
        """ Evaluates whethere valid file was specified """
        SubmitBase.validate(self)
        
        if not self.attachFile:
            self.msg = self._("File was not specified")
            raise SubmitValidationError(self.msg)
        
        if not self.attachContent:
            self.msg = self._("Invalid file '%(file)s'") % {'file': self.attachFile}
            raise SubmitValidationError(self.msg)
     
    def sanitize(self):
        SubmitBase.sanitize(self)
        self.request.files['file'].filename = self.attachFile = self.rewrite_filename(self.attachFile)
         
    def submit(self):
        AttachFile.add_attachment(self.request, self.targetpage, self.attachFile, self.attachContent, 0)
