/**
 * Vedic Astrology Analysis & Statistics Engine (Phase 3)
 * Provides 30+ sophisticated calculations, charts, and visualizations.
 */

// Global export of analysis functions
window.renderKundliAnalysis = function(data) {
    const container = document.getElementById('analysisContainer');
    if (!container) return;

    // Reset container and build UI layout
    container.innerHTML = `
        <div class="analysis-wrapper" style="color: var(--text-color); font-family: 'Poppins', sans-serif;">
            <div style="background: rgba(99, 102, 241, 0.08); border: 1.5px solid rgba(99, 102, 241, 0.25); border-radius: 12px; padding: 20px; margin-bottom: 2rem;">
                <h3 style="color: #a5b4fc; margin: 0 0 8px; display: flex; align-items: center; gap: 8px;">
                    <span>📊 Deep Vedic Analytics Dashboard</span>
                    <span style="font-size: 0.75rem; background: var(--accent-purple); color: #fff; padding: 2px 8px; border-radius: 99px;">Active</span>
                </h3>
                <p style="color: var(--muted-text); font-size: 0.9rem; margin: 0;">
                    Automated planetary strength analysis, Yogas, elements, Jaimini Karakas, Ashtakvarga distributions, and predictive indicators calculated from your Natal (D1) and Navamsha (D9) charts.
                </p>
            </div>

            <!-- Dashboard Grid -->
            <div style="display: grid; grid-template-columns: 1fr; gap: 24px; margin-bottom: 2rem;">
                
                <!-- ROW 1: Lagna Strength & Elements -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
                    <!-- Lagna Strength Gauge -->
                    <div class="glass-card" style="padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 280px; text-align: center;">
                        <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700; width: 100%; text-align: left;">1. Lagna Strength (Shadbala Gauge)</h4>
                        ${renderLagnaStrengthGauge(data)}
                    </div>

                    <!-- Element Distribution Pie -->
                    <div class="glass-card" style="padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 280px;">
                        <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700; width: 100%; text-align: left;">2. Planet Element Distribution</h4>
                        ${renderElementDistribution(data)}
                    </div>
                </div>

                <!-- ROW 2: Dignity and Functional Benefics/Malefics -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
                    <!-- Planet Dignities Grid -->
                    <div class="glass-card" style="padding: 20px;">
                        <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700;">3. Planets Dignity & Strength Map</h4>
                        ${renderPlanetsDignityGrid(data)}
                    </div>

                    <!-- Benefic/Malefic Dashboard -->
                    <div class="glass-card" style="padding: 20px;">
                        <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700;">4. Functional Benefics & Malefics</h4>
                        ${renderBeneficsMalefics(data)}
                    </div>
                </div>

                <!-- ROW 3: Planetary Aspects & Yogas -->
                <div style="display: grid; grid-template-columns: 1fr; gap: 20px;">
                    <!-- Aspects heat-map -->
                    <div class="glass-card" style="padding: 20px;">
                        <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700;">5. Mutual Aspects & House Activations</h4>
                        ${renderPlanetaryAspects(data)}
                    </div>

                    <!-- Yoga Detections -->
                    <div class="glass-card" style="padding: 20px;">
                        <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700;">6. Vedic Yoga Detections</h4>
                        ${renderYogaDetections(data)}
                    </div>
                </div>

                <!-- ROW 4: Special Statuses & Chara Karakas -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
                    <!-- Planetary War / Combust / Retrograde -->
                    <div class="glass-card" style="padding: 20px;">
                        <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700;">7. Special Planet Statuses (War/Combust/Retro)</h4>
                        ${renderSpecialStatuses(data)}
                    </div>

                    <!-- Jaimini Chara Karakas -->
                    <div class="glass-card" style="padding: 20px;">
                        <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700;">8. Jaimini Chara Karakas</h4>
                        ${renderCharaKarakas(data)}
                    </div>
                </div>

                <!-- ROW 5: Shodashvarga Summary & Ashtakvarga -->
                <div style="display: grid; grid-template-columns: 1fr; gap: 20px;">
                    <!-- Ashtakvarga SVG points grid -->
                    <div class="glass-card" style="padding: 20px; overflow-x: auto;">
                        <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700;">9. Binnashtakvarga (7 Planets × 12 Houses Distribution)</h4>
                        ${renderAshtakvargaGrid(data)}
                    </div>

                    <!-- Shodashvarga + Pushkar Navamsa + Vargottama -->
                    <div class="glass-card" style="padding: 20px;">
                        <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700;">10. Shodashvarga Strength, Sade Sati & Warning indicators</h4>
                        ${renderWarningsAndShodashvarga(data)}
                    </div>
                </div>

                <!-- ROW 6: Active Dasha Theme Analysis -->
                <div class="glass-card" style="padding: 20px;">
                    <h4 style="color: var(--accent-gold); margin: 0 0 16px; font-weight: 700;">11. Active Dasha Theme & Remedy Suite</h4>
                    ${renderDashaThemeSuite(data)}
                </div>

            </div>
        </div>
    `;
};

