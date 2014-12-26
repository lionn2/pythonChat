var interval;
var id = 0;
var users = [];
var me;

function main (user) {
	startInterval();
	sortUsers();
	me = user;
}

function startInterval () {
	setTimeout(function () {
		getMessagesFromID(id);
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
			},
			statusCode: {
				400: function () {
					console.log( $('#alert-placeholder').get(0) );
					$('#alert-placeholder').get(0).innerHTML = '<div class=\"alert alert-dismissable alert-danger\">' + 
					'<button type=\"button\" class=\"close\" data-dismiss=\"alert\">×</button>' + 
					'You can\'t post massage</div>';
					$('.close').click(function () {
						$('#alert-placeholder').get(0).innerHTML = '';
					});
				}
			}
         });

}
function getToken () {
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	return 'csrfmiddlewaretoken=' + token;
}

function formatDate (date) {
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
	$.ajax({
           type: "POST",
           url: 'messages_from_id/',
           data: getToken() + "&id=" + id,
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
		var m = messages[i];
		var table = document.getElementById('chatTable');
		//var n = table.rows.length;
		id = m.id;
		m.post_time = new Date(m.post_time);
		var row = table.insertRow(0/*table.rows.length*/);
		row.className = 'chat-row';
		var cell1 = row.insertCell(0);
		var cell2 = row.insertCell(1);
		var cell3 = row.insertCell(2);
		cell1.className = 'chat-cell-username';
		cell2.className = 'chat-cell-message';
		cell3.className = 'chat-cell-time';

		if(m.type == 1) {
			addUser(m.user);
		} else if(m.type == 2) {
			delUser(m.user);
		} else if(m.type == 0 || m.type == 3){
			cell1.innerHTML = m.user;
		}

		if(m.type == 3) {
			cell2.innerHTML = '<a>' + m.message + '</a>';
		} else {
			cell2.innerHTML = m.message.split('\r\n').join('<br />');
		}

		cell3.innerHTML = formateDateChat(m.post_time);
	};
}

function textAreaKey (el, event) {
	if (event.keyCode == 13 && event.shiftKey) {
		el.innterHTML += '\n'; 
	}
	else if (event.keyCode == 13) {
		post_message(); 
	}
}
function sortUsers () {
	var userPanel = $('#chat-users').get(0);
	var child_arr = userPanel.childNodes;
	console.log(child_arr);

	for (var i = 0; i < child_arr.length; i++) {
		if (child_arr[i].tagName == 'A') {
			users.push(child_arr[i]);
		};
	}
	console.log(users);
}

function addUser (user) {
	for (var i = 0; i < users.length; i++) 
		if (users[i].innerText == user)
			return;
	$('#chat-users').append('<a href=\'#\' class=\'list-group-item\'>' + user + '</a>\n');
}

function delUser (user) {
	/*if(user == me) {
		window.location = '/';
	}*/
	for (var i = 0; i < users.length; i++) {
		if (users[i].innerText == user) {
			users[i].parentNode.removeChild( users[i] );
			users.splice(i, 1);
		}
	};
}

function leaveChat (chat_id) {
	$.ajax({
       	type: "POST",
       	url: '/delete_user_from_chat/',
       	data: getToken() + "&chat_id=" + chat_id,
       	success: function()
       	{
       		window.location = '/';
        }
    });
}