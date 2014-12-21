function is_valid_form() {
	if (!$('#chat_name')[0].value)
		return false;
	return true;
}

function getToken () {
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	return 'csrfmiddlewaretoken=' + token;
}

function deleteChat (delButton, id) {
	$.ajax({
       	type: "POST",
       	url: '/delete_chat/',
       	data: getToken() + "&id=" + id,
       	success: function () {
			deleteParentRow(delButton);			
       	}
    });
}

function deleteParentRow(elem) {
	for(;!elem.insertCell;) { //if elem is <tr>
		elem = elem.parentNode;
	}
	elem.parentNode.removeChild(elem);
}