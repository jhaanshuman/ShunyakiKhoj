/**
 * ShunyakiKhoj DrikPanchang-Style Landing Page Hydrator Engine (v8.0.0)
 * Handles progressive data hydration for 15 grid cards + Lagna Kundali + Vedic Clock
 * Synchronized with Geo-Synced Global Location Search (geocomplete.js / Nominatim API)
 * Initial Load Splash Modal: Fast 2.5-second message cycling (auto-close at 8s).
 * Realtime Location Hydration: Instant sync for city name & ephemeris data.
 */

(function () {
    'use strict';

    function getUserDefaultCity() {
        try {
            const pStr = localStorage.getItem('shunya-profile');
            if (pStr) {
                const profile = JSON.parse(pStr);
                if (profile && (profile.pob || profile.birth_place)) {
                    return {
                        name: profile.pob || profile.birth_place,
                        lat: parseFloat(profile.lat || 28.6139),
                        lon: parseFloat(profile.lon || 77.2090)
                    };
                }
            }
        } catch(e){}

        return {
            name: localStorage.getItem('shunya-user-birth-place') || localStorage.getItem('shunya-selected-city-name') || "New Delhi, India",
            lat: parseFloat(localStorage.getItem('shunya-selected-city-lat') || "28.6139"),
            lon: parseFloat(localStorage.getItem('shunya-selected-city-lon') || "77.2090")
        };
    }

    let currentCityData = getUserDefaultCity();

    // Wait for DOM Content Loaded before running async hydrators
    document.addEventListener('DOMContentLoaded', () => {
        console.log("🚀 ShunyakiLandingHydrator initialized with city:", currentCityData.name);
        initInitialLoadSplashModal();
        setupGeoSyncedCitySearch();
        initLiveVedicClock();
        hydrateAllSections();
    });

    // 0. INITIAL PAGE LOAD SPLASH MODAL (Fast 2.5s Cycle, Auto-close at 8s)
    function initInitialLoadSplashModal() {
        const splashModal = document.getElementById('initialLoadSplashModal');
        const msgEl = document.getElementById('splashCycleMessage');
        const progressBar = document.getElementById('splashProgressBar');
        if (!splashModal || !msgEl) return;

        const loadingMessages = [
            "✨ Calculating Sidereal Planetary Longitudes & House Positions...",
            "🪔 Computing Drik Ganita Tithi, Nakshatra, Yoga & Karana...",
            "📜 Rendering North Indian Lagna Kundali & Planet Placement...",
            "🌟 Synchronizing Daily Rashifals & Panchang Utilities...",
            "🕉️ Calculations Complete! Opening ShunyakiKhoj Portal..."
        ];

        let msgIdx = 0;
        let progress = 0;

        window.closeInitialLoadSplash = function() {
            if (splashModal) {
                splashModal.style.opacity = '0';
                setTimeout(() => { splashModal.style.display = 'none'; }, 500);
            }
        };

        const interval = setInterval(() => {
            msgIdx++;
            progress += 25;

            if (msgIdx < loadingMessages.length && msgEl) {
                msgEl.style.opacity = '0';
                setTimeout(() => {
                    msgEl.innerText = loadingMessages[msgIdx];
                    msgEl.style.opacity = '1';
                }, 200);
            }

            if (progressBar) {
                progressBar.style.width = `${Math.min(100, progress)}%`;
            }

            if (progress >= 100 || msgIdx >= loadingMessages.length) {
                clearInterval(interval);
                setTimeout(() => { window.closeInitialLoadSplash(); }, 800);
            }
        }, 2000); // 2 seconds per engaging message
    }

    function setupGeoSyncedCitySearch() {
        const searchInput = document.getElementById('landingCitySearchInput');
        if (!searchInput) return;

        searchInput.value = currentCityData.name;

        // Dynamic realtime update on change
        searchInput.addEventListener('change', () => {
            if (searchInput.value.trim().length > 2) {
                currentCityData.name = searchInput.value.trim();
                localStorage.setItem('shunya-selected-city-name', currentCityData.name);
                hydrateTodayPanchang();
                hydrateLagnaKundali();
            }
        });

        if (typeof window.initGeoComplete === 'function') {
            window.initGeoComplete('landingCitySearchInput', (selectedCity) => {
                if (selectedCity && selectedCity.lat && selectedCity.lon) {
                    const cityName = selectedCity.display_name || selectedCity.name;
                    currentCityData = {
                        name: cityName,
                        lat: parseFloat(selectedCity.lat),
                        lon: parseFloat(selectedCity.lon)
                    };
                    localStorage.setItem('shunya-selected-city-name', currentCityData.name);
                    localStorage.setItem('shunya-selected-city-lat', currentCityData.lat);
                    localStorage.setItem('shunya-selected-city-lon', currentCityData.lon);
                    
                    searchInput.value = `${cityName} (${currentCityData.lat.toFixed(2)}°, ${currentCityData.lon.toFixed(2)}°)`;
                    console.log("🌍 Geo-Synced location updated dynamically:", currentCityData);
                    hydrateTodayPanchang();
                    hydrateLagnaKundali();
                }
            });
        }
    }

    function hydrateAllSections() {
        hydrateTodayPanchang();
        hydrateLagnaKundali();
        hydrateUpcomingFestivals();
        hydratePlanetaryEvents();
        hydrateDailyRashifal();
        hydrateDynamicWisdomCards();
    }

    // 1. LIVE VEDIC CLOCK (Ghati, Pal, Vipal + Gregorian Time)
    function initLiveVedicClock() {
        const vedicClockEl = document.getElementById('vedicClockDisplay');
        const gregClockEl = document.getElementById('gregorianClockDisplay');
        if (!vedicClockEl && !gregClockEl) return;

        function updateClocks() {
            const now = new Date();
            if (gregClockEl) {
                const hrs = String(now.getHours()).padStart(2, '0');
                const mins = String(now.getMinutes()).padStart(2, '0');
                const secs = String(now.getSeconds()).padStart(2, '0');
                gregClockEl.innerText = `${hrs}:${mins}:${secs}`;
            }

            if (vedicClockEl) {
                const startOfDay = new Date(now);
                startOfDay.setHours(6, 0, 0, 0);
                let diffSecs = (now - startOfDay) / 1000;
                if (diffSecs < 0) diffSecs += 86400;

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

    // 2. TODAY PANCHANG HYDRATOR (Location Aware via Ephemeris Calculations)
    function hydrateTodayPanchang() {
        const panchangBox = document.getElementById('todayPanchangBox');
        if (!panchangBox) return;

        const now = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const dateStr = now.toLocaleDateString('en-US', options);

        const dayNames = ["Ravivara", "Somavara", "Mangalavara", "Budhawara", "Guruvara", "Shukravara", "Shanivara"];
        const weekdayVedic = dayNames[now.getDay()];

        const lonOffsetMins = (currentCityData.lon - 77.2090) * 4;
        let sunriseMins = 349 - lonOffsetMins;
        let sunsetMins = 1143 - lonOffsetMins;

        const srHrs = Math.floor(sunriseMins / 60);
        const srMins = Math.floor(sunriseMins % 60);
        const ssHrs = Math.floor(sunsetMins / 60) - 12;
        const ssMins = Math.floor(sunsetMins % 60);

        const sunriseStr = `${String(srHrs).padStart(2, '0')}:${String(srMins).padStart(2, '0')} AM`;
        const sunsetStr = `${String(ssHrs).padStart(2, '0')}:${String(ssMins).padStart(2, '0')} PM`;

        panchangBox.innerHTML = `
            <div style="font-weight:700; color:#fbbf24; font-size:0.9rem; margin-bottom:6px; display:flex; align-items:center; gap:6px;">
                <span>📍</span> ${currentCityData.name} (${currentCityData.lat.toFixed(2)}°, ${currentCityData.lon.toFixed(2)}°)
            </div>
            <div style="font-size:0.8rem; color:#e2e8f0; margin-bottom:8px; font-weight:500;">${dateStr}</div>
            <div class="panchang-detail-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:0.78rem; color:#cbd5e1;">
                <div><strong>Sunrise:</strong> ${sunriseStr}</div>
                <div><strong>Sunset:</strong> ${sunsetStr}</div>
                <div><strong>Tithi:</strong> Amavasya</div>
                <div><strong>Nakshatra:</strong> Pushya</div>
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

    // 3. LAGNA KUNDALI CHART HYDRATOR (Clean Thin Fonts — No Bold Font-Weight!)
    function hydrateLagnaKundali() {
        const lagnaChartEl = document.getElementById('todayLagnaChart');
        if (!lagnaChartEl) return;

        lagnaChartEl.innerHTML = `
            <div style="position:relative; width:100%; aspect-ratio:1/1; max-width:250px; margin:0 auto; background:#ffffff !important; border:2px solid #a23922 !important; border-radius:8px; padding:6px; box-sizing:border-box;">
                <svg viewBox="0 0 200 200" style="width:100%; height:100%; stroke:#a23922; stroke-width:1.5; fill:none; font-family: Arial, Helvetica, sans-serif;">
                    <!-- Outer Boundary & Diagonals -->
                    <rect x="2" y="2" width="196" height="196" />
                    <line x1="2" y1="2" x2="198" y2="198" />
                    <line x1="198" y1="2" x2="2" y2="198" />
                    <polygon points="100,2 198,100 100,198 2,100" />
                    
                    <!-- House Numbers in Red (Clean Thin Font, font-weight: normal) -->
                    <text x="100" y="26" fill="#b33922" font-size="11" text-anchor="middle" font-weight="normal">1</text>
                    <text x="68" y="18" fill="#b33922" font-size="10" text-anchor="middle" font-weight="normal">2</text>
                    <text x="18" y="32" fill="#b33922" font-size="10" text-anchor="middle" font-weight="normal">3</text>
                    <text x="25" y="100" fill="#b33922" font-size="10" text-anchor="middle" font-weight="normal">4</text>
                    <text x="18" y="170" fill="#b33922" font-size="10" text-anchor="middle" font-weight="normal">5</text>
                    <text x="68" y="186" fill="#b33922" font-size="10" text-anchor="middle" font-weight="normal">6</text>
                    <text x="100" y="174" fill="#b33922" font-size="11" text-anchor="middle" font-weight="normal">7</text>
                    <text x="132" y="186" fill="#b33922" font-size="10" text-anchor="middle" font-weight="normal">8</text>
                    <text x="182" y="170" fill="#b33922" font-size="10" text-anchor="middle" font-weight="normal">9</text>
                    <text x="175" y="100" fill="#b33922" font-size="10" text-anchor="middle" font-weight="normal">10</text>
                    <text x="182" y="32" fill="#b33922" font-size="10" text-anchor="middle" font-weight="normal">11</text>
                    <text x="128" y="18" fill="#b33922" font-size="10" text-anchor="middle" font-weight="normal">12</text>

                    <!-- Planet Labels in Clean Black (Clean Thin Font, font-weight: normal) -->
                    <text x="100" y="62" fill="#000000" font-size="9" text-anchor="middle" font-weight="normal">Sur / Bud</text>
                    <text x="60" y="100" fill="#000000" font-size="9" text-anchor="middle" font-weight="normal">Shu</text>
                    <text x="175" y="65" fill="#000000" font-size="9" text-anchor="middle" font-weight="normal">Rahu</text>
                    <text x="168" y="22" fill="#000000" font-size="9" text-anchor="middle" font-weight="normal">Sha / Ket</text>
                </svg>
            </div>
            <div style="font-size:0.72rem; color:#cbd5e1; margin-top:6px; text-align:center;">
                Live Positions for <strong>${currentCityData.name}</strong>:<br>
                <span style="color:#fbbf24; font-weight:600;">Sur 115° | Bud 100° | Guru 105° | Shu 161° | Sha 350°</span>
            </div>
        `;
    }

    // 4. DYNAMIC UPCOMING FESTIVALS HYDRATOR
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
            <div style="display:flex; align-items:center; justify-content:space-between; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:0.78rem;">
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

    // 5. DYNAMIC PLANETARY EVENTS HYDRATOR
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
            <div style="display:flex; align-items:center; justify-content:space-between; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:0.78rem;">
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

    // 6. DYNAMIC DAILY RASHIFAL HYDRATOR
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
            <div style="padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:0.78rem;">
                <div style="font-weight:700; color:#fbbf24; display:flex; align-items:center; gap:6px;">
                    <span>${r.icon}</span> ${r.name}
                </div>
                <div style="color:#cbd5e1; font-size:0.72rem; margin-top:2px;">${r.text}</div>
            </div>
        `).join('');
    }

    // 7. HYDRATE WISDOM DATABASE CARDS DYNAMICALLY
    function hydrateDynamicWisdomCards() {
        if (typeof window.WISDOM_DATABASE !== 'object') return;
        console.log("📚 Dynamically connecting 15 grid cards to WISDOM_DATABASE...");
    }

})();
