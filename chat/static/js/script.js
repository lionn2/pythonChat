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
	console.log('createUser')
}
var date;
function authorisation () {
	console.log('authorisation')
	user.name = prompt('Enter your name');
	createUser(); 
	date = new Date();
	date.setHours(0,0,0,0);
	getMessagesFromDate(date);
}

function post_message () {

	console.log('post_message')
		console.log(user);
	var textArea = document.getElementById('textArea');
	if(!textArea.value)  {
		console.log('textArea is empty');
		return;
	}
	$.ajax({
           type: "POST",
           url: window.location.href + 'post_message/',
           data: $("#post_message").serialize(), // serializes the form's elements.
           success: function(messages)
           {
           		messages = jQuery.parseJSON(messages);
           		addMessagesToTable(messages);
                textArea.value = "";
           }
         });

}
function getToken () {
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	return 'csrfmiddlewaretoken=' + token;

}

function formatDate (date) {
	console.log('formatDate')
	var addZero = function (number) {
		var number = number.toString();
		if (number.length == 1) {
			number = '0' + number;
		}
		return number;
	};
	var year = addZero( date.getFullYear());
	var month = addZero( date.getMonth() + 1 );
	var date1 = addZero( date.getDate() );
	var hour = addZero( date.getHours() );
	var minute = addZero( date.getMinutes() );
	var second = addZero( date.getSeconds() );
	var res =  year + '-' + month + '-' + date1 + ' ' + hour + ':' + minute + ':' + second;
	console.log(res);
	return res;
}
function formateDateChat(date) {
	console.log('formateDateChat')
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
	console.log(res);
	return res;
}

function openChat (id) {
	
}
function getMessagesFromDate (date) {
	console.log('getMessagesFromDate');
	$.ajax({
           type: "POST",
           url: window.location.href + 'messages_from_date/',
           data: getToken() + "&date=" + formatDate(date),
           success: function(messages)
           {
           		messages = jQuery.parseJSON(messages);
               textArea.value = "";
               addMessagesToTable(messages);
           }
         });
}

function addMessagesToTable (messages) {
	console.log('addMessagesToTable')
	console.log(messages);
	for (var i = 0; i < messages.length; i++) {
		m = messages[i].fields;
		console.log(messages[i]);
		addMessageToTable(m);
	};
}

function addMessageToTable (m) {
	console.log('addMessageToTable')
	var table = document.getElementById('chatTable');
	var n = table.rows.length;
	m.post_time = new Date(m.post_time);
	console.log(m);
	var row = table.insertRow(table.rows.length);
	var cell1 = row.insertCell(0);
	cell1.innerHTML = m.user_id;
	var cell2 = row.insertCell(1);
	cell2.innerHTML = m.message;
	var cell3 = row.insertCell(2);
	cell3.innerHTML = formateDateChat(m.post_time);
}