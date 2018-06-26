/**
 * Created by jaquer on 10/10/16.
 */

/**
 * Checks the html view and implements the functions.
 */
$(document).ready(function() {
	init_table();

	$("#id_catalog").change(function() {
		var conf = confirm('Are you sure, you want to change the catalog?');
		if (conf == true) {
			init_table();
		} else {
			$("#id_catalog").val(catalog_id);
		}
	});

	init_values();

});

/**
 * @param {number} catalog_id The catalog value.
 * @param {object} display_fields Values obtained whit ajax.
 * @param {number} input_id The counter for the inputs id.
 * @param {number} select_id The counter for the selects id.
 */
var catalog_id;
var display_fields;
var input_id;
var select_id;

/**
 * @function init_table
 * Using Ajax, according whit the option selected in the catalog choice, the display fields in the table will
 * be updated.
 */
function init_table() {
	$("#id_catalog").find("option:selected").each(function() {
		$('#catalog_name').html($(this).text());
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
	});
}

/**
 * @function do_table
 * It allows add new rows for the table.
 */
function do_table() {
	input_id += 1;
	select_id += 1;
	var df_selector = $('#table');
	var bodyhtml = '<input id="id_header_' + input_id + '" name="header_' + input_id + '" class="form-control" type="text" placeholder="Write the header"><select id="id_display_field_' + select_id + '" name="display_field_' + select_id + '" class="form-control">';
	var endhtml = '</select> <br/>';
	for (var i = 0; i < display_fields.length; i++) {
		id = display_fields[i][1];
		bodyhtml += '<option value="' + id + '">' + display_fields[i][1] + '</option>';
	}
	bodyhtml += endhtml;
	df_selector.append(bodyhtml);
}

/**
 * @function remove_table
 * It allows delete the last row in the table.
 */
function remove_table() {
	if (input_id && select_id > 0) {
		$('#id_header_' + input_id + '').remove();
		$('#id_display_field_' + select_id + '').remove();
		$('#table').find('br:last').remove();
		input_id -= 1;
		select_id -= 1;
	}
}

/**
 * @function init_values
 * If the question exists, the data in answer_options_json will be used to define the form data.
 */
function init_values() {
	if (answer_options_json != '') {
		window.setTimeout(function() {
			var answer_options = JSON.parse(answer_options_json);
			var catalog = answer_options.catalog;
			var headers = answer_options.headers;
			var displays = answer_options.displays;

			$('#id_catalog').val(catalog);
			init_table();

			window.setTimeout(function() {
				for (var i = 1; i <= headers.length - 1; i++) {
					$('#id_header_0').val(headers[0]);
					$('#id_display_field_0').val(displays[0]);
					input_id = i;
					select_id = i;
					var df_selector = $('#table');
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
