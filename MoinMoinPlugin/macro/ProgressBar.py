"""
MoinMoin - ProgressBar Macro
Generates a progress bar (in the form of a table)

@copyright: Pascal Bauermeister <pascal DOT bauermeister AT gmail DOT cm>
@license: GPL

Updates:

  * [v0.1.2] Tue Nov 21 20:54:59 CET 2006
    Fixed the bar length errors (was a cell padding issue), works also
    with IE. Thanks go to Thilo Pfennig for reporting the problem and
    testing the fix.

  * [v0.1.1] Sun Dec 18 21:31:17 CET 2005
    Changed table cell percentage markup.

  * [v0.1.0] Fri Dec 16 22:30:10 CET 2005
    Original version

----

The ProgressBar macro generates a table showing a progress indicator.

Usage:
  [[ ProgressBar ]]
  [[ ProgressBar (TABLEWIDTH TABLEFORMAT PROGRESS%) ]]
  [[ ProgressBar (TABLEWIDTH TABLEFORMAT CURRENT/STEPS) ]]
  [[ ProgressBar (TABLEWIDTH TABLEFORMAT STARTDATE,ENDDATE) ]]  

If no arguments are given, the usage is inserted in the HTML result.

Options:

  TABLEWIDTH (optional prefix)
    A wiki tablewidth attribute value between []'s
    Examples:
      [100%]
      [80px]

  TABLEFORMAT (optional prefix)
    A pair of wiki table attribute, to format the inactive and active cells.
    Examples:
      <bgcolor="black"><bgcolor="white">                   # black on white bar
      <tablewidth="90%" bgcolor="black"><bgcolor="white">  # same, 90% table

    A third format may be given for STARTDATE,ENDDATE usage

    By default: <tablewidth="100px"#808080><><#8080ff>

  PROGRESS
    Will display a table with two cells:
    - left: completion, taking PROGRESS % of the table width
    - right: remaining

    By default, the table is 100px wide.

  CURRENT/STEPS
    Will display a table with STEPS cells, CURRENT of which are active.

    By default, each cell is 0.5em wide, unless the table width is
    specified.

  STARTDATE,ENDDATE
    Will display a table with the number of days, with the cell
    representing today in active format and background in inactive format.

    If today is before STARTDATE, the left-most cell will be in the
    3rd format. If today is after ENDDATE the rightmost cell will be
    in the 3rd format.

    Dates are in this format: YYYY-MM-DD

    By default, each cell is 0.5em wide, unless the table width is
    specified.

Debugging
  Please prepend a '?' to the arguments.

Examples:
  [[ProgressBar(60%)]]
  [[ProgressBar(6/10)]]
  [[ProgressBar(2005-11-01,2006-01-06)]]

  [[ProgressBar([50%] 60%)]]
  [[ProgressBar([50px] 60%)]]
  [[ProgressBar([90%]<#8080ff><#808080> 6/10)]]
----
"""


# Imports
import time, re, StringIO
from MoinMoin import version
from MoinMoin.Page import Page
#from MoinMoin.parser import wiki

Dependencies = ["time"] # macro cannot be cached


class _Error (Exception):
    pass


def escape (str):
    return str.replace ('&','&amp;').replace ('<', '&lt;').replace ('>', '&gt;')

def usage (full = False):

    """Returns the interesting part of the module's doc"""

    if full:
        return __doc__
    else:
        rx = re.compile ("--$(.*)^--", re.DOTALL + re.MULTILINE)
        return rx.findall (__doc__) [0].strip ()


def s2t (s):
    return time.mktime (time.strptime (s, "%Y-%m-%d"))


def macro_ProgressBar(macro, text, args_re=None):

    try:     res = _execute (macro, text)
    except Exception, msg:
        return """
        <p><strong class="error">
        Error: macro ProgressBar: %s</strong> </p>
        """ % escape ("%s" % msg)
    return res


def _execute (macro, text):

    fmt = ['#808080','','#8080ff']
    width ="100px"
    nopad = False
    
    res = ""
    text = text.strip ()

    # help if empty text
    help = len (text) == 0

    # debug if starts with '?'
    if text.startswith ('?'):
        debug = True
        text = text [1:]
    else:
        debug = False
    orig_text = text

    # Formats
    try:
        # Table width
        if text.startswith ('['):
            pos = text.rfind (']')
            width = text [1:pos]
            text = text [pos+1:].strip ()
            nopad = True

        # Cells format
        if text.startswith ('<'):
            pos = text.rfind ('>')
            f = text [1:pos].split ('><')
            text = text [pos+1:].strip ()
            fmt [:len (f)] = f
    except:
        help = True

    # Show help
    if help:
        return """
        <p>
        <pre>%s</pre></p>
        """ % escape (usage (0))

    # Cell formatting utility
    def cell (txt, fmt, nopad=False):
        if nopad:
            padding = 'style="padding: 0.25em 1px 0.25em 0px;" '
        else:
            padding = 'style="padding: 0.25em 0.25em 0.25em 0.25em;" ' + fmt
        fmt = padding + fmt
        if len (txt) == 0:
            fmt = 'tableheight="0.75em" tablewidth="%s" ' % width + fmt
            txt = "||"
        if len (fmt): t = "<%s> ||" % fmt.strip ()
        else: t = " ||"
        return txt + t
        
    # Progress
    if text.endswith ('%'):
        for f in fmt [0] + ' %s' % text, fmt [1] :
            res = cell (res, f, True)
            if text.startswith ('100'): break

    # Current/Steps
    elif text.find ('/') > 0:
        cur, steps = map (int, text.split ('/'))
        for i in range (steps):
            res = cell (res, fmt [i>=cur], nopad)

    # Start/end date
    else:
        starts, ends = map (lambda s:s.strip (),  text.split (","))
        start, end = s2t (starts), s2t (ends)
        now = time.mktime (time.localtime ())

        duration = int ( (end-start) / 86400)
        progress = int ( (now-start) / 86400) -1
        pcent = int (90 / duration)

        for i in range (duration):
            if i == 0 and progress < 0:
                f = fmt [2]
            elif i == progress:
                f = fmt [0]
            else:
                f = fmt [1]
            res = cell (res, f, nopad)
                            
        if progress >= duration:
            res = cell (res, fmt [2], nopad)
        else:
            res = cell (res, fmt [1], nopad)

    # Output
    if debug:
        res = "{{{[[ProgressBar(%s)]]\n%s}}}\n%s" % (orig_text, res, res)
    return _format (res, macro.request, macro.formatter)


def _format (src_text, request, formatter):
    # parse the text (in wiki source format) and make HTML,
    # after diverting sys.stdout to a string
    ##str_out = StringIO.StringIO ()      # create str to collect output
    ##request.redirect (str_out)          # divert output to that string
    # parse this line
    ##wiki.Parser (src_text, request).format (formatter)
    ##request.redirect ()                 # restore output
    ##return str_out.getvalue ()          # return what was generated

    page = Page(request, '__progressbar')
    page.set_raw_body(src_text, 1)
    wikitext = request.redirectedOutput(page.send_page,
        content_only=1, content_id="__progressbar")
    return wikitext