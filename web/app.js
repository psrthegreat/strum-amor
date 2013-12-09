/**
 * Module dependencies.
 */
var express = require('express');
var http = require('http');
var path = require('path');
var index = require('./routes/main');
var fs = require('fs')
//for tests
//var tests = require('./routes/tests');
//add any app-specific modules below

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
app.get('/main', index.show);
app.get('/', function(req, res) {
	res.redirect('main');
});
//get predictions
app.post('/main', index.submit);

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

//create the server
http.createServer(app).listen(app.get('port'), function() {
	console.log('Express server listening on port ' + app.get('port'));
});
