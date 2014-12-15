var user = {}
var chats = []
user.name = prompt('Enter your name');
// Пример с POST
function createUser() {
	var xhr = new XMLHttpRequest();

	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;\
	var params = 'csrfmiddlewaretoken=' + token + '&name=' + user.name;

	xhr.open("POST", '/create_user/', true);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	xhr.onreadystatechange = function() {
	  	if (this.readyState != 4) {
	  		alert(this.readyState)
	  		return;
		}
	}

	xhr.send(params);
}

function getChats (id) {
	
}