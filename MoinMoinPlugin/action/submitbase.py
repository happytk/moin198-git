# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - submitbase Action

    All actions handling forms should extend SubmitBase class.
    
    Basic methods to override:
        - validate
        - sanitize
        - submit
        
    Base class methods should be called at first from overriding methods.
    All data sent from user are filtered by _exlude_metadata() and then stored in 
    fields dictionary. Data are then sorted into labels and values lists.
    
    @copyright: 2008 by Peter Bodi <petrdll@centrum.sk>
    @license: GNU GPL, see COPYING for details.
"""

import copy

from MoinMoin import wikiutil
from MoinMoin.action import ActionBase
from MoinMoin.Page import Page
from MoinMoin.action import AttachFile
from MoinMoin.action import getHandler
from MoinMoin.security.textcha import TextCha


def execute(pagename, request):
    raise NotImplementedError


class SubmitBase(ActionBase):
    """ submit base class with some generic stuff to inherit """
    
    debug = True
    msgtype = 'text/html'

    metadata = [
        'doit', 
        'action', 
        'actions[]', 
        'labels', 
        'targetfile', 
        'targetpage', 
        'targetemail', 
        'file', 
        'file__filename__', 
        'uploadlabel',
        'textcha-question',
        'textcha-answer',
    ]
    
    def __init__(self, pagename, request):
        ActionBase.__init__(self, pagename, request)
        
        self.msg = ""
        self.actions = []
        self.fields = {}
        self.labels = []
        self.values = []
        self.attachFile = ""
        self.attachContent = ""
        self.targetpage = self.pagename
        self.module = self.__module__.split(".").pop()
        
        if "actions[]" in self.request.form:
            self.actions = copy.copy(self.request.form.getlist("actions[]"))
        else:
            self.actions.append(self.module)
        
        self.fields = self._exclude_metadata(self.request.form)
        
        # file upload is present
        file_upload = request.files.get('file')
        if file_upload:
            self.attachFile = wikiutil.taintfilename(file_upload.filename)
            self.attachContent = file_upload.stream
            self.attachLabel = request.form.get("uploadlabel")
            self.attachLabel = self.attachLabel.encode('utf-8')
            
        # page where all submited data will be stored
        if "targetpage" in request.form:
            targetpage = request.form.get("targetpage")
            page = Page(self.request, targetpage)
            if page.isStandardPage(False):
                self.targetpage = targetpage

    def is_last(self):
        """ Evaluates whether currently executed action is last action from actions array
        """
        module = self.module
        lastAction = self.actions.pop()
        
        if module == lastAction:
            return True
        else:
            return False
        
    def append_link(self):
        """ Makes formated link and apends it to fields dictionary
        """
        if self.attachFile:
            attachUrl = AttachFile.getAttachUrl(self.targetpage, self.attachFile, self.request)
            attachLink = self.request.getQualifiedURL() + attachUrl
            self.fields[self.attachLabel] = attachLink
        elif "file" in self.request.form:
            self.fields[self.attachLabel] = ""
            
    def validate(self):
        """ Validates user input.
            
        On error raise Exception and assign error message to self.msg property
        """      
        if not TextCha(self.request).check_answer_from_form(self.form):
            self.msg = self._("Incorrect answer to control question")
            raise SubmitValidationError(self.msg)
        
        empty = True
        for name, value in self.fields.iteritems():
            if value:
                empty = False
                break
        if empty:
            self.msg = self._("Form is empty")
            raise SubmitValidationError(self.msg)
    
    def sanitize(self):
        """ Sanitize input data passed by validation """        
        for label, value in self.fields.iteritems():
            self.fields[label] = wikiutil.escape(value)
    
    def submit(self):
        """ Main submit logic
        
        Works with validated and sanitized data 
        """
        self.append_link()
        self.labels, self.values = self._sort_fields(self.fields, self.request.form)
    
    def do_action(self):
        """ Executes core methods: validate, sanitize, submit.
        
        Method is executed from ActionBase.render()
        """
        if not self.debug:
            try:
                self.validate()
                self.sanitize()
                self.submit()
            except SubmitValidationError:
                return False, self.msg
            except Exception, e:
                # TODO: Log exception
                return False, e
        else:
            try:
                self.validate()
                self.sanitize()
                self.submit()
            except SubmitValidationError:
                return False, self.msg

        self.msg = self._("Data has been processed successfuly")
        
        return True, self.msg
    
    def do_action_finish(self, success):
        if success:
            if self.is_last():
                self.render_success(self.error, self.msgtype)
        else:
            self.render_msg(self.error, self.msgtype)
            if not self.is_last():
                raise SubmitError
            
    def render_success(self, msg, msgtype):
        """ Triggered on success """
        self._delete_cache()
        ActionBase.render_success(self, msg, self.msgtype)
        
    def render_msg(self, msg, msgtype):
        """ Triggered on error """
        if not msg:
            msg = self._("Failed to process data")
        msg = self._("Error - %s") % msg
        self._delete_cache()
        ActionBase.render_msg(self, msg, self.msgtype)
        
    def _delete_cache(self):
        """ Delete cache after each form submit """
        pagename = self.pagename
        request = self.request
        
        arena = request.form.get('arena', 'Page.py')
        if arena == 'Page.py':
            arena = Page(request, pagename)
        key = request.form.get('key', 'text_html')
    
        # Remove cache entry (if exists), and send the page
        from MoinMoin import caching
        caching.CacheEntry(request, arena, key, scope='item').remove()
        caching.CacheEntry(request, arena, "pagelinks", scope='item').remove()
        
    def _exclude_metadata(self, form):
        """ Filter all form metadata and returns only data send by user """
        fields = dict([(k, v) for k, v in form.to_dict().iteritems()
                       if k not in self.metadata])
        return fields
            
    def _sort_fields(self, fields, form):
        """ Sort form fields to order defined in CGI labels parameter
        
        labels is string containing field names separated by semicolon
        Generation should be defined in FormFooter macro
        """
        labels = []
        values = []                    
        
        if 'labels' in form:
            _labels = form.get('labels').split(";")
            for label in _labels:
                label = label.encode('utf-8')
                labels.append(label)
                if label == 'Attachment' and label not in fields and self.targetFile:
                    fields[label] = self.targetFile  # provide filename, if none is given
                values.append(fields[label])
        else:
            labels = fields.keys()
            values = fields.values()
        
        return labels, values


class SubmitError(Exception):
    """ Exception raised for submit action errors """


class SubmitValidationError(Exception):
    """ Exception raised for errors during validation """

