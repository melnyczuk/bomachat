js2xmlparser = require("js2xmlparser")
fs = require('fs')
process = require('process')

file_path = process.argv[2]
data = JSON.parse(fs.readFileSync(file_path))

let obj = {}
obj.aiml = {}
obj.aiml.category = []

for(let k in data.aiml.category){
  let cat = {}
  cat.pattern = k
  cat.template = data.aiml.category[k].template
  obj.aiml.category.push(cat)

  for (let s in data.aiml.category[k].srai) {
    if (data.aiml.category[k].srai[s].toUpperCase() !== k){
      let srai = {}
      srai.pattern = data.aiml.category[k].srai[s].toUpperCase()
      srai.template = {}
      srai.template.srai = k
      obj.aiml.category.push(srai)
    }
  }
}

const xml = js2xmlparser.parse('aiml', obj.aiml)
save(file_path,xml)


function save(name,data){
  name = name.split("\\").pop()
  name = name.split(".")[0]
  name = name + ".xml"
  fs.writeFileSync(name,data)
  console.log(name)
}
