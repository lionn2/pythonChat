alert('hi')
var user = {}
user.name = prompt('Enter your name');
// Пример с POST
function createUser2() {
	var xhr = new XMLHttpRequest();

	var params = 'name=' + encodeURIComponent(user.name);

	xhr.open("POST", '/create_user/', true)
	//xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')

	xhr.onreadystatechange = function() {
	  	if (this.readyState != 4) {
	  		alert(this.readyState)
	  		return;
		}
	  alert(this.responseText);
	}

	xhr.send(params);
}
function createUser () {
	var params = 'name=' + encodeURIComponent(user.name);
	$.ajax({
      type: "post",
      url: "/create_user/",
      data: params,
      success: function(data) {
        alert(data);
      }
    });	
}