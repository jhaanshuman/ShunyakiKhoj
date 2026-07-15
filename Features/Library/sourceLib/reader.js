let currentPage = 0;
let currentChapter = null;
let chapterVerses = [];

const VERSES_PER_PAGE = 6;

/* INIT */
function initReader(){
    loadChapter(0, 0); // first chapter
}

/* LOAD CHAPTER */
function loadChapter(partIndex, chapterIndex){

    const pageEl = document.getElementById("page");
    const progressInterval = startProgress();

    pageEl.classList.add("fold");

    setTimeout(()=>{

        let chapter = book.parts[partIndex].chapters[chapterIndex];

        currentChapter = { partIndex, chapterIndex };
        chapterVerses = chapter.verses;

        renderPage();

        // finish progress
        clearInterval(progressInterval);
        document.getElementById("progressBar").style.width = "100%";

        setTimeout(()=>{
            document.getElementById("progressContainer").style.display = "none";
        }, 400);

        // unfold
        pageEl.classList.remove("fold");
        pageEl.classList.add("unfold");

        setTimeout(()=>{
            pageEl.classList.remove("unfold");
        }, 600);

    }, 300);

    document.getElementById("sidebar").classList.remove("active");
}

/* CREATE VERSE */
function createVerseHTML(v){
    return `
    <div class="verse-block" data-id="${v.id}">
        <div class="verse-id">${v.id}</div>
        ${v.lines.map(l=>`<div class="verse">${l}</div>`).join("")}
    </div>`;
}

/* GET PAGE VERSES */
function getPageVerses(page){
    let start = page * VERSES_PER_PAGE;
    let end = start + VERSES_PER_PAGE;

    return chapterVerses.slice(start, end);
}

/* RENDER PAGE */
function renderPage(){
    // build full chapter content
    let html = chapterVerses.map(v => createVerseHTML(v)).join("");
    document.getElementById("content").innerHTML = html;
    // get current part & chapter details
    let part = book.parts[currentChapter.partIndex];
    let chapter = part.chapters[currentChapter.chapterIndex];
    // update indicator (clean + informative)
    document.getElementById("pageInfo").innerText =
        `${part.part} • ${chapter.name} (Chapter ${chapter.chapter})`;
    // attach interactions
    attachVerseClick();
}

function startProgress(){
    let bar = document.getElementById("progressBar");
    let width = 0;
    bar.style.width = "0%";
    let interval = setInterval(()=>{
        if(width >= 90){
            clearInterval(interval);
        } else {
            width += 5;
            bar.style.width = width + "%";
        }
    }, 100);
    return interval;
}

/* NAVIGATION */
function nextPage(){
    goToNextChapter();
}

function prevPage(){
    goToPrevChapter();
}

function goToNextChapter(){

    let { partIndex, chapterIndex } = currentChapter;
    let part = book.parts[partIndex];

    if(chapterIndex < part.chapters.length - 1){
        loadChapter(partIndex, chapterIndex + 1);
        return;
    }

    if(partIndex < book.parts.length - 1){
        loadChapter(partIndex + 1, 0);
    }
}

function goToPrevChapter(){
    let { partIndex, chapterIndex } = currentChapter;
    if(chapterIndex > 0){
        loadChapter(partIndex, chapterIndex - 1);
        return;
    }
    if(partIndex > 0){
        let prevPart = book.parts[partIndex - 1];
        let lastChapterIndex = prevPart.chapters.length - 1;

        loadChapter(partIndex - 1, lastChapterIndex);
    }
}


/* SCROLL */
//document.addEventListener("wheel", e=>{if(e.deltaY > 0) nextPage();else prevPage();});

/* SIDEBAR */
function toggleSidebar(){
    const s = document.getElementById("sidebar");
    s.classList.toggle("active");

    if(s.classList.contains("active")){
        s.innerHTML = buildChapterList();
    }
}

/* MODERN CHAPTER LIST */
function buildChapterList(){
    let html = "";

    book.parts.forEach((p,pi)=>{

        html += `<div class="part-title">${p.part}</div>`;

        p.chapters.forEach((c,ci)=>{
            html += `
            <div class="chapter-btn" onclick="loadChapter(${pi},${ci})">
                <div class="chapter-title">${c.name} ${c.chapter}</div>
            </div>`;
        });
    });

    return html;
}

/* SOUND */
function playFlip(){
    let a = document.getElementById("flipSound");
    if(a){
        a.currentTime = 0;
        a.play();
    }
}

/* BOOKMARK */
let bookmarkMode = false;
let bookmarks = JSON.parse(localStorage.getItem("bookmarks") || "[]");

function attachVerseClick(){
    document.querySelectorAll(".verse-block").forEach(el=>{
        el.onclick = ()=>{
            if(!bookmarkMode) return;

            el.classList.add("selected");

            bookmarks.push({
                id: el.getAttribute("data-id"),
                text: el.innerText
            });

            localStorage.setItem("bookmarks", JSON.stringify(bookmarks));

            bookmarkMode = false;
            alert("Bookmarked!");
        };
    });
}

function activateBookmark(){
    bookmarkMode = true;
    alert("Click a verse to bookmark");
}

/* SEARCH (within chapter) */
function searchText(){
    let q = prompt("Search:");
    if(!q) return;

    let index = chapterVerses.findIndex(v =>
        v.lines.join(" ").toLowerCase().includes(q.toLowerCase())
    );

    if(index >= 0){
        currentPage = Math.floor(index / VERSES_PER_PAGE);
        renderPage();
    } else {
        alert("Not found in this chapter");
    }
}

/* DARK MODE */
function toggleDark(){
    document.body.classList.toggle("dark");
}

/* INIT */
initReader();