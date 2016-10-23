# -*- coding: utf-8 -*-
"""
    MoinMoin - photo upload action

"""

from MoinMoin import wikiutil
from MoinMoin.Page import Page
import glob, os
from MoinMoin.action.AttachFile import add_attachment, AttachmentAlreadyExists

def photoupload(pagename, request):
    _ = request.getText

    # if not wikiutil.checkTicket(request, request.form.get('ticket', '')):
    #     return _('Please use the interactive user interface to use action %(actionname)s!') % {'actionname': 'AttachFile.upload' }

    # Currently we only check TextCha for upload (this is what spammers ususally do),
    # but it could be extended to more/all attachment write access
    # if not TextCha(request).check_answer_from_form():
    #     return _('TextCha: Wrong answer! Go back and try again...')

    form = request.form

    file_upload = request.files.get('file')
    if not file_upload:
        # This might happen when trying to upload file names
        # with non-ascii characters on Safari.
        return _("No file content. Delete non ASCII characters from the file name and try again.")

    try:
        overwrite = int(form.get('overwrite', '0'))
    except:
        overwrite = 0

    if not request.user.may.write(pagename):
        return _('You are not allowed to attach a file to this page.')

    if overwrite and not request.user.may.delete(pagename):
        return _('You are not allowed to overwrite a file attachment of this page.')

    # target = form.get('target', u'').strip()
    # if not target:
    #     target = file_upload.filename or u''

    # target = wikiutil.clean_input(target)
    file_upload_ext = os.path.splitext(file_upload.filename)[-1].lower()
    if file_upload_ext not in ('.jpg'):
        return _('You can upload only following extentions. -- .jpg, but ' + file_upload_ext)

    # if not target:
    #     return _("Filename of attachment not specified!")
    if pagename.encode('utf8') == '아메바사진':
        path = '/volume1/photo/webpub_amb'#/@eaDir'
    elif pagename.encode('utf8') == '사과나무사진관':
        path = '/volume1/photo/webpub_apt'#/@eaDir'
    else:
        path = '/volume1/photo/webpub_tst'

    try:
        lst = glob.glob(path + '/*.jpg')
        lastnumfilepath = sorted(lst)[-1]
        lastnumfile = os.path.split(lastnumfilepath)[1]
        filenm = os.path.splitext(lastnumfile)[0]
        filenum = int(filenm)
        filenum += 1
        target = "%05d%s" % (filenum, file_upload_ext)
    except:
        target = "00001" + file_upload_ext

    print '-'*100
    print path, target
    # add the attachment
    try:
        target, bytes = add_attachment(request, pagename, target, file_upload.stream, overwrite=overwrite)
        msg = "Picture '%(target)s' ('%(filename)s',%(bytes)d bytes) have been uploaded." % {
                'target': target, 'filename': file_upload.filename, 'bytes': bytes}
    except AttachmentAlreadyExists:
        msg = _("Attachment '%(target)s' (remote name '%(filename)s') already exists.") % {
            'target': target, 'filename': file_upload.filename}
    # return attachment list
    #upload_form(pagename, request, msg)

    # move
    # replace illegal chars
    target = wikiutil.taintfilename(target)

    # get directory, and possibly create it
    # attach_dir = getAttachDir(request, pagename, create=1)
    if request.page and pagename == request.page.page_name:
        page = request.page # reusing existing page obj is faster
    else:
        page = Page(request, pagename)
    attach_dir = page.getPagePath("attachments", check_create=1)
    fpath = os.path.join(attach_dir, target).encode(request.cfg.attachment_charset)

    os.rename(fpath, path + os.sep + target)
    # msg += ' mv %s %s/%s' % (fpath, path, target)

    # os.system('synoindex -a ' + path + '/' + target)
    # os.system('synoindxe -U photo')
    from subprocess import Popen
    pid = Popen(["/volume1/photo/create_tn.sh", path, target]).pid

    #request.page.send_page()
    return msg

def execute(pagename, request):
    msg = photoupload(pagename, request)
    request.theme.add_msg(msg)
    Page(request, pagename).send_page()



