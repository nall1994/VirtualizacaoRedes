var express = require('express');
var router = express.Router();
var axios = require('axios')

/* GET home page. */
router.get('/', function(req, res, next) {
  // Verificar se o utilizador tem um token válido!
  if(req.cookies.auth) {
    access_token = req.cookies.auth
    req.query.access_token = access_token
    axiosConfig = {
      params: req.query
    }
    axios.get('http://localhost:3001/users/checkToken',axiosConfig)
      .then(dados => {
        dados = dados.data
        if(dados.message == 'OK') {
          var user = dados.user
          res.render('index');
        } else {
          res.render('auth')
          //token não existe ou não é válido, fazer outra coisa
        }
      })
      .catch(error => res.render('error',{error: error, message: 'Ocorreu um erro ao verificar o token!'}))
  } else {
    res.render('auth')
  }
   
});

router.post('/enviar',(req,res) => {

})

module.exports = router;
