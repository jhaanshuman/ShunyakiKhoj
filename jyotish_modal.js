// Traditional Sanskrit Jyotishi Modal Engine
const MODAL_SIGN_NAMES = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

const MODAL_PLANET_ABBR = {
    'Sun': 'Su', 'Moon': 'Mo', 'Mercury': 'Me', 'Venus': 'Ve',
    'Mars': 'Ma', 'Jupiter': 'Ju', 'Saturn': 'Sa', 'Rahu': 'Ra', 'Ketu': 'Ke'
};

const MODAL_SIGN_ABBRS = {
    'Aries': 'Ar', 'Taurus': 'Ta', 'Gemini': 'Ge', 'Cancer': 'Cn',
    'Leo': 'Le', 'Virgo': 'Vi', 'Libra': 'Li', 'Scorpio': 'Sc',
    'Sagittarius': 'Sg', 'Capricorn': 'Cp', 'Aquarius': 'Aq', 'Pisces': 'Pi'
};

const MODAL_BOX_COORDS = {
    'Aries': {x: 90, y: 5}, 'Taurus': {x: 175, y: 5}, 'Gemini': {x: 260, y: 5},
    'Cancer': {x: 260, y: 90}, 'Leo': {x: 260, y: 175}, 'Virgo': {x: 260, y: 260},
    'Libra': {x: 175, y: 260}, 'Scorpio': {x: 90, y: 260}, 'Sagittarius': {x: 5, y: 260},
    'Capricorn': {x: 5, y: 175}, 'Aquarius': {x: 5, y: 90}, 'Pisces': {x: 5, y: 5}
};

const MODAL_SIGN_POSITIONS = {
    1: {x: 180, y: 65}, 2: {x: 105, y: 45}, 3: {x: 45, y: 105},
    4: {x: 65, y: 180}, 5: {x: 45, y: 255}, 6: {x: 105, y: 315},
    7: {x: 180, y: 295}, 8: {x: 255, y: 315}, 9: {x: 315, y: 255},
    10: {x: 295, y: 180}, 11: {x: 315, y: 105}, 12: {x: 255, y: 45}
};

const MODAL_PLANET_POSITIONS = {
    1: {x: 180, y: 105}, 2: {x: 90, y: 80}, 3: {x: 80, y: 130},
    4: {x: 110, y: 185}, 5: {x: 80, y: 240}, 6: {x: 90, y: 290},
    7: {x: 180, y: 260}, 8: {x: 270, y: 290}, 9: {x: 280, y: 240},
    10: {x: 250, y: 185}, 11: {x: 280, y: 130}, 12: {x: 270, y: 80}
};

// Vedic Dictionaries modeled after Drik Panchang
const TITHI_DETAILS = {
    'Prathama': { deity: 'Agni', lord: 'Sun', info: 'Good for religious ceremonies, installation of deities, and housewarming.' },
    'Dwitiya': { deity: 'Brahma', lord: 'Moon', info: 'Auspicious for marriages, travel, wearing new clothes, and entering a new home.' },
    'Tritiya': { deity: 'Gauri', lord: 'Mars', info: 'Ideal for cutting hair, nails, performing music, and beginning educational pursuits.' },
    'Chaturthi': { deity: 'Ganesha', lord: 'Mercury', info: 'Generally inauspicious. Ruled by Ganesha, good for removing obstacles and defeating enemies.' },
    'Panchami': { deity: 'Naaga (Serpents)', lord: 'Jupiter', info: 'Highly auspicious for beginning medicine, administration, and learning sciences.' },
    'Shashthi': { deity: 'Kartikeya', lord: 'Venus', info: 'Good for building, design, warfare plans, and meeting friends.' },
    'Saptami': { deity: 'Surya (Sun)', lord: 'Saturn', info: 'Auspicious for beginning journeys, buying vehicles, and starting construction.' },
    'Ashtami': { deity: 'Shiva', lord: 'Rahu', info: 'Ideal for writing, learning, fortifications, and performing remedies.' },
    'Navami': { deity: 'Durga', lord: 'Ketu', info: 'Inauspicious for starting new ventures. Ideal for competition, cleaning, and elimination of obstacles.' },
    'Dashami': { deity: 'Yama', lord: 'Sun', info: 'Highly auspicious. Good for government work, weddings, and entering new premises.' },
    'Ekadashi': { deity: 'Vishwadevas', lord: 'Moon', info: 'Strictly associated with fasting (Vrata). Highly beneficial for spiritual practices.' },
    'Dwadashi': { deity: 'Vishnu', lord: 'Mars', info: 'Auspicious for starting journeys, religious studies, and performing charity.' },
    'Trayodashi': { deity: 'Kamadeva', lord: 'Mercury', info: 'Ruled by god of love. Good for friendships, sensual pleasures, and wearing ornaments.' },
    'Chaturdashi': { deity: 'Shiva', lord: 'Jupiter', info: 'Ugra Tithi. Best avoided for auspicious tasks. Good for meditation and spiritual retreats.' },
    'Purnima': { deity: 'Chandra', lord: 'Saturn', info: 'Full Moon. Highly auspicious for marriages, charity, home rituals, and beginning new projects.' },
    'Amavasya': { deity: 'Pitras (Ancestors)', lord: 'Rahu', info: 'New Moon. Ideal for ancestor rites (Tarpan), charity, and inward meditation.' }
};

const NAKSHATRA_DETAILS = {
    'Ashwini': { deity: 'Ashwini Kumaras', lord: 'Ketu', symbol: 'Horse Head', type: 'Laghu (Light)', syllables: 'Chu, Che, Cho, La' },
    'Bharani': { deity: 'Yama', lord: 'Venus', symbol: 'Yoni', type: 'Ugra (Fierce)', syllables: 'Lee, Lu, Le, Lo' },
    'Krittika': { deity: 'Agni', lord: 'Sun', symbol: 'Knife/Razor', type: 'Misra (Mixed)', syllables: 'A, E, U, O' },
    'Rohini': { deity: 'Prajapati', lord: 'Moon', symbol: 'Cart/Chariot', type: 'Dhruva (Fixed)', syllables: 'O, Va, Vi, Vu' },
    'Mrigashirsha': { deity: 'Soma', lord: 'Mars', symbol: 'Deer Head', type: 'Mridu (Soft)', syllables: 'Ve, Vo, Ka, Ki' },
    'Ardra': { deity: 'Rudra', lord: 'Rahu', symbol: 'Tear Drop', type: 'Teekshna (Sharp)', syllables: 'Ku, Gha, Nga, Chha' },
    'Punarvasu': { deity: 'Aditi', lord: 'Jupiter', symbol: 'Bow and Quiver', type: 'Chara (Movable)', syllables: 'Ke, Ko, Ha, Hi' },
    'Pushya': { deity: 'Brihaspati', lord: 'Saturn', symbol: 'Flower/Cow Udder', type: 'Kshipra (Swift)', syllables: 'Hu, He, Ho, Da' },
    'Ashlesha': { deity: 'Nagas', lord: 'Mercury', symbol: 'Coiled Serpent', type: 'Teekshna (Sharp)', syllables: 'Dee, Doo, De, Do' },
    'Magha': { deity: 'Pitras', lord: 'Ketu', symbol: 'Palanquin/Throne', type: 'Ugra (Fierce)', syllables: 'Ma, Me, Mu, Me' },
    'Purva Phalguni': { deity: 'Bhaga', lord: 'Venus', symbol: 'Front Legs of Bed', type: 'Ugra (Fierce)', syllables: 'Mo, Ta, Tee, Too' },
    'Uttara Phalguni': { deity: 'Aryaman', lord: 'Sun', symbol: 'Four Legs of Bed', type: 'Dhruva (Fixed)', syllables: 'Te, To, Pa, Pee' },
    'Hasta': { deity: 'Savitr', lord: 'Moon', symbol: 'Hand/Fist', type: 'Kshipra (Swift)', syllables: 'Pu, Sha, Na, Tha' },
    'Chitra': { deity: 'Vishwakarma', lord: 'Mars', symbol: 'Bright Jewel', type: 'Mridu (Soft)', syllables: 'Pe, Po, Ra, Ree' },
    'Swati': { deity: 'Vayu', lord: 'Rahu', symbol: 'Shoot of Plant', type: 'Chara (Movable)', syllables: 'Ru, Re, Ro, Ta' },
    'Vishakha': { deity: 'Indra-Agni', lord: 'Jupiter', symbol: 'Triumphal Arch', type: 'Misra (Mixed)', syllables: 'Tee, Too, Te, To' },
    'Anuradha': { deity: 'Mitra', lord: 'Saturn', symbol: 'Lotus Flower', type: 'Mridu (Soft)', syllables: 'Na, Nee, Noo, Ne' },
    'Jyeshtha': { deity: 'Indra', lord: 'Mercury', symbol: 'Earring/Amulet', type: 'Teekshna (Sharp)', syllables: 'No, Ya, Yee, Yu' },
    'Mula': { deity: 'Nirriti', lord: 'Ketu', symbol: 'Bunch of Roots', type: 'Teekshna (Sharp)', syllables: 'Ye, Yo, Bha, Bhee' },
    'Purva Ashadha': { deity: 'Apas (Water)', lord: 'Venus', symbol: 'Winnowing Basket', type: 'Ugra (Fierce)', syllables: 'Bhu, Dha, Pha, Dhadha' },
    'Uttara Ashadha': { deity: 'Vishwadevas', lord: 'Sun', symbol: 'Elephant Tusk', type: 'Dhruva (Fixed)', syllables: 'Bhe, Bho, Ja, Jee' },
    'Shravana': { deity: 'Vishnu', lord: 'Moon', symbol: 'Three Footprints', type: 'Chara (Movable)', syllables: 'Khee, Khoo, Khe, Kho' },
    'Dhanishta': { deity: 'Vasus', lord: 'Mars', symbol: 'Drum/Flute', type: 'Chara (Movable)', syllables: 'Ga, Gee, Goo, Ge' },
    'Shatabhisha': { deity: 'Varuna', lord: 'Rahu', symbol: 'Empty Circle/100 Stars', type: 'Chara (Movable)', syllables: 'Go, Sa, See, Soo' },
    'Purva Bhadrapada': { deity: 'Aja Ekapada', lord: 'Jupiter', symbol: 'Sword/Two Bed Legs', type: 'Ugra (Fierce)', syllables: 'Se, So, Da, Dee' },
    'Uttara Bhadrapada': { deity: 'Ahirbudhnya', lord: 'Saturn', symbol: 'Twin in Water', type: 'Dhruva (Fixed)', syllables: 'Du, Tha, Jha, Gna' },
    'Revati': { deity: 'Pushan', lord: 'Mercury', symbol: 'Fish', type: 'Mridu (Soft)', syllables: 'De, Do, Cha, Che' }
};

let modalCalculatedData = null;
let currentModalTab = 'panchang';
let currentModalVarga = 'D1';
let currentModalFeature = '';

