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
		document.getElementById('username').innerHTML = 'User: ' + user.name;
		var user_id = document.getElementById('user_id');
		user_id.value = user.id;
	}
	xhr.send(params);
}
var date;
function authorisation () {
	user.name = prompt('Enter your name');
	createUser(); 
	date = new Date();
	date.setHours(0,0,0,0);
	//getMessagesFromDate(date);
	setInterval(function() {
		var date2 = new Date();
		getMessagesFromDate(date)
		date = date2;
		console.log(date);
	}, 1000);	
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
	var hour = addZero( date.getHours() + 2);
	var minute = addZero( date.getMinutes() );
	var second = addZero( date.getSeconds() );
	var res =  year + '-' + month + '-' + date1 + ' ' + hour + ':' + minute + ':' + second;
	return res;
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
}

function openChat (id) {
	
}
function getMessagesFromDate (date) {
	$.ajax({
           type: "POST",
           url: window.location.href + 'messages_from_date/',
           data: getToken() + "&date=" + formatDate(date),
           success: function(messages)
           {
           		messages = jQuery.parseJSON(messages);
                addMessagesToTable(messages);
           }
         });
}

function addMessagesToTable (messages) {
	for (var i = 0; i < messages.length; i++) {
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