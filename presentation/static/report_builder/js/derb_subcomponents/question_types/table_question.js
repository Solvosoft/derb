/**
 * Created by jaquer on 10/10/16.
 */
$(document).ready(function () {
    init_table();

    $("#id_catalog").change(function () {
        init_table();
    });

});

function init_table() {
    $("#id_catalog").find("option:selected").each(function () {
        var catalog_id = $(this).val();
        $.ajax({
            url: catalog_url,
            type: 'GET',
            data: {
                catalog_id: catalog_id
            },
            success: function (data) {
                var df_selector = $('#table');
                df_selector.html('');

                var display_fields = data.content;
                var col = 12;
                var html = '<div class="col-md-'+col+'"><input class="form-control" type="text" placeholder="Write the header"><select class="form-control">';
                var htmlend = '</select></div>';
                var count = 0;
                var id = '';
                for (var i = 0; i < display_fields.length; i++) {
                    id = 'id_display_fields_' + display_fields[i][1];
                    html += '<option value="'+ id +'">'+display_fields[i][1]+'</option>';
                    count++;
                }
                html+=htmlend;
                df_selector.html(html);
            }
        });
    });
}
