var users = require('./user');

//meant to test whether or not the user database works.
exports.clearUsers = function(req, res) {
	users.removeAll(function(err, result) {
		if (err)
			console.log('error')
		res.send("removed All")
	})
}

exports.showUsers = function(req,res){
	users.getAll(function(err, result) {
				if (err)
					console.log('error')
				res.send(JSON.stringify(result))
			});
}