
/*
 * GET home page.
 */

exports.show = function(req, res){
  res.render('main', { title: 'Strum-Amor', author: 'Pranav' });
};

exports.submit = function(req, res){
    //res.send('main');
};
