var express = require('express');
var router = express.Router();
var jwt = require('jsonwebtoken')
var jwt_options = require('../auth/jwt_options')
var bcrypt = require('bcrypt')
var userController = require('../controllers/user')

/* GET users listing. */
router.post('/access', function(req, res, next) {
  //Tentar obter token de acesso
  var user_email = req.body.email
  userController.consultar_user(user_email)
    .then(async user => {
      if(!user) {
        res.render('index',{info_err: 'O email que inseriu não consta na nossa base de dados!'})
      }
        var ok = await bcrypt.compare(req.body.password,user.password)
        if(ok) {        
          //criar e dar o token de acesso
          // redirecionar para o serviço de email
          payload = {
            email: user_email,
            nome: user.nome
            }
            access_token = jwt.sign(payload,'auth_server_tokens',jwt_options.signOptions)
            userController.atualizar_token(user.email,access_token)
              .then(dados => {
                console.log(access_token)
                res.cookie('auth',access_token)
                res.redirect('http://localhost:3000/?access_token=' + access_token)
              })
              .catch(error => res.render('error',{error:error, message: 'Algo correu mal ao atualizar o token!'}))       
        } else {
          res.render('index',{info_err: 'Password não coincidem!'})
        }
    })
    .catch(error => res.render('error',{error: error, message: 'ocorreu um erro ao consultar os dados do utilizador'}))
});

router.post('/register', async (req,res) => {
  //Registar um utilizador
  var hash = await bcrypt.hash(req.body.password,10)
  req.body.password = hash
  userController.registar(req.body.email,req.body.nome,req.body.password)
    .then(data => res.render('index',{info: 'Já pode pedir tokens de acesso!'}))
    .catch(error => res.render('error',{error:error, message: 'Erro no registo!'}))
  
})

router.get('/checkToken', (req,res) => {
  access_token = req.query.access_token
  var user = jwt.verify(access_token,'auth_server_tokens',jwt_options.verifyOptions)
  if(user) {
    userController.consultar_token(user.email)
      .then(ctoken => {
        ctoken = ctoken.current_token
        if(ctoken == access_token) {
          res.jsonp({message: 'OK', user:user})
        } else {
          res.jsonp({message: 'Token não coincide',user:undefined})
        }
      })
      .catch(error => res.jsonp({message: 'ERROR: ' + error, user:undefined}))
  } else {
    res.jsonp({message: 'O token já expirou ou não é válido!', user:undefined})
  }
})

module.exports = router;
