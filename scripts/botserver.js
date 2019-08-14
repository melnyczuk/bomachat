express = require('express')
cors = require('cors')
bodyParser = require('body-parser')
process = require('process')
fs = require('fs')
aimlHigh = require('aiml-high')
moby = require('moby')
hunspell = require('nodehun-sentences')

let answer
const app = express()
app.use(cors())
app.use(bodyParser.json());
const xmldir = './xml/'
const bot = new aimlHigh({name:'Bomachat'}, 'hello');
const aimlfiles = []
fs.readdirSync(xmldir).forEach(file => {aimlfiles.push(xmldir + file)});
bot.loadFiles(aimlfiles)
console.log('AIML files loaded')

app.post('/chat', (req,res) => getAnswer(req).then(res.send(answer)))
app.listen(5000, () => console.log('Example app listening on port 5000!'))

function getAnswer(request) {
  return new Promise((resolve,reject) => {
    request = request.body.body.trim()
    // request = checkSpelling(request)
    bot.findAnswer(request,(result, wildCardArray, input) =>  answer = result)
  })
}

function checkSpelling(request){
  request = hunspell.check(request)
  console.log(request)
  return request
}