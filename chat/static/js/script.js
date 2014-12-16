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
		document.getElementById('username').innerHTML = user.name;
	}
	xhr.send(params);

}
function authorisation () {
	user.name = prompt('Enter your name');
	createUser(); 
}

function openChat (id) {
	
}