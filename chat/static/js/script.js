var user = {}
var chats = []
var idChat;
var table;
var interval;
var id = 0;
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
		document.getElementById('username').innerHTML = 'User: ' + user.name;
		console.log('u'  + user);
		var user_id = document.getElementById('user_id');
		user_id.value = user.id;
}
	xhr.send(params);
}
function authorisation () {
	user.name = prompt('Enter your name');
	createUser(); 
	setTimeout(function {
		getMessagesFromID(id);
	}, 0);
	
}

function startInterval () {
	if(interval) clearTimeout(interval);
	interval = setTimeout(function() {
		getMessagesFromID(date);
		console.log(date.toISOString());
	}, 0);	
}

function post_message () {

	var textArea = document.getElementById('textArea');
	if(!textArea.value)  {
		return;
	}
	$.ajax({
           type: "POST",
           url: window.location.href + 'post_message/',
           data: $("#post_message").serialize(), // serializes the form's elements.
           success: function(messages)
           {
           		messages = jQuery.parseJSON(messages);
           		//addMessagesToTable(messages);
                textArea.value = "";
           }
         });

}
function getToken () {
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	return 'csrfmiddlewaretoken=' + token;

}

function formatDate (date) {
	/*var addZero = function (number) {
		var number = number.toString();
		if (number.length == 1) {
			number = '0' + number;
		}
		return number;
	};
	var year = addZero( date.getFullYear());
	var month = addZero( date.getMonth() + 1 );
	var date1 = addZero( date.getDate() );
	var hour = addZero( date.getHours() + 2);
	var minute = addZero( date.getMinutes() );
	var second = addZero( date.getSeconds() );
	var res =  year + '-' + month + '-' + date1 + ' ' + hour + ':' + minute + ':' + second;
	return res;*/

	return date.toISOString();
}
function formateDateChat(date) {
	var addZero = function (number) {
		var number = number.toString();
		if (number.length == 1) {
			number = '0' + number;
		}
		return number;
	};
	var hour = addZero( date.getHours() );
	var minute = addZero( date.getMinutes() );
	var second = addZero( date.getSeconds() );
	var res = hour + ':' + minute + ':' + second;
	return res;
	return date.toISOString();
}

function getMessagesFromID (id) {
	console.log(user);
	$.ajax({
           type: "POST",
           url: window.location.href + 'messages_from_id/',
           data: getToken() + "&id=" + id /*+ '&user=' + user.id*/,
           success: function(messages)
           {
           		messages = jQuery.parseJSON(messages);
                addMessagesToTable(messages);
                startInterval();
           }
         });
}

function addMessagesToTable (messages) {
	for (var i = 0; i < messages.length; i++) {
		id = messages[i].pk;
		m = messages[i].fields;
		addMessageToTable(m);
	};
}

function addMessageToTable (m) {
	var table = document.getElementById('chatTable');
	var n = table.rows.length;
	m.post_time = new Date(m.post_time);
	var row = table.insertRow(table.rows.length);
	var cell1 = row.insertCell(0);
	cell1.innerHTML = m.user_id;
	var cell2 = row.insertCell(1);
	cell2.innerHTML = m.message;
	var cell3 = row.insertCell(2);
	cell3.innerHTML = formateDateChat(m.post_time);
}