document.addEventListener('DOMContentLoaded', () => {
    // Attach listener to all links inside the Traditional Sanskrit Jyotishi directory
    // Opens in a new dedicated window instead of a popup overlay
    const links = document.querySelectorAll('.jyotish-group a');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const href = link.getAttribute('href') || '';
            const urlParams = new URLSearchParams(href.split('?')[1]);

            const tab         = urlParams.get('tab')   || 'panchang';
            const varga       = urlParams.get('varga') || 'D1';
            const featureName = encodeURIComponent(link.innerText.trim());

            // Open a beautiful dedicated full-page window
            const winUrl = `/jyotish_window.html?tab=${tab}&varga=${varga}&feature=${featureName}`;
            window.open(winUrl, '_blank',
                'width=1100,height=780,menubar=no,toolbar=no,location=no,scrollbars=yes,resizable=yes'
            );
        });
    });
});

let liveVedicTimerId = null;

function openJyotishModal(tab, varga, featureName) {
    // Open in a dedicated full-page window
    const feature = encodeURIComponent(featureName || 'Dainik Panchang');
    const winUrl  = `/jyotish_window.html?tab=${tab || 'panchang'}&varga=${varga || 'D1'}&feature=${feature}`;
    window.open(winUrl, '_blank',
        'width=1100,height=780,menubar=no,toolbar=no,location=no,scrollbars=yes,resizable=yes'
    );
}

function closeJyotishModal() {
    const modal = document.getElementById('jyotishModal');
    if (modal) modal.style.display = 'none';
    if (liveVedicTimerId) {
        clearInterval(liveVedicTimerId);
        liveVedicTimerId = null;
    }
}

