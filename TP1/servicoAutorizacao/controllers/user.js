var user = require('../models/user')

module.exports.consultar_user = email => {
    return user.findOne({email:email}).exec()
}

module.exports.registar = (email,nome,password) => {
    var user_to_insert = {
        email: email,
        nome: nome,
        password: password,
        current_token: 'none'
    }
    return user.create(user_to_insert)
}

module.exports.consultar_token = (email) => {
    return user.findOne({email:email},{current_token:1}).exec()
}

module.exports.atualizar_token = (email,token) => {
    return user.findOne({email: email}, (err,doc) => {
        doc.current_token = token
        doc.save()
    })
}