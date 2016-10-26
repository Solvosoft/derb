$(document).ready(function() {
	$("#id_observation").change(function() {
		submit_observation();
	});

});

function submit_observation() {
	var observation_id = $(this).val();
	        $.ajax({
            url: observation_url,
            type: 'GET',
            data: {
                observation_id: observation_id
            },
            success: function (response) {
            	$("#observation").html(response);
            }
        });

}
