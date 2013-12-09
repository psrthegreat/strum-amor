
/*
 * GET home page.
 */

exports.show = function(req, res){
  res.render('main');
};

exports.submit = function(req, res){
    fs.write("hello.wav", req.params.body, function(err){
        if(err) console.log(err);
    });
    res.end();
};
