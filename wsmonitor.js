var host = "hackathon.securityinnovation.com";

var WebSocketClient = require('websocket').client;
var client = new WebSocketClient();

client.on('connectFailed', function(error) {
    console.log('Connect Error: ' + error.toString());
});

client.on('connect', function(connection) {
    console.log('WebSocket Client Connected');
    connection.on('error', function(error) {
        console.log("Connection Error: " + error.toString());
    });
    connection.on('close', function() {
        console.log('echo-protocol Connection Closed');
    });
    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            console.log("Received: '" + message.utf8Data + "'");
        }
    });
    
    function keepalive() {
        if (connection.connected) {
            connection.sendUTF("");
            setTimeout(keepalive, 30000);
        }
    }
    keepalive();
});
 
// Have to get a JSESSIONID cookie
var jsessionid = null
var request = require('request');

request("https://"+host, function (error, response, body) {
  if (!error && response.statusCode == 200) {
    c = response.headers['set-cookie'][0];
    var re = /JSESSIONID=([^;]+)/;
    jsessionid = c.match(re);
    if(jsessionid) {
      jsessionid = jsessionid[1];
      console.log("Got session ID: " + jsessionid);
      client.connect("wss://" + host + "/ws", null, host+":443", { 'cookie' : "JSESSIONID=" + jsessionid } );
    }
  }
})

