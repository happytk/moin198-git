"""
    MoinMoin - AjaxLink Macro

    Usage: <<AjaxLink(url, txt, tagid, type=text|button, autostart=True|False)>>

    @copyright: 2011 happytk
    @license: GNU GPL
"""


def macro_AjaxLink(macro, page, txt=None, tagid=None, type=u'button', autostart=False, paramstring=''):

    ret = []

    if tagid == None:
        import hashlib
        import random
        import time
        m = hashlib.md5()
        m.update(str(random.getrandbits(128)))
        m.update(str(time.time()))
        m.update(page)
        tagid = m.hexdigest()
        tag_str = '<div id="%s" style="display:none;"></div>' % tagid
    else:
        tag_str = ''
    d = {}
    #d['url'] = url
    #d['tagid'] = tagid
    d['text'] = txt if txt != None else page
    if paramstring == '' or paramstring == None:
        paramstring = 'action=contentonly'
    else:
        if paramstring.find('action=') == -1:
            paramstring = 'action=contentonly&' + paramstring
    d['cmd'] = "proc_http_param('%s/%s', '%s', document.getElementById('%s'));" % (macro.request.script_root, page, paramstring, tagid)
    d['tagid'] = tagid

    if type == u'button':
        lnk_str = '''<input type="button" 
                onclick="%(cmd)s" id="btn%(tagid)s"
                value="%(text)s">''' % d
    else: #if type == u'text':
        lnk_str = '''<a href="#" 
                onclick="%(cmd)s" id="btn%(tagid)s">%(text)s</a>''' % d

    if not autostart:
        ret.append(lnk_str)
    ret.append(tag_str)

    if autostart:
        ret.append('''<script type="text/javascript">
<!--
%s
//-->
</script>''' % d['cmd'])


    return ''.join(ret)


