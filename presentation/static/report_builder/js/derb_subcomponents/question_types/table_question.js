/**
 * Created by jaquer on 10/10/16.
 */
var catalog_id;
var display_fields;
var input_id;
var select_id;
var catalog_url = '/get_catalog_display_fields';

function handle_table_question_load(question_html_id) {
    init_table(question_html_id);

    $(question_html_id + " #id_catalog").change(function () {
        var conf = confirm('Are you sure, you want to change the catalog?');
        if (conf == true) {
            init_table(question_html_id);
        } else {
            $(question_html_id + " #id_catalog").val(catalog_id);
        }
    });

    init_values(question_html_id);
}

function init_table(question_html_id) {
    $(question_html_id + " #id_catalog").find("option:selected").each(function () {
        $(question_html_id + ' #catalog_name').html($(this).text());
        catalog_id = $(this).val();
        var ajax_response = $.ajax({
            url: catalog_url,
            type: 'GET',
            data: {
                catalog_id: catalog_id
            },
            async: false,
            success: function (data) {
                var df_selector = $(question_html_id + ' #table');
                df_selector.html('');

                input_id = 0;
                select_id = 0;
                display_fields = data.content;
                var html = '<input id="id_header_' + input_id + '" name="header_' + input_id + '" class="form-control" type="text" placeholder="Write the header"><select id="id_display_field_' + select_id + '" name="display_field_' + select_id + '" class="form-control">';
                var htmlend = '</select> <br/>';
                var id = '';
                for (var i = 0; i < display_fields.length; i++) {
                    id = display_fields[i][1];
                    html += '<option value="' + id + '">' + display_fields[i][1] + '</option>';
                }
                html += htmlend;
                df_selector.html(html);
            }
        });
        display_fields = ajax_response.responseJSON.content;
    });
}

function do_table(question_html_id) {
    input_id += 1;
    select_id += 1;
    var df_selector = $(question_html_id + ' #table');
    var bodyhtml = '<input id="id_header_' + input_id + '" name="header_' + input_id + '" class="form-control" type="text" placeholder="Write the header"><select id="id_display_field_' + select_id + '" name="display_field_' + select_id + '" class="form-control">';
    var endhtml = '</select> <br/>';
    for (var i = 0; i < display_fields.length; i++) {
        id = display_fields[i][1];
        bodyhtml += '<option value="' + id + '">' + display_fields[i][1] + '</option>';
    }
    bodyhtml += endhtml;
    df_selector.append(bodyhtml);
}

function remove_table(question_html_id) {
    if (input_id && select_id > 0) {
        $(question_html_id + '#id_header_' + input_id + '').remove();
        $(question_html_id + '#id_display_field_' + select_id + '').remove();
        $(question_html_id + ' #table').find('br:last').remove();
        input_id -= 1;
        select_id -= 1;
    }
}

function init_values(question_html_id) {
    if (answer_options_json != '') {
        window.setTimeout(function () {
            var answer_options = JSON.parse(answer_options_json);
            var catalog = answer_options.catalog;
            var headers = answer_options.headers;
            var displays = answer_options.displays;

            $(question_html_id + ' #id_catalog').val(catalog);
            init_table(question_html_id);

            window.setTimeout(function () {
                for (var i = 1; i <= headers.length - 1; i++) {
                    $(question_html_id + ' #id_header_0').val(headers[0]);
                    $(question_html_id + ' #id_display_field_0').val(displays[0]);
                    input_id = i;
                    select_id = i;
                    var df_selector = $(question_html_id + ' #table');
                    var bodyhtml = '<input id="id_header_' + input_id + '" name="header_' + input_id + '" class="form-control" type="text" value="' + headers[i] + '"><select id="id_display_field_' + select_id + '" name="display_field_' + select_id + '" class="form-control">';
                    var endhtml = '</select> <br/>';
                    for (var j = 0; j < display_fields.length; j++) {
                        id = display_fields[j][1];
                        if (display_fields[j][1] == displays[i]) {
                            bodyhtml += '<option value="' + id + '" selected="selected">' + display_fields[j][1] + '</option>';
                        } else {
                            bodyhtml += '<option value="' + id + '">' + display_fields[j][1] + '</option>';
                        }
                    }
                    bodyhtml += endhtml;
                    df_selector.append(bodyhtml);
                }
            }, 100);

        }, 100);
    }
}
