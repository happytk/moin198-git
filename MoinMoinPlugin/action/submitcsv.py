# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - submitcsv Action
    
    Store submited data into CSV file. CSV file is located
    in standard MoinMoin attchment folder or defined in 
    targetpage CGI parameter.
    
    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

import os
import csv
import codecs
import cStringIO

from MoinMoin import config, wikiutil
from MoinMoin.Page import Page
from MoinMoin.action import AttachFile

from submitbase import SubmitBase


def execute(pagename, request):
    submitcsv(pagename, request).render()           


class submitcsv(SubmitBase):
        
    def __init__(self, pagename, request):
        SubmitBase.__init__(self, pagename, request)
        
        self.delimiter = ';'
        self.targetFile = request.form.get("targetfile", "list.csv")
        self.targetFile = wikiutil.taintfilename(self.targetFile)  # replace illegal chars

    def sanitize(self):
        SubmitBase.sanitize(self)
        self.targetFile = wikiutil.clean_input(self.targetFile)
            
    def submit(self):
        SubmitBase.submit(self)        
        request = self.request
        pagename = self.targetpage
                                
        attachDir = AttachFile.getAttachDir(request, pagename, create=1)
            
        targetFile = self.targetFile
        
        filePath = os.path.join(attachDir, targetFile).encode(config.charset)
        
        # save header
        if not os.path.exists(filePath):
            fh = open(filePath, 'wb')
            
            # Encoded Input to writer.writerow
            writer = csv.writer(fh, delimiter=self.delimiter)
            writer.writerow(self.labels)
            
            # Decoded Input to writer.writerow
            #writer = UnicodeWriter(fh, delimiter=self.delimiter)
            #writer.writerow(self.labels)
            
            fh.close()
        
        # save content
        fh = open(filePath, 'ab')
        
        # Encoded Input to writer.writerow
        #writer = csv.writer(fh, delimiter=self.delimiter, quoting=csv.QUOTE_MINIMAL)
        #writer.writerow(self.values)
        
        # Decoded Input to writer.writerow
        writer = UnicodeWriter(fh, delimiter=self.delimiter, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(self.values)
        
        fh.close()


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
