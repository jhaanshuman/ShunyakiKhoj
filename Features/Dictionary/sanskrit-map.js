/* ========================================= MW Sanskrit Transliteration Engine
Compatible with Monier-Williams dictionary===================================== */

const SanskritMap = {}

/* VOWELS */
const vowels = {
a:"अ",A:"आ",i:"इ",I:"ई",u:"उ",U:"ऊ",f:"ऋ",F:"ॠ",x:"ऌ",X:"ॡ",e:"ए",E:"ऐ",o:"ओ",O:"औ"
}

/* DIACRITICS */
const diacritics = { M:"ं", H:"ः", "~":"ँ"}

/* MATRAS */
const matra = {
a:"",A:"ा",i:"ि",I:"ी",u:"ु",U:"ू",f:"ृ",F:"ॄ",x:"ॢ",X:"ॣ",e:"े",E:"ै",o:"ो",O:"ौ"
}

/* CONSONANTS */
const consonants = {
"k":"क्","Kh":"ख्","g":"ग्","Gh":"घ्","N":"ङ्",
"c":"च्","Ch":"छ्","j":"ज्","Jh":"झ्","Y":"ञ्",
"w":"ट्","W":"ठ्","q":"ड्","Q":"ढ्","R":"ण्",
"t":"त्","Th":"थ्","d":"द्","Dh":"ध्","n":"न्",
"p":"प्","Ph":"फ्","b":"ब्","Bh":"भ्","m":"म्",
"y":"य्","r":"र्","l":"ल्","v":"व्",
"S":"श्","z":"ष्","s":"स्","h":"ह्"
}


/* SPECIAL LIGATURES */

const ligatures = {kz:"क्ष",jY:"ज्ञ",tr:"त्र",Sr:"श्र"}

/* BASE VOWELS */
for (let v in vowels)
SanskritMap[v] = vowels[v]

/* CONSONANTS */
for (let c in consonants)
SanskritMap[c] = consonants[c]

/* DIACRITICS */
for (let d in diacritics)
SanskritMap[d] = diacritics[d]

/* CONSONANT + VOWEL */
for (let c in consonants){for (let v in vowels){
    let base = consonants[c].replace("्","")
    SanskritMap[c+v] = base + matra[v]
}}

/* SPECIAL LIGATURES */
for (let l in ligatures)
SanskritMap[l] = ligatures[l]

for (let l in ligatures){  for (let v in vowels){
SanskritMap[l+v] = ligatures[l] + matra[v]
}
}

console.log("MW Sanskrit Map Size:", Object.keys(SanskritMap).length)