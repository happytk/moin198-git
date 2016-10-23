# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - submitemail Action
    
    Send submited data email address specified in targetemail CGI parameter

    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin import wikiutil
from MoinMoin.action import ActionBase
from MoinMoin.Page import Page
from MoinMoin.mail.sendmail import sendmail

from submitbase import SubmitBase


def execute(pagename, request):
    submitemail(pagename, request).render()


class submitemail(SubmitBase):          
    
    def __init__(self, pagename, request):
        SubmitBase.__init__(self, pagename, request)
        
        self.subject = "MoinMoin mail"
        self.targetemail = request.form.get("targetemail", "")
        
    def build_content(self):
        """ Builds simple 'label: value' string """
        text = ""
        for label in self.labels:
            index = self.labels.index(label)
            label = label.decode('utf-8')
            value = self.values[index]
            text += "%(label)s: %(value)s \n" % {'label': label, 'value': value}
        return text
        
    def submit(self):
        SubmitBase.submit(self)   
        text = self.build_content()
        status, msg = sendmail(self.request, self.targetemail, self.subject, text, mail_from=self.targetemail)
        self.msg = self._(msg)
        if status != 1:
            raise Exception(self.msg)