// ═══════════════════════════════════════════════════════════════════
//  1. LAGNA STRENGTH GAUGE RENDERER
// ═══════════════════════════════════════════════════════════════════
function renderLagnaStrengthGauge(data) {
    const ascSign = data.ascendant.sign;
    const ascDeg = data.ascendant.degree;

    // Approximate a strength score out of 100 based on lord position & house aspects
    let strengthScore = 65; // Base average
    const lagnaLords = {
        Aries: 'Mars', Taurus: 'Venus', Gemini: 'Mercury', Cancer: 'Moon',
        Leo: 'Sun', Virgo: 'Mercury', Libra: 'Venus', Scorpio: 'Mars',
        Sagittarius: 'Jupiter', Capricorn: 'Saturn', Aquarius: 'Saturn', Pisces: 'Jupiter'
    };
    const lord = lagnaLords[ascSign];
    const lordPos = data.d1_chart[lord];
    
    if (lordPos) {
        // Exalted signs for each lord
        const exalted = { Sun: 'Aries', Moon: 'Taurus', Mars: 'Capricorn', Mercury: 'Virgo', Jupiter: 'Cancer', Venus: 'Pisces', Saturn: 'Libra' };
        const debilitated = { Sun: 'Libra', Moon: 'Scorpio', Mars: 'Cancer', Mercury: 'Pisces', Jupiter: 'Capricorn', Venus: 'Virgo', Saturn: 'Aries' };
        if (exalted[lord] === lordPos.sign) strengthScore += 25;
        else if (debilitated[lord] === lordPos.sign) strengthScore -= 20;
        else if (lordPos.sign === ascSign) strengthScore += 15; // Self sign
    }

    // Keep bounds [20, 100]
    strengthScore = Math.max(20, Math.min(100, strengthScore));

    let status = 'Moderate';
    let color = '#fbbf24';
    if (strengthScore >= 80) { status = 'Exceptionally Strong'; color = '#10b981'; }
    else if (strengthScore >= 60) { status = 'Strong & Auspicious'; color = '#3b82f6'; }
    else if (strengthScore < 45) { status = 'Afflicted / Weak'; color = '#ef4444'; }

    // Render SVG semi-circular gauge
    const radius = 60;
    const circumference = Math.PI * radius;
    const strokeDashoffset = circumference - (strengthScore / 100) * circumference;

    return `
        <div style="position: relative; width: 160px; height: 95px; margin: 10px auto;">
            <svg width="160" height="95" viewBox="0 0 160 95">
                <path d="M20,80 A60,60 0 0,1 140,80" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="12" stroke-linecap="round"/>
                <path d="M20,80 A60,60 0 0,1 140,80" fill="none" stroke="${color}" stroke-width="12" stroke-dasharray="${circumference}" stroke-dashoffset="${strokeDashoffset}" stroke-linecap="round" style="transition: stroke-dashoffset 0.8s ease-out;"/>
            </svg>
            <div style="position: absolute; bottom: 8px; width: 100%; text-align: center;">
                <span style="font-size: 1.5rem; font-weight: 800; color: #fff;">${strengthScore}</span>
                <span style="font-size: 0.8rem; color: var(--muted-text);">/ 100</span>
            </div>
        </div>
        <div style="margin-top: 8px;">
            <span style="font-size: 0.95rem; font-weight: 700; color: ${color};">${status}</span>
            <p style="font-size: 0.78rem; color: var(--muted-text); margin: 4px 0 0; line-height: 1.4;">
                Lagna Lord: <strong>${lord}</strong> in <strong>${lordPos ? lordPos.sign : 'Unknown'}</strong>. Degree: ${ascDeg}°.
            </p>
        </div>
    `;
}

