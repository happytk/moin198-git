# -*- coding: utf-8 -*-
"""
    MoinMoin - (re)building of Xapian indices

    @copyright: 2007 MoinMoin:KarolNowak
    @license: GNU GPL, see COPYING for details.
"""

import MoinMoin.events as ev
import os
import codecs


from dulwich.repo import Repo, NotGitRepository
from MoinMoin.action.AttachFile import _get_files, getAttachDir

EXT = '.md'


def _get_repo(event):
    request = event.request
    path = os.path.join(request.cfg.data_dir, 'pages')
    try:
        repo = Repo(path)
    except NotGitRepository:
        repo = None

    return repo


def handle_renamed(event):

    request = event.request
    staged = []

    if event.old_page.page_name_fs.startswith('_') and event.page.page_name_fs.startswith('_'):
        return
    elif event.old_page.page_name_fs.startswith('_'):
        # make new page
        staged.append(event.page.page_name_fs + EXT)
        # attachments
        attach_dir = getAttachDir(request, event.page.page_name)
        files = _get_files(request, event.page.page_name)
        for filename in files:
            staged.append(os.path.join(event.page.page_name_fs, 'attachments', filename))
    elif event.page.page_name_fs.startswith('_'):
        # delete page
        staged.append(event.old_page.page_name_fs + EXT)
        # attachments
        attach_dir = getAttachDir(request, event.page.page_name)
        files = _get_files(request, event.page.page_name)
        for filename in files:
            # delete old-page-attachments
            staged.append(os.path.join(event.old_page.page_name_fs, 'attachments', filename))
    else:

        old_page_path = os.path.join(request.cfg.data_dir, 'pages', event.old_page.page_name_fs + EXT)
        new_page_path = os.path.join(request.cfg.data_dir, 'pages', event.page.page_name_fs + EXT)

        os.rename(old_page_path, new_page_path)

        staged.extend([event.old_page.page_name_fs + EXT, event.page.page_name_fs + EXT])

        # attachments
        attach_dir = getAttachDir(request, event.page.page_name)
        files = _get_files(request, event.page.page_name)
        for filename in files:
            staged.append(os.path.join(event.old_page.page_name_fs, 'attachments', filename))
            staged.append(os.path.join(event.page.page_name_fs, 'attachments', filename))

    if len(staged):
        # staged and commit
        repo = _get_repo(event)
        repo.stage(staged)
        ret = repo.do_commit(message='renamed ' + event.page.page_name_fs)
        request.theme.add_msg('Commited to the GIT repo [%s]' % str(ret), "info")


def handle_copied(event):
    """Updates Xapian index when a page is copied"""

    request = event.request

    if request.cfg.xapian_search:
        index = _get_index(request)
        if index and index.exists():
            index.update_item(event.page.page_name)


def handle_changed(event):
    if event.page.page_name_fs.startswith('_'):
        return

    request = event.request
    p = os.path.join(request.cfg.data_dir, 'pages', event.page.page_name_fs + EXT)

    with codecs.open(p, 'wb', 'utf8') as f:
        f.write(event.page.get_raw_body())

    repo = _get_repo(event)
    repo.stage([event.page.page_name_fs + EXT])
    ret = repo.do_commit(message='changed ' + event.page.page_name_fs)

    request.theme.add_msg('Commited to the GIT repo [%s]' % str(ret), "info")

def handle_deleted(event):

    if event.page.page_name_fs.startswith('_'):
        return

    request = event.request

    path = os.path.join(request.cfg.data_dir, 'pages', event.page.page_name_fs + EXT)

    try:
        os.remove(path)

        repo = _get_repo(event)
        repo.stage([event.page.page_name_fs + EXT])
        ret = repo.do_commit(message='renamed ' + event.page.page_name_fs)

        request.theme.add_msg('Commited to the GIT repo [%s]' % str(ret), "info")
    except OSError:
        request.theme.add_msg('Failed to git-commit [OSError]', "error")



def handle_attachment_change(event):
    """Updates Xapian index when attachment is added or removed"""

    if event.pagename.startswith('_'):
        return
    request = event.request
    filename = os.path.join(event.pagename, 'attachments', event.filename)
    filepath = os.path.join(event.request.cfg.data_dir, 'pages', filename)

    deleted = not os.path.exists(filepath)
    if deleted:
        message = u'deleted-attachment'
    else:
        message = u'new-attachment'

    repo = _get_repo(event)
    repo.stage([filename, filename.encode('utf8')])
    ret = repo.do_commit(message)

    request.theme.add_msg('[GIT] %s: %s [%s]' % (message, filename, str(ret)), "info")


def handle(event):

    if _get_repo(event) is None:
        return

    if isinstance(event, ev.PageRenamedEvent):
        handle_renamed(event)
    elif isinstance(event, ev.PageCopiedEvent):
        handle_copied(event)
    elif isinstance(event, (ev.PageChangedEvent, ev.TrivialPageChangedEvent)):
        handle_changed(event)
    elif isinstance(event, ev.PageDeletedEvent):
        handle_deleted(event)
    elif isinstance(event, (ev.FileAttachedEvent, ev.FileRemovedEvent)):
        handle_attachment_change(event)

