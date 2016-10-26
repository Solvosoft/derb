/**
 * Created by jaquer on 10/10/16.
 */
$(document).ready(function() {
	init_table();

	$("#id_catalog").change(function() {
		var conf = confirm('Are you sure, you want to change the catalog?');
		if (conf == true) {
			init_table();
		}
		else{
			$("#id_catalog").val(catalog_id);
		}
	});

});

var catalog_id;
var display_fields;

function init_table() {
	$("#id_catalog").find("option:selected").each(function() {
		catalog_id = $(this).val();
		$.ajax({
			url : catalog_url,
			type : 'GET',
			data : {
				catalog_id : catalog_id
			},
			success : function(data) {
				var df_selector = $('#table');
				df_selector.html('');

				display_fields = data.content;
				var html = '<div class="col-md-12"><input class="form-control" type="text" placeholder="Write the header"><select class="form-control">';
				var htmlend = '</select></div>';
				var id = '';
				for (var i = 0; i < display_fields.length; i++) {
					id = 'id_display_fields_' + display_fields[i][1];
					html += '<option value="' + id + '">' + display_fields[i][1] + '</option>';
				}
				html += htmlend;
				df_selector.html(html);
			}
		});
	});
}

function do_table() {
	var df_selector = $('#table');
	var bodyhtml = '<div class="col-md-12"><input class="form-control" type="text" placeholder="Write the header"><select class="form-control">';
	var endhtml = '</select></div>';
	for (var i = 0; i < display_fields.length; i++) {
		id = 'id_display_fields_' + display_fields[i][1];
		bodyhtml += '<option value="' + id + '">' + display_fields[i][1] + '</option>';
	}
	bodyhtml += endhtml;
	df_selector.append(bodyhtml);
}
