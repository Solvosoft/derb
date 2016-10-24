/**
 * Created by jaquer on 10/10/16.
 */
$(document).ready(function () {
    update_combo();

    $("#id_catalog").change(function () {
        update_combo();
    });

    initial_values();
});

function update_combo() {
    $("#id_catalog").find("option:selected").each(function () {
        $('#catalog_name').html($(this).text());
        var catalog_id = $(this).val();
        $.ajax({
            url: catalog_url,
            type: 'GET',
            data: {
                catalog_id: catalog_id
            },
            success: function (data) {
                var df_selector = $('#display_fields');
                df_selector.html('');

                var display_fields = data.content;
                var html = '';
                var count = 0;
                var id = '';
                for (var i = 0; i < display_fields.length; i++) {
                    id = 'id_display_fields_' + count;
                    html += '<ul><li><label for="' + id + '"><input id="' + id + '" type="checkbox" value="' + display_fields[i][0] + '" name="display_fields"> ' + display_fields[i][1] + '</label></li></ul>';
                    count++;
                }
                df_selector.html(html);
            }
        });
    });
}

function initial_values() {
    var answer_options = JSON.parse(answer_options_json);

    /* TODO */
}