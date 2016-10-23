"""
    MoinMoin - AjaxLink Macro

    Usage: <<AjaxLink(url, txt, tagid, type=text|button, autostart=True|False)>>

    @copyright: 2011 happytk
    @license: GNU GPL
"""

import hashlib


def macro_GoToAjax(macro, placeholder='SEARCH'):

    id = hashlib.md5().hexdigest()

    return '''<!-- select2 script -->
<!--<button class='js-programmatic-destroy'>destroy</button>//-->
<select id='%s'></select>
<script>
$select = $('#%s').select2({
    ajax: {
        url: "?action=datasearch&self=1&typ=name",
        dataType: 'json',
        delay: 250,
        data: function (params) {
            return {
                name: params.term,
                page: params.page
            };
        },
        processResults: function (data, params) {
            params.page = params.page || 1;
            return {
                results: data.items,
                pagination: {
                    more: data.more,
                }
            };
        },
        cache: true,
    },
    width: '300px',
    placeholder: '%s',
    escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
    minimumInputLength: 2,
    templateResult: function (repo) {
        if (repo.loading)
            return repo.text;
        return '<div><small>' + repo.text + '</small></div>';
    },
    templateSelection: function (repo) {
        return repo.full_name || repo.text;
    },
}).change(function() {
    //var theSelection = $(this).select2('data')[0].text;
    var theSelection = $(this).text();
    if (theSelection != 3620194) {
        //insert_textarea(theSelection);
        //$(this).val(3620194).trigger('change');
        window.location.href = '%s/' + theSelection; 
    }
});

//$(".js-programmatic-destroy").on("click", function () { $select.select2("destroy"); });
</script>
''' % (id, id, placeholder, macro.request.script_root)