function getXmlHttpRequestObject() {
	if (window.XMLHttpRequest) {
		return new XMLHttpRequest();
	} else if(window.ActiveXObject) {
		return new ActiveXObject("Microsoft.XMLHTTP");
	} else {
		document.getElementById('p_status').innerHTML = 
		'Status: Cound not create XmlHttpRequest Object.' +
		'Consider upgrading your browser.';
	}
}

var sendReq = getXmlHttpRequestObject();
var receiveReq = getXmlHttpRequestObject();
var lastMessage = 0;
var mTimer;