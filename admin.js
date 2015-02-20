//here we get new content and update html
var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );            
        anHttpRequest.send( null );
        // setTimeout(get, 1000);
    }
}
var update = function() {
	var aClient = new HttpClient();
	var yes = "";
	var no = "";
	aClient.get('/json', function(answer) {
		var response = $.parseJSON(answer);
		var speak = response['speak'];
		var quiet = response['quiet'];
		for(var i = 0; i<speak.length; i++) {
			yes = yes.concat('<li>' + speak[i] + '</li>');
		}
		if(speak.length === 0) {
			yes = "<li>No one!</li>";
		}
		for(var i = 0; i<quiet.length; i++) {
			no = no.concat('<li>' + quiet[i] + '</li>');
		}
		if(no === "") {
			no = "<li>No one!</li>";
		}
		$('#yes').html(yes);
		$('#no').html(no);
	});
}
$(document).ready(function(){
	update();
	$("button").click(function(){
		update();
	});
});
// // $(document).ready(function() {
// // 	function callAjax() {
// // 		$.ajax({
// // 			url: '/json',
// // 			dataType: 'json',
// // 			method: 'GET',
// // 			success: function(response){
// // 				//retrieved json, now parse it and submit to form
// // 				$("#input").html(response);
// // 				console.log('hello world');
// // 			}
// // 		});
// // 	}
// // 	setTimeout(callAjax, 1000);
// // }
// var interval;
// function callAjax() {
// 	interval = setTimeout(function() {
// 		$.ajax({
// 		url: '/json',
// 		dataType: 'json',
// 		method: 'GET',
// 		success: function(response){
// 			//retrieved json, now parse it and submit to form
// 			//$("#input").html(response);
// 			alert('hello!');
// 		},
// 		complete: callAjax});
// 	}, 1000);
// }

// function halt() {
// 	clearTimeout(interval);
// }