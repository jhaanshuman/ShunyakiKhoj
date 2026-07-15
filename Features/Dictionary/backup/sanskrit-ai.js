/* =============================
   PAGE NAVIGATION
============================= */

function showPage(page){

document.getElementById("featuresPage").style.display="none"
document.getElementById("dictionaryPage").style.display="none"

if(page==="features")
document.getElementById("featuresPage").style.display="block"

if(page==="dictionary")
document.getElementById("dictionaryPage").style.display="block"

}


/* =============================
   SANSKRIT IME
============================= */

class SanskritIME {

transliterate(text){

let result=""
let i=0

while(i<text.length){

let three=text.substring(i,i+3)
let two=text.substring(i,i+2)
let one=text.substring(i,i+1)

if(SanskritMap[three]){
result+=SanskritMap[three]
i+=3
continue
}

if(SanskritMap[two]){
result+=SanskritMap[two]
i+=2
continue
}

if(SanskritMap[one]){
result+=SanskritMap[one]
i++
continue
}

result+=one
i++

}

return result

}

}

const ime=new SanskritIME()


/* =============================
   GLOBALS
============================= */

let latinBuffer=""
let devBuffer=""
let slpWords=[]

let selectedToken=null


/* =============================
   INPUT HANDLER
============================= */

function handleInput(e){

let box = document.getElementById("inputBox")
let suggestions = document.getElementById("suggestions")

if(!box) return

// get full typed text
let text = box.value

// keep latin buffer
latinBuffer = text

// transliterate
devBuffer = ime.transliterate(latinBuffer)

// update input with devanagari
box.value = devBuffer


// split words
slpWords = latinBuffer.trim().split(/\s+/)
let devWords = devBuffer.trim().split(/\s+/)


// render tokens
renderTokens(devWords)


// update suggestions
updateSuggestions()

}

/* =============================
   FETCH SUGGESTIONS
============================= */

async function updateSuggestions(){

let prefix=latinBuffer.trim().split(/\s+/).pop()

if(!prefix) return

try{

let res=await fetch("service/search.php?q="+encodeURIComponent(prefix))

if(!res.ok) return

let data=await res.json()

let box=document.getElementById("suggestions")
box.innerHTML=""

data.forEach(item=>{

let div=document.createElement("div")

let dev=ime.transliterate(item.word)

div.className="suggestionItem"

div.innerHTML="<b>"+dev+"</b> — "+item.word

div.onclick=function(){

latinBuffer=latinBuffer.replace(/\S+$/,item.word)+" "

devBuffer=ime.transliterate(latinBuffer)

document.getElementById("inputBox").value=devBuffer

box.innerHTML=""

slpWords=latinBuffer.trim().split(/\s+/)

let devWords=devBuffer.trim().split(/\s+/)

renderTokens(devWords)

}

box.appendChild(div)

})

}catch(err){

console.log("Suggestion error",err)

}

}


/* =============================
   TOKEN RENDER
============================= */

function renderTokens(words){

let box=document.getElementById("tokens")

box.innerHTML=""

words.forEach((word,i)=>{

if(!word) return

let span=document.createElement("span")

span.className="token"

span.innerText=word

span.onclick=function(){

document.querySelectorAll(".token")
.forEach(t=>t.classList.remove("selectedToken"))

span.classList.add("selectedToken")

selectedToken=i

showWordMeaning(i)

}

box.appendChild(span)

})

}


/* =============================
   SHOW WORD MEANING
============================= */

async function showWordMeaning(indexPos){

let slp=slpWords[indexPos]

if(!slp) return

try{

let res=await fetch("service/search.php?q="+encodeURIComponent(slp))

if(!res.ok) return

let data=await res.json()

if(!data.length) return

let dev=ime.transliterate(slp)

let output="<b>"+dev+"</b> ("+slp+")<ul>"

data.forEach(row=>{
output+="<li>"+row.meaning+"</li>"
})

output+="</ul>"

document.getElementById("result").innerHTML=output

}catch(err){

console.log("Lookup error",err)

}

}


/* =============================
   SEARCH SENTENCE
============================= */

async function searchSentence(){

let output=""

for(let slp of slpWords){

try{

let res=await fetch("service/search.php?q="+encodeURIComponent(slp))

if(!res.ok) continue

let data=await res.json()

if(!data.length) continue

let dev=ime.transliterate(slp)

output+="<b>"+dev+"</b> ("+slp+")<ul>"

data.forEach(row=>{
output+="<li>"+row.meaning+"</li>"
})

output+="</ul>"

}catch(e){

console.log("Search error",e)

}

}

document.getElementById("result").innerHTML=output

}


/* =============================
   HIDE SUGGESTIONS OUTSIDE
============================= */

document.addEventListener("click",function(e){

let input=document.getElementById("inputBox")
let suggestions=document.getElementById("suggestions")

if(!input.contains(e.target) && !suggestions.contains(e.target))
suggestions.innerHTML=""

})


/* =============================
   PASTE HANDLER
============================= */

document.getElementById("inputBox").addEventListener("paste",function(e){

setTimeout(function(){

latinBuffer=e.target.value

devBuffer=ime.transliterate(latinBuffer)

e.target.value=devBuffer

},10)

})