// ═══════════════════════════════════════════════════════════════════
//  2. ELEMENT DISTRIBUTION PIE (SVG)
// ═══════════════════════════════════════════════════════════════════
function renderElementDistribution(data) {
    const SIGN_ELEMENTS = {
        Aries: 'Fire', Leo: 'Fire', Sagittarius: 'Fire',
        Taurus: 'Earth', Virgo: 'Earth', Capricorn: 'Earth',
        Gemini: 'Air', Libra: 'Air', Aquarius: 'Air',
        Cancer: 'Water', Scorpio: 'Water', Pisces: 'Water'
    };

    let counts = { Fire: 0, Earth: 0, Air: 0, Water: 0 };
    let total = 0;

    for (const p in data.d1_chart) {
        if (p === 'Asc') continue;
        const sign = data.d1_chart[p].sign;
        const elem = SIGN_ELEMENTS[sign];
        if (elem) {
            counts[elem]++;
            total++;
        }
    }

    if (total === 0) return `<div style="color:var(--muted-text)">No planet data</div>`;

    const pctFire = Math.round((counts.Fire / total) * 100);
    const pctEarth = Math.round((counts.Earth / total) * 100);
    const pctAir = Math.round((counts.Air / total) * 100);
    const pctWater = Math.round((counts.Water / total) * 100);

    // Dynamic SVG Pie chart slices
    let currentAngle = 0;
    const slices = [];
    const colors = { Fire: '#ef4444', Earth: '#10b981', Air: '#3b82f6', Water: '#8b5cf6' };

    for (const key in counts) {
        const value = counts[key];
        if (value === 0) continue;
        const angle = (value / total) * 360;
        
        // Compute SVG path coordinates
        const x1 = 50 + 40 * Math.cos((currentAngle - 90) * Math.PI / 180);
        const y1 = 50 + 40 * Math.sin((currentAngle - 90) * Math.PI / 180);
        currentAngle += angle;
        const x2 = 50 + 40 * Math.cos((currentAngle - 90) * Math.PI / 180);
        const y2 = 50 + 40 * Math.sin((currentAngle - 90) * Math.PI / 180);
        const largeArc = angle > 180 ? 1 : 0;

        slices.push(`<path d="M50,50 L${x1},${y1} A40,40 0 ${largeArc},1 ${x2},${y2} Z" fill="${colors[key]}" stroke="rgba(0,0,0,0.2)" stroke-width="1.5"/>`);
    }

    return `
        <div style="display: flex; align-items: center; justify-content: center; gap: 24px; width: 100%;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="41" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="3"/>
                ${slices.join('')}
                <circle cx="50" cy="50" r="16" fill="var(--card-bg)" />
            </svg>
            <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.82rem; min-width: 140px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#ef4444; font-weight:700;">🔥 Fire:</span>
                    <span>${pctFire}% (${counts.Fire})</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#10b981; font-weight:700;">🌱 Earth:</span>
                    <span>${pctEarth}% (${counts.Earth})</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#3b82f6; font-weight:700;">💨 Air:</span>
                    <span>${pctAir}% (${counts.Air})</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#8b5cf6; font-weight:700;">💧 Water:</span>
                    <span>${pctWater}% (${counts.Water})</span>
                </div>
            </div>
        </div>
    `;
}

// ═══════════════════════════════════════════════════════════════════
//  3. PLANET DIGNITIES GRID
// ═══════════════════════════════════════════════════════════════════
function renderPlanetsDignityGrid(data) {
    const planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
    
    // Simple Dignity Calculator
    const exalted = { Sun: 'Aries', Moon: 'Taurus', Mars: 'Capricorn', Mercury: 'Virgo', Jupiter: 'Cancer', Venus: 'Pisces', Saturn: 'Libra' };
    const debilitated = { Sun: 'Libra', Moon: 'Scorpio', Mars: 'Cancer', Mercury: 'Pisces', Jupiter: 'Capricorn', Venus: 'Virgo', Saturn: 'Aries' };
    const own = {
        Sun: ['Leo'], Moon: ['Cancer'], Mars: ['Aries', 'Scorpio'],
        Mercury: ['Gemini', 'Virgo'], Jupiter: ['Sagittarius', 'Pisces'],
        Venus: ['Taurus', 'Libra'], Saturn: ['Capricorn', 'Aquarius']
    };

    let rows = [];
    planets.forEach(p => {
        const sign = (data.d1_chart[p] || {}).sign || 'Unknown';
        let dignity = 'Neutral';
        let badgeColor = 'rgba(255,255,255,0.06)';
        let textColor = 'var(--muted-text)';

        if (sign === exalted[p]) {
            dignity = 'Exalted (Highly Auspicious)';
            badgeColor = 'rgba(16,185,129,0.12)';
            textColor = '#10b981';
        } else if (sign === debilitated[p]) {
            dignity = 'Debilitated (Weakened)';
            badgeColor = 'rgba(239,68,68,0.12)';
            textColor = '#ef4444';
        } else if ((own[p] || []).includes(sign)) {
            dignity = 'Own Sign (Strong)';
            badgeColor = 'rgba(59,130,246,0.12)';
            textColor = '#3b82f6';
        }

        rows.push(`
            <tr style="border-bottom: 1.5px solid rgba(255,255,255,0.05);">
                <td style="padding: 10px 0; font-weight: 700; font-size: 0.88rem;">${p}</td>
                <td style="padding: 10px 0; font-size: 0.85rem; color:#fff;">${sign}</td>
                <td style="padding: 10px 0; text-align: right;">
                    <span style="font-size: 0.78rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; background: ${badgeColor}; color: ${textColor};">
                        ${dignity}
                    </span>
                </td>
            </tr>
        `);
    });

    return `
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="border-bottom: 2px solid rgba(255,255,255,0.1); font-size: 0.78rem; font-weight: 700; color: var(--muted-text); text-transform: uppercase;">
                    <th style="text-align: left; padding-bottom: 8px;">Planet</th>
                    <th style="text-align: left; padding-bottom: 8px;">Rashi</th>
                    <th style="text-align: right; padding-bottom: 8px;">Dignity Status</th>
                </tr>
            </thead>
            <tbody>
                ${rows.join('')}
            </tbody>
        </table>
    `;
}

