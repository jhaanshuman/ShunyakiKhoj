<?php
$source = $_GET['source'] ?? 'sarit';
$metaPath = "../../../bookLibrary/meta/" . $source . ".json";
$data = json_decode(file_get_contents($metaPath), true);
?>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title><?php echo strtoupper($source); ?> Library</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&display=swap" rel="stylesheet">

<style>
html, body{
    height:100%;
}

body{
    font-family:'Poppins',sans-serif;
    margin:0;

    /* IMPORTANT: full coverage */
    min-height:100vh;

    background:
        radial-gradient(circle at 10% 50%, rgba(25,13,177,5), transparent 90%),
        radial-gradient(circle at 80% 20%, rgba(99,102,241,0.25), transparent 40%),
        radial-gradient(circle at 50% 80%, rgba(134,17,194,7), transparent 60%),
        linear-gradient(135deg,#a12af5,#e29cdf,#3ed5b2);

    background-attachment: fixed;

    color:#1e293b;
}

/* HEADER */
.header{
    position:sticky;
    top:0;
    background: linear-gradient(90deg,#f59e0b,#6366f1);
    color:white;
    padding:16px 40px;
    font-size:20px;
    font-weight:600;
    box-shadow:0 4px 15px rgba(0,0,0,0.1);
}

/* CONTROLS */
.controls{
    display:flex;
    gap:15px;
    padding:20px 40px;
}

input, select{
    padding:10px 12px;
    border-radius:10px;
    border:1px solid #ddd;
    background:white;
}

/* GRID */
.grid{
    display:grid;
    grid-template-columns: repeat(auto-fit,minmax(220px,1fr));
    gap:25px;
    padding:30px 40px;
    background: transparent !important;
}

/* BOOK CARD */
.card{
    height:160px;
    border-radius:16px;
    padding:18px;
    color:white;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    cursor:pointer;
    transition:0.4s;
    position:relative;
    overflow:hidden;
}

/* book shine */
.card::after{
    content:"";
    position:absolute;
    top:0;
    left:-100%;
    width:60%;
    height:100%;
    background: rgba(255,255,255,0.2);
    transform: skewX(-25deg);
}

.card:hover::after{
    animation: shine 0.8s;
}

@keyframes shine{
    to{
        left:150%;
    }
}

/* hover */
.card:hover{
    transform: translateY(-10px) scale(1.03);
    box-shadow:0 15px 30px rgba(0,0,0,0.2);
}

/* TEXT */
.title{
    font-size:16px;
    font-weight:600;
}

.author{
    font-size:13px;
    opacity:0.9;
}

/* SCROLL ANIMATION */
.card{
    opacity:0;
    transform: translateY(40px);
    transition:0.6s;
}

.card.show{
    opacity:1;
    transform: translateY(0);
}

/* FOOTER */
.footer{
    margin-top:60px;
    padding:30px 20px;
    text-align:center;
    font-size:13px;
    color:#475569;

    /* REAL FIX */
    background: rgba(17,15,25,5);   /* lighter */
    backdrop-filter: blur(12px);

    border-top:1px solid rgba(0,0,0,0.05);

    box-shadow: 0 -5px 20px rgba(0,0,0,0.05);
}

/* footer text spacing */
.footer p{
    margin:6px 0;
}

/* links */
.footer a{
    color:#6366f1;
    text-decoration:none;
    font-weight:500;
}

.footer a:hover{
    text-decoration:underline;
}
    
.footer::before{
    content:"";
    display:block;
    height:2px;
    width:100%;
    background: linear-gradient(90deg,#f59e0b,#6366f1,#22c55e);
    margin-bottom:15px;
    opacity:0.5;
}
</style>
</head>

<body>

<!-- HEADER -->
<div class="header">
    <div class="logo">📚 <span><?php echo strtoupper($source); ?></span> Library</div>
</div>

<!-- CONTROLS -->
<div class="controls">
    <input type="text" id="search" placeholder="🔍 Search books...">
    <select id="authorFilter">
        <option value="">All Authors</option>
    </select>
</div>

<!-- GRID -->
<div class="grid" id="grid"></div>

<!-- FOOTER -->
<div class="footer">
    <p>
        Source:
        <a href="https://github.com/sarit/SARIT-corpus" target="_blank">
            SARIT Corpus
        </a>
    </p>
    <p>
        Content belongs to respective contributors. Used for educational purposes.
    </p>
    <br>
    <p>✨ Created and Designed by <b>Anshuman Jha</b></p>
</div>

<script>
const books = <?php echo json_encode($data['books']); ?>;

const grid = document.getElementById("grid");
const search = document.getElementById("search");
const authorFilter = document.getElementById("authorFilter");

// Populate authors
const authors = [...new Set(books.map(b => b.author).filter(a => a))];
authors.forEach(author=>{
    let opt = document.createElement("option");
    opt.value = author;
    opt.textContent = author;
    authorFilter.appendChild(opt);
});

const colors = [
    "linear-gradient(135deg,#f97316,#facc15)",   // orange-yellow
    "linear-gradient(135deg,#3b82f6,#06b6d4)",   // blue-cyan
    "linear-gradient(135deg,#22c55e,#4ade80)",   // green
    "linear-gradient(135deg,#a855f7,#6366f1)",   // purple-indigo
    "linear-gradient(135deg,#ef4444,#f97316)",   // red-orange
    "linear-gradient(135deg,#14b8a6,#22c55e)"    // teal-green
];

function render(){
    const query = search.value.toLowerCase();
    const author = authorFilter.value;

    grid.innerHTML = "";

    books
    .filter(book=>{
        return (
            (!query || book.title.toLowerCase().includes(query)) &&
            (!author || book.author === author)
        );
    })
    .forEach((book,index)=>{

        const div = document.createElement("div");
        div.className = "card";
        div.style.background = colors[index % colors.length];

        div.innerHTML = `
            <div class="title">${book.title}</div>
            <div class="author">✍ ${book.author || "Unknown"}</div>
        `;

        div.onclick = ()=>{
            window.location.href = "reader.php?source=<?php echo $source; ?>&file=" + book.file;
        };

        grid.appendChild(div);
    });

    animateCards();
}

/* SCROLL ANIMATION */
function animateCards(){
    const cards = document.querySelectorAll(".card");

    const observer = new IntersectionObserver(entries=>{
        entries.forEach(entry=>{
            if(entry.isIntersecting){
                entry.target.classList.add("show");
            }
        });
    },{threshold:0.1});

    cards.forEach(card=>observer.observe(card));
}

// Events
search.addEventListener("input", render);
authorFilter.addEventListener("change", render);

// Initial render
render();
</script>

</body>
</html>