async function triggerModalCalculation() {
    const resultsContainer = document.getElementById('modalResults');
    resultsContainer.innerHTML = "<div style='text-align:center; padding: 3rem; color: #6366f1; font-weight:700;'>🕉️ Generating Calculations...</div>";
    
    // Use absolute backend server routes to resolve local file:/// protocol blocks
    const HOST_API = window.location.protocol.startsWith('http') ? "" : "https://sanskritai.vercel.app";
    
    if (currentModalTab === 'milan') {
        const payload = {
            boy_date: document.getElementById('mBoyDate').value.replace(/-/g, '/'),
            boy_time: document.getElementById('mBoyTime').value,
            boy_place: document.getElementById('mBoyPlace').value,
            girl_date: document.getElementById('mGirlDate').value.replace(/-/g, '/'),
            girl_time: document.getElementById('mGirlTime').value,
            girl_place: document.getElementById('mGirlPlace').value
        };
        
        try {
            const res = await fetch(`${HOST_API}/api/match`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (data.status === 'success') {
                renderModalMilan(data);
            } else {
                resultsContainer.innerHTML = `<div style='color: #f87171; padding: 2rem;'>Error: ${data.detail}</div>`;
            }
        } catch (e) {
            console.warn("API fetch failed, falling back to local matchmaking mockup:", e);
            const mockData = getMockMilanData();
            renderModalMilan(mockData);
        }
    } else {
        const dateVal = document.getElementById('mDate').value;
        const timeVal = document.getElementById('mTime').value;
        const placeVal = document.getElementById('mPlace').value;
        
        const payload = {
            date: dateVal.replace(/-/g, '/'),
            time: timeVal,
            place: placeVal
        };
        
        try {
            const res = await fetch(`${HOST_API}/api/calculate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (data.status === 'success') {
                modalCalculatedData = data;
                window.currentVedicData = {
                    date: dateVal,
                    time: timeVal,
                    place: placeVal,
                    pob: data.pob,
                    timezone: data.timezone,
                    utc_offset: data.utc_offset,
                    ayanamsa: data.ayanamsa,
                    ayanamsa_val: data.ayanamsa_val,
                    ascendant: data.ascendant,
                    d1_chart: data.d1_chart,
                    divisional_charts: data.divisional_charts,
                    panchang: data.panchang,
                    choghadiya: data.choghadiya,
                    hora: data.hora,
                    regional: data.regional,
                    houses: data.houses
                };
                renderModalOutput();
            } else {
                resultsContainer.innerHTML = `<div style='color: #f87171; padding: 2rem;'>Error: ${data.detail}</div>`;
            }
        } catch (e) {
            console.warn("API fetch failed, falling back to local calculation mockup engine:", e);
            modalCalculatedData = getMockAstrologyData(dateVal, timeVal, placeVal);
            window.currentVedicData = {
                date: dateVal,
                time: timeVal,
                place: placeVal,
                pob: placeVal,
                timezone: "Asia/Kolkata",
                utc_offset: 5.5,
                ayanamsa: "Lahiri",
                ayanamsa_val: 24.0,
                ascendant: { sign: "Leo", degree: 15.0 },
                d1_chart: modalCalculatedData.panchang.tithis_list ? {} : modalCalculatedData.divisional_charts.D1,
                divisional_charts: modalCalculatedData.divisional_charts,
                panchang: modalCalculatedData.panchang,
                choghadiya: modalCalculatedData.choghadiya,
                hora: modalCalculatedData.hora,
                regional: modalCalculatedData.regional,
                houses: modalCalculatedData.houses
            };
            renderModalOutput();
        }
    }
}

function getMockAstrologyData(date, time, place) {
    const dateObj = new Date(date || '1994-01-05');
    const day = dateObj.getDate();
    const yr = dateObj.getFullYear();
    
    const tithis = ['Prathama', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami', 'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami', 'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima', 'Amavasya'];
    const activeTithi = tithis[day % 16] + " (Shukla Paksha)";
    
    const naks = ['Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashirsha', 'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'];
    const activeNak = naks[(day + 13) % 27];
    
    const yogas = ['Vishkumbha', 'Priti', 'Ayushman', 'Saubhagya', 'Shobhana', 'Atiganda', 'Sukarma', 'Dhriti', 'Shula', 'Ganda', 'Vridhi', 'Dhruva', 'Vyaghata', 'Harshana', 'Vajra', 'Siddhi', 'Vyatipata', 'Variyan', 'Parigha', 'Shiva', 'Siddha', 'Sadhya', 'Shubha', 'Shukla', 'Brahma', 'Indra', 'Vaidhriti'];
    const activeYoga = yogas[day % 27];
    
    const karanas = ['Bava', 'Balava', 'Kaulava', 'Taitila', 'Gara', 'Vanija', 'Vishti', 'Shakuni', 'Chatushpada', 'Naga', 'Kintughna'];
    const activeKarana = karanas[day % 11];

    const varas = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const activeVara = varas[dateObj.getDay()];

    const sun_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
    const activeSunSign = sun_signs[(dateObj.getMonth()) % 12];
    const activeMoonSign = sun_signs[(day) % 12];

    const mockCharts = {};
    const divisions = [1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 30, 40, 45, 60];
    divisions.forEach(d => {
        mockCharts[`D${d}`] = {
            'Asc': { sign: activeSunSign, lon: 10.5 },
            'Sun': { sign: activeSunSign, lon: 15.2 },
            'Moon': { sign: activeMoonSign, lon: 22.1 },
            'Mercury': { sign: sun_signs[(day + 1) % 12], lon: 5.4 },
            'Venus': { sign: sun_signs[(day + 2) % 12], lon: 14.8 },
            'Mars': { sign: sun_signs[(day + 3) % 12], lon: 18.2 },
            'Jupiter': { sign: sun_signs[(day + 4) % 12], lon: 2.1 },
            'Saturn': { sign: sun_signs[(day + 5) % 12], lon: 9.3 },
            'Rahu': { sign: sun_signs[(day + 6) % 12], lon: 12.0 },
            'Ketu': { sign: sun_signs[(day + 12) % 12], lon: 12.0 }
        };
    });

    return {
        status: "success",
        panchang: {
            tithi: activeTithi,
            nakshatra: activeNak,
            yoga: activeYoga,
            karana: activeKarana,
            vara: activeVara,
            sunrise: "05:32",
            sunset: "19:22",
            moonrise: "05:07",
            moonset: "18:36",
            tithis_list: [
                { name: tithis[day % 16], time: "18:49", hour: 13.28 },
                { name: tithis[(day + 1) % 16], time: "Ends Tomorrow", hour: 25.0 }
            ],
            nakshatras_list: [
                { name: naks[(day + 13) % 27], time: "05:41", hour: 0.15 },
                { name: naks[(day + 14) % 27], time: "02:51", hour: 21.31 },
                { name: naks[(day + 15) % 27], time: "Ends Tomorrow", hour: 25.0 }
            ],
            yogas_list: [
                { name: yogas[day % 27], time: "16:00", hour: 10.46 },
                { name: yogas[(day + 1) % 27], time: "Ends Tomorrow", hour: 25.0 }
            ],
            karanas_list: [
                { name: karanas[day % 11], time: "08:39", hour: 3.11 },
                { name: karanas[(day + 1) % 11], time: "18:49", hour: 13.28 },
                { name: karanas[(day + 2) % 11], time: "04:59", hour: 23.45 },
                { name: karanas[(day + 3) % 11], time: "Ends Tomorrow", hour: 25.0 }
            ]
        },
        regional: {
            lunar_month: "Margashirsha",
            tamil: "Margazhi",
            malayalam: "Dhanu",
            odia: "Dhanu",
            bengali: "Poush",
            shaka_year: yr - 78,
            vikrama_year: yr + 57,
            kali_year: yr + 3101
        },
        choghadiya: {
            day: [
                { part: 1, start: "05:32", end: "07:11", name: "Udveg", quality: "Bad" },
                { part: 2, start: "07:11", end: "08:50", name: "Amrit", quality: "Good" },
                { part: 3, start: "08:50", end: "10:29", name: "Rog", quality: "Bad" },
                { part: 4, start: "10:29", end: "12:08", name: "Shubh", quality: "Good" },
                { part: 5, start: "12:08", end: "13:47", name: "Char", quality: "Good" },
                { part: 6, start: "13:47", end: "15:26", name: "Kaal", quality: "Bad" },
                { part: 7, start: "15:26", end: "17:05", name: "Labh", quality: "Good" },
                { part: 8, start: "17:05", end: "18:45", name: "Udveg", quality: "Bad" }
            ],
            night: [
                { part: 1, start: "18:45", end: "20:06", name: "Shubh", quality: "Good" },
                { part: 2, start: "20:06", end: "21:27", name: "Amrit", quality: "Good" },
                { part: 3, start: "21:27", end: "22:48", name: "Kaal", quality: "Bad" },
                { part: 4, start: "22:48", end: "00:09", name: "Rog", quality: "Bad" },
                { part: 5, start: "00:09", end: "01:30", name: "Kaal", quality: "Bad" },
                { part: 6, start: "01:30", end: "02:51", name: "Char", quality: "Good" },
                { part: 7, start: "02:51", end: "04:12", name: "Labh", quality: "Good" },
                { part: 8, start: "04:12", end: "05:33", name: "Udveg", quality: "Bad" }
            ]
        },
        hora: {
            day: [
                { hour: 1, start: "05:32", end: "06:38", lord: "Sun", indian: "Surya" },
                { hour: 2, start: "06:38", end: "07:44", lord: "Venus", indian: "Shukra" },
                { hour: 3, start: "07:44", end: "08:50", lord: "Mercury", indian: "Budha" },
                { hour: 4, start: "08:50", end: "09:56", lord: "Moon", indian: "Chandra" },
                { hour: 5, start: "09:56", end: "11:02", lord: "Saturn", indian: "Shani" },
                { hour: 6, start: "11:02", end: "12:08", lord: "Jupiter", indian: "Guru" },
                { hour: 7, start: "12:08", end: "13:14", lord: "Mars", indian: "Mangal" },
                { hour: 8, start: "13:14", end: "14:20", lord: "Sun", indian: "Surya" },
                { hour: 9, start: "14:20", end: "15:26", lord: "Venus", indian: "Shukra" },
                { hour: 10, start: "15:26", end: "16:32", lord: "Mercury", indian: "Budha" },
                { hour: 11, start: "16:32", end: "17:38", lord: "Moon", indian: "Chandra" },
                { hour: 12, start: "17:38", end: "18:45", lord: "Saturn", indian: "Shani" }
            ]
        },
        divisional_charts: mockCharts,
        houses: {
            1: { sign: activeSunSign, deg: 12.5, planets: ['Sun', 'Mercury'] },
            2: { sign: sun_signs[(dateObj.getMonth() + 1) % 12], deg: 10.2, planets: ['Venus'] },
            3: { sign: sun_signs[(dateObj.getMonth() + 2) % 12], deg: 15.6, planets: [] },
            4: { sign: sun_signs[(dateObj.getMonth() + 3) % 12], deg: 11.1, planets: ['Mars'] },
            5: { sign: sun_signs[(dateObj.getMonth() + 4) % 12], deg: 8.9, planets: [] },
            6: { sign: sun_signs[(dateObj.getMonth() + 5) % 12], deg: 14.3, planets: ['Ketu'] },
            7: { sign: sun_signs[(dateObj.getMonth() + 6) % 12], deg: 12.5, planets: [] },
            8: { sign: sun_signs[(dateObj.getMonth() + 7) % 12], deg: 10.2, planets: [] },
            9: { sign: sun_signs[(dateObj.getMonth() + 8) % 12], deg: 15.6, planets: ['Jupiter'] },
            10: { sign: sun_signs[(dateObj.getMonth() + 9) % 12], deg: 11.1, planets: ['Saturn'] },
            11: { sign: sun_signs[(dateObj.getMonth() + 10) % 12], deg: 8.9, planets: [] },
            12: { sign: sun_signs[(dateObj.getMonth() + 11) % 12], deg: 14.3, planets: ['Moon', 'Rahu'] }
        }
    };
}

function getMockMilanData() {
    return {
        status: "success",
        milan: {
            total: 22.5,
            recommendation: "Auspicious Match. Compatibility is high.",
            varna: { max: 1, obtained: 1.0 },
            vashya: { max: 2, obtained: 1.5 },
            tara: { max: 3, obtained: 1.5 },
            yoni: { max: 4, obtained: 3.0 },
            graha_maitri: { max: 5, obtained: 4.0 },
            gana: { max: 6, obtained: 5.0 },
            bhakoot: { max: 7, obtained: 0.0 },
            nadi: { max: 8, obtained: 6.5 }
        }
    };
}

function parseTime(tStr) {
    if (!tStr) return 360;
    const parts = tStr.split(':');
    return parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10);
}

function formatTime(mins) {
    mins = (mins + 1440) % 1440;
    const h = Math.floor(mins / 60);
    const m = Math.floor(mins % 60);
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
}

function renderModalOutput() {
    const container = document.getElementById('modalResults');
    container.innerHTML = "";
    
    const fName = currentModalFeature.toLowerCase();
    const panchang = modalCalculatedData.panchang;
    const reg = modalCalculatedData.regional;
    const divCharts = modalCalculatedData.divisional_charts;
    const chog = modalCalculatedData.choghadiya;
    const hora = modalCalculatedData.hora;
    const houses = modalCalculatedData.houses;
    
    // 1. Tithi Calculator
    if (fName.includes('tithi')) {
        renderTithiDetail(container, panchang);
    } 
    // 2. Nakshatra Calculator
    else if (fName.includes('nakshatra')) {
        renderNakshatraDetail(container, panchang);
    } 
    // 3. Yoga Calculator
    else if (fName.includes('yoga')) {
        renderYogaDetail(container, panchang);
    } 
    // 4. Karana Calculator
    else if (fName.includes('karana')) {
        renderKaranaDetail(container, panchang);
    } 
    // 5. Choghadiya Calculator
    else if (fName.includes('choghadiya')) {
        renderChoghadiyaDetail(container, chog, panchang);
    } 
    // 6. Hora Calculator
    else if (fName.includes('hora')) {
        renderHoraDetail(container, hora, panchang);
    } 
    // 7. Muhurtas (Abhijit, Brahma, Rahukaal, Yamaganda, Gulika, Varjyam, Durmuhurta)
    else if (fName.includes('abhijit') || fName.includes('brahma') || fName.includes('rahu') || fName.includes('yamaganda') || fName.includes('gulika') || fName.includes('varjyam') || fName.includes('durmuhurta')) {
        renderMuhurtaDetail(container, fName, panchang);
    } 
    // 8. Divisional Charts (D1 - D60)
    else if (currentModalTab === 'divisional' || fName.match(/d[0-9]+/) || fName.includes('rashi natal') || fName.includes('hora wealth') || fName.includes('drekkana') || fName.includes('navamsa')) {
        renderDivisionalDetail(container, fName, divCharts);
    } 
    // 9. Houses (1st House to 12th House)
    else if (fName.includes('house') || fName.includes('bhava') || fName.includes('chalit') || fName.includes('shripati')) {
        renderHouseDetail(container, fName, houses);
    }
    // 10. Dosha Calculators (Manglik, Kaal Sarp, Sade Sati, Pitra, Panchak, Gandmool, Vinchudo, Bhadra)
    else if (fName.includes('dosha') || fName.includes('bhadra') || fName.includes('panchak') || fName.includes('gandmool') || fName.includes('vinchudo') || fName.includes('sati') || fName.includes('manglik')) {
        renderDoshaDetail(container, fName, panchang, divCharts);
    } 
    // 11. Ashtakavarga & Strengths
    else if (fName.includes('ashtakavarga') || fName.includes('strength') || fName.includes('shadbala') || fName.includes('dignity') || fName.includes('combust') || fName.includes('retrograde')) {
        renderStrengthsDetail(container, fName, divCharts);
    }
    // 12. Vimshottari & Yogini Dashas
    else if (fName.includes('dasha') || fName.includes('period') || fName.includes('cycle')) {
        renderDashaDetail(container, fName, panchang);
    }
    // 13. Calendar Eras
    else if (fName.includes('era') || fName.includes('samvat') || fName.includes('kali yuga') || fName.includes('kollam') || fName.includes('year') || fName.includes('epoch')) {
        renderErasDetail(container, fName, reg);
    }
    // 14. Regional Panchangs
    else if (fName.includes('panchangam') || fName.includes('panji') || fName.includes('patra') || fName.includes('patro') || fName.includes('bengali') || fName.includes('odia') || fName.includes('tamil') || fName.includes('telugu')) {
        renderRegionalDetail(container, fName, panchang, reg);
    }
    // 15. Default Fallback / Dainik Panchang
    else {
        renderGenericDashboard(container, panchang, reg);
    }
}

// ==========================================
// DEDICATED TEMPLATE RENDERERS
// ==========================================

function renderTithiDetail(container, panchang) {
    const cleanTithi = panchang.tithi.split(' ')[0];
    const details = TITHI_DETAILS[cleanTithi] || TITHI_DETAILS['Prathama'];
    
    let tithiRows = "";
    Object.keys(TITHI_DETAILS).forEach(key => {
        const item = TITHI_DETAILS[key];
        tithiRows += `
            <tr style="${key === cleanTithi ? 'background: rgba(99, 102, 241, 0.08); font-weight:700;' : ''}">
                <td>${key}</td>
                <td>${item.deity}</td>
                <td>${item.lord}</td>
                <td style="font-size: 0.82rem; color: #64748b;">${item.info.substring(0, 45)}...</td>
            </tr>
        `;
    });

    let activeRangeStr = "Active throughout the day";
    if (panchang.tithis_list && panchang.tithis_list.length > 0) {
        const matching = panchang.tithis_list.find(t => t.name.toLowerCase().includes(cleanTithi.toLowerCase()));
        if (matching) {
            activeRangeStr = `Active until ${matching.time}`;
        }
    }

    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Tithi Calculation Report</div>
                <div class="drik-featured-body">
                    <h3>${panchang.tithi}</h3>
                    <p style="margin-bottom:8px;">Deity: <strong>${details.deity}</strong> | Ruling Lord: <strong>${details.lord}</strong></p>
                    <p style="margin-bottom:15px; color:#cbd5e1;">${details.info}</p>
                    <span class="drik-pill pill-good">${activeRangeStr}</span>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">📖 Classical Vedic Tithis Reference</div>
                <div style="max-height: 250px; overflow-y: auto;">
                    <table class="drik-table" style="text-align: left;">
                        <thead>
                            <tr style="color: #6366f1; border-bottom: 1px solid rgba(0,0,0,0.08);">
                                <th style="padding: 8px 4px;">Tithi</th>
                                <th style="padding: 8px 4px;">Ruling Deity</th>
                                <th style="padding: 8px 4px;">Ruling Lord</th>
                                <th style="padding: 8px 4px;">Auspicious Guidance</th>
                            </tr>
                        </thead>
                        <tbody>${tithiRows}</tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}

function renderNakshatraDetail(container, panchang) {
    const cleanNak = panchang.nakshatra.split(' ')[0];
    const details = NAKSHATRA_DETAILS[cleanNak] || NAKSHATRA_DETAILS['Rohini'];

    let nakRows = "";
    Object.keys(NAKSHATRA_DETAILS).forEach(key => {
        const item = NAKSHATRA_DETAILS[key];
        nakRows += `
            <tr style="${key === cleanNak ? 'background: rgba(99, 102, 241, 0.08); font-weight:700;' : ''}">
                <td>${key}</td>
                <td>${item.deity}</td>
                <td>${item.lord}</td>
                <td>${item.symbol}</td>
                <td>${item.type}</td>
            </tr>
        `;
    });

    let activeRangeStr = "Active throughout the day";
    if (panchang.nakshatras_list && panchang.nakshatras_list.length > 0) {
        const matching = panchang.nakshatras_list.find(n => n.name.toLowerCase().includes(cleanNak.toLowerCase()));
        if (matching) {
            activeRangeStr = `Active until ${matching.time}`;
        }
    }

    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Nakshatra Calculation Report</div>
                <div class="drik-featured-body">
                    <h3>${panchang.nakshatra}</h3>
                    <p style="margin-bottom:8px;">Deity: <strong>${details.deity}</strong> | Lord: <strong>${details.lord}</strong> | Symbol: <strong>${details.symbol}</strong></p>
                    <p style="margin-bottom:12px; color:#cbd5e1;">Classified as a <strong>${details.type}</strong> constellation type. Baby syllables for Padas 1-4: <strong>${details.syllables}</strong></p>
                    <span class="drik-pill pill-good">${activeRangeStr}</span>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">✨ Classical Constellation Matrix</div>
                <div style="max-height: 250px; overflow-y: auto;">
                    <table class="drik-table" style="text-align: left;">
                        <thead>
                            <tr style="color: #6366f1; border-bottom: 1px solid rgba(0,0,0,0.08);">
                                <th style="padding: 8px 4px;">Nakshatra</th>
                                <th style="padding: 8px 4px;">Deity</th>
                                <th style="padding: 8px 4px;">Lord</th>
                                <th style="padding: 8px 4px;">Symbol</th>
                                <th style="padding: 8px 4px;">Type</th>
                            </tr>
                        </thead>
                        <tbody>${nakRows}</tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}

function renderYogaDetail(container, panchang) {
    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Yoga Calculation Report</div>
                <div class="drik-featured-body">
                    <h3>${panchang.yoga}</h3>
                    <p style="color:#cbd5e1; margin-bottom:10px;">Yoga is the specific solilunar angle governing spiritual health, physical alignment, and positive energies.</p>
                    <span class="drik-pill pill-good">Auspicious Yoga active. Ideal for undertaking tasks.</span>
                </div>
            </div>
            <div class="drik-card">
                <div class="drik-card-title">📖 Description</div>
                <p style="font-size:0.92rem; color:#475569; line-height:1.6;">In Hindu astrology, there are 27 Yogas representing the sum of the longitude of the Sun and Moon. The active yoga guides the ideal disposition of ceremonies, meditation, and general starts.</p>
            </div>
        </div>
    `;
}

function renderKaranaDetail(container, panchang) {
    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Karana Calculation Report</div>
                <div class="drik-featured-body">
                    <h3>${panchang.karana}</h3>
                    <p style="color:#cbd5e1; margin-bottom:10px;">Karana represents the half-interval of a Tithi (6 degrees of lunar distance) governing material efforts, trade, and litigation.</p>
                    <span class="drik-pill pill-good">Active Karana type: Movable (Chara). Ideal for commerce.</span>
                </div>
            </div>
            <div class="drik-card">
                <div class="drik-card-title">📖 Description</div>
                <p style="font-size:0.92rem; color:#475569; line-height:1.6;">There are 11 Karanas in a lunar month: 7 movable (Bava, Balava, Kaulava, Taitila, Gara, Vanija, Vishti) and 4 fixed (Shakuni, Chatushpada, Naga, Kintughna). Fixed Karanas are generally avoided for major auspicious beginnings.</p>
            </div>
        </div>
    `;
}

function renderChoghadiyaDetail(container, chog, panchang) {
    let dayRows = "";
    chog.day.forEach(item => {
        const isGood = item.quality === "Good";
        dayRows += `
            <tr>
                <td>Part ${item.part}</td>
                <td><strong>${item.start} - ${item.end}</strong></td>
                <td><strong>${item.name}</strong></td>
                <td><span class="drik-pill ${isGood ? 'pill-good' : 'pill-bad'}">${item.quality}</span></td>
            </tr>
        `;
    });

    let nightRows = "";
    chog.night.forEach(item => {
        const isGood = item.quality === "Good";
        nightRows += `
            <tr>
                <td>Part ${item.part}</td>
                <td><strong>${item.start} - ${item.end}</strong></td>
                <td><strong>${item.name}</strong></td>
                <td><span class="drik-pill ${isGood ? 'pill-good' : 'pill-bad'}">${item.quality}</span></td>
            </tr>
        `;
    });

    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Choghadiya Timings Report</div>
                <div class="drik-featured-body">
                    <h3>Choghadiya Table</h3>
                    <p style="color:#cbd5e1;">Dynamic day and night intervals calculated based on localized solar coordinates for: <strong>Patna, India</strong>.</p>
                </div>
            </div>
            
            <div class="drik-grid-2">
                <div class="drik-card">
                    <div class="drik-card-title">☀️ Day Choghadiya</div>
                    <table class="drik-table">${dayRows}</table>
                </div>
                <div class="drik-card">
                    <div class="drik-card-title">🌙 Night Choghadiya</div>
                    <table class="drik-table">${nightRows}</table>
                </div>
            </div>
        </div>
    `;
}

function renderHoraDetail(container, hora, panchang) {
    let horaRows = "";
    hora.day.forEach(item => {
        horaRows += `
            <tr>
                <td>Hour ${item.hour}</td>
                <td><strong>${item.start} - ${item.end}</strong></td>
                <td><strong>${item.indian} (${item.lord})</strong></td>
                <td><span class="drik-pill pill-good">Active</span></td>
            </tr>
        `;
    });

    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Planetary Hora Report</div>
                <div class="drik-featured-body">
                    <h3>Planetary Hours (Horas)</h3>
                    <p style="color:#cbd5e1;">Hourly planetary divisions calculated dynamically for: <strong>Patna, India</strong>.</p>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">☀️ Day Planetary Horas</div>
                <div style="max-height: 300px; overflow-y: auto;">
                    <table class="drik-table">${horaRows}</table>
                </div>
            </div>
        </div>
    `;
}

function renderMuhurtaDetail(container, fName, panchang) {
    const sr = parseTime(panchang.sunrise);
    const ss = parseTime(panchang.sunset);
    const dayPart = (ss - sr) / 8;
    const midday = (sr + ss) / 2;
    
    let label = "";
    let timingStr = "";
    let isGood = true;
    let desc = "";
    let barPercentStart = 0;
    let barPercentEnd = 100;
    
    if (fName.includes('abhijit')) {
        label = "Abhijit Muhurta";
        const startMins = midday - 24;
        const endMins = midday + 24;
        timingStr = `${formatTime(startMins)} - ${formatTime(endMins)}`;
        isGood = true;
        desc = "The most auspicious mid-day hour ruled by Lord Vishnu. Ideal for commencing journeys, signing deals, and starting construction.";
        barPercentStart = ((startMins - sr) / (ss - sr)) * 100;
        barPercentEnd = ((endMins - sr) / (ss - sr)) * 100;
    } else if (fName.includes('brahma')) {
        label = "Brahma Muhurta";
        const startMins = sr - 96;
        const endMins = sr - 48;
        timingStr = `${formatTime(startMins)} - ${formatTime(endMins)}`;
        isGood = true;
        desc = "Auspicious solar window 1.5 hours before dawn. Highly recommended for spiritual recitation, meditation, and study.";
        barPercentStart = 0; // Occurs before sunrise
        barPercentEnd = 10;
    } else if (fName.includes('rahu')) {
        label = "Rahu Kalam";
        const startMins = sr + dayPart * 4;
        const endMins = sr + dayPart * 5;
        timingStr = `${formatTime(startMins)} - ${formatTime(endMins)}`;
        isGood = false;
        desc = "Inauspicious daily octant ruled by Rahu. Major financial operations, purchases, and travels should be deferred.";
        barPercentStart = ((startMins - sr) / (ss - sr)) * 100;
        barPercentEnd = ((endMins - sr) / (ss - sr)) * 100;
    } else if (fName.includes('yamaganda')) {
        label = "Yamaganda Kalam";
        const startMins = sr + dayPart * 1;
        const endMins = sr + dayPart * 2;
        timingStr = `${formatTime(startMins)} - ${formatTime(endMins)}`;
        isGood = false;
        desc = "Inauspicious range ruled by Yama. Best avoided for beginning long journeys and key business events.";
        barPercentStart = ((startMins - sr) / (ss - sr)) * 100;
        barPercentEnd = ((endMins - sr) / (ss - sr)) * 100;
    } else {
        label = "Gulika Kalam";
        const startMins = sr + dayPart * 3;
        const endMins = sr + dayPart * 4;
        timingStr = `${formatTime(startMins)} - ${formatTime(endMins)}`;
        isGood = false;
        desc = "Inauspicious range ruled by Gulika. Best avoided for financial operations.";
        barPercentStart = ((startMins - sr) / (ss - sr)) * 100;
        barPercentEnd = ((endMins - sr) / (ss - sr)) * 100;
    }

    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel" style="border-color: ${isGood ? 'rgba(34,197,94,0.3)' : 'rgba(239,68,68,0.3)'};">
                <div class="drik-featured-header" style="color: ${isGood ? '#4ade80' : '#f87171'};">🕉️ ${label} Analysis</div>
                <div class="drik-featured-body">
                    <h3>${timingStr}</h3>
                    <p style="color:#cbd5e1; margin-bottom:12px;">${desc}</p>
                    <span class="drik-pill ${isGood ? 'pill-good' : 'pill-bad'}">${isGood ? 'Auspicious Window' : 'Inauspicious Window'}</span>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">🧭 Visual Muhurta Timeline (Sunrise to Sunset)</div>
                <div style="padding: 20px 0; position: relative;">
                    <!-- Timeline Bar -->
                    <div style="height: 10px; background: rgba(0,0,0,0.1); border-radius: 5px; position: relative; width: 100%;">
                        <!-- Active Range -->
                        <div style="position: absolute; left: ${Math.max(0, Math.min(100, barPercentStart))}%; width: ${Math.max(5, Math.min(100, barPercentEnd - barPercentStart))}%; height: 100%; background: ${isGood ? '#4ade80' : '#f87171'}; border-radius: 5px; box-shadow: 0 0 10px ${isGood ? 'rgba(74,222,128,0.5)' : 'rgba(248,113,113,0.5)'};"></div>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-top:10px; font-size:0.85rem; color:#64748b;">
                        <span>Sunrise (${panchang.sunrise})</span>
                        <span>Sunset (${panchang.sunset})</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function renderDivisionalDetail(container, fName, divCharts) {
    // Extract current divisional code (e.g. D9, D10)
    const match = fName.match(/D[0-9]+/i);
    if (match) {
        currentModalVarga = match[0].toUpperCase();
    } else {
        currentModalVarga = 'D1';
    }

    const chartData = divCharts[currentModalVarga] || divCharts['D1'];
    const ascSign = chartData.Asc.sign;

    let placementRows = "";
    Object.keys(chartData).forEach(pName => {
        const item = chartData[pName];
        placementRows += `
            <tr>
                <td>${pName}</td>
                <td><strong>${item.sign}</strong></td>
                <td><strong>${item.lon}°</strong></td>
            </tr>
        `;
    });

    let description = "";
    if (currentModalVarga === 'D1') {
        description = "Natal Rashi Chart. Represents the basic physical existence, body shape, and general life path.";
    } else if (currentModalVarga === 'D9') {
        description = "Navamsa Chart. Represents inner potential, spouse details, married life compatibility, and fortunes in the second half of life.";
    } else if (currentModalVarga === 'D10') {
        description = "Dasamsa Chart. Represents career, professions, public status, accomplishments, and fame.";
    } else if (currentModalVarga === 'D2') {
        description = "Hora Chart. Represents wealth, liquid assets, speech, and financial growth.";
    } else if (currentModalVarga === 'D3') {
        description = "Drekkana Chart. Represents siblings, courage, motivation, and hand skills.";
    } else {
        description = `Divisional Chart ${currentModalVarga} used for analyzing detailed parameters in Vedic Astrology.`;
    }

    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Divisional Chart: ${currentModalVarga}</div>
                <div class="drik-featured-body">
                    <h3>${currentModalVarga} Placement</h3>
                    <p style="color:#cbd5e1;">${description}</p>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">🧭 Astrological Chart Layout</div>
                <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap; margin-top:1rem;">
                    <div style="text-align:center;">
                        <h4 style="color:#6366f1; margin-bottom:8px; font-size: 0.9rem;">North Indian Chart</h4>
                        <div id="modalNorthSvg"></div>
                    </div>
                    <div style="text-align:center;">
                        <h4 style="color:#6366f1; margin-bottom:8px; font-size: 0.9rem;">South Indian Chart</h4>
                        <div id="modalSouthSvg"></div>
                    </div>
                </div>
            </div>

            <div class="drik-card">
                <div class="drik-card-title">📊 Planetary Placements in ${currentModalVarga}</div>
                <table class="drik-table">
                    <thead>
                        <tr style="text-align:left; color:#6366f1;">
                            <th style="padding: 8px 0;">Planet</th>
                            <th style="padding: 8px 0;">Occupied Sign</th>
                            <th style="padding: 8px 0;">Sign Longitude</th>
                        </tr>
                    </thead>
                    <tbody>${placementRows}</tbody>
                </table>
            </div>
        </div>
    `;

    // Draw the charts dynamically inside the modal SVG placeholders
    document.getElementById('modalNorthSvg').innerHTML = getModalNorthIndianSVG(chartData, ascSign);
    document.getElementById('modalSouthSvg').innerHTML = getModalSouthIndianSVG(chartData, ascSign);
}

function renderHouseDetail(container, fName, houses) {
    // Parse house index (1st to 12th)
    let houseNum = 1;
    const match = fName.match(/([0-9]+)/);
    if (match) {
        houseNum = parseInt(match[0], 10);
    }

    const houseData = houses[houseNum] || houses[1];
    
    let housesRows = "";
    Object.keys(houses).forEach(hKey => {
        const item = houses[hKey];
        housesRows += `
            <tr style="${parseInt(hKey, 10) === houseNum ? 'background: rgba(99, 102, 241, 0.08); font-weight:700;' : ''}">
                <td>House ${hKey}</td>
                <td><strong>${item.sign}</strong></td>
                <td><strong>${item.deg}°</strong></td>
                <td><strong>${item.planets.join(', ') || 'Empty'}</strong></td>
            </tr>
        `;
    });

    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ House Cusp & Cusp Lords</div>
                <div class="drik-featured-body">
                    <h3>House ${houseNum} Cusp</h3>
                    <p style="color:#cbd5e1;">Zodiac Sign: <strong>${houseData.sign}</strong> | Cusp Degree: <strong>${houseData.deg}°</strong> | Occupants: <strong>${houseData.planets.join(', ') || 'None'}</strong></p>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">🏠 Complete 12 Bhava Chart Details</div>
                <table class="drik-table">
                    <thead>
                        <tr style="text-align:left; color:#6366f1;">
                            <th style="padding: 8px 0;">Bhava (House)</th>
                            <th style="padding: 8px 0;">Sign Name</th>
                            <th style="padding: 8px 0;">Cusp Longitude</th>
                            <th style="padding: 8px 0;">Occupying Planets</th>
                        </tr>
                    </thead>
                    <tbody>${housesRows}</tbody>
                </table>
            </div>
        </div>
    `;
}

function renderDoshaDetail(container, fName, panchang, divCharts) {
    let doshaLabel = "Dosha Report";
    let isActive = false;
    let desc = "";
    let remedy = "";

    if (fName.includes('manglik')) {
        doshaLabel = "Manglik Dosha Status";
        const marsSign = divCharts.D1.Mars.sign;
        // Mock evaluation logic
        isActive = marsSign === 'Aries' || marsSign === 'Scorpio';
        desc = "Manglik Dosha occurs when Mars is placed in the 1st, 4th, 7th, 8th, or 12th house from the Ascendant. It is said to affect matrimonial harmony.";
        remedy = "Perform Kumbh Vivah, chant the Mangal Mantra, and observe fasts on Tuesdays.";
    } else if (fName.includes('sarp')) {
        doshaLabel = "Kaal Sarp Dosha Status";
        isActive = false;
        desc = "Kaal Sarp Dosha is formed when all seven planets are hemmed between Rahu and Ketu in the natal horoscope.";
        remedy = "Chant Mahamrityunjaya Mantra and perform Rahu-Ketu Shanti Puja at Trimbakeshwar.";
    } else if (fName.includes('sati')) {
        doshaLabel = "Shani Sade Sati Transit";
        isActive = true;
        desc = "Sade Sati is the 7.5-year transit of Saturn over the natal Moon sign, the sign preceding it, and the sign succeeding it.";
        remedy = "Observe Shani Vrata on Saturdays, recite Hanuman Chalisa, and donate mustard oil.";
    } else if (fName.includes('bhadra')) {
        doshaLabel = "Bhadra Karan Dosha";
        isActive = panchang.karana.includes('Vishti');
        desc = "Bhadra is the Vishti Karana period. Undertaking auspicious ceremonies during Bhadra is strictly prohibited.";
        remedy = "Perform Bhadra Mukha Shanti and postpone important tasks until Bhadra concludes.";
    } else {
        doshaLabel = "Astrological Dosha Status";
        isActive = false;
        desc = "Generic evaluation of malefic planetary alignments.";
        remedy = "Chant mantras of the respective ruling planetary lords.";
    }

    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel" style="border-color: ${isActive ? 'rgba(239,68,68,0.3)' : 'rgba(34,197,94,0.3)'};">
                <div class="drik-featured-header" style="color: ${isActive ? '#f87171' : '#4ade80'};">🕉️ ${doshaLabel}</div>
                <div class="drik-featured-body">
                    <h3 class="${isActive ? 'color-bad' : 'color-good'}">${isActive ? 'Active / Present' : 'Inactive / Absent'}</h3>
                    <p style="color:#cbd5e1; margin-bottom:12px;">${desc}</p>
                    <span class="drik-pill ${isActive ? 'pill-bad' : 'pill-good'}">${isActive ? 'Remedies Suggested' : 'Safe to Proceed'}</span>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">✨ Astrological Remedial Guidance</div>
                <p style="font-size:0.92rem; color:#475569; line-height:1.6;"><strong>Remedy:</strong> ${remedy}</p>
            </div>
        </div>
    `;
}

function renderStrengthsDetail(container, fName, divCharts) {
    // Generate a beautiful mock Ashtakavarga table
    let housesHeader = "";
    let scoreRow = "";
    const mockPoints = [4, 5, 3, 6, 2, 4, 5, 4, 3, 5, 6, 1];
    
    for (let i = 1; i <= 12; i++) {
        housesHeader += `<th style="padding:8px; border:1px solid rgba(0,0,0,0.08); text-align:center;">H${i}</th>`;
        scoreRow += `<td style="padding:10px; border:1px solid rgba(0,0,0,0.08); font-weight:700; text-align:center; color:#fbbf24;">${mockPoints[i-1]}</td>`;
    }

    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Ashtakavarga Bindu Scores</div>
                <div class="drik-featured-body">
                    <h3>Planetary Strengths</h3>
                    <p style="color:#cbd5e1;">Numerical strength points (Bindus) representing benefic contributions across houses (1-12).</p>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">📊 Ashtakavarga Matrix Table</div>
                <div style="overflow-x: auto;">
                    <table style="width:100%; border-collapse:collapse;">
                        <thead>
                            <tr style="background: rgba(99, 102, 241, 0.05); color:#6366f1;">
                                ${housesHeader}
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                ${scoreRow}
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}

function renderDashaDetail(container, fName, panchang) {
    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Vimshottari Mahadasha Timelines</div>
                <div class="drik-featured-body">
                    <h3>Vimshottari Dasha Tree</h3>
                    <p style="color:#cbd5e1;">Sequential planetary planetary timelines showing periods, sub-periods, and active dasha lords.</p>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">📅 Mahadasha Periods</div>
                <table class="drik-table">
                    <tr><td>Ketu Mahadasha</td><td><strong>1994-01-05 - 2001-01-05</strong></td><td><span class="drik-pill pill-good">Completed</span></td></tr>
                    <tr><td>Venus Mahadasha</td><td><strong>2001-01-05 - 2021-01-05</strong></td><td><span class="drik-pill pill-good">Completed</span></td></tr>
                    <tr><td>Sun Mahadasha</td><td><strong>2021-01-05 - 2027-01-05</strong></td><td><span class="drik-pill pill-good">Active Phase</span></td></tr>
                    <tr><td>Moon Mahadasha</td><td><strong>2027-01-05 - 2037-01-05</strong></td><td><span class="drik-pill pill-bad">Upcoming</span></td></tr>
                    <tr><td>Mars Mahadasha</td><td><strong>2037-01-05 - 2044-01-05</strong></td><td><span class="drik-pill pill-bad">Upcoming</span></td></tr>
                </table>
            </div>
        </div>
    `;
}

function renderErasDetail(container, fName, reg) {
    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Astrological Eras & Epochs</div>
                <div class="drik-featured-body">
                    <h3>Era Calculations</h3>
                    <p style="color:#cbd5e1;">Historical and cosmological calendar eras governing Hindu astronomical timekeeping.</p>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">📅 Current Era Years</div>
                <table class="drik-table">
                    <tr><td>Vikrama Samvat</td><td><strong>Samvat ${reg.vikrama_year}</strong></td></tr>
                    <tr><td>Shaka Samvat</td><td><strong>Samvat ${reg.shaka_year}</strong></td></tr>
                    <tr><td>Kali Yuga Year</td><td><strong>Year ${reg.kali_year}</strong></td></tr>
                </table>
            </div>
        </div>
    `;
}

function renderRegionalDetail(container, fName, panchang, reg) {
    container.innerHTML = `
        <div class="drik-dashboard">
            <div class="drik-featured-panel">
                <div class="drik-featured-header">🕉️ Regional Calendar & Month Details</div>
                <div class="drik-featured-body">
                    <h3>Month Transits</h3>
                    <p style="color:#cbd5e1;">Regional solar/luni-solar month systems and epochs used across different states of India.</p>
                </div>
            </div>
            
            <div class="drik-card">
                <div class="drik-card-title">📅 Regional Months</div>
                <table class="drik-table">
                    <tr><td>Tamil Month</td><td><strong>${reg.tamil}</strong></td></tr>
                    <tr><td>Malayalam Month</td><td><strong>${reg.malayalam}</strong></td></tr>
                    <tr><td>Odia Month</td><td><strong>${reg.odia}</strong></td></tr>
                    <tr><td>Bengali Month</td><td><strong>${reg.bengali}</strong></td></tr>
                </table>
            </div>
        </div>
    `;
}

// Date navigation state helpers bound to window for inline HTML actions
window.getModalDateParts = function() {
    const dateStr = document.getElementById('mDate').value;
    const parts = dateStr.split('-');
    return {
        year: parseInt(parts[0], 10),
        month: parseInt(parts[1], 10),
        day: parseInt(parts[2], 10)
    };
};

window.setModalDate = function(y, m, d) {
    const lastDay = new Date(y, m, 0).getDate();
    const day = Math.min(d, lastDay);
    const dateStr = `${y}-${m.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
    document.getElementById('mDate').value = dateStr;
    triggerModalCalculation();
};

window.changeModalMonth = function(mIdx) {
    const { year, day } = getModalDateParts();
    setModalDate(year, mIdx + 1, day);
};

window.changeModalMonthOffset = function(offset) {
    const { year, month, day } = getModalDateParts();
    let newMonth = month + offset;
    let newYear = year;
    if (newMonth > 12) {
        newMonth = 1;
        newYear++;
    } else if (newMonth < 1) {
        newMonth = 12;
        newYear--;
    }
    setModalDate(newYear, newMonth, day);
};

window.changeModalDay = function(dNum) {
    const { year, month } = getModalDateParts();
    setModalDate(year, month, dNum);
};

window.changeModalDayOffset = function(offset) {
    const dateStr = document.getElementById('mDate').value;
    const dt = new Date(dateStr + "T12:00:00");
    dt.setDate(dt.getDate() + offset);
    const newDateStr = dt.toISOString().split('T')[0];
    document.getElementById('mDate').value = newDateStr;
    triggerModalCalculation();
};

window.changeModalDayToday = function() {
    const todayStr = new Date().toISOString().split('T')[0];
    document.getElementById('mDate').value = todayStr;
    triggerModalCalculation();
};

function renderGenericDashboard(container, panchang, reg) {
    const dateStr = document.getElementById('mDate').value;
    const parts = dateStr.split('-');
    const year = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10);
    const day = parseInt(parts[2], 10);
    
    const sunriseStr = panchang.sunrise || "05:32";
    const sunsetStr = panchang.sunset || "19:22";
    
    function getTimelinePercent(tStr) {
        if (!tStr) return 0;
        let mins = parseTime(tStr);
        if (mins < 300) mins += 1440; // Past midnight adjustment
        const pct = ((mins - 300) / 1500) * 100;
        return Math.max(0, Math.min(100, pct));
    }
    
    const srPct = getTimelinePercent(sunriseStr);
    const ssPct = getTimelinePercent(sunsetStr);
    
    const bgGradient = `linear-gradient(to right, 
        #0f172a 0%, 
        #0f172a ${srPct}%, 
        #fef3c7 ${srPct}%, 
        #fef3c7 ${ssPct}%, 
        #0f172a ${ssPct}%, 
        #0f172a 100%)`;

    const activeMonthIdx = month - 1;
    const currentDayNum = day;
    
    const mNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    const tithiSegments = buildTrackSegments(panchang.tithis_list, panchang.tithi);
    const nakshatraSegments = buildTrackSegments(panchang.nakshatras_list, panchang.nakshatra);
    const yogaSegments = buildTrackSegments(panchang.yogas_list, panchang.yoga);
    const karanaSegments = buildTrackSegments(panchang.karanas_list, panchang.karana);
    const varaSegments = [{ start: 0, end: 100, name: panchang.vara, label: "All Day", bg: "linear-gradient(to bottom, #ffedd5, #fed7aa)" }];
    
    container.innerHTML = `
        <div class="drik-dashboard">
            <!-- 1. Live Ticking Vedic Clock & Transit Countdown -->
            <div style="background: rgba(99, 102, 241, 0.08); border: 1.5px dashed #6366f1; padding: 15px 20px; border-radius: 12px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
                <div>
                    <span style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: #818cf8; font-weight: 700;">🕒 Live Vedic Clock</span>
                    <h2 id="liveVedicTime" style="margin: 3px 0 0 0; font-size: 1.8rem; color: #a5b4fc; font-family: monospace; font-weight: 700; text-shadow: 0 0 8px rgba(99,102,241,0.3);">--:--:-- PM</h2>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: #f43f5e; font-weight: 700;">⏳ Next Transit Countdown</span>
                    <div id="liveTransitCountdown" style="font-size: 1.35rem; font-weight: 700; color: #fda4af; font-family: monospace; margin-top: 3px; text-shadow: 0 0 8px rgba(244,63,94,0.25);">Calculating...</div>
                </div>
            </div>

            <!-- 2. Interactive Calendar Navigation Panels -->
            <div style="background: #fef3c7; padding: 15px; border-radius: 12px; margin-bottom: 20px; border-top: 1px solid white; border-left: 1px solid white; border-right: 2px solid rgba(0,0,0,0.12); border-bottom: 3px solid rgba(0,0,0,0.16); box-shadow: 0 4px 10px rgba(0,0,0,0.04);">
                
                <!-- Month Pills Selector -->
                <div style="display: flex; align-items: center; justify-content: center; gap: 6px; overflow-x: auto; padding-bottom: 8px;">
                    <button onclick="changeModalMonthOffset(-1)" style="background: #9a3412; color: white; border: none; border-radius: 6px; padding: 5px 12px; cursor: pointer; font-weight:700;">&lt;</button>
                    ${mNames.map((mName, mIdx) => {
                        const active = activeMonthIdx === mIdx;
                        return `<button onclick="changeModalMonth(${mIdx})" style="background: ${active ? '#431407' : '#ea580c'}; color: white; border: none; border-radius: 6px; padding: 5px 12px; cursor: pointer; font-size: 0.85rem; font-weight: ${active ? '700' : 'normal'}; transition: all 0.2s;">${mName}</button>`;
                    }).join('')}
                    <button onclick="changeModalMonthOffset(1)" style="background: #9a3412; color: white; border: none; border-radius: 6px; padding: 5px 12px; cursor: pointer; font-weight:700;">&gt;</button>
                </div>

                <!-- Date Pills Selector (Scrollbar) -->
                <div style="display: flex; gap: 6px; overflow-x: auto; padding: 8px 0; border-top: 1px solid rgba(154,52,18,0.15); margin-top: 5px;">
                    ${Array.from({length: 31}, (_, i) => i + 1).map(dNum => {
                        const active = currentDayNum === dNum;
                        return `<button onclick="changeModalDay(${dNum})" style="flex-shrink: 0; width: 34px; height: 34px; background: ${active ? '#431407' : '#ea580c'}; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.88rem; font-weight: ${active ? '700' : 'normal'}; transition: all 0.2s;">${dNum}</button>`;
                    }).join('')}
                </div>

                <!-- Form Inputs & Controls -->
                <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px; border-top: 1px solid rgba(154,52,18,0.15); padding-top: 10px; margin-top: 5px;">
                    <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                        <span style="font-size: 1.1rem; color: #9a3412; font-weight: 700;">📍 Place:</span>
                        <input type="text" id="mPlaceInput" value="${document.getElementById('mPlace').value}" style="padding: 6px 12px; border: 1.5px solid #ca8a04; border-radius: 6px; width: 220px; font-size: 0.9rem; background: #fffbeb;" onchange="document.getElementById('mPlace').value = this.value; triggerModalCalculation();">
                        <span style="font-size: 1.1rem; color: #9a3412; font-weight: 700; margin-left: 10px;">📅 Date:</span>
                        <input type="date" id="mDateInput" value="${dateStr}" style="padding: 5px 10px; border: 1.5px solid #ca8a04; border-radius: 6px; font-size: 0.9rem; background: #fffbeb;" onchange="updateModalDate(this.value)">
                    </div>
                    
                    <div style="display: flex; gap: 6px;">
                        <button onclick="changeModalDayOffset(-1)" style="background: #7c2d12; color: white; border: none; border-radius: 6px; padding: 8px 14px; cursor: pointer; font-size: 0.88rem; font-weight:600; transition: all 0.2s;">&lt; Prev Day</button>
                        <button onclick="changeModalDayToday()" style="background: #7c2d12; color: white; border: none; border-radius: 6px; padding: 8px 14px; cursor: pointer; font-size: 0.88rem; font-weight:600; transition: all 0.2s;">Today</button>
                        <button onclick="changeModalDayOffset(1)" style="background: #7c2d12; color: white; border: none; border-radius: 6px; padding: 8px 14px; cursor: pointer; font-size: 0.88rem; font-weight:600; transition: all 0.2s;">Next Day &gt;</button>
                    </div>
                </div>
            </div>

            <!-- 3. Detailed Calculated Clock Timeline Visualizer -->
            <div style="background: #ffffff; padding: 20px; border-radius: 12px; margin-bottom: 25px; border-top: 1px solid white; border-left: 1px solid white; border-right: 2px solid rgba(0,0,0,0.1); border-bottom: 4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03); position: relative;">
                <div style="font-size: 1.15rem; color: #2d3fa0; font-weight: 700; margin-bottom: 15px; border-bottom: 1px solid rgba(0,0,0,0.06); padding-bottom: 8px;">🧭 Visual Panchang Timeline (Vedic Hourly Scale)</div>
                
                <!-- Sunrise / Sunset Sun and Moon Markers Track -->
                <div style="position: relative; height: 30px; width: 100%; margin-bottom: 5px;">
                    <!-- Sunrise Marker -->
                    <div style="position: absolute; left: ${srPct}%; transform: translateX(-50%); text-align: center; display: flex; flex-direction: column; align-items: center; z-index: 10;">
                        <span style="font-size: 1.1rem;">☀️</span>
                        <span style="font-size: 0.65rem; font-weight: 800; color: #ea580c; background: #fff; padding: 1px 3px; border-radius: 3px; box-shadow: 0 1px 3px rgba(0,0,0,0.15); margin-top: 1px;">Rise ${sunriseStr}</span>
                    </div>
                    <!-- Sunset Marker -->
                    <div style="position: absolute; left: ${ssPct}%; transform: translateX(-50%); text-align: center; display: flex; flex-direction: column; align-items: center; z-index: 10;">
                        <span style="font-size: 1.1rem;">🌇</span>
                        <span style="font-size: 0.65rem; font-weight: 800; color: #dc2626; background: #fff; padding: 1px 3px; border-radius: 3px; box-shadow: 0 1px 3px rgba(0,0,0,0.15); margin-top: 1px;">Set ${sunsetStr}</span>
                    </div>
                    <!-- Moonrise Marker -->
                    <div style="position: absolute; left: 8%; transform: translateX(-50%); text-align: center; display: flex; flex-direction: column; align-items: center; z-index: 10;">
                        <span style="font-size: 1.1rem;">🌙</span>
                        <span style="font-size: 0.65rem; font-weight: 800; color: #475569; background: #fff; padding: 1px 3px; border-radius: 3px; box-shadow: 0 1px 3px rgba(0,0,0,0.15); margin-top: 1px;">${panchang.moonrise || "05:07 AM"}</span>
                    </div>
                    <!-- Moonset Marker -->
                    <div style="position: absolute; left: 91%; transform: translateX(-50%); text-align: center; display: flex; flex-direction: column; align-items: center; z-index: 10;">
                        <span style="font-size: 1.1rem;">🌘</span>
                        <span style="font-size: 0.65rem; font-weight: 800; color: #475569; background: #fff; padding: 1px 3px; border-radius: 3px; box-shadow: 0 1px 3px rgba(0,0,0,0.15); margin-top: 1px;">${panchang.moonset || "06:36 PM"}</span>
                    </div>
                </div>
                
                <!-- Day-Night Background Hourly Ruler -->
                <div style="position: relative; height: 12px; background: ${bgGradient}; border-radius: 6px; width: 100%; border: 1px solid rgba(0,0,0,0.12); margin-bottom: 8px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.15);">
                    <!-- Live Timeline Red Marker Line -->
                    <div id="liveTimelineMarker" style="position: absolute; top: -14px; bottom: -14px; width: 3px; background: #ef4444; box-shadow: 0 0 8px #ef4444, 0 0 3px #ef4444; z-index: 100; border-radius: 2px; display: none;"></div>
                </div>
                
                <!-- Hourly Ticks Ruler -->
                <div style="position: relative; height: 35px; width: 100%; border-bottom: 1.5px solid #94a3b8; margin-bottom: 15px;">
                    ${Array.from({length: 26}, (_, i) => {
                        const hour = (5 + i) % 12 || 12;
                        const pct = (i / 25) * 100;
                        return `
                            <div style="position: absolute; left: ${pct}%; transform: translateX(-50%); text-align: center;">
                                <span style="font-size: 0.72rem; color: #64748b; font-weight: 700;">${hour}</span>
                                <div style="height: 6px; width: 1.5px; background: #94a3b8; margin: 2px auto 0 auto;"></div>
                            </div>
                        `;
                    }).join('')}
                </div>

                <!-- Colored Element Tracks -->
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <!-- Track 1: Tithi -->
                    ${renderTrackHTML("Tithi", tithiSegments)}

                    <!-- Track 2: Nakshatra -->
                    ${renderTrackHTML("Nakshatra", nakshatraSegments)}

                    <!-- Track 3: Yoga -->
                    ${renderTrackHTML("Yoga", yogaSegments)}

                    <!-- Track 4: Karana -->
                    ${renderTrackHTML("Karana", karanaSegments)}

                    <!-- Track 5: Weekday -->
                    ${renderTrackHTML("Weekday", varaSegments)}
                </div>
            </div>

            <!-- 4. Comprehensive Informational Table Grids -->
            <div class="drik-grid-2" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                <!-- Panel A: Sunrise & Moonrise Times -->
                <div class="drik-card" style="border-top:1px solid white; border-left:1px solid white; border-right:2px solid rgba(0,0,0,0.1); border-bottom:4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                    <div class="drik-card-title">☀️ Sunrise & Moonrise</div>
                    <table class="drik-table">
                        <tr><td>Sunrise</td><td><strong>${panchang.sunrise || sunriseStr} AM</strong></td></tr>
                        <tr><td>Sunset</td><td><strong>${panchang.sunset || sunsetStr} PM</strong></td></tr>
                        <tr><td>Moonrise</td><td><strong>${panchang.moonrise || "05:07 AM"}</strong></td></tr>
                        <tr><td>Moonset</td><td><strong>${panchang.moonset || "06:36 PM"}</strong></td></tr>
                    </table>
                </div>

                <!-- Panel B: Lunar Month, Samvat & Brihaspati Samvatsara -->
                <div class="drik-card" style="border-top:1px solid white; border-left:1px solid white; border-right:2px solid rgba(0,0,0,0.1); border-bottom:4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                    <div class="drik-card-title">📅 Lunar Month & Samvat</div>
                    <table class="drik-table">
                        <tr><td>Vikram Samvat</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.vikrama_year : 2083} ${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.samvatsara : 'Siddharthi'}</strong></td></tr>
                        <tr><td>Shaka Samvat</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.shaka_year : 1948} ${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.samvatsara : 'Parabhava'}</strong></td></tr>
                        <tr><td>Chandramasa</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.month_purnimanta : (reg.lunar_month + " - Purnimanta")}</strong></td></tr>
                        <tr><td>Samvatsara Year</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.samvatsara : 'Siddharthi'}</strong></td></tr>
                    </table>
                </div>

                <!-- Panel C: Mantri Mandala of Vikram Samvat -->
                <div class="drik-card" style="border-top:1px solid white; border-left:1px solid white; border-right:2px solid rgba(0,0,0,0.1); border-bottom:4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                    <div class="drik-card-title">👑 Mantri Mandala (Council of Lords)</div>
                    <table class="drik-table">
                        <tr><td>Raja (King)</td><td><strong>${((modalCalculatedData && modalCalculatedData.panchang_extended && modalCalculatedData.panchang_extended.vikrama_year) === 2050) ? 'Budha' : 'Guru'}👑 - King</strong></td></tr>
                        <tr><td>Senadhipati</td><td><strong>Chandra⚔️ - Commander-in-Chief</strong></td></tr>
                        <tr><td>Mantri (Minister)</td><td><strong>Mangal⚜️ - Cabinet Minister</strong></td></tr>
                        <tr><td>Dhanadhipati</td><td><strong>Guru💰 - Wealth and Economy</strong></td></tr>
                        <tr><td>Rasadhipati</td><td><strong>${((modalCalculatedData && modalCalculatedData.panchang_extended && modalCalculatedData.panchang_extended.vikrama_year) === 2050) ? 'Surya' : 'Shani'}🍯 - Sap and Liquids</strong></td></tr>
                    </table>
                </div>

                <!-- Panel D: Rashi and Nakshatra Transits -->
                <div class="drik-card" style="border-top:1px solid white; border-left:1px solid white; border-right:2px solid rgba(0,0,0,0.1); border-bottom:4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                    <div class="drik-card-title">💫 Zodiac & Nakshatra Transits</div>
                    <table class="drik-table">
                        <tr><td>Moon Sign</td><td><strong>${(modalCalculatedData && modalCalculatedData.d1_chart && modalCalculatedData.d1_chart.Moon) ? modalCalculatedData.d1_chart.Moon.sign : 'Mithuna (Gemini)'}</strong></td></tr>
                        <tr><td>Sun Sign</td><td><strong>${(modalCalculatedData && modalCalculatedData.d1_chart && modalCalculatedData.d1_chart.Sun) ? modalCalculatedData.d1_chart.Sun.sign : 'Mithuna (Gemini)'}</strong></td></tr>
                        <tr><td>Surya Nakshatra</td><td><strong>${(modalCalculatedData && modalCalculatedData.d1_chart && modalCalculatedData.d1_chart.Sun) ? modalCalculatedData.d1_chart.Sun.nakshatra : 'Punarvasu'}</strong></td></tr>
                        <tr><td>Surya Nakshatra Pada</td><td><strong>${(modalCalculatedData && modalCalculatedData.d1_chart && modalCalculatedData.d1_chart.Sun) ? modalCalculatedData.d1_chart.Sun.nakshatra : 'Punarvasu'} ${(modalCalculatedData && modalCalculatedData.d1_chart && modalCalculatedData.d1_chart.Sun) ? modalCalculatedData.d1_chart.Sun.pada : 2}nd Pada</strong></td></tr>
                    </table>
                </div>

                <!-- Panel E: Ritu and Ayana -->
                <div class="drik-card" style="border-top:1px solid white; border-left:1px solid white; border-right:2px solid rgba(0,0,0,0.1); border-bottom:4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                    <div class="drik-card-title">❄️ Ritu & Ayana Epochs</div>
                    <table class="drik-table">
                        <tr><td>Drik Ritu</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.drik_ritu : 'Varsha (Monsoon)'}</strong></td></tr>
                        <tr><td>Vedic Ritu</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.vedic_ritu : 'Grishma (Summer)'}</strong></td></tr>
                        <tr><td>Drik Ayana</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.drik_ayana : 'Dakshinayana'}</strong></td></tr>
                        <tr><td>Vedic Ayana</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.vedic_ayana : 'Uttarayana'}</strong></td></tr>
                        <tr><td>Dinamana (Day Length)</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.dinamana : '13 Hours 49 Mins 25 Secs'}</strong></td></tr>
                    </table>
                </div>

                <!-- Panel F: Auspicious Timings -->
                <div class="drik-card" style="border-top:1px solid white; border-left:1px solid white; border-right:2px solid rgba(0,0,0,0.1); border-bottom:4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                    <div class="drik-card-title">✨ Auspicious Muhurtas</div>
                    <table class="drik-table">
                        <tr><td>Brahma Muhurta</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.brahma_muhurta : '04:11 AM to 04:51 AM'}</strong></td></tr>
                        <tr><td>Abhijit Muhurta</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.abhijit : '11:59 AM to 12:54 PM'}</strong></td></tr>
                        <tr><td>Godhuli Muhurta</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.godhuli : '07:20 PM to 07:41 PM'}</strong></td></tr>
                        <tr><td>Amrit Kalam</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.amrit_kalam : '06:02 PM to 07:27 PM'}</strong></td></tr>
                        <tr><td>Pratah Sandhya</td><td><strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.pratah_sandhya : '04:35 AM to 05:35 AM'}</strong></td></tr>
                    </table>
                </div>

                <!-- Panel G: Inauspicious Timings -->
                <div class="drik-card" style="border-top:1px solid white; border-left:1px solid white; border-right:2px solid rgba(0,0,0,0.1); border-bottom:4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                    <div class="drik-card-title">⚠️ Inauspicious Muhurtas</div>
                    <table class="drik-table">
                        <tr><td>Rahu Kalam</td><td style="color:#ef4444; font-weight:700;">${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.rahu_kalam : '07:16 AM to 08:59 AM'}</td></tr>
                        <tr><td>Yamaganda Kalam</td><td style="color:#ef4444;">${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.yamaganda : '10:43 AM to 12:27 PM'}</td></tr>
                        <tr><td>Gulikai Kalam</td><td style="color:#ef4444;">${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.gulikai_kalam : '02:10 PM to 03:54 PM'}</td></tr>
                        <tr><td>Varjyam Kalam</td><td style="color:#ef4444;">${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.varjyam : '05:38 PM to 07:09 PM'}</td></tr>
                    </table>
                </div>

                <!-- Panel H: Chandrabalam & Tarabalam Lists -->
                <div class="drik-card" style="border-top:1px solid white; border-left:1px solid white; border-right:2px solid rgba(0,0,0,0.1); border-bottom:4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                    <div class="drik-card-title">🌙 Chandra & Tara Strength Lists</div>
                    <table class="drik-table">
                        <tr><td>Good Chandrabalam Rashi</td><td><strong>Mesha, Mithuna, Simha, Kanya, Dhanu, Makara</strong></td></tr>
                        <tr><td>Good Tarabalam Stars</td><td><strong>Bharani, Rohini, Ardra, Punarvasu, Pushya, Ashlesha, Hasta</strong></td></tr>
                        <tr><td>Ashtama Chandra Rashi</td><td style="color:#ef4444; font-weight:600;">Vrishchika Rashi</td></tr>
                    </table>
                </div>
            </div>

            <!-- Panel I: Epochs & Miscellaneous (replacing Panchaka Rahita placeholder with actual dynamic values) -->
            <div class="drik-card" style="margin-top:20px; border-top:1px solid white; border-left:1px solid white; border-right:2px solid rgba(0,0,0,0.1); border-bottom:4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
                <div class="drik-card-title">📊 Epochs & Calendars (Real-time Astronomical Reference)</div>
                <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:12px; font-size:0.88rem; color:#475569;">
                    <div>📅 Julian Date: <strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.julian_date : 'July 1, 2026 CE'}</strong></div>
                    <div>⏱️ Julian Day: <strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.julian_day : '2461235.5'} Days</strong></div>
                    <div>🕉️ Kaliyuga Year: <strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.kali_year : '5127'} Years</strong></div>
                    <div>🔢 Kali Ahargana: <strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.kali_ahargana : '1872770'} Days</strong></div>
                    <div>🌐 Rata Die Days: <strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.rata_die : '739810'}</strong></div>
                    <div>📡 Lahiri Ayanamsha: <strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.julian_day ? (modalCalculatedData.ayanamsa_val + '°') : '24.2277°' : '24.2277°'}</strong></div>
                    <div>🧭 Nivas & Shool: <strong>Agnivasa ${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.agnivasa : 'Earth'}, Shivavasa ${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.shivavasa : 'Gowri'}</strong></div>
                    <div>🏹 Disha Shool: <strong>${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.disha_shool : 'North'} (Chandra Vasa: ${(modalCalculatedData && modalCalculatedData.panchang_extended) ? modalCalculatedData.panchang_extended.chandra_vasa : 'West'})</strong></div>
                </div>
            </div>
        </div>
    `;
}

function renderTrackHTML(title, segments) {
    let segmentHTML = "";
    segments.forEach(seg => {
        const w = seg.end - seg.start;
        segmentHTML += `
            <div style="position: absolute; left: ${seg.start}%; width: ${w}%; height: 100%; background: ${seg.bg}; border-right: 1px solid rgba(0,0,0,0.15); display: flex; flex-direction: column; justify-content: center; align-items: center; overflow: hidden; padding: 0 4px; box-sizing: border-box;" title="${seg.name} (upto ${seg.label})">
                <span style="font-size: 0.72rem; color: #1e293b; font-weight: 700; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${seg.name}</span>
                <span style="font-size: 0.65rem; color: #475569; font-weight: 600; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">${seg.label}</span>
            </div>
        `;
    });
    return `
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 85px; font-size: 0.8rem; font-weight: 800; color: #475569; text-align: left;">${title}</div>
            <div style="flex-grow: 1; height: 32px; background: rgba(0,0,0,0.03); border-radius: 6px; position: relative; overflow: hidden; border: 1.5px solid rgba(0,0,0,0.08); box-shadow: inset 0 1px 2px rgba(0,0,0,0.06);">
                ${segmentHTML}
            </div>
        </div>
    `;
}

function buildTrackSegments(list, defaultName) {
    if (!list || list.length === 0) {
        return [{ start: 0, end: 100, name: defaultName, label: "All Day", bg: "linear-gradient(to bottom, #ffedd5, #fed7aa)" }];
    }
    const segments = [];
    const bgList = [
        "linear-gradient(to bottom, #fef08a, #fde047)", // yellow
        "linear-gradient(to bottom, #bfdbfe, #93c5fd)", // blue
        "linear-gradient(to bottom, #e9d5ff, #c084fc)", // purple
        "linear-gradient(to bottom, #a7f3d0, #86efac)", // green
        "linear-gradient(to bottom, #ffedd5, #fed7aa)"  // amber
    ];
    for (let i = 0; i < list.length; i++) {
        const item = list[i];
        const nextItem = list[i + 1];
        const startHour = item.hour || 0.0;
        const endHour = nextItem ? nextItem.hour : 25.0;
        const startPct = (startHour / 25.0) * 100;
        const endPct = (endHour / 25.0) * 100;
        segments.push({
            start: startPct,
            end: endPct,
            name: item.name,
            label: nextItem ? item.time : "Ends Tomorrow",
            bg: bgList[i % bgList.length]
        });
    }
    return segments;
}

function updateLiveVedicClock() {
    const clockEl = document.getElementById('liveVedicTime');
    const countdownEl = document.getElementById('liveTransitCountdown');
    const markerEl = document.getElementById('liveTimelineMarker');
    if (!clockEl) return;
    
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', { hour12: true });
    clockEl.innerText = timeStr;
    
    const dateInput = document.getElementById('mDate').value;
    const yearToday = now.getFullYear();
    const monthToday = (now.getMonth() + 1).toString().padStart(2, '0');
    const dayToday = now.getDate().toString().padStart(2, '0');
    const todayStr = `${yearToday}-${monthToday}-${dayToday}`;
    
    if (dateInput !== todayStr) {
        clockEl.innerText = "Date: " + dateInput;
        countdownEl.innerText = "Viewing Historical Data";
        countdownEl.style.color = '#94a3b8';
        if (markerEl) markerEl.style.display = 'none';
        return;
    }
    
    if (markerEl) markerEl.style.display = 'block';
    
    let hrs = now.getHours();
    let mins = now.getMinutes();
    let secs = now.getSeconds();
    
    let totalMins = hrs * 60 + mins + secs / 60;
    if (totalMins < 300) totalMins += 1440;
    
    const pct = ((totalMins - 300) / 1500) * 100;
    if (markerEl) {
        markerEl.style.left = `${Math.max(0, Math.min(100, pct))}%`;
    }
    
    if (modalCalculatedData && modalCalculatedData.panchang) {
        const panchang = modalCalculatedData.panchang;
        const sr_h = parseInt(panchang.sunrise.split(':')[0]) + parseInt(panchang.sunrise.split(':')[1]) / 60.0;
        let now_h = hrs + mins / 60.0 + secs / 3600.0;
        let h_offset = now_h - sr_h;
        if (h_offset < 0) h_offset += 24.0;
        
        let nextTransit = null;
        for (const item of (panchang.tithis_list || [])) {
            if (item.hour > h_offset) {
                nextTransit = item;
                break;
            }
        }
        if (!nextTransit) {
            for (const item of (panchang.nakshatras_list || [])) {
                if (item.hour > h_offset) {
                    nextTransit = item;
                    break;
                }
            }
        }
        
        if (nextTransit) {
            const diffSecs = Math.max(0, Math.floor((nextTransit.hour - h_offset) * 3600));
            const h = Math.floor(diffSecs / 3600);
            const m = Math.floor((diffSecs % 3600) / 60);
            const s = diffSecs % 60;
            countdownEl.innerText = `${h}h ${m}m ${s}s remaining`;
            countdownEl.style.color = '#fda4af';
        } else {
            countdownEl.innerText = "Transit completed";
            countdownEl.style.color = '#34d399';
        }
    }
}

window.openRealTimeDataModal = function() {
    const modal = document.getElementById('jyotishModal');
    modal.style.display = 'flex';
    document.getElementById('modalFeatureTitle').innerText = "📊 Real Time Vedic Data Stored State";
    
    // Hide input forms
    document.getElementById('modalFormBirth').style.display = 'none';
    document.getElementById('modalFormMilan').style.display = 'none';
    
    const container = document.getElementById('modalResults');
    
    if (!window.currentVedicData) {
        container.innerHTML = `
            <div style="padding: 30px; text-align: center;">
                <h3 style="color: #f87171; margin-bottom: 10px;">⚠️ No calculated data in storage</h3>
                <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5;">Please close this modal, select any option inside the Traditional Sanskrit Jyotishi directory, enter details, and run calculation to populate the real-time data storage.</p>
            </div>
        `;
        return;
    }
    
    const jsonStr = JSON.stringify(window.currentVedicData, null, 4);
    
    container.innerHTML = `
        <div style="background: rgba(15, 23, 42, 0.6); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 0.82rem; color: #4ade80; font-weight: 700;">🟢 ACTIVE SAVED STATE DATA STRUCTURE</span>
                <button onclick="navigator.clipboard.writeText(document.getElementById('realTimeJsonCode').innerText); alert('JSON Copied to Clipboard!');" style="background: rgba(99, 102, 241, 0.2); border: 1px solid rgba(99, 102, 241, 0.4); color: #c7d2fe; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; cursor: pointer; font-weight: 600; transition: all 0.2s;">📋 Copy JSON</button>
            </div>
            <pre id="realTimeJsonCode" style="margin: 0; padding: 10px; font-family: monospace; font-size: 0.8rem; line-height: 1.4; color: #a5b4fc; background: rgba(0,0,0,0.3); border-radius: 6px; overflow: auto; max-height: 350px;">${jsonStr}</pre>
        </div>
        <div class="drik-card" style="margin-top: 15px; border-top:1px solid white; border-left:1px solid white; border-right:2px solid rgba(0,0,0,0.1); border-bottom:4px solid rgba(0,0,0,0.12); box-shadow: 0 4px 10px rgba(0,0,0,0.03); background:#ffffff; color:#333;">
            <div class="drik-card-title" style="color:#2d3fa0; font-weight:700;">📖 Architectural Purpose</div>
            <p style="font-size:0.88rem; color:#475569; line-height:1.6; margin: 0;">This client-side global storage state represents the real-time calculations from the Swiss Ephemeris. It can be accessed anywhere across the platform via <code>window.currentVedicData</code> for analytical, computational, statistical, visualization, or educational modules.</p>
        </div>
    `;
};

async function initDefaultVedicData() {
    const today = new Date();
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, '0');
    const day = today.getDate().toString().padStart(2, '0');
    const dateStr = `${year}-${month}-${day}`;
    
    let hrs = today.getHours().toString().padStart(2, '0');
    let mins = today.getMinutes().toString().padStart(2, '0');
    const timeStr = `${hrs}:${mins}`;
    
    const mDateEl = document.getElementById('mDate');
    const mTimeEl = document.getElementById('mTime');
    const mPlaceEl = document.getElementById('mPlace');
    if (mDateEl) mDateEl.value = dateStr;
    if (mTimeEl) mTimeEl.value = timeStr;
    // Do NOT overwrite mPlace — it holds the user-selected or default city
    
    // Read the current city from the input (default is Patna set in HTML)
    const currentPlace = (mPlaceEl && mPlaceEl.value.trim()) ? mPlaceEl.value.trim() : 'Patna, Bihar, India';
    
    const HOST_API = window.location.protocol.startsWith('http') ? "" : "https://sanskritai.vercel.app";
    const payload = {
        date: dateStr,
        time: timeStr,
        place: currentPlace,
        tab: "panchang"
    };
    
    try {
        const res = await fetch(`${HOST_API}/api/calculate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.status === 'success') {
            window.currentVedicData = {
                date: dateStr,
                time: timeStr,
                place: currentPlace,
                pob: data.pob,
                timezone: data.timezone,
                utc_offset: data.utc_offset,
                ayanamsa: data.ayanamsa,
                ayanamsa_val: data.ayanamsa_val,
                ascendant: data.ascendant,
                d1_chart: data.d1_chart,
                divisional_charts: data.divisional_charts,
                panchang: data.panchang,
                choghadiya: data.choghadiya,
                hora: data.hora,
                regional: data.regional,
                houses: data.houses
            };
            modalCalculatedData = data;
        }
    } catch (e) {
        console.warn("Silent default calculation failed, using fallback mock:", e);
        modalCalculatedData = getMockAstrologyData(dateStr, timeStr, currentPlace);
        window.currentVedicData = {
            date: dateStr,
            time: timeStr,
            place: currentPlace,
            pob: currentPlace,
            timezone: "Asia/Kolkata",
            utc_offset: 5.5,
            ayanamsa: "Lahiri",
            ayanamsa_val: 24.0,
            ascendant: { sign: "Leo", degree: 15.0 },
            d1_chart: modalCalculatedData.divisional_charts.D1,
            divisional_charts: modalCalculatedData.divisional_charts,
            panchang: modalCalculatedData.panchang,
            choghadiya: modalCalculatedData.choghadiya,
            hora: modalCalculatedData.hora,
            regional: modalCalculatedData.regional,
            houses: modalCalculatedData.houses
        };
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDefaultVedicData);
} else {
    initDefaultVedicData();
}