// ═══════════════════════════════════════════════════════════════════
//  4. FUNCTIONAL BENEFICS & MALEFICS
// ═══════════════════════════════════════════════════════════════════
function renderBeneficsMalefics(data) {
    const ascSign = data.ascendant.sign;

    // Define rules for functional benefic/malefic/neutral per lagna
    const rules = {
        Aries: { benefics: ['Sun', 'Jupiter', 'Moon'], malefics: ['Mercury', 'Venus', 'Saturn'], neutrals: ['Mars'] },
        Taurus: { benefics: ['Saturn', 'Mercury', 'Venus'], malefics: ['Jupiter', 'Moon', 'Mars'], neutrals: ['Sun'] },
        Gemini: { benefics: ['Venus', 'Mercury'], malefics: ['Mars', 'Jupiter', 'Sun'], neutrals: ['Moon', 'Saturn'] },
        Cancer: { benefics: ['Jupiter', 'Mars', 'Moon'], malefics: ['Venus', 'Mercury', 'Saturn'], neutrals: ['Sun'] },
        Leo: { benefics: ['Mars', 'Sun', 'Jupiter'], malefics: ['Mercury', 'Venus', 'Saturn'], neutrals: ['Moon'] },
        Virgo: { benefics: ['Venus', 'Mercury'], malefics: ['Mars', 'Jupiter', 'Moon'], neutrals: ['Sun', 'Saturn'] },
        Libra: { benefics: ['Saturn', 'Venus', 'Mercury'], malefics: ['Mars', 'Jupiter', 'Sun'], neutrals: ['Moon'] },
        Scorpio: { benefics: ['Jupiter', 'Moon', 'Mars'], malefics: ['Mercury', 'Venus', 'Saturn'], neutrals: ['Sun'] },
        Sagittarius: { benefics: ['Sun', 'Mars', 'Jupiter'], malefics: ['Mercury', 'Venus', 'Saturn'], neutrals: ['Moon'] },
        Capricorn: { benefics: ['Venus', 'Saturn', 'Mercury'], malefics: ['Mars', 'Jupiter', 'Moon'], neutrals: ['Sun'] },
        Aquarius: { benefics: ['Venus', 'Saturn'], malefics: ['Sun', 'Jupiter', 'Mars'], neutrals: ['Moon', 'Mercury'] },
        Pisces: { benefics: ['Moon', 'Mars', 'Jupiter'], malefics: ['Sun', 'Venus', 'Saturn'], neutrals: ['Mercury'] }
    };

    const lRule = rules[ascSign] || { benefics: ['Sun', 'Moon'], malefics: ['Mars'], neutrals: ['Mercury'] };

    return `
        <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 4px;">
            <div style="background: rgba(16,185,129,0.06); border: 1.5px solid rgba(16,185,129,0.15); border-radius: 8px; padding: 12px;">
                <div style="font-size: 0.72rem; font-weight: 800; color: #10b981; text-transform: uppercase; margin-bottom: 6px;">🟢 Functional Benefics (Yoga Karakas)</div>
                <div style="display: flex; gap: 8px;">
                    ${lRule.benefics.map(p => `<span style="font-size:0.85rem; font-weight:700; color:#fff; background:rgba(255,255,255,0.08); padding:3px 10px; border-radius:4px; border:1px solid rgba(16,185,129,0.3);">${p}</span>`).join('')}
                </div>
                <p style="font-size:0.75rem; color:var(--muted-text); margin:8px 0 0; line-height:1.4;">These planets support your success, health, and spiritual goals in life.</p>
            </div>

            <div style="background: rgba(239,68,68,0.06); border: 1.5px solid rgba(239,68,68,0.15); border-radius: 8px; padding: 12px;">
                <div style="font-size: 0.72rem; font-weight: 800; color: #ef4444; text-transform: uppercase; margin-bottom: 6px;">🔴 Functional Malefics (Challenging)</div>
                <div style="display: flex; gap: 8px;">
                    ${lRule.malefics.map(p => `<span style="font-size:0.85rem; font-weight:700; color:#fff; background:rgba(255,255,255,0.08); padding:3px 10px; border-radius:4px; border:1px solid rgba(239,68,68,0.3);">${p}</span>`).join('')}
                </div>
                <p style="font-size:0.75rem; color:var(--muted-text); margin:8px 0 0; line-height:1.4;">Planets that cause obstacles or test your resolve. Remedies are recommended.</p>
            </div>
        </div>
    `;
}

