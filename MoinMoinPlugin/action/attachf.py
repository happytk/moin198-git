#-*-encoding:utf-8-*-
import os
import zipfile
import mimetypes
import jinja2
from MoinMoin.Page import Page
from MoinMoin import wikiutil

# action_name = __name__.split('.')[-1]

def getAttachDir(request, pagename, create=0):
    """ Get directory where attachments for page `pagename` are stored. """
    if request.page and pagename == request.page.page_name:
        page = request.page # reusing existing page obj is faster
    else:
        page = Page(request, pagename)
    return page.getPagePath("attachments", check_create=create)

def _get_files(request, pagename, attach_dir):
    if os.path.isdir(attach_dir):
        files = [fn.decode(request.cfg.attachment_charset) for fn in os.listdir(attach_dir)]
    else:
        files = []
    return files


def get_action(request, filename, do):
    # generic_do_mapping = {
    #     # do -> action
    #     'get': action_name,
    #     'view': action_name,
    #     'move': action_name,
    #     'del': action_name,
    #     'unzip': action_name,
    #     'install': action_name,
    #     'upload_form': action_name,
    # }
    # basename, ext = os.path.splitext(filename)
    # do_mapping = request.cfg.extensions_mapping.get(ext, {})
    # action = do_mapping.get(do, None)
    # if action is None:
    #     # we have no special support for this,
    #     # look up whether we have generic support:
    #     action = generic_do_mapping.get(do, None)
    # return action
    return 'AttachFile'

def getAttachUrl(pagename, filename, request, addts=0, do='get'):
    """ Get URL that points to attachment `filename` of page `pagename`.
        For upload url, call with do='upload_form'.
        Returns the URL to do the specified "do" action or None,
        if this action is not supported.
    """
    action = get_action(request, filename, do)
    if action:
        args = dict(action=action, do=do, target=filename)
        if do not in ['get', 'view', # harmless
                      'modify', # just renders the applet html, which has own ticket
                      'move', # renders rename form, which has own ticket
            ]:
            # create a ticket for the not so harmless operations
            # we need action= here because the current action (e.g. "show" page
            # with a macro AttachList) may not be the linked-to action, e.g.
            # "AttachFile". Also, AttachList can list attachments of another page,
            # thus we need to give pagename= also.
            args['ticket'] = wikiutil.createTicket(request,
                                                   pagename=pagename, action=action_name)
        url = request.href(pagename, **args)
        return url

def send_attachlist_select(pagename, request):
    html = [u'''
<select class="attachment_select" style="width: 32%">
  <option value="3620194" selected="selected">첨부파일붙여넣기</option>
</select>
<select class="pagename_select" style="width: 32%">
  <option value="3620194" selected="selected">문서이름링크하기</option>
</select>
<select class="recentchanges_select" style="width: 32%">
  <option value="3620194" selected="selected">문서이름링크하기(최근변경)</option>
</select>
'''
    ]
    return request.write(''.join(html))


def send_attachlist(pagename, request):
    files = _get_files(request, pagename)
    fmt = request.formatter
    _ = request.getText
    readonly = False
    attach_dir = getAttachDir(request, pagename)

    html = []
    if files:

        label_del = _("del")
        label_move = _("move")
        label_get = _("get")
        label_edit = _("edit")
        label_view = _("view")
        label_unzip = _("unzip")
        label_install = _("install")

        may_read = request.user.may.read(pagename)
        may_write = request.user.may.write(pagename)
        may_delete = request.user.may.delete(pagename)

        html.append(fmt.bullet_list(1, id='att_list'))
        for file in files:
            mt = wikiutil.MimeType(filename=file)
            fullpath = os.path.join(attach_dir, file).encode(request.cfg.attachment_charset)
            st = os.stat(fullpath)
            base, ext = os.path.splitext(file)
            parmdict = {'file': wikiutil.escape(file),
                        'fsize': "%.1f" % (float(st.st_size) / 1024),
                        'fmtime': request.user.getFormattedDateTime(st.st_mtime),
                       }

            links = []
            # if may_delete and not readonly:
            #     links.append(fmt.url(1, getAttachUrl(pagename, file, request, do='del')) +
            #                  fmt.text(label_del) +
            #                  fmt.url(0))

            # if may_delete and not readonly:
            #     links.append(fmt.url(1, getAttachUrl(pagename, file, request, do='move')) +
            #                  fmt.text(label_move) +
            #                  fmt.url(0))

            # links.append(fmt.url(1, getAttachUrl(pagename, file, request)) +
            #              fmt.text(label_get) +
            #              fmt.url(0))

            # links.append(fmt.url(1, getAttachUrl(pagename, file, request, do='view')) +
            #              fmt.text(label_view) +
            #              fmt.url(0))

            # if may_write and not readonly:
            #     edit_url = getAttachUrl(pagename, file, request, do='modify')
            #     if edit_url:
            #         links.append(fmt.url(1, edit_url) +
            #                      fmt.text(label_edit) +
            #                      fmt.url(0))

            # try:
            #     is_zipfile = zipfile.is_zipfile(fullpath)
            #     if is_zipfile and not readonly:
            #         is_package = packages.ZipPackage(request, fullpath).isPackage()
            #         if is_package and request.user.isSuperUser():
            #             links.append(fmt.url(1, getAttachUrl(pagename, file, request, do='install')) +
            #                          fmt.text(label_install) +
            #                          fmt.url(0))
            #         elif (not is_package and mt.minor == 'zip' and
            #               may_read and may_write and may_delete):
            #             links.append(fmt.url(1, getAttachUrl(pagename, file, request, do='unzip')) +
            #                          fmt.text(label_unzip) +
            #                          fmt.url(0))
            # except RuntimeError:
            #     # We don't want to crash with a traceback here (an exception
            #     # here could be caused by an uploaded defective zip file - and
            #     # if we crash here, the user does not get a UI to remove the
            #     # defective zip file again).
            #     # RuntimeError is raised by zipfile stdlib module in case of
            #     # problems (like inconsistent slash and backslash usage in the
            #     # archive).
            #     logging.exception("An exception within zip file attachment handling occurred:")

            html.append(fmt.listitem(1))
            # html.append("[%s]" % "&nbsp;| ".join(links))
            html.append(u"<div>")
            html.append(u"<span class='att_info'>(%(fmtime)s, %(fsize)s KB)</span>" % parmdict)
            html.append(u"<span style='background-color:yellow;'>{{attachment:%(file)s}}</span>" % parmdict)
            # html.append(u"<button onclick='insert_textarea(\"{{attachment:%(file)s}}\");'>본문에붙여넣기</button>" % parmdict)
            html.append(u"</div>")
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.gif'):
                html.append("<div><img src='%s' class='attachment' style='max-width:300px'></div>" % getAttachUrl(pagename, file, request))
            html.append(fmt.listitem(0))
        html.append(fmt.bullet_list(0))


    request.write(''.join(html))



