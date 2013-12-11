/**
 * Module dependencies.
 */
var express = require('express');
var https = require('https');
var path = require('path');
var fs = require('fs');
var http = require('http');
var exec = require('child_process').exec;
var spawn = require('child_process').spawn;

var options = {
	key : fs.readFileSync('./keys/key.pem'),
	cert : fs.readFileSync('./keys/key-cert.pem')
};
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
app.get('/main', function(req, res) {
	res.render('new');
});

app.get('/', function(req, res) {
	res.redirect('main');
});

//get predictions
app.post('/main', function(req, res) {
	var str = req.body.data.split(",")[1]
	var buf = new Buffer(str, 'base64');
	fs.writeFile("hello.wav", buf, function(err) {
		if (err)
			res.send(500, {
				error : 'something blew up'
			})
		var child = exec("./recog", function(error, stdout, stderr) {
			res.send(stdout);
		});
	});
});

function writeSegment(){
	fs.writeFile("hello.wav", buf, function(err) {
		if (err)
			res.send(500, {
				error : 'something blew up'
			})
		var child = exec("./recog", function(error, stdout, stderr) {
			console.log('stdout: ' + stdout);
			res.send(stdout);
		});
	});
}

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

// Create an HTTPS service identical to the HTTP service.
var server = https.createServer(options, app)
//var server = http.createServer(app)
server.listen(app.get('port'));
var io = require('socket.io').listen(server);

io.sockets.on('connection', function(socket) {
	socket.set('id', socket.id);
	socket.set('count', 0);
	socket.emit('ready', socket.id);
	socket.on('data', function(data) {
		socket.get('id', function(err, id) {
			socket.get('count', function(err, count) {
				socket.set('count', count + 1);
				if(data == undefined) return;
				var str = data.split(",")[1]
				var buf = new Buffer(str, 'base64');

				/* without file--doesn't work yet.
				var child = spawn('python', ['-u', '../learning/predict.py']);
				child.stdin.write(str, 'base64', function(){
					child.stdin.end();
				});
				child.stdout.on('data', function(data){
				    console.log(data.toString('utf8'))
				    socket.volatile.emit('res', data)	
				});
				child.stderr.on('data', function(data){
				    console.log(data.toString('utf8'));
				});*/

				prefix = "./clientwavs/"
				name = id + count + ".wav"
				file = prefix + name
				fs.writeFile(file, buf, function(err) {
					if (err) socket.emit('res', 'something blew up')
					var child = exec("python ../learning/500test-wav.py " + file, function(error, stdout, stderr) {
						if(stdout != "[]\n"){
							socket.volatile.emit('res', stdout)
						}
					});
				});
			});
		});
	});

	socket.on('disconnect',function(){
		console.log('User Disconnect. Removing files!')
	   	socket.get('id', function(err, id){
	   		fs.readdir('./clientwavs/', function(e,files){
	   			for (var i = 0; i < files.length; i++) {
					if (!files[i].match(new RegExp('^'+id))) continue;
	   				//fs.unlink('./clientwavs/'+files[i], function(err){
	   				//	if (err) throw err;
	   				//});
	   			}
	   		})
	   	});
	 });
});
