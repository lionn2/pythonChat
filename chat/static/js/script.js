var user = {}
var chats = []
var idChat;
var table;
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
var date;
function authorisation () {
	user.name = prompt('Enter your name');
	createUser(); 
	date = new Date();
	date.setHours(0,0,0,0);
	getMessagesFromDate(date);
}

function post_message () {
	var textArea = document.getElementById('textArea');
	if(!textArea.value)  {
		console.log('textArea is empty');
		return;
	}
	$.ajax({
           type: "POST",
           url: window.location.href + 'post_message/',
           data: $("#post_message").serialize(), // serializes the form's elements.
           success: function(message)
           {
           		addMessagesToTable( new Array(message) );
                textArea.value = "";
           }
         });
}

function openChat (id) {
	
}
function getMessagesFromDate (date) {
	$.ajax({
           type: "POST",
           url: window.location.href + 'messages_from_date/',
           data: "date=" + date,
           success: function(messages)
           {
               console.log(messages); // show response from the php script.
               textArea.value = "";
               addMessagesToTable(messages);
           }
         });
}

function addMessagesToTable (messages) {
	var table = getElementById('chatTable');
	var n = table.rows.length;
	for (var m = 0; i < messages.length; i++) {
		var row = table.insertRow(table.rows.length);
		var cell1 = row.insertCell(0);
		cell1.innerHTML = m.user;
		var cell2 = row.insertCell(1);
		cell2.innerHTML = m.message;
		var cell3 = row.insertCell(2);
		cell3.innerHTML = m.post_time;
	};
}