def send_uploadform(pagename, request):

    path = getAttachDir(request, pagename)
    request.write('''
<noscript>Note: You must have javascript enabled in order to upload and
dynamically view new images.</noscript>
  <h2>Select a file(or a image)</h2>
  <p id="status"></p>
  <div id="progressbar"></div>
  <input id="file" type="file" multiple/>
  <div id="drop">or drop file(image) here</div>
<script>
  $('#drop').bind('drop', function(e) {
      handle_hover(e);
      if (e.originalEvent.dataTransfer.files.length < 1) {
          return;
      }
      //alert(e.originalEvent.dataTransfer.files[0].name);
      var v;
      for (v = 0; v<e.originalEvent.dataTransfer.files.length; v++) {
        file_select_handler(e.originalEvent.dataTransfer.files[v], '%s');
      }
  }).bind('dragenter dragleave dragover', handle_hover);
  $('#file').change(function(e){
      //alert(e.target.files[0].name);
      var v;
      for (v = 0; v<e.target.files.length; v++) {
        file_select_handler(e.target.files[v], '%s');
      }
      e.target.value = '';
  });
  // sse();

</script>
''' % (path, path))


def get_attachments(pagename, request, attach_dir):
    files = _get_files(request, pagename, attach_dir)

    if files:
        lst = []
        for file in files:
            mt = wikiutil.MimeType(filename=file)
            fullpath = os.path.join(attach_dir, file).encode(request.cfg.attachment_charset)
            st = os.stat(fullpath)
            base, ext = os.path.splitext(file)
            parmdict = {'file': wikiutil.escape(file),
                        'fsize': "%.1f" % (float(st.st_size) / 1024),
                        'fmtime': request.user.getFormattedDateTime(st.st_mtime),
                        'ext': ext,
                        'url': getAttachUrl(pagename, file, request),
                       }
            lst.append(parmdict)
        lst = sorted(lst, key=lambda x:x['fmtime'], reverse=True)
        return lst
    else:
          return []

def send_body(pagename, request, editor=False):
    _ = request.getText

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'attachf.html')
    template = jinja2.Template(open(path, 'r').read().decode('utf8'))

    attach_dir = getAttachDir(request, pagename)
    files = get_attachments(pagename, request, attach_dir)
    request.write(template.render(editor=editor, pagename=pagename, may_write=request.user.may.write(pagename),\
                  attachment_path=attach_dir, files=files, script_root=request.script_root,\
                  static_url=request.cfg.url_prefix_static))

def execute(pagename, request):
    """ Main dispatcher for the 'AttachFile' action. """
    _ = request.getText

    # Use user interface language for this generated page
    request.setContentLanguage(request.lang)
    # request.theme.add_msg(msg, "dialog")
    request.theme.send_title(_('Attachments for "%(pagename)s"') % {'pagename': pagename}, pagename=pagename)
    send_body(pagename, request)
    request.theme.send_footer(pagename)
    request.theme.send_closing_html()

