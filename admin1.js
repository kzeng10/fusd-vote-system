$(document).ready(function() {
	function callAjax() {
		$.ajax({
			url: '/json',
			dataType: 'json',
			method: 'GET',
			success: function(response){
				//retrieved json, now parse it and submit to form
				$("#input").html(response);
				console.log('hello world');
			}
		});
	}
	setInterval(callAjax, 1000);
}

function halt() {
	clearTimeout(interval);
}