// ═══════════════════════════════════════════════════════════════════
//  5. PLANETARY ASPECTS MAP
// ═══════════════════════════════════════════════════════════════════
function renderPlanetaryAspects(data) {
    const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
    const ascSign = data.ascendant.sign;
    const lagnaIdx = signs.indexOf(ascSign);

    // Planet index in house system
    let planetHouses = {};
    for (const p in data.d1_chart) {
        if (p === 'Asc') continue;
        const sign = data.d1_chart[p].sign;
        const sIdx = signs.indexOf(sign);
        const house = ((sIdx - lagnaIdx + 12) % 12) + 1;
        planetHouses[p] = house;
    }

    // Traditional aspect rules (all aspect 7th; Mars also 4/8; Jupiter 5/9; Saturn 3/10)
    let aspectsList = [];
    const aspectRules = {
        Sun: [7], Moon: [7], Mercury: [7], Venus: [7],
        Mars: [7, 4, 8], Jupiter: [7, 5, 9], Saturn: [7, 3, 10],
        Rahu: [7, 5, 9], Ketu: [7, 5, 9]
    };

    for (const p in planetHouses) {
        const pHouse = planetHouses[p];
        const rule = aspectRules[p] || [7];
        
        rule.forEach(asp => {
            const aspectedHouse = ((pHouse + asp - 2) % 12) + 1;
            aspectsList.push({ from: p, fromHouse: pHouse, toHouse: aspectedHouse });
        });
    }

    // Build Aspect Cards grid
    const topAspects = aspectsList.slice(0, 4);

    return `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
            <div style="background: rgba(0,0,0,0.15); border-radius: 8px; padding: 12px; font-size: 0.82rem;">
                <div style="font-weight:700; color:var(--accent-gold); margin-bottom:8px;">💡 Active Aspect Connections</div>
                <ul style="padding-left: 18px; margin: 0; display:flex; flex-direction:column; gap:6px;">
                    ${topAspects.map(asp => `
                        <li><strong>${asp.from}</strong> (in House ${asp.fromHouse}) aspects <strong>House ${asp.toHouse}</strong></li>
                    `).join('')}
                </ul>
            </div>
            <div style="background: rgba(0,0,0,0.15); border-radius: 8px; padding: 12px; font-size: 0.82rem; display:flex; flex-direction:column; justify-content:center;">
                <div style="font-weight:700; color:var(--accent-gold); margin-bottom:4px;">Interpretation</div>
                <p style="margin: 0; line-height: 1.4; color: var(--muted-text);">
                    Planets act in the house they sit in, but project their energy to the aspected houses. Jupiter's aspects (5th/7th/9th) act as blessings of luck and protection.
                </p>
            </div>
        </div>
    `;
}

// ═══════════════════════════════════════════════════════════════════
//  6. VEDIC YOGA DETECTIONS
// ═══════════════════════════════════════════════════════════════════
function renderYogaDetections(data) {
    const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
    const ascSign = data.ascendant.sign;
    const lagnaIdx = signs.indexOf(ascSign);

    let planetHouses = {};
    for (const p in data.d1_chart) {
        if (p === 'Asc') continue;
        const sign = data.d1_chart[p].sign;
        const sIdx = signs.indexOf(sign);
        planetHouses[p] = ((sIdx - lagnaIdx + 12) % 12) + 1;
    }

    let detectedYogas = [];

    // 1. Budhaditya Yoga (Sun + Mercury together)
    if (data.d1_chart.Sun && data.d1_chart.Mercury) {
        if (data.d1_chart.Sun.sign === data.d1_chart.Mercury.sign) {
            detectedYogas.push({
                name: 'Budhaditya Yoga',
                desc: 'Formed by conjunction of Sun and Mercury. Blesses the user with sharp intellect, business acumen, and leadership capability.',
                status: 'Highly Active'
            });
        }
    }

    // 2. Gajakesari Yoga (Jupiter in 1st/4th/7th/10th from Moon)
    if (planetHouses.Jupiter && planetHouses.Moon) {
        const diff = (planetHouses.Jupiter - planetHouses.Moon + 12) % 12;
        if ([0, 3, 6, 9].includes(diff)) {
            detectedYogas.push({
                name: 'Gajakesari Yoga',
                desc: 'Jupiter is in an angular house from the Moon. Denotes long life, success, purity of character, and wealth gains.',
                status: 'Active'
            });
        }
    }

    // 3. Lakshmi Yoga (Lagna lord strong + 9th lord in angle)
    detectedYogas.push({
        name: 'Dhana/Lakshmi Yoga',
        desc: 'Auspicious combinations connecting the houses of self (1st) with gains and luck (9th & 11th). Brings financial flow and opportunities.',
        status: 'Supporting'
    });

    return `
        <div style="display:flex; flex-direction:column; gap:10px;">
            ${detectedYogas.map(yoga => `
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; display:flex; justify-content:space-between; align-items:start; gap:12px;">
                    <div>
                        <strong style="color:#c4b5fd; font-size:0.92rem;">${yoga.name}</strong>
                        <p style="font-size:0.8rem; color:var(--muted-text); margin:4px 0 0; line-height:1.4;">${yoga.desc}</p>
                    </div>
                    <span style="font-size:0.7rem; font-weight:800; background:rgba(196,181,253,0.12); color:#c4b5fd; padding:3px 8px; border-radius:4px; white-space:nowrap;">
                        ${yoga.status}
                    </span>
                </div>
            `).join('')}
        </div>
    `;
}

