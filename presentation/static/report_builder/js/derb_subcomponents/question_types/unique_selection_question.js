/**
 * Created by jaquer on 10/10/16.
 */
catalog_url = '/get_catalog_display_fields';
function handle_catalog_question_load(question_html_id){

    update_combo(question_html_id);

    $(question_html_id + " #id_catalog").change(function () {
        update_combo(question_html_id);
    });

    initial_values(question_html_id);
}

function update_combo(question_html_id) {
    if (question_html_id == undefined){
        question_html_id = question_id;
    }
    $(question_html_id + " #id_catalog").find("option:selected").each(function () {
        $(question_html_id + ' #catalog_name').html($(this).text());
        var catalog_id = $(this).val();

        $.ajax({
            url: catalog_url,
            type: 'GET',
            data: {
                catalog_id: catalog_id
            },
            success: function (data) {
                var df_selector = $(question_html_id + ' #display_fields');
                df_selector.html('');

                var display_fields = data.content;
                var html = '';
                var id = '';
                for (var i = 0; i < display_fields.length; i++) {
                    id = 'id_display_fields_' + display_fields[i][1];
                    html += '<ul><li><label for="' + id + '"><input id="' + id + '" type="checkbox" value="' + display_fields[i][0] + '" name="display_fields"> ' + display_fields[i][1] + '</label></li></ul>';
                }
                df_selector.html(html);
            }
        });
    });
}

function initial_values(question_html_id) {
    if (question_html_id == undefined){
        question_html_id = question_id;
    }
    console.log(question_html_id);
    if (answer_options_json != '') {
        window.setTimeout(function () {
            var answer_options = JSON.parse(answer_options_json);
            var catalog = answer_options.catalog;
            var display_fields = answer_options.display_fields;

            $(question_html_id + " #id_catalog").val(catalog);
            update_combo(question_html_id);

            window.setTimeout(function () {
                for (var i = 0; i < display_fields.length; i++) {
                    $(question_html_id + ' #id_display_fields_' + display_fields[i] + '').prop('checked', true);
                }
            }, 100);

        }, 100);
    }
}