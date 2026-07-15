function toggleGuide(){

const guide =
document.getElementById("guideWindow")

if(guide.style.display==="block"){

guide.style.display="none"
return

}

guide.style.display="block"

renderGuide()

}

function renderGuide(){

const container =
document.getElementById("guideContent")

container.innerHTML=""

MWGuide.sections.forEach(section=>{

const block=document.createElement("div")

block.innerHTML=

"<h3>"+section.title+"</h3>"+
"<pre>"+section.content+"</pre>"

container.appendChild(block)

})

}