'''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>
  Examples - Select2
</title>

<script type="text/javascript" src="vendor/js/jquery.min.js"></script>
<script type="text/javascript" src="dist/js/select2.full.js"></script>
<script type="text/javascript" src="vendor/js/bootstrap.min.js"></script>
<script type="text/javascript" src="vendor/js/prettify.min.js"></script>

<link href="vendor/css/bootstrap.min.css" type="text/css" rel="stylesheet" />
<link href="dist/css/select2.min.css" type="text/css" rel="stylesheet" />

<link href="vendor/css/font-awesome.min.css" type="text/css" rel="stylesheet" />
<link href="vendor/css/prettify.css" type="text/css" rel="stylesheet" />

<style type="text/css">
  body { font-size: 16px; }
  footer { background-color: #eee; margin-top: 1em; padding: 1em; text-align: center; }
  .navbar-inverse .navbar-brand { color: #fff; }
</style>

    </head>
    <body>
        <header class="navbar navbar-inverse navbar-static-top" id="top" role="banner">
  <div class="container">
    <div class="navbar-header">
      <button class="navbar-toggle collapsed" type="button" data-toggle="collapse" data-target=".select2-navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a href="./" class="navbar-brand">Select2</a>
    </div>

    <nav class="collapse navbar-collapse select2-navbar-collapse" role="navigation">
      <ul class="nav navbar-nav">
        <li>
          <a href="./">Home</a>
        </li>
        <li class="active">
          <a href="./examples.html">Examples</a>
        </li>
        <li>
          <a href="./options.html">Options</a>
        </li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown">
            Topics
            <span class="caret"></span>
          </a>
          <ul class="dropdown-menu">
            <li>
              <a href="https://github.com/select2/select2/releases">
                Release notes
              </a>
            </li>
            <li>
              <a href="./announcements-4.0.html">4.0 Announcement</a>
            </li>
          </ul>
        </li>
        <li>
          <a href="./community.html">Community</a>
        </li>
      </ul>

      <ul class="nav navbar-nav navbar-right">
        <li>
          <a href="https://github.com/select2/select2">
            <i class="fa fa-github"></i>
            GitHub
          </a>
        </li>
      </ul>
    </nav>
  </div>
</header>


        <script type="text/javascript" src="vendor/js/placeholders.jquery.min.js"></script>
<script type="text/javascript" src="dist/js/i18n/es.js"></script>

<style type="text/css">
.img-flag {
  height: 15px;
  width: 18px;
}
</style>

<div class="container">
  <section id="basic" class="row">
    <div class="col-md-4">
      <h1>The basics</h1>

      <p>
        Select2 can take a regular select box like this...
      </p>

      <p>
        <select class="js-states form-control"></select>
      </p>

      <p>
        and turn it into this...
      </p>

      <p>
        <select class="js-example-basic-single js-states form-control"></select>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre class="code" data-fill-from=".js-code-basic"></pre>

<script type="text/x-example-code" class="js-code-basic">
$(document).ready(function() {
  $(".js-example-basic-single").select2();
});

<select class="js-example-basic-single">
  <option value="AL">Alabama</option>
    ...
  <option value="WY">Wyoming</option>
</select>
</script>
    </div>
  </section>

  <section id="multiple" class="row">
    <div class="col-md-4">
      <h1>Multiple select boxes</h1>

      <p>
        Select2 also supports multi-value select boxes. The select below is declared with the <code>multiple</code> attribute.
      </p>

      <p>
        <select class="js-example-basic-multiple js-states form-control" multiple="multiple"></select>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-multiple"></pre>

<script type="text/x-example-code" class="js-code-multiple">
$(".js-example-basic-multiple").select2();

<select class="js-example-basic-multiple" multiple="multiple">
  <option value="AL">Alabama</option>
    ...
  <option value="WY">Wyoming</option>
</select>
</script>
    </div>
  </section>

  <section id="placeholders" class="row">
    <div class="col-md-4">
      <h1>Placeholders</h1>

      <p>
        A placeholder value can be defined and will be displayed until a selection is made.
      </p>

      <p>
        <select class="js-example-placeholder-single js-states form-control">
          <option></option>
        </select>
      </p>

      <p>
        Select2 uses the <code>placeholder</code> attribute on multiple select
        boxes, which requires IE 10+. You can support it in older versions with
        <a href="https://github.com/jamesallardice/Placeholders.js">the Placeholders.js polyfill</a>.
      </p>

      <p>
        <select class="js-example-placeholder-multiple js-states form-control" multiple="multiple"></select>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-placeholder"></pre>

<script type="text/javascript" class="js-code-placeholder">
$(".js-example-placeholder-single").select2({
  placeholder: "Select a state",
  allowClear: true
});

$(".js-example-placeholder-multiple").select2({
  placeholder: "Select a state"
});
</script>
    </div>
  </section>

  <section id="templating" class="row">
    <div class="col-md-4">
      <h1>Templating</h1>

      <p>
        Various display options of the Select2 component can be changed
      </p>

      <p>
        <select class="js-example-templating js-states form-control"></select>
      </p>

      <p>
        You can access the <code>&lt;option&gt;</code> element
        (or <code>&lt;optgroup&gt;</code>) and any attributes on those elements
        using <code>.element</code>.
      </p>

      <p>
        Templating is primarily controlled by the
        <a href="options.html#templateResult"><code>templateResult</code></a>
        and <a href="options.html#templateSelection"><code>templateSelection</code></a>
        options.
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-templating"></pre>

<script type="text/x-example-code" class="js-code-templating">
function formatState (state) {
  if (!state.id) { return state.text; }
  var $state = $(
    '<span><img src="vendor/images/flags/' + state.element.value.toLowerCase() + '.png" class="img-flag" /> ' + state.text + '</span>'
  );
  return $state;
};

$(".js-example-templating").select2({
  templateResult: formatState
});
</script>
    </div>
  </section>

  <section id="data-array" class="row">
    <div class="col-md-4">
      <h1>Loading array data</h1>

      <p>
        Select2 provides a way to load the data from a local array.
      </p>

      <p>
        <select class="js-example-data-array form-control"></select>
      </p>

      <p>
        You can provide initial selections with array data by providing the
        option tag for the selected values, similar to how it would be done for
        a standard select.
      </p>

      <p>
        <select class="js-example-data-array-selected form-control">
          <option value="2" selected="selected">duplicate</option>
        </select>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-data-array"></pre>

<script type="text/x-example-code" class="js-code-data-array">
var data = [{ id: 0, text: 'enhancement' }, { id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }];

$(".js-example-data-array").select2({
  data: data
})

$(".js-example-data-array-selected").select2({
  data: data
})

<select class="js-example-data-array-selected"></select>

<select class="js-example-data-array-selected">
  <option value="2" selected="selected">duplicate</option>
</select>
</script>
    </div>
  </section>

  <section id="data-ajax" class="row">
    <div class="col-md-12">
      <h1>Loading remote data</h1>

      <p>
        Select2 comes with AJAX support built in, using jQuery's AJAX methods.
        In this example, we can search for repositories using GitHub's API.
      </p>

      <p>
        <select class="js-example-data-ajax form-control">
          <option value="3620194" selected="selected">select2/select2</option>
        </select>
      </p>

      <p>
        When using Select2 with remote data, the HTML required for the
        <code>select</code> is the same as any other Select2. If you need to
        provide default selections, you just need to include an
        <code>option</code> for each selection that contains the value and text
        that should be displayed.
      </p>

      <pre data-fill-from=".js-code-data-ajax-html"></pre>

      <p>
        You can configure how Select2 searches for remote data using the
        <code>ajax</code> option. More information on the individual options
        that Select2 handles can be found in the
        <a href="options.html#ajax">options documentation for <code>ajax</code></a>.
      </p>

      <pre data-fill-from=".js-code-data-ajax"></pre>

      <p>
        Select2 will pass any options in the <code>ajax</code> object to
        jQuery's <code>$.ajax</code> function, or the <code>transport</code>
        function you specify.
      </p>

<script type="text/x-example-code" class="js-code-data-ajax">
$(".js-data-example-ajax").select2({
  ajax: {
    url: "https://api.github.com/search/repositories",
    dataType: 'json',
    delay: 250,
    data: function (params) {
      return {
        q: params.term, // search term
        page: params.page
      };
    },
    processResults: function (data, page) {
      // parse the results into the format expected by Select2.
      // since we are using custom formatting functions we do not need to
      // alter the remote JSON data
      return {
        results: data.items
      };
    },
    cache: true
  },
  escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
  minimumInputLength: 1,
  templateResult: formatRepo, // omitted for brevity, see the source of this page
  templateSelection: formatRepoSelection // omitted for brevity, see the source of this page
});
</script>

<script type="text/x-example-code" class="js-code-data-ajax-html">
<select class="js-data-example-ajax">
  <option value="3620194" selected="selected">select2/select2</option>
</select>
</script>
    </div>
  </section>

  <section id="responsive" class="row">
    <div class="col-md-4">
      <h1>Responsive design - Percent width</h1>

      <p>
        Select2's width can be set to a percentage of its parent to support
        responsive design. The two Select2 boxes below are styled to 50% and 75%
        width respectively.
      </p>

      <p>
        <select class="js-example-responsive js-states" style="width: 50%"></select>
      </p>

      <p>
        <select class="js-example-responsive js-states" multiple="multiple" style="width: 75%"></select>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-responsive"></pre>

      <div class="alert alert-warning">
        Select2 will do its best to resolve the percent width specified via a
        css class, but it is not always possible. The best way to ensure that
        Select2 is using a percent based width is to inline the
        <code>style</code> declaration into the tag.
      </div>

<script type="text/x-example-code" class="js-code-responsive">
<select class="js-example-responsive" style="width: 50%"></select>
<select class="js-example-responsive" multiple="multiple" style="width: 75%"></select>
</script>
    </div>
  </section>

  <section id="disabled" class="row">
    <div class="col-md-4">
      <h1>Disabled mode</h1>

      <p>
        Select2 will response the <code>disabled</code> attribute on
        <code>&lt;select&gt;</code> elements. You can also initialize Select2
        with <code>disabled: true</code> to get the same effect.
      </p>

      <p>
        <select class="js-example-disabled js-states form-control" disabled="disabled"></select>
      </p>

      <p>
        <select class="js-example-disabled-multi js-states form-control" multiple="multiple" disabled="disabled"></select>
      </p>

      <p>
        <button class="js-programmatic-enable btn btn-primary">
          Enable
        </button>
        <button class="js-programmatic-disable btn btn-warning">
          Disable
        </button>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-disabled"></pre>

<script type="text/javascript" class="js-code-disabled">
$(".js-programmatic-enable").on("click", function () {
  $(".js-example-disabled").prop("disabled", false);
  $(".js-example-disabled-multi").prop("disabled", false);
});

$(".js-programmatic-disable").on("click", function () {
  $(".js-example-disabled").prop("disabled", true);
  $(".js-example-disabled-multi").prop("disabled", true);
});
</script>
    </div>
  </section>

  <section id="disabled-results" class="row">
    <div class="col-md-4">
      <h1>Disabled results</h1>

      <p>
        Select2 will correctly handled disabled results, both with data coming
        from a standard select (when the <code>disabled</code> attribute is set)
        and from remote sources, where the object has
        <code>disabled: true</code> set.
      </p>

      <p>
        <select class="js-example-disabled-results form-control">
          <option value="one">First</option>
          <option value="two" disabled="disabled">Second (disabled)</option>
          <option value="three">Third</option>
        </select>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-disabled-results"></pre>

<script type="text/x-example-code" class="js-code-disabled-results">
<select class="js-example-disabled-results">
  <option value="one">First</option>
  <option value="two" disabled="disabled">Second (disabled)</option>
  <option value="three">Third</option>
</select>
</script>
    </div>
  </section>

  <section id="programmatic" class="row">
    <div class="col-md-4">
      <h1>Programmatic access</h1>

      <p>
        Select2 supports methods that allow programmatic control of the
        component.
      </p>

      <p>
        <button class="js-programmatic-set-val btn btn-primary">
          Set to California
        </button>

        <button class="js-programmatic-open btn btn-success">
          Open
        </button>

        <button class="js-programmatic-close btn btn-success">
          Close
        </button>

        <button class="js-programmatic-init btn btn-danger">
          Init
        </button>

        <button class="js-programmatic-destroy btn btn-danger">
          Destroy
        </button>
      </p>

      <p>
        <select class="js-example-programmatic js-states form-control"></select>
      </p>

      <p>
        <button class="js-programmatic-multi-set-val btn btn-primary">
          Set to California and Alabama
        </button>

        <button class="js-programmatic-multi-clear btn btn-primary">
          Clear
        </button>
      </p>

      <p>
        <select class="js-example-programmatic-multi js-states form-control" multiple="multiple"></select>
      </p>

    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-programmatic"></pre>

<script type="text/javascript" class="js-code-programmatic">
var $example = $(".js-example-programmatic");
var $exampleMulti = $(".js-example-programmatic-multi");

$(".js-programmatic-set-val").on("click", function () { $example.val("CA").trigger("change"); });

$(".js-programmatic-open").on("click", function () { $example.select2("open"); });
$(".js-programmatic-close").on("click", function () { $example.select2("close"); });

$(".js-programmatic-init").on("click", function () { $example.select2(); });
$(".js-programmatic-destroy").on("click", function () { $example.select2("destroy"); });

$(".js-programmatic-multi-set-val").on("click", function () { $exampleMulti.val(["CA", "AL"]).trigger("change"); });
$(".js-programmatic-multi-clear").on("click", function () { $exampleMulti.val(null).trigger("change"); });
</script>
    </div>
  </section>

  <section id="multiple-max" class="row">
    <div class="col-md-4">
      <h1>Limiting the number of selections</h1>
      <p>Select2 multi-value select boxes can set restrictions regarding the maximum number of options selected.
        The select below is declared with the <code>multiple</code> attribute with <code>maxSelectionLength</code> in the select2 options</p>

      <p>
        <select class="js-example-basic-multiple-limit js-states form-control" multiple="multiple"></select>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-multiple-limit"></pre>

<script type="text/x-example-code" class="js-code-multiple-limit">
$(".js-example-basic-multiple-limit").select2({
  maximumSelectionLength: 2
});
</script>
    </div>
  </section>

  <section id="hide-search" class="row">
    <div class="col-md-4">
      <h1>Hiding the search box</h1>

      <p>
        Select2 allows you to hide the search box depending on the numbeer of
        options which are displayed. In this example, we use the value
        <code>Infinity</code> to tell Select2 to never display the search box.
      </p>

      <p>
        <select class="js-example-basic-hide-search js-states form-control"></select>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-hide-search"></pre>

<script type="text/x-example-code" class="js-code-hide-search">
$(".js-example-basic-hide-search").select2({
  minimumResultsForSearch: Infinity
});
</script>
    </div>
  </section>

  <section id="events" class="row">
    <div class="col-md-4">
      <h1>Events</h1>

      <p>
        Select2 will trigger some events on the original select element,
        allowing you to integrate it with other components. You can find more
        information on events
        <a href="options.html#events">on the options page</a>.
      </p>

      <p>
        <select class="js-states js-example-events form-control"></select>
      </p>

      <p>
        <select class="js-states js-example-events form-control" multiple="multiple"></select>
      </p>

      <p>
        <code>change</code> is fired whenever an option is selected or removed.
      </p>

      <p>
        <code>select2:open</code> is fired whenever the dropdown is opened.
        <code>select2:opening</code> is fired before this and can be prevented.
      </p>

      <p>
        <code>select2:close</code> is fired whenever the dropdown is closed.
        <code>select2:closing</code> is fired before this and can be prevented.
      </p>

      <p>
        <code>select2:select</code> is fired whenever a result is selected.
        <code>select2:selecting</code> is fired before this and can be prevented.
      </p>

      <p>
        <code>select2:unselect</code> is fired whenever a result is unselected.
        <code>select2:unselecting</code> is fired before this and can be prevented.
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <ul class="js-event-log"></ul>

      <pre data-fill-from=".js-code-events"></pre>

<script type="text/javascript" class="js-code-events">
var $eventLog = $(".js-event-log");
var $eventSelect = $(".js-example-events");

$eventSelect.on("select2:open", function (e) { log("select2:open", e); });
$eventSelect.on("select2:close", function (e) { log("select2:close", e); });
$eventSelect.on("select2:select", function (e) { log("select2:select", e); });
$eventSelect.on("select2:unselect", function (e) { log("select2:unselect", e); });

$eventSelect.on("change", function (e) { log("change"); });

function log (name, evt) {
  if (!evt) {
    var args = "{}";
  } else {
    var args = JSON.stringify(evt.params, function (key, value) {
      if (value && value.nodeName) return "[DOM node]";
      if (value instanceof $.Event) return "[$.Event]";
      return value;
    });
  }
  var $e = $("<li>" + name + " -> " + args + "</li>");
  $eventLog.append($e);
  $e.animate({ opacity: 1 }, 10000, 'linear', function () {
    $e.animate({ opacity: 0 }, 2000, 'linear', function () {
      $e.remove();
    });
  });
}
</script>
    </div>
  </section>

  <section id="tags" class="row">
    <div class="col-md-4">
      <h1>Tagging support</h1>

      <p>
        Select2 can be used to quickly set up fields used for tagging.
      </p>

      <p>
        <select class="js-example-tags form-control" multiple="multiple">
          <option selected="selected">orange</option>
          <option>white</option>
          <option selected="selected">purple</option>
        </select>
      </p>

      <p>
        Note that when tagging is enabled the user can select from pre-existing
        options or create a new tag by picking the first choice, which is what
        the user has typed into the search box so far.
      </p>

    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-tags"></pre>

<script type="text/x-example-code" class="js-code-tags">
$(".js-example-tags").select2({
  tags: true
})
</script>
    </div>
  </section>

  <section id="tokenizer" class="row">
    <div class="col-md-4">
      <h1>Automatic tokenization</h1>

      <p>
        Select2 supports ability to add choices automatically as the user is
        typing into the search field. Try typing in the search field below and
        entering a space or a comma.
      </p>

      <p>
        <select class="js-example-tokenizer form-control" multiple="multiple">
          <option>red</option>
          <option>blue</option>
          <option>green</option>
        </select>
      </p>

      <p>
        The separators that should be used when tokenizing can be specified
        using the <a href="options.html#tokenSeparators">tokenSeparators</a>
        options.
      </p>

    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-tokenizer"></pre>

<script type="text/x-example-code" class="js-code-tokenizer">
$(".js-example-tokenizer").select2({
  tags: true,
  tokenSeparators: [',', ' ']
})
</script>
    </div>
  </section>

  <section id="matcher" class="row">
    <div class="col-md-4">
      <h1>Custom matcher</h1>

      <p>
        Unlike other dropdowns on this page, this one matches options only if
        the term appears in the beginning of the string as opposed to anywhere:
      </p>

      <p>
        <select class="js-example-matcher-start js-states form-control"></select>
      </p>

      <p>
        This custom matcher uses a
        <a href="options.html#compat-matcher">compatibility module</a> that is
        only bundled in the
        <a href="index.html#builds-full">full version of Select2</a>. You also
        have the option of using a
        <a href="options.html#matcher">more complex matcher</a>.
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-matcher-start"></pre>

<script type="text/x-example-code" class="js-code-matcher-start">
function matchStart (term, text) {
  if (text.toUpperCase().indexOf(term.toUpperCase()) == 0) {
    return true;
  }

  return false;
}

$.fn.select2.amd.require(['select2/compat/matcher'], function (oldMatcher) {
  $(".js-example-matcher-start").select2({
    matcher: oldMatcher(matchStart)
  })
});
</script>
    </div>
  </section>

  <section id="diacritics" class="row">
    <div class="col-md-4">
      <h1>Diacritics support</h1>

      <p>
        Select2's default matcher will ignore diacritics, making it easier for
        users to filter results in international selects. Type "aero" into the
        select below.
      </p>

      <p>
        <select class="js-example-diacritics form-control">
          <option>Aeróbics</option>
          <option>Aeróbics en Agua</option>
          <option>Aerografía</option>
          <option>Aeromodelaje</option>
          <option>Águilas</option>
          <option>Ajedrez</option>
          <option>Ala Delta</option>
          <option>Álbumes de Música</option>
          <option>Alusivos</option>
          <option>Análisis de Escritura a Mano</option>
        </select>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-diacritics"></pre>

<script type="text/x-example-code" class="js-code-diacritics">
$(".js-example-diacritics").select2();
</script>
    </div>
  </section>

  <section id="language" class="row">
    <div class="col-md-4">
      <h1>Multiple languages</h1>

      <p>
        Select2 supports displaying the messages in different languages, as well
        as providing your own
        <a href="options.html#language">custom messages</a>
        that can be displayed.
      </p>

      <p>
        <select class="js-example-language js-states form-control">
        </select>
      </p>

      <p>
        The language does not have to be defined when Select2 is being
        initialized, but instead can be defined in the <code>[lang]</code>
        attribute of any parent elements as <code>[lang="es"]</code>.
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-language"></pre>

<script type="text/x-example-code" class="js-code-language">
$(".js-example-language").select2({
  language: "es"
});
</script>
    </div>
  </section>

  <section id="themes" class="row">
    <div class="col-md-4">
      <h1>Theme support</h1>

      <p>
        Select2 supports custom themes using the
        <a href="options.html#theme">theme option</a>
        so you can style Select2 to match the rest of your application.
      </p>

      <p>
        <select class="js-example-theme-single js-states form-control">
        </select>
      </p>

      <p>
        These are using the <code>classic</code> theme, which matches the old
        look of Select2.
      </p>

      <p>
        <select class="js-example-theme-multiple js-states form-control" multiple="multiple"></select>
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-theme"></pre>

<script type="text/x-example-code" class="js-code-theme">
$(".js-example-theme-single").select2({
  theme: "classic"
});

$(".js-example-theme-multiple").select2({
  theme: "classic"
});
</script>
    </div>
  </section>

  <section id="rtl" class="row">
    <div class="col-md-4">
      <h1>RTL support</h1>

      <p>
        Select2 will work on RTL websites if the <code>dir</code> attribute is
        set on the <code>&lt;select&gt;</code> or any parents of it.
      </p>

      <p>
        <select class="js-example-rtl js-states form-control" dir="rtl"></select>
      </p>

      <p>
        You can also use initialize Select2 with <code>dir: "rtl"</code> set.
      </p>
    </div>
    <div class="col-md-8">
      <h2>Example code</h2>

      <pre data-fill-from=".js-code-rtl"></pre>

<script type="text/x-example-code" class="js-code-rtl">
$(".js-example-rtl").select2({
  dir: "rtl"
});
</script>
    </div>
  </section>
</div>

<select class="js-source-states" style="display: none;">
  <optgroup label="Alaskan/Hawaiian Time Zone">
    <option value="AK">Alaska</option>
    <option value="HI">Hawaii</option>
  </optgroup>
  <optgroup label="Pacific Time Zone">
    <option value="CA">California</option>
    <option value="NV">Nevada</option>
    <option value="OR">Oregon</option>
    <option value="WA">Washington</option>
  </optgroup>
  <optgroup label="Mountain Time Zone">
    <option value="AZ">Arizona</option>
    <option value="CO">Colorado</option>
    <option value="ID">Idaho</option>
    <option value="MT">Montana</option>
    <option value="NE">Nebraska</option>
    <option value="NM">New Mexico</option>
    <option value="ND">North Dakota</option>
    <option value="UT">Utah</option>
    <option value="WY">Wyoming</option>
  </optgroup>
  <optgroup label="Central Time Zone">
    <option value="AL">Alabama</option>
    <option value="AR">Arkansas</option>
    <option value="IL">Illinois</option>
    <option value="IA">Iowa</option>
    <option value="KS">Kansas</option>
    <option value="KY">Kentucky</option>
    <option value="LA">Louisiana</option>
    <option value="MN">Minnesota</option>
    <option value="MS">Mississippi</option>
    <option value="MO">Missouri</option>
    <option value="OK">Oklahoma</option>
    <option value="SD">South Dakota</option>
    <option value="TX">Texas</option>
    <option value="TN">Tennessee</option>
    <option value="WI">Wisconsin</option>
  </optgroup>
  <optgroup label="Eastern Time Zone">
    <option value="CT">Connecticut</option>
    <option value="DE">Delaware</option>
    <option value="FL">Florida</option>
    <option value="GA">Georgia</option>
    <option value="IN">Indiana</option>
    <option value="ME">Maine</option>
    <option value="MD">Maryland</option>
    <option value="MA">Massachusetts</option>
    <option value="MI">Michigan</option>
    <option value="NH">New Hampshire</option>
    <option value="NJ">New Jersey</option>
    <option value="NY">New York</option>
    <option value="NC">North Carolina</option>
    <option value="OH">Ohio</option>
    <option value="PA">Pennsylvania</option>
    <option value="RI">Rhode Island</option>
    <option value="SC">South Carolina</option>
    <option value="VT">Vermont</option>
    <option value="VA">Virginia</option>
    <option value="WV">West Virginia</option>
  </optgroup>
</select>

<script type="text/javascript">
var $states = $(".js-source-states");
var statesOptions = $states.html();
$states.remove();

$(".js-states").append(statesOptions);

$("[data-fill-from]").each(function () {
  var $this = $(this);

  var codeContainer = $this.data("fill-from");
  var $container = $(codeContainer);

  var code = $.trim($container.html());

  $this.text(code);
  $this.addClass("prettyprint linenums");
});

prettyPrint();

$.fn.select2.amd.require(
    ["select2/core", "select2/utils", "select2/compat/matcher"],
    function (Select2, Utils, oldMatcher) {
  var $basicSingle = $(".js-example-basic-single");
  var $basicMultiple = $(".js-example-basic-multiple");
  var $limitMultiple = $(".js-example-basic-multiple-limit");

  var $dataArray = $(".js-example-data-array");
  var $dataArraySelected = $(".js-example-data-array-selected");

  var data = [{ id: 0, text: 'enhancement' }, { id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }];

  var $ajax = $(".js-example-data-ajax");

  var $disabledResults = $(".js-example-disabled-results");

  var $tags = $(".js-example-tags");

  var $matcherStart = $('.js-example-matcher-start');

  var $diacritics = $(".js-example-diacritics");
  var $language = $(".js-example-language");

  $basicSingle.select2();
  $basicMultiple.select2();
  $limitMultiple.select2({
    maximumSelectionLength: 2
  });

  function formatState (state) {
    if (!state.id) {
      return state.text;
    }
    var $state = $(
      '<span>' +
        '<img src="vendor/images/flags/' +
          state.element.value.toLowerCase() +
        '.png" class="img-flag" /> ' +
        state.text +
      '</span>'
    );
    return $state;
  };

  $(".js-example-templating").select2({
    templateResult: formatState,
    templateSelection: formatState
  });

  $dataArray.select2({
    data: data
  });

  $dataArraySelected.select2({
    data: data
  });

  function formatRepo (repo) {
    if (repo.loading) return repo.text;

    var markup = '<div class="clearfix">' +
    '<div class="col-sm-1">' +
    '<img src="' + repo.owner.avatar_url + '" style="max-width: 100%" />' +
    '</div>' +
    '<div clas="col-sm-10">' +
    '<div class="clearfix">' +
    '<div class="col-sm-6">' + repo.full_name + '</div>' +
    '<div class="col-sm-3"><i class="fa fa-code-fork"></i> ' + repo.forks_count + '</div>' +
    '<div class="col-sm-2"><i class="fa fa-star"></i> ' + repo.stargazers_count + '</div>' +
    '</div>';

    if (repo.description) {
      markup += '<div>' + repo.description + '</div>';
    }

    markup += '</div></div>';

    return markup;
  }

  function formatRepoSelection (repo) {
    return repo.full_name || repo.text;
  }

  $ajax.select2({
    ajax: {
      url: "https://api.github.com/search/repositories",
      dataType: 'json',
      delay: 250,
      data: function (params) {
        return {
          q: params.term, // search term
          page: params.page
        };
      },
      processResults: function (data, params) {
        // parse the results into the format expected by Select2
        // since we are using custom formatting functions we do not need to
        // alter the remote JSON data, except to indicate that infinite
        // scrolling can be used
        params.page = params.page || 1;

        return {
          results: data.items,
          pagination: {
            more: (params.page * 30) < data.total_count
          }
        };
      },
      cache: true
    },
    escapeMarkup: function (markup) { return markup; },
    minimumInputLength: 1,
    templateResult: formatRepo,
    templateSelection: formatRepoSelection
  });

  $(".js-example-disabled").select2();
  $(".js-example-disabled-multi").select2();

  $(".js-example-responsive").select2();

  $disabledResults.select2();

  $(".js-example-programmatic").select2();
  $(".js-example-programmatic-multi").select2();

  $eventSelect.select2();

  $tags.select2({
    tags: ['red', 'blue', 'green']
  });

  $(".js-example-tokenizer").select2({
    tags: true,
    tokenSeparators: [',', ' ']
  });

  function matchStart (term, text) {
    if (text.toUpperCase().indexOf(term.toUpperCase()) == 0) {
      return true;
    }

    return false;
  }

  $matcherStart.select2({
    matcher: oldMatcher(matchStart)
  });

  $(".js-example-basic-hide-search").select2({
    minimumResultsForSearch: Infinity
  });

  $diacritics.select2();

  $language.select2({
    language: "es"
  });

  $(".js-example-theme-single").select2({
    theme: "classic"
  });

  $(".js-example-theme-multiple").select2({
    theme: "classic"
  });

  $(".js-example-rtl").select2();
});
</script>


        <footer>
  Select2 is licensed under the
  <a href="https://github.com/select2/select2/blob/master/LICENSE.md">
    MIT license.
  </a>
  The documentation is licensed under
  <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0.</a>
  Maintained by
  <a href="https://github.com/kevin-brown">Kevin Brown</a> and
  <a href="https://github.com/ivaynberg">Igor Vaynberg</a>.
</footer>


        <script type="text/javascript">
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

        ga('create', 'UA-57144786-2', 'auto');
        ga('send', 'pageview');
        </script>
    </body>
</html>

$(".js-data-example-ajax").select2({
  ajax: {
    url: "?action=",
    dataType: 'json',
    delay: 250,
    data: function (params) {
      return {
        q: params.term, // search term
        page: params.page
      };
    },
    processResults: function (data, page) {
      // parse the results into the format expected by Select2.
      // since we are using custom formatting functions we do not need to
      // alter the remote JSON data
      return {
        results: data.items
      };
    },
    cache: true
  },
  escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
  minimumInputLength: 1,
  templateResult: formatRepo, // omitted for brevity, see the source of this page
  templateSelection: formatRepoSelection // omitted for brevity, see the source of this page
});
'''