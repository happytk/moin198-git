# -*- coding: utf-8 -*-
"""
    MoinMoin - PhotoUpload Macro
"""

from MoinMoin.action.AttachFile import *
from MoinMoin import wikiutil

Dependencies = []

def macro_PhotoUpload(macro):

    """ Send the HTML code for the list of already stored attachments and
        the file upload form.
    """
    request = macro.request
    pagename = request.page.page_name
    _ = request.getText

    if not request.user.may.read(pagename):
        request.write('<p>%s</p>' % _('You are not allowed to view this page.'))
        return

    writeable = request.user.may.write(pagename)

    # First send out the upload new attachment form on top of everything else.
    # This avoids usability issues if you have to scroll down a lot to upload
    # a new file when the page already has lots of attachments:
    if writeable:
        request.write('<h2>' + u"새로운 사진 올리기" + '</h2>')
        request.write("""
<form action="%(url)s?action=PhotoUpload" method="POST" enctype="multipart/form-data">
<dl>
<dt>%(upload_label_file)s <input type="file" name="file" size="50"></dt>
<dd></dd>
</dl>
%(textcha)s
<p>
<input type="hidden" name="action" value="%(action_name)s">
<input type="submit" value="%(upload_button)s">
</p>
</form>
""" % {
    'url': request.href(pagename),
    'action_name': 'PhotoUpload',
    'upload_label_file': u'좋은사진 이쁜사진 고릅시다.',
    'upload_label_target': _('Sequence'),
    # 'target': wikiutil.escape(request.values.get('target', ''), 1),
    # 'target': '00001.jpg',
    'upload_label_overwrite': _('Overwrite existing attachment of same name'),
    'overwrite_checked': ('', 'checked')[request.form.get('overwrite', '0') == '1'],
    'upload_button': _('Upload'),
    'textcha': TextCha(request).render(),
    'ticket': wikiutil.createTicket(request),
})

    # request.write('<h2>' + _("Attached Files") + '</h2>')
    # #request.write(_get_filelist(request, pagename))

    # if not writeable:
    #     request.write('<p>%s</p>' % _('You are not allowed to attach a file to this page.'))


	#send_photouploadform('FrontPage', request)
	return ""