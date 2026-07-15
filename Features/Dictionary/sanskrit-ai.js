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

if(!e) return
if(e.ctrlKey || e.metaKey) return
let box=document.getElementById("inputBox")
let suggestions=document.getElementById("suggestions")

/* BACKSPACE */
if(e.key==="Backspace"){
latinBuffer=latinBuffer.slice(0,-1)
e.preventDefault()
}

/* SPACE */
else if(e.key===" "){
latinBuffer+=" "
e.preventDefault()
suggestions.innerHTML=""
}

/* NORMAL CHARACTER */
else if(e.key.length===1){
latinBuffer+=e.key
e.preventDefault()
}
else{
return
}

/* TRANSLITERATE */
devBuffer=ime.transliterate(latinBuffer)
box.value=devBuffer

/* TOKENIZE */
slpWords=latinBuffer.trim().split(/\s+/)
let devWords=devBuffer.trim().split(/\s+/)
renderTokens(devWords)

/* SUGGESTIONS */
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
let text = await res.text()
if(!text.trim()) return
let data = JSON.parse(text)
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
    document.getElementById("suggestions").innerHTML=""
let output=""
for(let slp of slpWords){
try{
let res=await fetch("service/search.php?q="+encodeURIComponent(slp))
if(!res.ok) continue
let text = await res.text()
if(!text.trim()) continue
let data = JSON.parse(text)
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

/* launch Search*/
function addUserMessage(text){
const chat=document.getElementById("chatArea")
const msg=document.createElement("div")
msg.className="message user"
msg.innerText=text
chat.appendChild(msg)
chat.scrollTop=chat.scrollHeight
}
function addAIMessage(text){
const chat=document.getElementById("chatArea")
const msg=document.createElement("div")
msg.className="message ai"
msg.innerHTML=text
chat.appendChild(msg)
chat.scrollTop=chat.scrollHeight
}

/*Enter Button*/
document.getElementById("inputBox").addEventListener("keydown", function(e){
if(e.key === "Enter" && !e.shiftKey){
e.preventDefault()
document.getElementById("searchBtn").click()
}
})

async function sendMessage(){
const box=document.getElementById("inputBox")
const text=box.value.trim()

if(!text) return
addUserMessage(text)
box.value=""
await searchSentence()
const result=document.getElementById("result")

if(result && result.innerHTML.trim()){
addAIMessage(result.innerHTML)
}
   /* clean buffers for next input */

latinBuffer=""
devBuffer=""
slpWords=[]
 document.getElementById("suggestions").innerHTML=""
}