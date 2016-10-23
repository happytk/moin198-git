#-*- coding: utf-8 -*-
"""
    MoinMoin - Photo Macro

    @copyright: 2013 Taewook Kang <rainyblue@gmail.com>
"""

Dependencies = ["pages"]

"""
-rwxrwxrwx    1 root     root         69773 Aug  7 21:18 SYNOPHOTO:THUMB_B.jpg
-rwxrwxrwx    1 root     root        147966 Aug  7 21:18 SYNOPHOTO:THUMB_L.jpg
-rwxrwxrwx    1 root     root         34124 Aug  7 21:18 SYNOPHOTO:THUMB_M.jpg
-rwxrwxrwx    1 root     root          7035 Aug  7 21:18 SYNOPHOTO:THUMB_S.jpg
-rwxrwxrwx    1 root     root        298435 Aug  7 21:18 SYNOPHOTO:THUMB_XL.jpg
"""

def macro_PhotoList(macro, alias='tst', size='S', limit=-1):
    if size not in ('B', 'L', 'M', 'S', 'XL'):
        return 'error. size can be B,L,M,S,XL.'
    # attach_dir = '/volume1/photo/webpub_%s/@eaDir' % alias
    attach_dir = '/volume1/photo/webpub_%s' % alias
    import glob
    import os
    rst = glob.glob(attach_dir + "/*.jpg")
    result = []
    rst.sort()
    rst.reverse()
    if limit >= 0:
        rst = rst[:limit]
    proc = False
    idx = 1
    result.append("<div style='clear:both;'>")
    for r in rst:
        filename = os.path.split(r)[1]
        photo_num = os.path.splitext(filename)[0] # int로 변환 필요가 있나?
        imagepath = '/moin_static195/webpub_%s/@eaDir/%s/SYNOPHOTO:THUMB_%s.jpg' % (alias, filename, size)
        if not proc:
            proc = os.path.isdir('/volume1/photo/webpub_%s/@eaDir/%s' % (alias, filename))
            isfile = os.path.isfile('/volume1/photo/webpub_%s/@eaDir/%s/SYNOPHOTO:THUMB_%s.jpg' % (alias, filename, size))
            if proc and isfile:
                result.append(u'''<table style="float:left; padding:0; margin:0;">
                    <tr><td style="font-size:11px; font-family:Tahoma; font-weight:bold;">#%s</td></tr>
                    <tr><td style="padding:0;"><img src="%s"/></td></tr>
                    </table>''' % (photo_num, imagepath))
            else:
            	result.append(u'''<table style="float:left; padding:0; margin:0;">
                    <tr><td style="font-size:11px; font-family:Tahoma; font-weight:bold;">#%s</td></tr>
                    <tr><td>현상중</td></tr>
                    </table>''' % (photo_num))
        else:
            #result.append('<img src="/moin_static195/webpub_%s/%s/SYNOPHOTO:THUMB_%s.jpg"/>' % (alias, filename, size))
            result.append(u'''<table style="float:left; padding:0; margin:0;">
                <tr><td style="font-size:11px; font-family:Tahoma; font-weight:bold;">#%s</td></tr>
                <tr><td style="padding:0;"><img src="%s"/></td></tr>
                </table>''' % (photo_num, imagepath))
        idx += 1
        if idx % 5 == 0:
            result.append('''<div style='clear:both;'></div>''')
    result.append("</div>")
    result.append("<div style='clear:both;'></div>")
    return u''.join(result)