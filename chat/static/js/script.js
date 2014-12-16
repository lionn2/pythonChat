var user = {}
var chats = []
var idChat;
// Пример с POST
function createUser() {
	var xhr = new XMLHttpRequest();

	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	var params = 'csrfmiddlewaretoken=' + token + '&name=' + user.name;

	xhr.open("POST", window.location.href + 'create_user/', true);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	xhr.onreadystatechange = function() {
	  	if (this.readyState != 4) {
	  		return;
		}
		user = jQuery.parseJSON(xhr.responseText);
		console.log(user);
		document.getElementById('username').innerHTML = 'User: ' + user.name;
		var user_id = document.getElementById('user_id');
		user_id.value = user.id;
		console.log(user_id.value);
	}
	xhr.send(params);

}
function authorisation () {
	user.name = prompt('Enter your name');
	createUser(); 

}

function post_message () {
	$.ajax({
           type: "POST",
           url: window.location.href + 'post_message/',
           data: $("#post_message").serialize(), // serializes the form's elements.
           success: function(data)
           {
               console.log(data); // show response from the php script.
           }
         });
}

function openChat (id) {
	
}