<!doctype html>
<html>
  <head>
    <title>Node.js server - HTML client - Websocket Service Page</title>
    <meta charset="utf-8" />
    <style type="text/css">
      body {
        text-align: center;
        min-width: 500px;
      }
    </style>
    <script src="http://code.jquery.com/jquery.min.js"></script>
    <script>
 
      // log function
      log = function(data){
        $("div#terminal").prepend("</br>" +data);
        console.log(data);
      };
 
      $(document).ready(function () {
 
        var ws;
 
          // create websocket instance
		  ws = new WebSocket("ws://192.168.50.111:9898/");

          // Open Websocket callback
          ws.onopen = function(evt) { 
            log("***Connection Opened***");
          };
           
          // Handle incoming websocket message callback
          ws.onmessage = function(evt) {
            log("Message Received: " + evt.data);
            alert("message received: " + evt.data);
			$("#Tornado_Immediate").html(evt.data);
            };
 
          // Close Websocket callback
          ws.onclose = function(evt) {
            log("***Connection Closed***");
            alert("Connection close");
            $("#host").css("background", "#ff0000"); 
            $("#port").css("background", "#ff0000"); 
            $("#uri").css("background",  "#ff0000");
            $("div#message_details").empty();
 
            };
 
        // Send websocket message function
        $("#Get_Single_Tornado").click(function(evt) {
        
        //log("Sending Message: DHT22_DATA_TSTAMP");
		ws.send("DHT22_DATA_TSTAMP");
        });
		
        $("#Change_Unit").click(function(evt) {
            //log("Sending Message: FLIP_UNIT");
			ws.send("FLIP_UNIT");
        });
 
      });
    </script>
  </head>
 
  <body>
    <h1>Node.js server - HTML client - Websocket Service Page</h1>
    <div id="message_details">
        </br></br>
		<button type="button" id="Get_Single_Tornado">Last data entry via Node.js</button>
        <button type="button" id="Change_Unit">Flip Unit</button>
    </div>
	<br/><b>Immediate Data from DHT22 via Node.js</b>
	<p id="Tornado_Immediate"></p>
    <div id="terminal">
        
    </div>
  </body>
</html>
