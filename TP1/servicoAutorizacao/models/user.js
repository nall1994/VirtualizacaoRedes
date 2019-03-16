var mongoose = require('mongoose')
var Schema = mongoose.Schema
var bcrypt = require('bcrypt')

var UserSchema = new Schema({
    email: {type:String, required:true,unique:true},
    nome: {type:String, required:true},
    password: {type:String, required:true},
    current_token: String
})

module.exports = mongoose.model('user',UserSchema,'users')