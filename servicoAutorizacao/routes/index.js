var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  // apresentar página de login ou registo
  res.render('index');
});

router.get('/checkToken',(req,res) => {
  token_received = req.query.token
})

module.exports = router;
