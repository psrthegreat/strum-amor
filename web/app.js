/**
 * Module dependencies.
 */
var express = require('express');
var https = require('https');
var path = require('path');
var fs = require('fs');
var http = require('http');
var exec = require('child_process').exec;


var options = {
  key: fs.readFileSync('./keys/key.pem'),
  cert: fs.readFileSync('./keys/key-cert.pem')
};

//for tests
//var tests = require('./routes/tests');


var app = express();

// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
//app.use(require('stylus').middleware(__dirname + '/public'));
app.use(express.static(path.join(__dirname, 'public')));


// When in development mode, use the error handler
if ('development' == app.get('env')) {
	app.use(express.errorHandler());
}

//app.router should always be last
app.use(app.router);

//Logins
app.get('/main', function(req, res){
	 res.render('main');
});

app.get('/', function(req, res) {
	res.redirect('main');
});

//get predictions
app.post('/main', function(req, res){
	var str = req.body.data.split(",")[1]
	var buf = new Buffer(str, 'base64'); // Ta-da
	fs.writeFile("hello.wav", buf, function(err){
        if(err) res.send(500, { error: 'something blew up' })
        var child = exec("pwd", function (error, stdout, stderr) {
			console.log('stdout: ' + stdout);
			res.send(stdout);
		});
    });
});

//app specific gets here

var executeTests = false;

if (executeTests) {
	//tests only during development only
	if ('development' == app.get('env')) {
	}
	//tests during production require a password
	else if ('production' == app.get('env')) {
		var auth = express.basicAuth(function(user, pass, callback) {
			var result = (user === 'psr' && pass === 'psr2');
			callback(null/* error */, result);
		});
		app.get('/testusers', auth, tests.testUser);
	}
}

//if the page does not exist
app.get("*", function(req, res) {
	res.status(404).send('Not found dude');
});


/*
// Create an HTTP service.
http.createServer(app).listen(app.get('port'), function() {
	console.log('Express server listening on port ' + app.get('port'));
});
*/
// Create an HTTPS service identical to the HTTP service.
https.createServer(options, app).listen(app.get('port'));
