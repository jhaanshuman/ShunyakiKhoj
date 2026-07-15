function validateDictionary(dict){

const missing = []

for (let key in dict){

let test = transliterate(key)

if(!test)
missing.push(key)

}

console.log(
"Unrenderable words:",
missing.length
)

return missing
}