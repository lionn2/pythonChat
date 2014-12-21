var interval;
var id = 0;

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
	$.ajax({
           type: "POST",
           url: 'messages_from_id/',
           data: getToken() + "&id=" + id,
           success: function(messages)
           {
           		messages = jQuery.parseJSON(messages);
           		console.log(messages);
                addMessagesToTable(messages);

                startInterval();
           }
         });
}

function addMessagesToTable (messages) {
	for (var i = 0; i < messages.length; i++) {
		var m = messages[i];
		console.log(m);
		var table = document.getElementById('chatTable');
		//var n = table.rows.length;
		id = m.id;
		m.post_time = new Date(m.post_time);
		var row = table.insertRow(0/*table.rows.length*/);
		row.className = 'chat-row';
		var cell1 = row.insertCell(0);
		cell1.innerHTML = m.user;
		cell1.className = 'chat-cell-username';
		/*cell1['min-width'] = 'auto';
		cell1['max-width'] = 150;
		cell1.width = 120;
		cell1['text-align'] = 'right';*/
		var cell2 = row.insertCell(1);
		cell2.className = 'chat-cell-message';
		cell2.innerHTML = m.message.split('\r\n').join('<br />');
		//cell2['word-break'] = 'break-word';
		var cell3 = row.insertCell(2);
		cell3.innerHTML = formateDateChat(m.post_time);
		cell3.className = 'chat-cell-time';
		//cell3.width = 80;
		//cell2.width = table.width - cell1.width - cell3.width;
		//var objDiv = document.getElementById("mygrid-wrapper-div");
		//var d = $('#mygrid-wrapper-div');	
	};
}