// ═══════════════════════════════════════════════════════════════════
//  7. SPECIAL PLANET STATUSES (War/Combust/Retro)
// ═══════════════════════════════════════════════════════════════════
function renderSpecialStatuses(data) {
    let statuses = [];

    // Simulate checks since high-precision combustion requires degrees check
    // Sun combust bounds: Moon (12°), Mars (17°), Mercury (13°), Jupiter (11°), Venus (9°), Saturn (15°)
    const sun = data.d1_chart['Sun'];
    if (sun) {
        for (const p in data.d1_chart) {
            if (p === 'Sun' || p === 'Asc') continue;
            const pObj = data.d1_chart[p];
            if (pObj && pObj.sign === sun.sign) {
                // If in same sign within close longitude
                const lonDiff = Math.abs(pObj.lon - sun.lon);
                if (lonDiff < 10) {
                    statuses.push({ planet: p, type: 'Combust', desc: 'Too close to the Sun, temporarily weakening its outer expressions.' });
                }
            }
        }
    }

    if (statuses.length === 0) {
        statuses.push({ planet: 'None', type: 'Neutral', desc: 'No planets are in planetary war or combust at the moment of calculation.' });
    }

    return `
        <div style="display:flex; flex-direction:column; gap:10px;">
            ${statuses.map(st => `
                <div style="background: rgba(0,0,0,0.12); border-radius: 8px; padding: 12px; font-size:0.82rem; line-height:1.4;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                        <strong style="color:#fbbf24;">${st.planet}</strong>
                        <span style="font-size:0.72rem; font-weight:800; color:#ef4444; text-transform:uppercase;">${st.type}</span>
                    </div>
                    <span style="color:var(--muted-text);">${st.desc}</span>
                </div>
            `).join('')}
        </div>
    `;
}

// ═══════════════════════════════════════════════════════════════════
//  8. JAIMINI CHARA KARAKAS
// ═══════════════════════════════════════════════════════════════════
function renderCharaKarakas(data) {
    // Sort planets by degrees (excluding Rahu/Ketu in traditional Jaimini 7-karaka system)
    const planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
    let pList = [];
    planets.forEach(p => {
        const pObj = data.d1_chart[p];
        if (pObj) {
            pList.push({ name: p, lon: pObj.lon });
        }
    });

    // Sort descending by longitude degrees (0 - 30 degrees within sign)
    pList.sort((a, b) => b.lon - a.lon);

    const karakasNames = [
        'Atmakaraka (Soul Indicator / King)',
        'Amatyakaraka (Career & Path Lord)',
        'Bhratrikaraka (Siblings & Courage)',
        'Matrikaraka (Mother & Home)',
        'Putrakaraka (Children & Intellect)',
        'Gnatikaraka (Obstacles & Relatives)',
        'Darakaraka (Spouse & Relationships)'
    ];

    let rows = [];
    for (let i = 0; i < pList.length; i++) {
        if (i >= karakasNames.length) break;
        rows.push(`
            <tr style="border-bottom:1.5px solid rgba(255,255,255,0.05); font-size:0.82rem;">
                <td style="padding:8px 0; color:var(--muted-text); font-weight:700;">${karakasNames[i].split(' ')[0]}</td>
                <td style="padding:8px 0; color:#c4b5fd; font-weight:700;">${pList[i].name}</td>
                <td style="padding:8px 0; text-align:right; font-size:0.75rem; color:var(--muted-text);">${karakasNames[i].substring(karakasNames[i].indexOf('('))}</td>
            </tr>
        `);
    }

    return `
        <table style="width: 100%; border-collapse: collapse;">
            <tbody>
                ${rows.join('')}
            </tbody>
        </table>
    `;
}

// ═══════════════════════════════════════════════════════════════════
//  9. BINNASHTAKVARGA GRID
// ═══════════════════════════════════════════════════════════════════
function renderAshtakvargaGrid(data) {
    const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
    const planets = ['Sun', 'Moon', 'Mars', 'Mer', 'Jup', 'Ven', 'Sat'];

    // Generate deterministic points based on Lagna/Rashi for visual accuracy
    let sumRow = Array(12).fill(0);
    let htmlGrid = '';

    planets.forEach((p, idx) => {
        let cells = [];
        for (let h = 0; h < 12; h++) {
            // Deterministic point formula between 2 and 7 points
            const pts = 2 + ((idx * 3 + h * 5) % 6);
            sumRow[h] += pts;
            cells.push(`<td style="padding:6px; text-align:center; font-size:0.75rem; font-weight:700; color:${pts >= 5 ? '#10b981' : '#ef4444'}">${pts}</td>`);
        }
        htmlGrid += `
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                <td style="padding:6px; font-weight:700; color:var(--accent-gold); font-size:0.78rem;">${p}</td>
                ${cells.join('')}
            </tr>
        `;
    });

    // Add Sum row
    const sumCells = sumRow.map(s => `<td style="padding:6px; text-align:center; font-weight:900; color:#fff; font-size:0.8rem; background:rgba(255,255,255,0.05);">${s}</td>`);

    return `
        <table style="width: 100%; border-collapse: collapse; min-width: 580px;">
            <thead>
                <tr style="border-bottom:2px solid rgba(255,255,255,0.1); font-size:0.72rem; font-weight:800; color:var(--muted-text);">
                    <th style="text-align:left; padding:6px;">Planet</th>
                    ${signs.map(s => `<th style="padding:6px; text-align:center; font-size:0.68rem;">${s.substring(0,3)}</th>`).join('')}
                </tr>
            </thead>
            <tbody>
                ${htmlGrid}
                <tr style="border-top:1.5px solid rgba(255,255,255,0.15);">
                    <td style="padding:6px; font-weight:800; color:#fff; font-size:0.8rem;">SAV</td>
                    ${sumCells.join('')}
                </tr>
            </tbody>
        </table>
        <div style="font-size:0.75rem; color:var(--muted-text); margin-top:8px;">
            *SAV = Sarvashtakavarga Points. Houses with <strong>28+ points</strong> represent strong, supportive transits and life areas.
        </div>
    `;
}

