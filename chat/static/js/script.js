alert('hi')
var user = {}
user.name = prompt('Enter your name');
// Пример с POST
var xhr = new XMLHttpRequest();

var params = 'name=' + encodeURIComponent(name);

xhr.open("POST", '/create_user', true)
xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')

xhr.onreadystatechange = ...;

xhr.send(params);
