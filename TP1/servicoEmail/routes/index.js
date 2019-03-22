var express = require('express');
var router = express.Router();
var axios = require('axios')
var smtp_client = require('smtp-client')

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
    axios.get('http://servicoAuth_1:3001/users/checkToken',axiosConfig)
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
    axios.get('http://servicoAuth_1:3001/users/checkToken',axiosConfig)
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
  var data = subject + '\n' + message

  s = new smtp_client.SMTPClient({
    host: 'servidorEmail',
    port: 25
  })

  async () => {
    await s.connect()
    await s.greet({hostname: 'serviço de email'})
    await s.mail({from: 'vr-5.gcom.di.uminho.pt'})
    await s.rcpt({to: recetor})
    await s.data(data)
    await s.quit()
  }

  res.redirect('/index')
})

module.exports = router;