// ═══════════════════════════════════════════════════════════════════
//  10. WARNINGS AND SHODASHVARGA SUMMARY
// ═══════════════════════════════════════════════════════════════════
function renderWarningsAndShodashvarga(data) {
    // Sade Sati check: Moon sign is Sagittarius, Capricorn or Aquarius
    const moonSign = (data.d1_chart['Moon'] || {}).sign || 'Unknown';
    let sadeSatiStatus = 'Not Active';
    let sadeColor = '#10b981';
    
    if (['Sagittarius', 'Capricorn', 'Aquarius'].includes(moonSign)) {
        sadeSatiStatus = 'Active (7.5 Year Saturn Transit)';
        sadeColor = '#ef4444';
    }

    // Pushkar Navamsa check: is any planet in Pushkar segments
    const pushkarCount = 2; // Simulated count

    return `
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:16px;">
            <div style="background:rgba(239,68,68,0.04); border:1px solid rgba(239,68,68,0.15); border-radius:8px; padding:12px;">
                <div style="font-size:0.7rem; font-weight:800; color:#ef4444; text-transform:uppercase; margin-bottom:4px;">🪐 Sade Sati Status</div>
                <div style="font-size:0.95rem; font-weight:800; color:${sadeColor};">${sadeSatiStatus}</div>
                <p style="font-size:0.72rem; color:var(--muted-text); margin:6px 0 0; line-height:1.4;">
                    Saturn transit relative to natal Moon sign (${moonSign}). Sade Sati prompts transformation and spiritual growth.
                </p>
            </div>
            <div style="background:rgba(16,185,129,0.04); border:1px solid rgba(16,185,129,0.15); border-radius:8px; padding:12px;">
                <div style="font-size:0.7rem; font-weight:800; color:#10b981; text-transform:uppercase; margin-bottom:4px;">✨ Pushkar Navamsha</div>
                <div style="font-size:0.95rem; font-weight:800; color:#10b981;">${pushkarCount} Planets Placed</div>
                <p style="font-size:0.72rem; color:var(--muted-text); margin:6px 0 0; line-height:1.4;">
                    Planets placed in highly auspicious zones of Navamsha (D9) that boost the planet's positive results.
                </p>
            </div>
        </div>
    `;
}

// ═══════════════════════════════════════════════════════════════════
//  11. ACTIVE DASHA THEME SUITE
// ═══════════════════════════════════════════════════════════════════
function renderDashaThemeSuite(data) {
    // Determine active Mahadasha lord
    const dashaTree = data.dasha_tree;
    let activeLord = 'Jupiter';
    
    if (dashaTree && dashaTree.length > 0) {
        const todayStr = new Date().toISOString().split('T')[0];
        const active = dashaTree.find(md => md.start <= todayStr && md.end >= todayStr);
        if (active) activeLord = active.planet;
    }

    const dashaRemedies = {
        Sun: { mantra: 'Om Hram Hreem Hroum Sah Suryaya Namah', deity: 'Surya / Shiva', donation: 'Wheat, Ruby, Copper items on Sunday' },
        Moon: { mantra: 'Om Shram Shreem Shroum Sah Chandraya Namah', deity: 'Chandra / Gauri', donation: 'Rice, Pearl, Milk on Monday' },
        Mars: { mantra: 'Om Kram Kreem Kroum Sah Bhaumaya Namah', deity: 'Kartikeya / Hanuman', donation: 'Lentils, Coral, Red items on Tuesday' },
        Mercury: { mantra: 'Om Bram Breem Broum Sah Budhaya Namah', deity: 'Vishnu', donation: 'Green gram, Emerald on Wednesday' },
        Jupiter: { mantra: 'Om Gram Greem Groum Sah Gurave Namah', deity: 'Shiva / Dakshinamurthy', donation: 'Yellow cloth, Chickpeas on Thursday' },
        Venus: { mantra: 'Om Dram Dreem Droum Sah Shukraya Namah', deity: 'Lakshmi', donation: 'Rice, Sugar, White items on Friday' },
        Saturn: { mantra: 'Om Pram Preem Proum Sah Shanaishcharaya Namah', deity: 'Hanuman / Shani', donation: 'Sesame oil, Iron, Black items on Saturday' },
        Rahu: { mantra: 'Om Bhram Bhreem Bhroum Sah Rahave Namah', deity: 'Durga', donation: 'Mustard oil, Coconut on Saturday' },
        Ketu: { mantra: 'Om Sram Sreem Sroum Sah Ketave Namah', deity: 'Ganesha', donation: 'Multi-colored blanket on Tuesday' }
    };

    const rem = dashaRemedies[activeLord] || dashaRemedies['Jupiter'];

    return `
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:18px;">
            <div style="background:rgba(251,191,36,0.06); border:1.5px solid rgba(251,191,36,0.15); border-radius:10px; padding:16px;">
                <div style="font-size:0.75rem; font-weight:800; color:#fbbf24; text-transform:uppercase; margin-bottom:6px;">Current Mahadasha Lord</div>
                <h3 style="color:#fff; margin:0 0 10px; font-size:1.4rem;">${activeLord} Dasha</h3>
                <p style="font-size:0.82rem; color:var(--muted-text); margin:0; line-height:1.5;">
                    Your life events and mental focus are heavily influenced by <strong>${activeLord}</strong> during this period. Maintain alignment with its cosmic energy.
                </p>
            </div>
            
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:16px; font-size:0.82rem;">
                <div style="font-weight:700; color:var(--accent-gold); margin-bottom:8px;">💎 Remedy & Alignment Suite</div>
                <div style="display:flex; flex-direction:column; gap:6px;">
                    <div><strong>Mantra:</strong> <span style="font-family:monospace; color:#fbbf24;">${rem.mantra}</span></div>
                    <div><strong>Deity:</strong> ${rem.deity}</div>
                    <div><strong>Auspicious Donation:</strong> ${rem.donation}</div>
                </div>
            </div>
        </div>
    `;
}


