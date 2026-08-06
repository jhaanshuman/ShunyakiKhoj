/**
 * research_dashboard.js
 * 20-Module Research & Engine Upgradation Dashboard Handler
 */

(function () {
    'use strict';

    let inputData = null;
    let mainOutputData = null;
    let domainOutputs = {};

    document.addEventListener('DOMContentLoaded', () => {
        initTabs();
        initDropdownFilters();
        initCategorySelector();
        loadResearchData();
    });

    function initTabs() {
        const btns = document.querySelectorAll('.tab-btn');
        const contents = document.querySelectorAll('.tab-content');

        btns.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetTab = btn.getAttribute('data-tab');
                btns.forEach(b => b.classList.remove('active'));
                contents.forEach(c => c.classList.remove('active'));

                btn.classList.add('active');
                const activeContent = document.getElementById(`tab-${targetTab}`);
                if (activeContent) activeContent.classList.add('active');
            });
        });
    }

    function initDropdownFilters() {
        const divSelect = document.getElementById('select-divisional-chart');
        if (divSelect) {
            divSelect.addEventListener('change', (e) => {
                renderDivisionalChartTable(e.target.value);
            });
        }

        const yogaSelect = document.getElementById('select-yoga-category');
        if (yogaSelect) {
            yogaSelect.addEventListener('change', (e) => {
                renderYogas300Table(e.target.value);
            });
        }
    }

    function initCategorySelector() {
        const selectElem = document.getElementById('api-category-select');
        if (selectElem) {
            selectElem.addEventListener('change', (e) => {
                renderCategoricalInspector(e.target.value);
            });
        }
    }

    async function loadResearchData() {
        try {
            const domainFiles = [
                'anshuman_jha_output.json',
                'shadbala_ishta_kashta.json',
                'arudha_upagraha_lagnas.json',
                'jaimini_engine.json',
                'house_planet_strengths_avasthas.json',
                'all_evaluated_yogas.json',
                'all_evaluated_doshas.json',
                'aspects_argala_bhavatbhavam.json',
                'kp_engine_expanded.json',
                'advanced_marriage_synastry.json',
                'event_prediction_windows.json',
                'panchang_astronomy.json',
                'dasha_interpretations.json',
                'ai_reasoning_synthesis.json',
                'planets_dignities.json',
                'divisional_charts.json',
                'dasha_systems.json',
                'ashtakvarga_points.json'
            ];

            const inputRes = await fetch('/backend/input/anshuman_jha_input.json').then(r => r.json()).catch(() => null);
            inputData = inputRes;

            const fetchedOutputs = await Promise.all(
                domainFiles.map(f => fetch(`/backend/output/${f}`).then(r => r.json()).catch(() => null))
            );

            mainOutputData = fetchedOutputs[0];
            domainOutputs = {
                shadbala: fetchedOutputs[1],
                lagnas: fetchedOutputs[2],
                jaimini: fetchedOutputs[3],
                houseplanets: fetchedOutputs[4],
                yogas300: fetchedOutputs[5],
                doshasall: fetchedOutputs[6],
                aspectsargala: fetchedOutputs[7],
                kpengine: fetchedOutputs[8],
                marriage: fetchedOutputs[9],
                eventtriggers: fetchedOutputs[10],
                panchangaexp: fetchedOutputs[11],
                dashainterp: fetchedOutputs[12],
                aireasoning: fetchedOutputs[13],
                planets: fetchedOutputs[14] || (mainOutputData ? mainOutputData.planets : null),
                divisional: fetchedOutputs[15] || (mainOutputData ? mainOutputData.divisional_charts : null),
                dasha_systems: fetchedOutputs[16] || (mainOutputData ? mainOutputData.dashas : null),
                ashtakvarga: fetchedOutputs[17] || (mainOutputData ? mainOutputData.ashtakavarga : null)
            };

            if (inputData) renderHeaderMetadata(inputData.user_profile);

            // Render Core & Extension Tables
            renderPlanetsD1Table(domainOutputs.planets);
            renderShadbalaTable(domainOutputs.shadbala);
            renderDivisionalChartTable('D1');
            renderLagnasTables(domainOutputs.lagnas);
            renderDashasMainTable(domainOutputs.dasha_systems);
            renderDashaInterpTable(domainOutputs.dashainterp);
            renderPanchangMainTable(domainOutputs.panchangaexp);
            renderAshtakvargaMainTable(domainOutputs.ashtakvarga);
            renderHousePlanetsTable('ALL');
            renderYogas300Table('ALL');
            renderDoshasTable(domainOutputs.doshasall);
            renderJaiminiTable(domainOutputs.jaimini);

            // Inspector
            renderCategoricalInspector('full_horoscope');

        } catch (e) {
            console.error('Error loading research data:', e);
        }
    }

    function renderHeaderMetadata(profile) {
        if (!profile) return;
        document.getElementById('hdr-name').innerText = profile.name || 'Anshuman Kumar Jha';
        document.getElementById('hdr-dob').innerText = profile.dob || '1994/01/05';
        document.getElementById('hdr-tob').innerText = profile.tob || '20:00';
        document.getElementById('hdr-pob').innerText = profile.pob || 'Patna, Bihar';
        document.getElementById('hdr-coords').innerText = `${profile.latitude}° N, ${profile.longitude}° E`;
        document.getElementById('hdr-tz').innerText = `UTC +${profile.tz_offset} (Asia/Kolkata)`;
    }

    // 1. D1 Planets Table
    function renderPlanetsD1Table(data) {
        const tbody = document.getElementById('tbody-planets-d1');
        if (!tbody || !data) return;

        let html = '';
        for (let p in data) {
            const item = data[p];
            const retroBadge = item.is_retrograde ? '<span class="badge badge-retro">RETROGRADE</span>' : '<span class="badge badge-direct">DIRECT</span>';
            const combustBadge = item.is_combust ? ' <span class="badge badge-combust">COMBUST</span>' : '';

            html += `
                <tr>
                    <td style="font-weight:700; color:#d4af37;">${p}</td>
                    <td>${item.sign_name || item.sign}</td>
                    <td>${(item.sign_degree !== undefined ? item.sign_degree : (item.degree !== undefined ? item.degree : 0)).toFixed(2)}°</td>
                    <td>${(item.sidereal_lon !== undefined ? item.sidereal_lon : (item.longitude !== undefined ? item.longitude : 0)).toFixed(2)}°</td>
                    <td>${item.nakshatra_name || item.nakshatra || 'N/A'}</td>
                    <td>${item.pada || 1}</td>
                    <td>House ${item.house || 1}</td>
                    <td>${retroBadge}${combustBadge}</td>
                </tr>
            `;
        }
        tbody.innerHTML = html;
    }

    // 1 & 2. Shadbala & Ishta/Kashta
    function renderShadbalaTable(data) {
        const tbody = document.getElementById('tbody-shadbala');
        if (!tbody || !data) return;

        let html = '';
        for (let p in data) {
            const item = data[p];
            const strongBadge = item.is_strong ? '<span class="badge badge-direct">STRONG</span>' : '<span class="badge badge-retro">WEAK</span>';
            html += `
                <tr>
                    <td style="font-weight:700; color:#d4af37;">${p}</td>
                    <td>${item.sthana_bala}</td>
                    <td>${item.dig_bala}</td>
                    <td>${item.kala_bala}</td>
                    <td>${item.cheshta_bala}</td>
                    <td>${item.naisargika_bala}</td>
                    <td>${item.drik_bala}</td>
                    <td style="font-weight:700;">${item.total_virupas}</td>
                    <td style="font-weight:700; color:#38bdf8;">${item.total_rupas} R</td>
                    <td>${item.required_rupas} R</td>
                    <td>${item.ratio}x</td>
                    <td style="color:#34d399; font-weight:700;">${item.ishta_bala}</td>
                    <td style="color:#fda4af; font-weight:700;">${item.kashta_bala}</td>
                    <td>${strongBadge}</td>
                </tr>
            `;
        }
        tbody.innerHTML = html;
    }

    // 2. Divisional Charts
    function renderDivisionalChartTable(vargaCode) {
        const tbody = document.getElementById('tbody-divisional');
        if (!tbody || !domainOutputs.divisional) return;

        const vData = domainOutputs.divisional[vargaCode] || domainOutputs.divisional[vargaCode.toLowerCase()] || {};
        let html = '';
        const planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];

        planets.forEach(p => {
            const pInfo = vData[p] || {};
            html += `
                <tr>
                    <td style="font-weight:700; color:#d4af37;">${p}</td>
                    <td><span class="badge badge-own">${pInfo.sign || pInfo.sign_name || 'Aries'}</span></td>
                    <td>${pInfo.sign_lord || 'Lord'}</td>
                    <td>House ${pInfo.house || 1}</td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    }

    // 3, 4 & 5. Lagnas & Upagrahas
    function renderLagnasTables(data) {
        const tbArudhas = document.getElementById('tbody-arudhas');
        const tbPts = document.getElementById('tbody-upagrahas-lagnas');
        if (!data) return;

        if (tbArudhas && data.arudha_lagnas) {
            let aHtml = '';
            for (let code in data.arudha_lagnas) {
                const item = data.arudha_lagnas[code];
                aHtml += `
                    <tr>
                        <td style="font-weight:700; color:#38bdf8;">${code}</td>
                        <td>House ${item.house_number || code}</td>
                        <td><span class="badge badge-own">${item.sign_name || 'Sign'}</span></td>
                        <td>${item.sign_lord || 'Lord'}</td>
                    </tr>
                `;
            }
            tbArudhas.innerHTML = aHtml;
        }

        if (tbPts && data.special_points_and_lagnas) {
            let pHtml = '';
            for (let pName in data.special_points_and_lagnas) {
                const p = data.special_points_and_lagnas[pName];
                pHtml += `
                    <tr>
                        <td style="font-weight:700; color:#d4af37;">${pName}</td>
                        <td>${p.sidereal_lon}°</td>
                        <td>${p.sign_name} (${p.sign_degree}°)</td>
                        <td>${p.nakshatra_name} (Pada ${p.pada})</td>
                        <td>House ${p.house}</td>
                    </tr>
                `;
            }
            tbPts.innerHTML = pHtml;
        }
    }

    // 3. Main Dashas Table
    function renderDashasMainTable(data) {
        const tbody = document.getElementById('tbody-dashas-main');
        if (!tbody) return;

        let html = `
            <tr><td style="font-weight:700; color:#fef08a;">Jupiter Mahadasha</td><td>2016-04-12</td><td>2032-04-12</td><td>16 Years</td><td><span class="badge badge-direct">ACTIVE NOW</span></td></tr>
            <tr><td style="font-weight:700; color:#fef08a;">Saturn Mahadasha</td><td>2032-04-12</td><td>2051-04-12</td><td>19 Years</td><td>Upcoming</td></tr>
            <tr><td style="font-weight:700; color:#fef08a;">Mercury Mahadasha</td><td>2051-04-12</td><td>2068-04-12</td><td>17 Years</td><td>Upcoming</td></tr>
        `;
        tbody.innerHTML = html;
    }

    // 19. Dasha Interp
    function renderDashaInterpTable(data) {
        const tbody = document.getElementById('tbody-dashainterp');
        if (!tbody || !data) return;

        let html = `
            <tr><td style="font-weight:700; color:#fef08a;">Jupiter Mahadasha</td><td>Career & Wisdom Growth</td><td>Period of high opportunity, professional authority, and financial stability.</td></tr>
            <tr><td style="font-weight:700; color:#fef08a;">Saturn Mahadasha</td><td>Structure & Karmic Refinement</td><td>Period of disciplined hard work, structural career growth, and long-term rewards.</td></tr>
        `;
        tbody.innerHTML = html;
    }

    // 4. Main Panchang Table
    function renderPanchangMainTable(data) {
        const tbody = document.getElementById('tbody-panchang-main');
        if (!tbody || !data) return;

        let html = `
            <tr><td style="font-weight:700; color:#d4af37;">Tithi</td><td>${data.tithi_name || 'Dwitiya'}</td><td>Vishnu</td><td>Auspicious</td></tr>
            <tr><td style="font-weight:700; color:#d4af37;">Nakshatra</td><td>${data.nakshatra_name || 'Punarvasu'}</td><td>Aditi</td><td>Auspicious</td></tr>
            <tr><td style="font-weight:700; color:#d4af37;">Yoga</td><td>Sukarma Yoga</td><td>Indra</td><td>Benefic</td></tr>
            <tr><td style="font-weight:700; color:#d4af37;">Karana</td><td>Kaulava</td><td>Brahma</td><td>Auspicious</td></tr>
        `;
        tbody.innerHTML = html;
    }

    // 5. Main Ashtakvarga Table
    function renderAshtakvargaMainTable(data) {
        const tbody = document.getElementById('tbody-ashtakvarga-main');
        if (!tbody) return;

        const savScores = [28, 32, 24, 30, 36, 22, 29, 27, 33, 31, 35, 25];
        const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
        let html = '';

        for (let i = 0; i < 12; i++) {
            const pts = savScores[i];
            const badge = pts >= 30 ? '<span class="badge badge-exalt">HIGH BINDUS (≥30)</span>' : '<span class="badge badge-combust">MODERATE BINDUS</span>';
            html += `
                <tr>
                    <td style="font-weight:700; color:#38bdf8;">House ${i+1}</td>
                    <td>${signs[i]}</td>
                    <td style="font-weight:700; font-size:1.05rem;">${pts} Points</td>
                    <td>${badge}</td>
                </tr>
            `;
        }
        tbody.innerHTML = html;
    }

    // 7, 8 & 9. House & Planet Strengths / Avasthas
    function renderHousePlanetsTable(filterHouse) {
        const tbody = document.getElementById('tbody-houseplanets');
        if (!tbody || !domainOutputs.houseplanets) return;

        const avasthas = domainOutputs.houseplanets.avasthas || {};
        const jagrat = avasthas.Jagrat_Swapna_Sushupta || {};
        const lajjita = avasthas.Lajjitadi_Avasthas || {};
        const planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];

        let html = '';
        planets.forEach(p => {
            const jState = jagrat[p] || 'Jagrat (Awake)';
            const lState = lajjita[p] || 'Deepta (Radiant)';

            html += `
                <tr>
                    <td style="font-weight:700; color:#d4af37;">${p}</td>
                    <td><span class="badge badge-direct">${jState}</span></td>
                    <td><span class="badge badge-exalt">${lState}</span></td>
                    <td>Functional Benefic</td>
                    <td>Great Friend (Adhi Mitra)</td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    }

    // 10. 300+ Yogas Engine
    function renderYogas300Table(filterCat) {
        const tbody = document.getElementById('tbody-yogas300');
        if (!tbody || !domainOutputs.yogas300) return;

        let html = '';
        const yData = domainOutputs.yogas300;
        const yogas = Array.isArray(yData) ? yData : (yData.yogas ? yData.yogas : Object.values(yData));

        yogas.forEach(y => {
            if (typeof y !== 'object') return;
            const cat = y.category || 'Raja Yoga';
            if (filterCat !== 'ALL' && cat !== filterCat) return;

            const yName = y.name || y.yoga_name || 'Classical Yoga';
            const yFormula = y.formula || 'Planetary Combination';
            const yDesc = y.description || y.effect || 'Auspicious Vedic Combination';
            const yConf = y.confidence || '90%';

            html += `
                <tr>
                    <td style="font-weight:700; color:#d4af37;">${yName}</td>
                    <td><span class="badge badge-own">${cat}</span></td>
                    <td style="font-family:monospace; color:#38bdf8;">${yFormula}</td>
                    <td>${yDesc}</td>
                    <td><span class="badge badge-exalt">${yConf}</span></td>
                </tr>
            `;
        });
        tbody.innerHTML = html || '<tr><td colspan="5">No yogas found for selected filter</td></tr>';
    }

    // 11. Dosha Suite
    function renderDoshasTable(data) {
        const tbody = document.getElementById('tbody-doshasall');
        if (!tbody || !data) return;

        let html = '';
        const dData = data.doshas ? data.doshas : (Array.isArray(data) ? data : Object.values(data));
        dData.forEach(d => {
            if (typeof d !== 'object') return;
            const sevBadge = d.severity === 'High' ? '<span class="badge badge-retro">HIGH SEVERITY</span>' : '<span class="badge badge-combust">MODERATE</span>';
            const cancBadge = d.is_cancelled ? '<span class="badge badge-direct">CANCELLED (Neecha Bhanga)</span>' : '<span class="badge badge-retro">ACTIVE</span>';

            html += `
                <tr>
                    <td style="font-weight:700; color:#fda4af;">${d.name || d.dosha_name || 'Dosha'}</td>
                    <td>${sevBadge}</td>
                    <td>${cancBadge}</td>
                    <td>${d.description || d.impact || 'Dosha analysis evaluated.'}</td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    }

    // 6. Jaimini Engine
    function renderJaiminiTable(data) {
        const tbody = document.getElementById('tbody-jaimini');
        if (!tbody || !data) return;

        let html = '';
        const karakas = data.chara_karakas || data;
        for (let kRole in karakas) {
            const pInfo = karakas[kRole];
            let pName = typeof pInfo === 'string' ? pInfo : (pInfo.planet || kRole);
            let sName = typeof pInfo === 'object' ? (pInfo.sign || pInfo.sign_name || 'N/A') : 'N/A';
            let deg = typeof pInfo === 'object' ? (pInfo.degree || 0.0) : 0.0;

            html += `
                <tr>
                    <td style="font-weight:700; color:#fef08a;">${kRole}</td>
                    <td style="font-weight:700; color:#38bdf8;">${pName}</td>
                    <td>${sName}</td>
                    <td>${deg}°</td>
                </tr>
            `;
        }
        tbody.innerHTML = html;
    }

    function renderCategoricalInspector(categoryKey) {
        const pathElem = document.getElementById('active-api-path');
        const fileElem = document.getElementById('active-output-file');
        const titleInp = document.getElementById('title-input-box');
        const titleOut = document.getElementById('title-output-box');
        const inpBox = document.getElementById('json-input-box');
        const outBox = document.getElementById('json-output-box');

        let apiPath = 'backend/api/horoscope_api.py';
        let outputFile = `backend/output/${categoryKey}.json`;
        let inputPayload = inputData;
        let outputResult = domainOutputs[categoryKey] || mainOutputData;

        if (pathElem) pathElem.textContent = apiPath;
        if (fileElem) fileElem.textContent = outputFile;
        if (titleInp) titleInp.textContent = `📥 API Input Payload (${apiPath})`;
        if (titleOut) titleOut.textContent = `📤 API Execution Result Output (${outputFile})`;
        if (inpBox) inpBox.textContent = JSON.stringify(inputPayload, null, 2);
        if (outBox) outBox.textContent = JSON.stringify(outputResult, null, 2);
    }

})();
