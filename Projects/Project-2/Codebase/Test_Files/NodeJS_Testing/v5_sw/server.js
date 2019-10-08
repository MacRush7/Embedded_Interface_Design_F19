var mydata;
var myJSON = []; 
var myTIME;

var mode1 = "LAST_ENTRY"; //mode1 for sending data to the client
var mode2 = "NET_TEST"; //mode2 for sending 10 data to the client

var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'user',
  password : 'password',
  database : 'db1'
});
 
connection.connect(function(err) {
  if (err) {
    console.error('error connecting: ' + err.stack);
    return;
  }
 
  console.log('connected as id ' + connection.threadId);
});
 
var queryString = 'SELECT * FROM eid';

//////////////////START TIME//////////////////////
const perf = require('execution-time')();

//at beginning of your code, pass any name
var begin = new Date();
perf.start('apiCall');



connection.query(queryString, function(err, rows, fields) {
    if (err) throw err;
    
    //for (var i in rows) {
    for (var i=0; i<=9; i++){
    //console.log(rows[i]);
    //}
    
    
    mydata = rows[i];
    //JSON.stringify(mydata);
    
    myJSON[i] = JSON.stringify(mydata);
    
    //console.log(mydata);
  }
  

//at end of your code, pass the same name (anywhere in your flow)
const results = perf.stop('apiCall');
var end = new Date();

console.log(begin);
console.log(end);
console.log(results.time);  // in milliseconds

var temp = results.time;

var d = {begin, end, temp};
myTIME = JSON.stringify(d);
   
//////////////////END TIME//////////////////////    
    
    
    //console.log(util.inspect(mydata, false, null));
    
});
 
connection.end();



var WebSocketServer = require('websocket').server;
var http = require('http');

var server = http.createServer(function(request, response) {
  // process HTTP request. Since we're writing just WebSockets
  // server we don't have to implement anything.
});
server.listen(9898, function() { });

// create the server
wsServer = new WebSocketServer({
  httpServer: server
});

// WebSocket server
wsServer.on('request', function(request) {
  var connection = request.accept(null, request.origin);

  // This is the most important callback for us, we'll handle
  // all messages from users here.
  connection.on('message', function(message) {
    if (message.type === 'utf8') 
    {
      console.log(message.utf8Data);

      if(message.utf8Data == "LAST_ENTRY")
      {
        connection.sendUTF(myJSON[9]);
      }
      else if(message.utf8Data == "NET_TEST")
      {
        connection.sendUTF(myTIME);
        for(var i=0; i<=9; i++)
        {
          connection.sendUTF(myJSON[i]);
        }
      }
      else
      {
          console.log("UNDEFINED CLIENT REQUEST");
      }
      // process WebSocket message
    }
  });

  connection.on('close', function(connection) {
    // close user connection
  });
});
