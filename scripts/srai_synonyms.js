moby = require('moby') 
fs = require('fs')
process = require('process')

const path = process.argv[2]
let data = JSON.parse(fs.readFileSync(path))

for (let k in data.aiml.category){
  let synonymns = moby.search(k)
  for (let w in synonymns) data['aiml']['category'][k]['srai'].push(synonymns[w])
}

fs.writeFileSync(process.argv[2],JSON.stringify(data,null,2))