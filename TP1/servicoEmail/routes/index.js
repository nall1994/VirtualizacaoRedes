var express = require('express');
var router = express.Router();
var axios = require('axios')
var nodemailer = require('nodemailer')

/*
Os pedidos internos como o /checkToken e o /needAuth devem comunicar diretamente com o container
posteriormente e não pelo localhost.
Basicamente o localhost só deve escutar pedidos externos. Tudo o que seja troca de informação entre os dois
deve ser feita utilizando os nomes dos containers pela rede interna.
*/

/* GET home page. */
router.get('/', function(req, res, next) {
  // Verificar se o utilizador tem um token válido!
  if(req.query.access_token) {
    access_token = req.query.access_token
    axiosConfig = {
      params: req.query
    }
    axios.get('http://tp1_servicoauth_1:3001/users/checkToken',axiosConfig)
      .then(dados => {
        dados = dados.data
        if(dados.message == 'OK') {
          var user = dados.user
          console.log(user)
          res.render('index',{user:user})
        } else {
          // need authentication
          res.redirect('http://localhost:3001/needAuth')
        }
      })
      .catch(error => res.render('error',{error:error, message: 'Ocorreu um erro ao verificar o token!'}))
  } else if(req.cookies.auth) {
    access_token = req.cookies.auth
    req.query.access_token = access_token
    axiosConfig = {
      params: req.query
    }
    axios.get('http://tp1_servicoauth_1:3001/users/checkToken',axiosConfig)
      .then(dados => {
        dados = dados.data
        if(dados.message == 'OK') {
          var user = dados.user
          res.render('index',{user:user});
        } else {
          //need authentication
          res.redirect('http://localhost:3001/needAuth')
        }
      })
      .catch(error => res.render('error',{error: error, message: 'Ocorreu um erro ao verificar o token!'}))
  } else {
    //need authentication
    res.redirect('http://localhost:3001/needAuth')
  }
   
});

router.post('/enviar',(req,res) => {
  var recetor = req.body.receiveremail
  var subject = req.body.subject
  var message = req.body.message

  var transport = nodemailer.createTransport({
    host: 'tp1_servidorEmail_1',
    port: 25,
    secure: false, // upgrade later with STARTTLS
    auth: {
      user: "username",
      pass: "password"
    }
  })

  const mailOptions = {
    from: 'no-reply@vrg5.gcom.di.uminho.pt',
    to: 'bmfd.carvalho@gmail.com',
    subject: subject,
    text: message
  };

  var message_send = {
    from: 'nl@vr-5.gcom.di.uminho.pt',
    to: recetor,
    subject: subject,
    text: message
  }

  transport.sendMail(mailOptions, function(error,info){
    if (error) {
      console.log(error);
    } else {
      console.log('Email sent: ' + info.response);
    }
    res.redirect('http://localhost:3000/')
  }) 

})

module.exports = router;
