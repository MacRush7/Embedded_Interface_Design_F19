var mydata;
var lastJSON;
var myJSON_out = []; 
var myTIME;
var len;
var last_val;

my2obj = new Object();
my2obj.Readings = 1000;
my2obj.Temperature = 0;
my2obj.Humidity = 0;
my2obj.Updated = 0;

var myobj = JSON.stringify(my2obj);


var mode1 = "LAST_ENTRY"; //mode1 for sending data to the client
var mode2 = "NET_TEST"; //mode2 for sending 10 data to the client

var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'poorn',
  password : 'root',
  database : 'EID_Project1_DB'
});
 
connection.connect(function(err) {
  if (err) {
    console.error('error connecting: ' + err.stack);
    return;
  }
 
  console.log('connected as id ' + connection.threadId);
});
 
var queryString = 'SELECT * FROM DHT22_Table';


//////////////////START TIME//////////////////////
const perf = require('execution-time')();

//at beginning of your code, pass any name
//var begin = new Date();
//perf.start('apiCall');


function Poll_DB() {
  connection.query(queryString, function(err, rows, fields) {
    
      if (err) throw err;
  
      //at beginning of your code, pass any name
      var begin = new Date();
      perf.start('apiCall');
      
      var i, j;
      
      len = rows.length;
      mydata = rows[len - 1];
      lastJSON = JSON.stringify(mydata);
      
      if(len < 10) {
        for(i = 0; i < len; i ++) {
          mydata = rows[i];
          myJSON_out[i] = JSON.stringify(mydata);
        }
        for(j = i; j < 10; j ++) {
          myJSON_out[j] = myobj;
        }
      }
      else {
        for(i = (len - 10), j = 0; i < len; i ++, j ++) {
          mydata = rows[i];
          myJSON_out[j] = JSON.stringify(mydata);
        }
      }


    //at end of your code, pass the same name (anywhere in your flow)
    const results = perf.stop('apiCall');
    var end = new Date();

    var exec = results.time;
    var t_flt = parseFloat(exec);
    t_flt = t_flt * 1000;
    exec = t_flt.toFixed(3);

    var d = {begin, end, exec};
    myTIME = JSON.stringify(d);
       
    //////////////////END TIME//////////////////////    

      
  });
  
}

setInterval(Poll_DB, 4000);
 
//connection.end();



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
        connection.sendUTF(lastJSON);
      }
      else if(message.utf8Data == "NET_TEST")
      {
        connection.sendUTF(myTIME);
        for(var i = 0; i < 10; i ++)
        {
          connection.sendUTF(myJSON_out[i]);
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
