/**
 * Dynamic View Builder for Monier-Williams Sanskrit AI Dictionary
 */
function renderDictionaryView() {
    return `
    <div id="dictionaryViewContainer">
        <header>
            <div class="logo">
                <img src="./logo.png">
                <span>Sanskrit AI</span>
            </div>
        </header>
        <main>

<div id="chatArea"></div>

<div id="result" style="display:none"></div>
<div id="tokens"></div>
<div id="suggestions"></div>

<div class="inputPanel">

<textarea id="inputBox"
placeholder="Type Sanskrit (English phonetic)"
onkeydown="handleInput(event)"></textarea>

<button id="searchBtn" onclick="sendMessage()">Search</button>

</div>

</main>

<div id="guideButton" onclick="toggleGuide()">⌨ Typing Help</div>

<div id="guideWindow">

<div class="guideHeader">
<span>Sanskrit Typing Guide</span>
<button onclick="toggleGuide()">✕</button>
</div>

<div class="guideContent" id="guideContent"></div>

</div>
    </div>
    `;
}