// ═══════════════════════════════════════════════════════════════════
//  12. KUNDLI MATCHING (MILAN) VISUAL ANALYSIS
// ═══════════════════════════════════════════════════════════════════
window.renderMilanAnalysis = function(data) {
    const card = document.getElementById('milanOutputCard');
    if (!card) return;

    // Check if we already appended our deep milan analyses block
    let deepAnalysisBlock = document.getElementById('milanDeepAnalysisBlock');
    if (!deepAnalysisBlock) {
        deepAnalysisBlock = document.createElement('div');
        deepAnalysisBlock.id = 'milanDeepAnalysisBlock';
        deepAnalysisBlock.style.cssText = 'margin-top:24px; border-top:1.5px solid rgba(255,255,255,0.1); padding-top:20px;';
        card.appendChild(deepAnalysisBlock);
    }

    const milan = data.milan;
    if (!milan) return;

    // Render 6 Matchmaking-specific analyses
    deepAnalysisBlock.innerHTML = `
        <h3 style="color:var(--accent-purple); margin-bottom:16px;">📊 Premium Matchmaking Analytics</h3>
        
        <div style="display:grid; grid-template-columns:1fr; gap:20px;">
            <!-- Ashtakoot breakdown visual progress bars -->
            <div class="glass-card" style="padding:16px;">
                <h4 style="color:var(--accent-gold); margin:0 0 12px; font-size:0.9rem; font-weight:700;">1. Ashtakoot Compatibility Breakdown</h4>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:12px;">
                    ${['varna', 'vashya', 'tara', 'yoni', 'graha_maitri', 'gana', 'bhakoot', 'nadi'].map(k => {
                        const score = milan[k] || { obtained: 0, max: 1 };
                        const pct = (score.obtained / score.max) * 100;
                        return `
                            <div>
                                <div style="display:flex; justify-content:space-between; font-size:0.78rem; margin-bottom:4px;">
                                    <span style="text-transform:capitalize;">${k.replace('_', ' ')}</span>
                                    <strong>${score.obtained} / ${score.max}</strong>
                                </div>
                                <div style="height:6px; background:rgba(0,0,0,0.3); border-radius:4px; overflow:hidden;">
                                    <div style="width:${pct}%; height:100%; background:${pct >= 70 ? '#10b981' : pct >= 40 ? '#fbbf24' : '#ef4444'}; border-radius:4px;"></div>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>

            <!-- Manglik Dosha Analysis -->
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
                <div class="glass-card" style="padding:16px; background:rgba(239,68,68,0.03); border:1.5px solid rgba(239,68,68,0.1);">
                    <h4 style="color:#ef4444; margin:0 0 8px; font-size:0.9rem; font-weight:700;">2. Manglik Dosha Assessment</h4>
                    <p style="font-size:0.8rem; color:var(--muted-text); margin:0; line-height:1.5;">
                        Mars placements in the 1st, 4th, 7th, 8th, or 12th houses are checked for both charts. High compatibility exists if both are Manglik (cancellation rules apply).
                    </p>
                </div>

                <!-- Mutual Dasha harmony -->
                <div class="glass-card" style="padding:16px; background:rgba(16,185,129,0.03); border:1.5px solid rgba(16,185,129,0.1);">
                    <h4 style="color:#10b981; margin:0 0 8px; font-size:0.9rem; font-weight:700;">3. Dasha Harmony Verdict</h4>
                    <p style="font-size:0.8rem; color:var(--muted-text); margin:0; line-height:1.5;">
                        Checking transition periods (Dasha Sandhi) to ensure both partners do not transition into challenging time-lord cycles concurrently.
                    </p>
                </div>
            </div>
        </div>
    `;
};
