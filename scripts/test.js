aimlHigh = require('aiml-high');
var interpreter = new aimlHigh({name:'Bot', age:'42'}, 'Goodbye');
interpreter.loadFiles(['./bot/boma-hello.xml', "./bot/boma-user.xml"]);

function ponder(request){
  return new Promise(
    resolve => {interpreter.findAnswer( request, function(answer, wildCardArray, input){ resolve(answer)})},
    reject => {reject('error')}
  )
}

const talk = async (request) => {
  return await ponder(request)
    .then(function(response){return response})
    .catch(function(e){return e})
}

export default talk;