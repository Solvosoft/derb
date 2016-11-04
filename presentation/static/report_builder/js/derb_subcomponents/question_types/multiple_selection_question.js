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

function initial_values() {
    if (answer_options_json != '') {
        window.setTimeout(function () {
            var answer_options = JSON.parse(answer_options_json);
            var catalog = answer_options.catalog;
            var display_fields = answer_options.display_fields;

            $('#id_catalog').val(catalog);
            update_combo();

            window.setTimeout(function() {
            	for (var i=0; i < display_fields.length; i++){
            		$('#id_display_fields_'+display_fields[i]+'').prop('checked', true);
            	}
            }, 100);

        }, 100);
    }
}