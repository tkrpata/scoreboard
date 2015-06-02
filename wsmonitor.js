var host = HOST;
var current_score = null;
// global point delta - web service will use this
global.delta = null;

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
        console.log('Connection Closed');
    });
    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            console.log('current score: ', current_score);
            json = JSON.parse(message.utf8Data);
            var points = 0;
            for (var p of json) {
              points += p.points;
            }
            console.log('new score: ', points);
            if(global.delta === null) {
              global.delta = 0; // init
            } else {
              global.delta = global.delta + (points - current_score); 
            }
            console.log('delta: ', global.delta);
            current_score = points;
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

