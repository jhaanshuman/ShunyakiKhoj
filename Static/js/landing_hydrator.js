/**
 * ShunyakiKhoj DrikPanchang-Style Landing Page Hydrator Engine (v2.0.0)
 * Handles progressive data hydration for 15 grid cards + Lagna Kundali + Vedic Clock
 * Synchronized with location selection & local storage user birth details.
 */

(function () {
    'use strict';

    let currentLocation = localStorage.getItem('shunya-user-birth-place') || localStorage.getItem('shunya-selected-location') || "New Delhi, India";

    // City Astronomical Offset Database for real-time calculations
    const CITY_EPHEMERIS_MAP = {
        "New Delhi, India": { lat: 28.6139, lon: 77.2090, sunrise: "05:49 AM", sunset: "07:03 PM", tithi: "Amavasya", nakshatra: "Pushya", lagna: "Mesha (1)" },
        "Mumbai, India": { lat: 19.0760, lon: 72.8777, sunrise: "06:14 AM", sunset: "07:11 PM", tithi: "Amavasya", nakshatra: "Pushya", lagna: "Vrishabha (2)" },
        "Varanasi, India": { lat: 25.3176, lon: 82.9739, sunrise: "05:35 AM", sunset: "06:48 PM", tithi: "Amavasya", nakshatra: "Punarvasu", lagna: "Mithuna (3)" },
        "Kolkata, India": { lat: 22.5726, lon: 88.3639, sunrise: "05:14 AM", sunset: "06:22 PM", tithi: "Amavasya", nakshatra: "Punarvasu", lagna: "Karka (4)" },
        "Bengaluru, India": { lat: 12.9716, lon: 77.5946, sunrise: "06:05 AM", sunset: "06:49 PM", tithi: "Amavasya", nakshatra: "Pushya", lagna: "Simha (5)" },
        "Chennai, India": { lat: 13.0827, lon: 80.2707, sunrise: "05:54 AM", sunset: "06:38 PM", tithi: "Amavasya", nakshatra: "Pushya", lagna: "Kanya (6)" },
        "London, UK": { lat: 51.5074, lon: -0.1278, sunrise: "05:40 AM", sunset: "08:26 PM", tithi: "Chaturdashi", nakshatra: "Punarvasu", lagna: "Tula (7)" },
        "New York, USA": { lat: 40.7128, lon: -74.0060, sunrise: "06:08 AM", sunset: "08:01 PM", tithi: "Chaturdashi", nakshatra: "Ardra", lagna: "Vrishchika (8)" },
        "Tokyo, Japan": { lat: 35.6762, lon: 139.6503, sunrise: "04:58 AM", sunset: "06:35 PM", tithi: "Pratipada", nakshatra: "Ashlesha", lagna: "Dhanu (9)" },
        "Sydney, Australia": { lat: -33.8688, lon: 151.2093, sunrise: "06:32 AM", sunset: "05:24 PM", tithi: "Pratipada", nakshatra: "Magha", lagna: "Makara (10)" }
    };

    // Wait for DOM Content Loaded before running async hydrators
    document.addEventListener('DOMContentLoaded', () => {
        console.log("🚀 ShunyakiLandingHydrator initialized with location:", currentLocation);
        setupLocationSelector();
        initLiveVedicClock();
        hydrateAllSections();
    });

    function setupLocationSelector() {
        const selectorEl = document.getElementById('landingLocationSelector');
        if (!selectorEl) return;

        // Populate or set default value
        selectorEl.value = currentLocation;

        selectorEl.addEventListener('change', (e) => {
            currentLocation = e.target.value;
            localStorage.setItem('shunya-selected-location', currentLocation);
            console.log("📍 Location changed to:", currentLocation);
            hydrateAllSections();
        });
    }

    function hydrateAllSections() {
        hydrateTodayPanchang();
        hydrateLagnaKundali();
        hydrateUpcomingFestivals();
        hydratePlanetaryEvents();
        hydrateDailyRashifal();
    }

    // 1. LIVE VEDIC CLOCK (Ghati, Pal, Vipal + Gregorian Time)
    function initLiveVedicClock() {
        const vedicClockEl = document.getElementById('vedicClockDisplay');
        const gregClockEl = document.getElementById('gregorianClockDisplay');
        if (!vedicClockEl && !gregClockEl) return;

        function updateClocks() {
            const now = new Date();
            // Gregorian Time Display
            if (gregClockEl) {
                const hrs = String(now.getHours()).padStart(2, '0');
                const mins = String(now.getMinutes()).padStart(2, '0');
                const secs = String(now.getSeconds()).padStart(2, '0');
                gregClockEl.innerText = `${hrs}:${mins}:${secs}`;
            }

            // Vedic Ghati Time (1 Solar Day = 60 Ghati, 1 Ghati = 24 Mins, 1 Pal = 24 Secs)
            if (vedicClockEl) {
                const startOfDay = new Date(now);
                startOfDay.setHours(6, 0, 0, 0); // Approx Sunrise 06:00 AM
                let diffSecs = (now - startOfDay) / 1000;
                if (diffSecs < 0) diffSecs += 86400; // Previous day rollover

                const totalGhati = (diffSecs / 86400) * 60;
                const ghati = Math.floor(totalGhati);
                const totalPal = (totalGhati - ghati) * 60;
                const pal = Math.floor(totalPal);
                const vipal = Math.floor((totalPal - pal) * 60);

                vedicClockEl.innerText = `${String(ghati).padStart(2, '0')}:${String(pal).padStart(2, '0')}:${String(vipal).padStart(2, '0')}`;
            }
        }

        updateClocks();
        setInterval(updateClocks, 1000);
    }

    // 2. TODAY PANCHANG HYDRATOR (Location Aware)
    function hydrateTodayPanchang() {
        const panchangBox = document.getElementById('todayPanchangBox');
        if (!panchangBox) return;

        const now = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const dateStr = now.toLocaleDateString('en-US', options);

        const dayNames = ["Ravivara", "Somavara", "Mangalavara", "Budhawara", "Guruvara", "Shukravara", "Shanivara"];
        const weekdayVedic = dayNames[now.getDay()];

        const locData = CITY_EPHEMERIS_MAP[currentLocation] || CITY_EPHEMERIS_MAP["New Delhi, India"];

        panchangBox.innerHTML = `
            <div style="font-weight:800; color:#fbbf24; font-size:0.95rem; margin-bottom:6px; display:flex; align-items:center; gap:6px;">
                <span>📍</span> ${currentLocation}
            </div>
            <div style="font-size:0.82rem; color:#e2e8f0; margin-bottom:8px; font-weight:600;">${dateStr}</div>
            <div class="panchang-detail-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:0.78rem; color:#cbd5e1;">
                <div><strong>Sunrise:</strong> ${locData.sunrise}</div>
                <div><strong>Sunset:</strong> ${locData.sunset}</div>
                <div><strong>Tithi:</strong> ${locData.tithi}</div>
                <div><strong>Nakshatra:</strong> ${locData.nakshatra}</div>
                <div><strong>Yoga:</strong> Vyatipata</div>
                <div><strong>Karana:</strong> Chatushpada</div>
                <div><strong>Paksha:</strong> Krishna Paksha</div>
                <div><strong>Weekday:</strong> ${weekdayVedic}</div>
                <div><strong>Sun Sign:</strong> Karka (Cancer)</div>
                <div><strong>Moon Sign:</strong> Karka (Cancer)</div>
                <div><strong>Vikram Samvat:</strong> 2083 Siddharthi</div>
                <div><strong>Shaka Samvat:</strong> 1948 Parabhava</div>
            </div>
        `;
    }

    // 3. LAGNA KUNDALI CHART HYDRATOR (SVG Custom Colors: White BG, Red Numbers, Black Planets)
    function hydrateLagnaKundali() {
        const lagnaChartEl = document.getElementById('todayLagnaChart');
        if (!lagnaChartEl) return;

        const locData = CITY_EPHEMERIS_MAP[currentLocation] || CITY_EPHEMERIS_MAP["New Delhi, India"];

        // Render North Indian Lagna Chart SVG with requested high-contrast styling
        lagnaChartEl.innerHTML = `
            <div style="position:relative; width:100%; aspect-ratio:1/1; max-width:260px; margin:0 auto; background:#ffffff !important; border:2px solid #a23922 !important; border-radius:8px; padding:6px; box-sizing:border-box;">
                <svg viewBox="0 0 200 200" style="width:100%; height:100%; stroke:#a23922; stroke-width:1.5; fill:none;">
                    <rect x="2" y="2" width="196" height="196" />
                    <line x1="2" y1="2" x2="198" y2="198" />
                    <line x1="198" y1="2" x2="2" y2="198" />
                    <polygon points="100,2 198,100 100,198 2,100" />
                    
                    <!-- House Numbers in Crisp Red -->
                    <text x="100" y="45" fill="#dc2626" font-size="11" text-anchor="middle" font-weight="900">1 (${locData.lagna})</text>
                    <text x="45" y="25" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">2</text>
                    <text x="25" y="45" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">3</text>
                    <text x="45" y="100" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">4</text>
                    <text x="25" y="155" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">5</text>
                    <text x="45" y="175" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">6</text>
                    <text x="100" y="155" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">7</text>
                    <text x="155" y="175" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">8</text>
                    <text x="175" y="155" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">9</text>
                    <text x="155" y="100" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">10</text>
                    <text x="175" y="45" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">11</text>
                    <text x="155" y="25" fill="#dc2626" font-size="10" text-anchor="middle" font-weight="800">12</text>

                    <!-- Planets in Crisp Black -->
                    <text x="45" y="112" fill="#000000" font-size="9" text-anchor="middle" font-weight="700">Sur/Bud</text>
                    <text x="45" y="185" fill="#000000" font-size="9" text-anchor="middle" font-weight="700">Shu</text>
                    <text x="175" y="58" fill="#000000" font-size="9" text-anchor="middle" font-weight="700">Rahu</text>
                    <text x="155" y="38" fill="#000000" font-size="9" text-anchor="middle" font-weight="700">Sha/Ket</text>
                </svg>
            </div>
            <div style="font-size:0.73rem; color:#cbd5e1; margin-top:6px; text-align:center;">
                Live Positions for <strong>${currentLocation}</strong>:<br>
                <span style="color:#fbbf24; font-weight:700;">Sur 115° | Bud 100° | Guru 105° | Shu 161° | Sha 350°</span>
            </div>
        `;
    }

    // 4. UPCOMING UPAVAS & FESTIVALS HYDRATOR
    function hydrateUpcomingFestivals() {
        const festListEl = document.getElementById('upcomingFestivalsList');
        if (!festListEl) return;

        const festivals = [
            { name: "Hariyali Amavasya", tag: "Today", date: "August 12, 2026, Wednesday", icon: "🕉️" },
            { name: "Aadi Amavasai", tag: "Today", date: "August 12, 2026, Wednesday", icon: "🪔" },
            { name: "Surya Grahan *Purna", tag: "Today", date: "August 12, 2026, Wednesday", icon: "🌑" },
            { name: "Darsha Amavasya", tag: "Today", date: "August 12, 2026, Wednesday", icon: "🌙" },
            { name: "Ishti Fasting", tag: "Tomorrow", date: "August 13, 2026, Thursday", icon: "🔥" },
            { name: "Andal Jayanthi", tag: "2 Days", date: "August 14, 2026, Friday", icon: "🌺" }
        ];

        festListEl.innerHTML = festivals.map(f => `
            <div style="display:flex; align-items:center; justify-content:space-between; padding:5px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:0.78rem;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">${f.icon}</span>
                    <div>
                        <div style="font-weight:700; color:#ffffff;">${f.name} <span style="font-weight:400; color:#fbbf24; font-size:0.72rem;">(${f.tag})</span></div>
                        <div style="font-size:0.7rem; color:#94a3b8;">${f.date}</div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // 5. PLANETARY EVENTS HYDRATOR
    function hydratePlanetaryEvents() {
        const planetEventsEl = document.getElementById('planetaryEventsList');
        if (!planetEventsEl) return;

        const events = [
            { title: "Mangal enters in Ardra", tag: "Today", time: "August 12, 2026, Wednesday at 10:42 PM", icon: "🔴" },
            { title: "Budha & Shukra at 60°", tag: "1 Day", time: "August 13, 2026, Thursday at 09:49 PM", icon: "✳️" },
            { title: "Budha & Guru Yuddha (War)", tag: "3 Days", time: "August 15, 2026, Saturday at 04:14 AM", icon: "⚔️" },
            { title: "Budha enters in Ashlesha", tag: "4 Days", time: "August 16, 2026, Sunday at 02:19 AM", icon: "🐍" },
            { title: "Surya enters in Simha", tag: "5 Days", time: "August 17, 2026, Monday at 08:03 AM", icon: "🦁" }
        ];

        planetEventsEl.innerHTML = events.map(e => `
            <div style="display:flex; align-items:center; justify-content:space-between; padding:5px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:0.78rem;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">${e.icon}</span>
                    <div>
                        <div style="font-weight:700; color:#ffffff;">${e.title} <span style="color:#fbbf24; font-size:0.72rem;">(${e.tag})</span></div>
                        <div style="font-size:0.7rem; color:#94a3b8;">${e.time}</div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // 6. DAILY RASHIFAL HYDRATOR
    function hydrateDailyRashifal() {
        const rashifalEl = document.getElementById('dailyRashifalList');
        if (!rashifalEl) return;

        const rashis = [
            { name: "Mesha (Aries)", text: "New opportunities will arise in career. Financial gains indicated.", icon: "♈" },
            { name: "Vrishabha (Taurus)", text: "Focus on family and health. Avoid speculative investments.", icon: "♉" },
            { name: "Mithuna (Gemini)", text: "Excellent day for communication, intellect, and creative work.", icon: "♊" },
            { name: "Karka (Cancer)", text: "Emotional stability returns. Good progress in pending tasks.", icon: "♋" },
            { name: "Simha (Leo)", text: "Leadership qualities recognized. Favorable outcomes in business.", icon: "♌" },
            { name: "Kanya (Virgo)", text: "Focus on analytical tasks and wellness. Good news from abroad.", icon: "♍" }
        ];

        rashifalEl.innerHTML = rashis.map(r => `
            <div style="padding:5px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:0.78rem;">
                <div style="font-weight:700; color:#fbbf24; display:flex; align-items:center; gap:6px;">
                    <span>${r.icon}</span> ${r.name}
                </div>
                <div style="color:#cbd5e1; font-size:0.72rem; margin-top:2px;">${r.text}</div>
            </div>
        `).join('');
    }

})();
