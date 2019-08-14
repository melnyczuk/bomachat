xml2js = require('xml2js')
fs = require('fs')
process = require('process')

let data;
const xmlpath = process.argv[2]
const xml = fs.readFileSync(xmlpath, "utf-8")
xml2js.parseString(xml, function (err, result) { 
  try { data = result } 
  catch(err) { throw err; process.exit() } 
});
// console.log(data)
let o = {}
o.aiml = {}
o.aiml.category = {}
for (let i in data.aiml.category){
  const patterns = data.aiml.category[i].pattern[0].split('\n')
  for (let p in patterns) if (patterns[p].trim().length < 1) patterns.splice(p,1)
  let call = patterns.reverse().pop().toUpperCase().replace('\n','').trim()
  let reply = data.aiml.category[i].template[0]
  if (!o.aiml.category.hasOwnProperty(call)) {
    o.aiml.category[call] = {}
    o.aiml.category[call].template = {}
    o.aiml.category[call].template.random = []
    o.aiml.category[call].template.random[0] = {}
    o.aiml.category[call].template.random[0].li = []
    o.aiml.category[call].srai = []
  }
  if (!reply.hasOwnProperty('random')) reply = {'random':[{'li':[reply.replace("â€™", "'")]}]}
  for (let li in reply.random[0].li) o.aiml.category[call].template.random[0].li.push(reply.random[0].li[li].replace("'", "'"))
  for (let si in data.aiml.category[i].srai) o.aiml.category[call].srai.push(data.aiml.category[i].srai[si].toUpperCase().replace('\n','').replace("â€™", "'").trim())
  if (patterns.length > 0) for (let p in patterns) o.aiml.category[call].srai.push(patterns[p].replace("â€™", "'"))
}

link_srai(o)
writejson(xmlpath,o)

function writejson(name,obj) {
  name = name.split("\\").pop()
  name = name.split(".")[0]
  name = "./json/" + name + ".json"
  fs.writeFileSync(name, JSON.stringify(obj,null,2))
  console.log(name)
}

function link_srai(obj) {
  const keys = []
  for (let key in obj.aiml.category) keys.push(key.toUpperCase().replace('\n','').trim())
  for (let pattern in obj.aiml.category){
    if (obj.aiml.category[pattern].template.hasOwnProperty('srai')){
      for (let s in obj.aiml.category[pattern].template.srai){
        if (keys.includes(obj.aiml.category[pattern].template.srai[s].toUpperCase().replace('\n','').trim())){            
          let srai = obj.aiml.category[pattern].template.srai[s].toUpperCase().replace('\n','').trim()
          obj.aiml.category[srai].srai.push(pattern.toUpperCase().replace('\n','').replace("â€™", "'").trim())
          delete obj.aiml.category[call]
        }
      }
    }
  }
}

function filter(str){
  return str.replace("â€™", "'")
}