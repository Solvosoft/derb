$(document).ready(function() {
	
	init_responsable_view();
	
});

function init_responsable_view() {
	var answer_options = JSON.parse(answer_options_json);
	var headers = answer_options.headers;
	var responsable = $('#responsable');
	
	for (var i = 0; i < headers.length; i++) {
		var html = '<strong>'+headers[i]+'</strong><br/><select id="id_display_field_' + i + '" name="display_field_' + i + '" class="form-control"></select> <br/>';
		responsable.append(html);
	}

}
