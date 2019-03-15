var express = require('express');
var router = express.Router();

/*
Os pedidos internos como o /checkToken e o /needAuth devem comunicar diretamente com o container
posteriormente e não pelo localhost.
Basicamente o localhost só deve escutar pedidos externos. Tudo o que seja troca de informação entre os dois
deve ser feita utilizando os nomes dos containers pela rede interna.
*/

/* GET home page. */
router.get('/', function(req, res, next) {
  // apresentar página de login ou registo
  res.render('index');
});

router.get('/needAuth', (req,res) => {
  res.render('index',{info_err: 'Autentique-se para obter um token de acesso para utilizar o serviço de email!'})
})

module.exports = router;
