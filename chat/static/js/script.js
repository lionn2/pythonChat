alert('hi')
var user = {}
user.name = prompt('Enter your name');
// Пример с POST
function createUser() {
	var xhr = new XMLHttpRequest();

	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	//alert(token);
	var params = 'csrfmiddlewaretoken=' + token + '&name=' + user.name;
	
	xhr.open("POST", '/create_user/', true);
	//xnr.setRequestHeader('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8');
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	xhr.onreadystatechange = function() {
	  	if (this.readyState != 4) {
	  		alert(this.readyState)
	  		return;
		}
	  alert(this.responseText);
	}

	xhr.send(params);
}
function createUser3 () {
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