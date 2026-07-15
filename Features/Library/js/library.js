const search=document.getElementById("search")

if(search){

search.addEventListener("keyup",function(){

let value=this.value.toLowerCase()

document.querySelectorAll("[data-title]").forEach(tile=>{

let title=tile.dataset.title

if(title.includes(value))
tile.style.display="block"
else
tile.style.display="none"

})

})

}