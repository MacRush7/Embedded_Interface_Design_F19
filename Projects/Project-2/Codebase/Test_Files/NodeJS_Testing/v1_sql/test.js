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
 
connection.query(queryString, function(err, rows, fields) {
    if (err) throw err;
 
    for (var i in rows) {
        console.log(rows[i]);
    }
});
 
connection.end();

// Source - https://www.codediesel.com/nodejs/querying-mysql-with-node-js/
// Source - https://www.npmjs.com/package/mysql#establishing-connections
// Source - https://www.npmjs.com/package/mysql#establishing-connections
