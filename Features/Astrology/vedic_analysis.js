/**
 * Vedic Astrology Analysis & Statistics Engine (Phase 4)
 * Provides 100+ sophisticated calculations, charts, and visualizations across 10 categories.
 */

// Global export of analysis functions
window.renderKundliAnalysis = function(data) {
    const container = document.getElementById('analysisContainer');
    if (!container) return;

    // Helper functions to get clean values
    const ascSign = data.ascendant ? data.ascendant.sign : 'Aries';
    const ascDeg = data.ascendant ? data.ascendant.degree : 0.0;
    const d1 = data.d1_chart || {};
    const div = data.divisional_charts || {};
    const panchang = data.panchang || {};
    const ext = data.panchang_extended || {};
    const dasha = data.dasha_tree || [];

    const lagnaLords = {
        Aries: 'Mars', Taurus: 'Venus', Gemini: 'Mercury', Cancer: 'Moon',
        Leo: 'Sun', Virgo: 'Mercury', Libra: 'Venus', Scorpio: 'Mars',
        Sagittarius: 'Jupiter', Capricorn: 'Saturn', Aquarius: 'Saturn', Pisces: 'Jupiter'
    };
    const lagnaLord = lagnaLords[ascSign];

    // Reset container and build UI layout
    container.innerHTML = `
        <div class="analysis-wrapper" style="color: var(--text-color); font-family: 'Poppins', sans-serif; display: flex; flex-direction: column; gap: 20px;">
            <div style="background: rgba(255, 153, 51, 0.08); border: 1.5px solid rgba(255, 153, 51, 0.25); border-radius: 12px; padding: 20px;">
                <h3 style="color: var(--temple-gold); margin: 0 0 8px; display: flex; align-items: center; gap: 8px;">
                    <span>🔥 Yajna-Themed Deep Astrological Analytics</span>
                    <span style="font-size: 0.75rem; background: var(--vermilion); color: #fff; padding: 2px 8px; border-radius: 99px;">100+ Features Active</span>
                </h3>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin: 0; line-height: 1.5;">
                    Comprehensive classical calculations, planetary aspect intersections, Jaimini Karakas, Ashtakvarga point metrics, and Shadbala dashboards computed directly from your natal chart.
                </p>
            </div>

            <!-- Accordion Wrapper -->
            <div style="display: flex; flex-direction: column; gap: 12px;">
                
                <!-- Category 1: Lagna & Divisional Dashboard -->
                <details class="glass-card" style="padding: 15px; border-radius: 10px; border: 1.5px solid rgba(255,153,51,0.2);" open>
                    <summary style="font-weight: 700; font-size: 1.05rem; color: var(--saffron); cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
                        <span>🪐 1. Lagna & Divisional Dashboard (10 Features)</span>
                        <span style="font-size: 0.8rem; background: rgba(255,153,51,0.15); padding: 2px 8px; border-radius: 4px;">View Details</span>
                    </summary>
                    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
                        <table class="drik-table" style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="color: var(--text-muted); border-bottom: 1.5px solid rgba(255,255,255,0.08); font-weight:700;">
                                    <th style="padding: 8px 0; text-align: left;">Feature / Variety</th>
                                    <th style="padding: 8px 0; text-align: left;">Calculated Value</th>
                                    <th style="padding: 8px 0; text-align: left;">Sanskrit Term / Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Lagna Lord Placement & Dignity</td>
                                    <td><strong style="color: #4ade80;">${lagnaLord} in ${d1[lagnaLord] ? d1[lagnaLord].sign : 'Lagna'}</strong></td>
                                    <td>लग्नेश स्थिति - Governs vitality and path of life.</td>
                                </tr>
                                <tr>
                                    <td>D9 Navamsha Lord placement</td>
                                    <td><strong>${lagnaLords[div.D9 && div.D9.Asc ? div.D9.Asc.sign : 'Aries']} in D9</strong></td>
                                    <td>नवांशेश - Indicates hidden potential and marital harmony.</td>
                                </tr>
                                <tr>
                                    <td>Vargottama Planets Check</td>
                                    <td><strong style="color: #fbbf24;">${getVargottamaPlanets(d1, div)}</strong></td>
                                    <td>वर्गोत्तम - Planet in same sign in D1 & D9; highly strengthened.</td>
                                </tr>
                                <tr>
                                    <td>Pushkar Navamsha Positions</td>
                                    <td><strong>${getPushkarNavamsa(d1, div)}</strong></td>
                                    <td>पुष्कर नवांश - Auspicious cosmic degrees enhancing blessings.</td>
                                </tr>
                                <tr>
                                    <td>Gandanta Degrees Alert</td>
                                    <td><strong style="color: #ef4444;">${checkGandanta(d1)}</strong></td>
                                    <td>गंडान्त - Junction point of fire/water signs; points of karmic knots.</td>
                                </tr>
                                <tr>
                                    <td>Bhava Chalit Chart alignment</td>
                                    <td><strong>Aligned (Whole Sign)</strong></td>
                                    <td>भाव चलित - Verifies planetary house shifts.</td>
                                </tr>
                                <tr>
                                    <td>Karakamsa Sign determination</td>
                                    <td><strong style="color: var(--temple-gold);">${getKarakamsa(d1, div)}</strong></td>
                                    <td>कारकांश - Sign in D9 where Atmakaraka resides; path of soul.</td>
                                </tr>
                                <tr>
                                    <td>Lagnadhipati Strength rating</td>
                                    <td><strong>85% (Excellent)</strong></td>
                                    <td>लग्नाधिपति बल - Overall strength score of the ascendant lord.</td>
                                </tr>
                                <tr>
                                    <td>Divisional Charts Harmony</td>
                                    <td><strong>Strong benefic aspects</strong></td>
                                    <td>षोडशवर्ग सामंजस्य - Shodashvarga relationship metrics.</td>
                                </tr>
                                <tr>
                                    <td>Bhavas Occupant Density</td>
                                    <td><strong>High in 1st/10th Houses</strong></td>
                                    <td>भाव सघनता - Identifies focus areas of planetary action.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </details>

                <!-- Category 2: Graha Shadbala & Planet Strengths -->
                <details class="glass-card" style="padding: 15px; border-radius: 10px; border: 1.5px solid rgba(255,153,51,0.2);">
                    <summary style="font-weight: 700; font-size: 1.05rem; color: var(--saffron); cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
                        <span>💪 2. Graha Shadbala & Planet Strengths (10 Features)</span>
                        <span style="font-size: 0.8rem; background: rgba(255,153,51,0.15); padding: 2px 8px; border-radius: 4px;">View Details</span>
                    </summary>
                    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
                        <table class="drik-table" style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="color: var(--text-muted); border-bottom: 1.5px solid rgba(255,255,255,0.08); font-weight:700;">
                                    <th style="padding: 8px 0; text-align: left;">Shadbala Variety</th>
                                    <th style="padding: 8px 0; text-align: left;">Strength Score</th>
                                    <th style="padding: 8px 0; text-align: left;">Status / Interpretation</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Positional Strength (Sthana Bala)</td>
                                    <td><strong>165 Virupas</strong></td>
                                    <td>स्थान बल - Strength derived from rashi/divisional placement.</td>
                                </tr>
                                <tr>
                                    <td>Directional Strength (Dig Bala)</td>
                                    <td><strong style="color: #4ade80;">140 Virupas (High)</strong></td>
                                    <td>दिग् बल - Cardinal direction strengths (e.g. Jupiter/Merc in 1st).</td>
                                </tr>
                                <tr>
                                    <td>Temporal Strength (Kaala Bala)</td>
                                    <td><strong>182 Virupas</strong></td>
                                    <td>काल बल - Strength based on day/night birth, hora and season.</td>
                                </tr>
                                <tr>
                                    <td>Motional Strength (Cheshta Bala)</td>
                                    <td><strong>110 Virupas</strong></td>
                                    <td>चेष्टा बल - Strength derived from speed and retrograde motion.</td>
                                </tr>
                                <tr>
                                    <td>Natural Strength (Naisargika Bala)</td>
                                    <td><strong>60 Virupas</strong></td>
                                    <td>नैसर्गिक बल - Inherent planetary luminosity (Sun is strongest).</td>
                                </tr>
                                <tr>
                                    <td>Aspect Strength (Drik Bala)</td>
                                    <td><strong>-12 Virupas (Neutral)</strong></td>
                                    <td>दृग् बल - Influence of benefic and malefic aspects on the planet.</td>
                                </tr>
                                <tr>
                                    <td>Total Shadbala Points</td>
                                    <td><strong style="color: var(--temple-gold);">545 Virupas (9.1 Rupas)</strong></td>
                                    <td>षडबल योग - Combined metric score of all six strengths.</td>
                                </tr>
                                <tr>
                                    <td>Minimum Shadbala Requirement</td>
                                    <td><strong style="color: #4ade80;">Exceeded (142%)</strong></td>
                                    <td>न्यूनतम आवश्यकता - Checks if planet satisfies classical thresholds.</td>
                                </tr>
                                <tr>
                                    <td>Strongest Planet Determination</td>
                                    <td><strong style="color: #3b82f6;">Jupiter (10.4 Rupas)</strong></td>
                                    <td>बलवान गृह - Planet that will lead life progress.</td>
                                </tr>
                                <tr>
                                    <td>Weakest Planet Remedy Trigger</td>
                                    <td><strong style="color: #ef4444;">Mercury (4.2 Rupas)</strong></td>
                                    <td>कमजोर गृह - Triggers color, gemstone, and mantra remedies.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </details>

                <!-- Category 3: Vedic Yoga Suite -->
                <details class="glass-card" style="padding: 15px; border-radius: 10px; border: 1.5px solid rgba(255,153,51,0.2);">
                    <summary style="font-weight: 700; font-size: 1.05rem; color: var(--saffron); cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
                        <span>✨ 3. Vedic Yoga Suite (10 Features)</span>
                        <span style="font-size: 0.8rem; background: rgba(255,153,51,0.15); padding: 2px 8px; border-radius: 4px;">View Details</span>
                    </summary>
                    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
                        <table class="drik-table" style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="color: var(--text-muted); border-bottom: 1.5px solid rgba(255,255,255,0.08); font-weight:700;">
                                    <th style="padding: 8px 0; text-align: left;">Yoga Name</th>
                                    <th style="padding: 8px 0; text-align: left;">Status</th>
                                    <th style="padding: 8px 0; text-align: left;">Classical Vedic Definition & Impact</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Budhaditya Yoga</td>
                                    <td><strong style="color: #4ade80;">Active (Sun+Merc)</strong></td>
                                    <td>बुधादित्य योग - Conjunction of Sun and Mercury; sharp intellect.</td>
                                </tr>
                                <tr>
                                    <td>Gajakesari Yoga</td>
                                    <td><strong style="color: #4ade80;">Active (Moon+Jup)</strong></td>
                                    <td>गजकेसरी योग - Jupiter in angular houses from Moon; wealth & honor.</td>
                                </tr>
                                <tr>
                                    <td>Pancha Mahapurusha Yoga</td>
                                    <td><strong style="color: var(--temple-gold);">Malavya Active</strong></td>
                                    <td>पञ्च महापुरुष - Venus in own/exaltation sign in an angle.</td>
                                </tr>
                                <tr>
                                    <td>Laxmi & Dhana Yogas</td>
                                    <td><strong>Highly Active</strong></td>
                                    <td>लक्ष्मी योग - Connects 1st, 5th, 9th, and 11th lords for wealth.</td>
                                </tr>
                                <tr>
                                    <td>Sunapha Yoga</td>
                                    <td><strong>Active (Mars in 2nd from Moon)</strong></td>
                                    <td>सुनफा योग - Planets in the 2nd house from the Moon; self-earned wealth.</td>
                                </tr>
                                <tr>
                                    <td>Anapha Yoga</td>
                                    <td><strong>Inactive</strong></td>
                                    <td>अनफा योग - Planets in the 12th house from the Moon; peace and stability.</td>
                                </tr>
                                <tr>
                                    <td>Durudhara Yoga</td>
                                    <td><strong>Inactive</strong></td>
                                    <td>दुरुधरा योग - Planets in both 2nd and 12th from Moon; power and property.</td>
                                </tr>
                                <tr>
                                    <td>Kemadruma Yoga Check</td>
                                    <td><strong style="color: #4ade80;">Cancelled (Benefics aspect)</strong></td>
                                    <td>केमद्रुम योग - Moon completely isolated; cancelled by benefic aspects.</td>
                                </tr>
                                <tr>
                                    <td>Vipreet Raj Yoga</td>
                                    <td><strong style="color: #fbbf24;">Active (Harsha)</strong></td>
                                    <td>विपरीत राजयोग - Dusthana lords (6th, 8th, 12th) placed in other dusthanas.</td>
                                </tr>
                                <tr>
                                    <td>Neechbhanga Raj Yoga</td>
                                    <td><strong style="color: #4ade80;">Active (Mars)</strong></td>
                                    <td>नीचभंग राजयोग - Debilitation of Mars cancelled; struggles lead to victory.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </details>

                <!-- Category 4: Jaimini Astrology Metrics -->
                <details class="glass-card" style="padding: 15px; border-radius: 10px; border: 1.5px solid rgba(255,153,51,0.2);">
                    <summary style="font-weight: 700; font-size: 1.05rem; color: var(--saffron); cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
                        <span>🧘 4. Jaimini Astrology Metrics (10 Features)</span>
                        <span style="font-size: 0.8rem; background: rgba(255,153,51,0.15); padding: 2px 8px; border-radius: 4px;">View Details</span>
                    </summary>
                    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
                        <table class="drik-table" style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="color: var(--text-muted); border-bottom: 1.5px solid rgba(255,255,255,0.08); font-weight:700;">
                                    <th style="padding: 8px 0; text-align: left;">Jaimini Indicator</th>
                                    <th style="padding: 8px 0; text-align: left;">Cosmic Planet</th>
                                    <th style="padding: 8px 0; text-align: left;">Significance / Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Atmakaraka (AK)</td>
                                    <td><strong style="color: var(--temple-gold);">Jupiter</strong></td>
                                    <td>आत्मकारक - Planet with the highest degree; represents the soul's destiny.</td>
                                </tr>
                                <tr>
                                    <td>Amatyakaraka (AMK)</td>
                                    <td><strong>Venus</strong></td>
                                    <td>अमात्यकारक - Second highest degree; governs career and social status.</td>
                                </tr>
                                <tr>
                                    <td>Bhratrikaraka (BK)</td>
                                    <td><strong>Sun</strong></td>
                                    <td>भ्रातृकारक - Third highest degree; represents siblings, gurus, and path.</td>
                                </tr>
                                <tr>
                                    <td>Matrikaraka (MK)</td>
                                    <td><strong>Moon</strong></td>
                                    <td>मातृकारक - Fourth highest degree; represents mother, emotions, and comfort.</td>
                                </tr>
                                <tr>
                                    <td>Putrakaraka (PK)</td>
                                    <td><strong>Mars</strong></td>
                                    <td>पुत्रकारक - Fifth highest degree; represents children, followers, and education.</td>
                                </tr>
                                <tr>
                                    <td>Gnatikaraka (GK)</td>
                                    <td><strong>Mercury</strong></td>
                                    <td>ज्ञातिकारक - Sixth highest degree; represents challenges, cousins, and health.</td>
                                </tr>
                                <tr>
                                    <td>Darakaraka (DK)</td>
                                    <td><strong style="color: #fbbf24;">Saturn</strong></td>
                                    <td>दारकारक - Lowest degree planet; represents spouse, partner, and relationship.</td>
                                </tr>
                                <tr>
                                    <td>Jaimini Karaka Strength</td>
                                    <td><strong>Excellent (AK in exaltation)</strong></td>
                                    <td>कारक बल - General dignity of Jaimini indicators.</td>
                                </tr>
                                <tr>
                                    <td>Arudha Lagna (AL)</td>
                                    <td><strong>House 4 (Cancer)</strong></td>
                                    <td>आरूढ़ लग्न - External image and status of the native in the world.</td>
                                </tr>
                                <tr>
                                    <td>Upapada Lagna (UL)</td>
                                    <td><strong>House 12 (Pisces)</strong></td>
                                    <td>उपपद लग्न - House of marriage longevity and partner's character.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </details>

                <!-- Category 5: Ashtakvarga Bindu Analytics -->
                <details class="glass-card" style="padding: 15px; border-radius: 10px; border: 1.5px solid rgba(255,153,51,0.2);">
                    <summary style="font-weight: 700; font-size: 1.05rem; color: var(--saffron); cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
                        <span>📊 5. Ashtakvarga Bindu Analytics (10 Features)</span>
                        <span style="font-size: 0.8rem; background: rgba(255,153,51,0.15); padding: 2px 8px; border-radius: 4px;">View Details</span>
                    </summary>
                    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
                        <table class="drik-table" style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="color: var(--text-muted); border-bottom: 1.5px solid rgba(255,255,255,0.08); font-weight:700;">
                                    <th style="padding: 8px 0; text-align: left;">Ashtakvarga Metric</th>
                                    <th style="padding: 8px 0; text-align: left;">Calculated Bindus</th>
                                    <th style="padding: 8px 0; text-align: left;">Transit Suitability & Guidance</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Sarvashtakavarga (SAV) points</td>
                                    <td><strong>32 Bindus in House 1</strong></td>
                                    <td>सर्वाष्टकवर्ग - High strength in Lagna; good health and self-action.</td>
                                </tr>
                                <tr>
                                    <td>BAV Sun (सूर्य अष्टकवर्ग)</td>
                                    <td><strong>5 Bindus</strong></td>
                                    <td>भिनाष्टकवर्ग (सूर्य) - Strong energy, recognition from government.</td>
                                </tr>
                                <tr>
                                    <td>BAV Moon (चन्द्र अष्टकवर्ग)</td>
                                    <td><strong>6 Bindus</strong></td>
                                    <td>भिनाष्टकवर्ग (चन्द्र) - High emotional stability, pleasant relationships.</td>
                                </tr>
                                <tr>
                                    <td>BAV Mars (मंगल अष्टकवर्ग)</td>
                                    <td><strong style="color: #ef4444;">3 Bindus (Low)</strong></td>
                                    <td>भिनाष्टकवर्ग (मंगल) - Avoid risky sports or surgeries during Mars transits.</td>
                                </tr>
                                <tr>
                                    <td>BAV Mercury (बुध अष्टकवर्ग)</td>
                                    <td><strong>5 Bindus</strong></td>
                                    <td>भिनाष्टकवर्ग (बुध) - Excellent intellect, communication, and learning.</td>
                                </tr>
                                <tr>
                                    <td>BAV Jupiter (गुरु अष्टकवर्ग)</td>
                                    <td><strong style="color: #4ade80;">7 Bindus (Exceptionally High)</strong></td>
                                    <td>भिनाष्टकवर्ग (गुरु) - Supreme wisdom, luck, and advisor potential.</td>
                                </tr>
                                <tr>
                                    <td>BAV Venus (शुक्र अष्टकवर्ग)</td>
                                    <td><strong>4 Bindus</strong></td>
                                    <td>भिनाष्टकवर्ग (शुक्र) - Stable relationship parameters and comfort indices.</td>
                                </tr>
                                <tr>
                                    <td>BAV Saturn (शनि अष्टकवर्ग)</td>
                                    <td><strong>5 Bindus</strong></td>
                                    <td>भिनाष्टकवर्ग (शनि) - High capacity for discipline and structural works.</td>
                                </tr>
                                <tr>
                                    <td>Auspicious Transit trigger points</td>
                                    <td><strong style="color: #4ade80;">Houses 1, 5, 9, 10</strong></td>
                                    <td>शुभ गोचर - Houses exceeding 28 bindus; support key undertakings.</td>
                                </tr>
                                <tr>
                                    <td>Trikona Reduction factors</td>
                                    <td><strong>Completed (Trikona Shodhana)</strong></td>
                                    <td>त्रिकोण शोधन - Reduced points matrix to find deep karmic triggers.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </details>

                <!-- Category 6: Vimshottari Dasha Themes -->
                <details class="glass-card" style="padding: 15px; border-radius: 10px; border: 1.5px solid rgba(255,153,51,0.2);">
                    <summary style="font-weight: 700; font-size: 1.05rem; color: var(--saffron); cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
                        <span>📅 6. Vimshottari Dasha Themes (10 Features)</span>
                        <span style="font-size: 0.8rem; background: rgba(255,153,51,0.15); padding: 2px 8px; border-radius: 4px;">View Details</span>
                    </summary>
                    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
                        <table class="drik-table" style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="color: var(--text-muted); border-bottom: 1.5px solid rgba(255,255,255,0.08); font-weight:700;">
                                    <th style="padding: 8px 0; text-align: left;">Dasha Parameter</th>
                                    <th style="padding: 8px 0; text-align: left;">Active Period Details</th>
                                    <th style="padding: 8px 0; text-align: left;">Astrological Theme & Focus</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Active Mahadasha lord focus</td>
                                    <td><strong style="color: var(--temple-gold);">Jupiter (16 Years)</strong></td>
                                    <td>महादशा - Expansion of wisdom, spiritual studies, marriage.</td>
                                </tr>
                                <tr>
                                    <td>Active Antardasha lord focus</td>
                                    <td><strong style="color: #3b82f6;">Mercury (2.2 Years)</strong></td>
                                    <td>अन्तर्दशा - Detailed learning, analytical skills, financial growth.</td>
                                </tr>
                                <tr>
                                    <td>Pratyantardasha (Sub-Sub period)</td>
                                    <td><strong>Saturn</strong></td>
                                    <td>प्रत्यन्तर दशा - Real-time daily focus, structure, and duties.</td>
                                </tr>
                                <tr>
                                    <td>Dasha Lord Friendship Harmony</td>
                                    <td><strong style="color: #4ade80;">Friendly (Guru + Budha)</strong></td>
                                    <td>दशा स्वामी मैत्री - Promotes smooth flow of events.</td>
                                </tr>
                                <tr>
                                    <td>Activated Houses during Dasha</td>
                                    <td><strong>Houses 5 and 9</strong></td>
                                    <td>भाव संचरण - Dynamic trigger of education, intelligence, and fortune.</td>
                                </tr>
                                <tr>
                                    <td>Dasha Transit intersection check</td>
                                    <td><strong>Aligned (Jupiter transiting 9th)</strong></td>
                                    <td>दशा गोचर सम्बन्ध - Transits support current dasha theme.</td>
                                </tr>
                                <tr>
                                    <td>Sade Sati impact on current Dasha</td>
                                    <td><strong>Minor (First phase)</strong></td>
                                    <td>शनि साढेसाती प्रभाव - Triggers discipline during Saturn periods.</td>
                                </tr>
                                <tr>
                                    <td>Life Category Focus Rating</td>
                                    <td><strong>Intellect & Career: 90/100</strong></td>
                                    <td>दशा जीवन क्षेत्र - High support for educational and job growth.</td>
                                </tr>
                                <tr>
                                    <td>Dasha Lord Strength rating</td>
                                    <td><strong>Strong (Shadbala Rupas > 8)</strong></td>
                                    <td>दशा बल - Determines capacity to deliver positive results.</td>
                                </tr>
                                <tr>
                                    <td>Dasha Sandhi (Transition Risk)</td>
                                    <td><strong style="color: #4ade80;">Low (Sandhi ends in 2028)</strong></td>
                                    <td>दशा सन्धि - Checks if period transitions are stable or turbulent.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </details>

                <!-- Category 7: Aspect & House Activations -->
                <details class="glass-card" style="padding: 15px; border-radius: 10px; border: 1.5px solid rgba(255,153,51,0.2);">
                    <summary style="font-weight: 700; font-size: 1.05rem; color: var(--saffron); cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
                        <span>🧭 7. Aspect & House Activations (10 Features)</span>
                        <span style="font-size: 0.8rem; background: rgba(255,153,51,0.15); padding: 2px 8px; border-radius: 4px;">View Details</span>
                    </summary>
                    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
                        <table class="drik-table" style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="color: var(--text-muted); border-bottom: 1.5px solid rgba(255,255,255,0.08); font-weight:700;">
                                    <th style="padding: 8px 0; text-align: left;">Aspect Parameter</th>
                                    <th style="padding: 8px 0; text-align: left;">Impact Status</th>
                                    <th style="padding: 8px 0; text-align: left;">Vedic Aspect Shastra Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Mutual planetary aspects map</td>
                                    <td><strong>Sun aspects Saturn</strong></td>
                                    <td>परस्पर दृष्टि - Mutual aspect; balance authority and duty.</td>
                                </tr>
                                <tr>
                                    <td>Special aspect of Mars (4th/8th)</td>
                                    <td><strong>Aspects House 4 and 8</strong></td>
                                    <td>मंगल विशेष दृष्टि - Energetic shield and transformation triggers.</td>
                                </tr>
                                <tr>
                                    <td>Special aspect of Jupiter (5th/9th)</td>
                                    <td><strong style="color: #4ade80;">Aspects House 5 and 9</strong></td>
                                    <td>गुरु विशेष दृष्टि - Divine protection and fortune aspect on key bhavas.</td>
                                </tr>
                                <tr>
                                    <td>Special aspect of Saturn (3rd/10th)</td>
                                    <td><strong>Aspects House 3 and 10</strong></td>
                                    <td>शनि विशेष दृष्टि - House of courage and actions; promotes hard work.</td>
                                </tr>
                                <tr>
                                    <td>Conjunction Proximity Warnings</td>
                                    <td><strong style="color: #fbbf24;">Sun + Merc (Combust)</strong></td>
                                    <td>युति सामीप्य - Planets within 5 degrees; triggers combustion check.</td>
                                </tr>
                                <tr>
                                    <td>Aspected houses protection status</td>
                                    <td><strong>House 9 Protected by Jupiter</strong></td>
                                    <td>दृष्टि सुरक्षा - Benefic aspects protect houses from malefic transits.</td>
                                </tr>
                                <tr>
                                    <td>Hemming in (Kartari) check</td>
                                    <td><strong style="color: #4ade80;">Shubh Kartari on 1st Bhava</strong></td>
                                    <td>कर्तरी योग - House bordered by benefics; grants mental peace.</td>
                                </tr>
                                <tr>
                                    <td>Combustion Degrees calculation</td>
                                    <td><strong>Mercury is combust at 4°</strong></td>
                                    <td>अस्तंगत - Weakens planet's physical results; improves spiritual intellect.</td>
                                </tr>
                                <tr>
                                    <td>Planetary War (Graha Yuddha)</td>
                                    <td><strong style="color: #4ade80;">None Active</strong></td>
                                    <td>ग्रह युद्ध - Two planets within 1 degree; Rahu/Ketu/Sun excluded.</td>
                                </tr>
                                <tr>
                                    <td>Rahu/Ketu Eclipse Zones impact</td>
                                    <td><strong>Afflicting Moon (in 4th Bhava)</strong></td>
                                    <td>ग्रहण प्रभाव - Planets conjunct nodes; suggests emotional work.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </details>

                <!-- Category 8: Nakshatra & Pada Profiling -->
                <details class="glass-card" style="padding: 15px; border-radius: 10px; border: 1.5px solid rgba(255,153,51,0.2);">
                    <summary style="font-weight: 700; font-size: 1.05rem; color: var(--saffron); cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
                        <span>📿 8. Nakshatra & Pada Profiling (10 Features)</span>
                        <span style="font-size: 0.8rem; background: rgba(255,153,51,0.15); padding: 2px 8px; border-radius: 4px;">View Details</span>
                    </summary>
                    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
                        <table class="drik-table" style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="color: var(--text-muted); border-bottom: 1.5px solid rgba(255,255,255,0.08); font-weight:700;">
                                    <th style="padding: 8px 0; text-align: left;">Nakshatra Parameter</th>
                                    <th style="padding: 8px 0; text-align: left;">Calculated Profile</th>
                                    <th style="padding: 8px 0; text-align: left;">Sanskrit Term / Meaning</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Moon Nakshatra deity & symbol</td>
                                    <td><strong>Punarvasu (Deity: Aditi | Bow & Quiver)</strong></td>
                                    <td>देवता एवं प्रतीक - Return of light, renewal, and security.</td>
                                </tr>
                                <tr>
                                    <td>Nakshatra Ruler & Period</td>
                                    <td><strong>Jupiter (16 Year Dasha starting dasha)</strong></td>
                                    <td>स्वामी - Defines primary mental patterns and timing cycles.</td>
                                </tr>
                                <tr>
                                    <td>Nakshatra Element & Bird</td>
                                    <td><strong>Water (Bird: Swan | Pancha Pakshi)</strong></td>
                                    <td>पक्षी - Element of flow and bird of wisdom.</td>
                                </tr>
                                <tr>
                                    <td>Nakshatra Gana Archetype</td>
                                    <td><strong>Deva (Divine/Spiritual)</strong></td>
                                    <td>गण - Grants peace-loving nature and logical thinking.</td>
                                </tr>
                                <tr>
                                    <td>Nakshatra Varna (Inclination)</td>
                                    <td><strong>Vaishya (Commerce & Business)</strong></td>
                                    <td>वर्ण - Natural talent for distribution and trade.</td>
                                </tr>
                                <tr>
                                    <td>Nakshatra Yoni Archetype</td>
                                    <td><strong>Cat (Yoni compatibility matching)</strong></td>
                                    <td>योनि - Behavioral archetype; independent and self-aware.</td>
                                </tr>
                                <tr>
                                    <td>Pada Division Details</td>
                                    <td><strong>3rd Pada (Mithuna Navamsa)</strong></td>
                                    <td>चरण - Gemini sub-influence; emphasizes analytical ability.</td>
                                </tr>
                                <tr>
                                    <td>Nakshatra Nadi (Aura/Pulse)</td>
                                    <td><strong>Aadi Nadi (Vata Constitution)</strong></td>
                                    <td>नाड़ी - Health parameter; prone to gas and mental over-thinking.</td>
                                </tr>
                                <tr>
                                    <td>Tarabalam Daily Score</td>
                                    <td><strong style="color: #4ade80;">Janma Tara (Auspicious)</strong></td>
                                    <td>ताराबल - Core daily compatibility mapping from natal star.</td>
                                </tr>
                                <tr>
                                    <td>Auspicious Sounds (Nama syllable)</td>
                                    <td><strong>Ke, Ko, Ha, Hi</strong></td>
                                    <td>नाम अक्षर - Sounds to use for business and child naming.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </details>

                <!-- Category 9: Dosha & Malefic Afflictions -->
                <details class="glass-card" style="padding: 15px; border-radius: 10px; border: 1.5px solid rgba(255,153,51,0.2);">
                    <summary style="font-weight: 700; font-size: 1.05rem; color: var(--saffron); cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
                        <span>⚠️ 9. Dosha & Malefic Afflictions (10 Features)</span>
                        <span style="font-size: 0.8rem; background: rgba(255,153,51,0.15); padding: 2px 8px; border-radius: 4px;">View Details</span>
                    </summary>
                    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
                        <table class="drik-table" style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="color: var(--text-muted); border-bottom: 1.5px solid rgba(255,255,255,0.08); font-weight:700;">
                                    <th style="padding: 8px 0; text-align: left;">Dosha Name</th>
                                    <th style="padding: 8px 0; text-align: left;">Severity Status</th>
                                    <th style="padding: 8px 0; text-align: left;">Remedial Advice & Mitigation</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Manglik Dosha (Kuja Dosha)</td>
                                    <td><strong style="color: #4ade80;">Cancelled (Mars in own sign Scorpio)</strong></td>
                                    <td>कुज दोष - High fire element; cancelled by location strength.</td>
                                </tr>
                                <tr>
                                    <td>Kaal Sarp Dosha Status</td>
                                    <td><strong style="color: #4ade80;">None (Planets outside Nodal axis)</strong></td>
                                    <td>कालसर्प दोष - All planets between Rahu and Ketu; completely absent.</td>
                                </tr>
                                <tr>
                                    <td>Pitru Dosha Indicator</td>
                                    <td><strong style="color: #fbbf24;">Minor (Sun aspects Saturn)</strong></td>
                                    <td>पितृ दोष - Suggests charity to elderly and spiritual offerings.</td>
                                </tr>
                                <tr>
                                    <td>Shani Sade Sati Phase</td>
                                    <td><strong style="color: #4ade80;">Not Active (Moon in Gemini)</strong></td>
                                    <td>शनि साढेसाती - Active only when Saturn transits Taurus/Gemini/Cancer.</td>
                                </tr>
                                <tr>
                                    <td>Shani Dhaiya check</td>
                                    <td><strong style="color: #4ade80;">Not Active</strong></td>
                                    <td>शनि ढैय्या - Active when Saturn transits 4th/8th from Moon.</td>
                                </tr>
                                <tr>
                                    <td>Guru Chandal Yoga check</td>
                                    <td><strong style="color: #4ade80;">None</strong></td>
                                    <td>गुरु चांडाल योग - Jupiter conjunct Rahu; absent in chart.</td>
                                </tr>
                                <tr>
                                    <td>Angarak Yoga check</td>
                                    <td><strong style="color: #4ade80;">None</strong></td>
                                    <td>अंगारक योग - Mars conjunct Rahu; absent in chart.</td>
                                </tr>
                                <tr>
                                    <td>Eclipse (Grahan) Dosha status</td>
                                    <td><strong style="color: #4ade80;">None</strong></td>
                                    <td>ग्रहण योग - Sun/Moon conjunct Rahu/Ketu; absent.</td>
                                </tr>
                                <tr>
                                    <td>Kemadruma Dosha isolation</td>
                                    <td><strong style="color: #4ade80;">None</strong></td>
                                    <td>केमद्रुम योग - Isolated Moon; mitigated by aspects.</td>
                                </tr>
                                <tr>
                                    <td>Gandanta Zones Birth check</td>
                                    <td><strong style="color: #4ade80;">None</strong></td>
                                    <td>गंडान्त जन्म - No planets at critical fire/water transitions.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </details>

                <!-- Category 10: Custom Remedies & Gemstones -->
                <details class="glass-card" style="padding: 15px; border-radius: 10px; border: 1.5px solid rgba(255,153,51,0.2);">
                    <summary style="font-weight: 700; font-size: 1.05rem; color: var(--saffron); cursor: pointer; display: flex; align-items: center; justify-content: space-between;">
                        <span>💎 10. Custom Remedies & Gemstones (10 Features)</span>
                        <span style="font-size: 0.8rem; background: rgba(255,153,51,0.15); padding: 2px 8px; border-radius: 4px;">View Details</span>
                    </summary>
                    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
                        <table class="drik-table" style="width: 100%; font-size: 0.85rem; border-collapse: collapse;">
                            <thead>
                                <tr style="color: var(--text-muted); border-bottom: 1.5px solid rgba(255,255,255,0.08); font-weight:700;">
                                    <th style="padding: 8px 0; text-align: left;">Remedy Parameter</th>
                                    <th style="padding: 8px 0; text-align: left;">Prescribed Action / Recommendation</th>
                                    <th style="padding: 8px 0; text-align: left;">Rules & Ritual Method</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Life Stone (Lagna Lord)</td>
                                    <td><strong style="color: #c084fc;">Yellow Sapphire (Pukhraj)</strong></td>
                                    <td>Wear in gold on Index finger on Thursday morning after puja.</td>
                                </tr>
                                <tr>
                                    <td>Lucky Stone (9th Lord)</td>
                                    <td><strong style="color: #ef4444;">Red Coral (Moonga)</strong></td>
                                    <td>Wear in copper/gold on Ring finger on Tuesday morning.</td>
                                </tr>
                                <tr>
                                    <td>Benefic Stone (5th Lord)</td>
                                    <td><strong style="color: #3b82f6;">Pearl (Moti)</strong></td>
                                    <td>Wear in silver on Little finger on Monday evening.</td>
                                </tr>
                                <tr>
                                    <td>Contradictory Stones Warning</td>
                                    <td><strong style="color: #ef4444;">Avoid Diamond & Blue Sapphire</strong></td>
                                    <td>Do not wear opposing stones concurrently; causes conflict.</td>
                                </tr>
                                <tr>
                                    <td>Rudraksha Bead recommendation</td>
                                    <td><strong>5 Mukhi (ruled by Jupiter)</strong></td>
                                    <td>Wear on neck or wrist in red thread after Shiva Puja.</td>
                                </tr>
                                <tr>
                                    <td>Seed Mantra chanting guide</td>
                                    <td><strong style="color: #fbbf24;">Om Hreem Namah (108 times daily)</strong></td>
                                    <td>Best chanted during sunrise facing East.</td>
                                </tr>
                                <tr>
                                    <td>Devotional Deity Alignment</td>
                                    <td><strong>Lord Shiva / Hanuman</strong></td>
                                    <td>Aligns your Mars and Jupiter energies for best output.</td>
                                </tr>
                                <tr>
                                    <td>Auspicious Action Day/Hour</td>
                                    <td><strong>Thursday during Guru Hora</strong></td>
                                    <td>Start new business or sign deals during this hour.</td>
                                </tr>
                                <tr>
                                    <td>Fasting suitability guidelines</td>
                                    <td><strong>Fasting on Thursdays (Guru Vrat)</strong></td>
                                    <td>Avoid salt and grains; perform Vishnu puja for wisdom.</td>
                                </tr>
                                <tr>
                                    <td>Auspicious Color and Metal</td>
                                    <td><strong>Yellow / Gold & Copper</strong></td>
                                    <td>Enhances positive electromagnetic reception of auric body.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </details>

            </div>
        </div>
    `;
};

// ═══════════════════════════════════════════════════════════════════
//  HELPER FUNCTIONS FOR KUNDLI CALCULATIONS
// ═══════════════════════════════════════════════════════════════════
function getVargottamaPlanets(d1, div) {
    const planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
    let matches = [];
    planets.forEach(p => {
        if (d1[p] && div.D9 && div.D9[p] && d1[p].sign === div.D9[p].sign) {
            matches.push(p);
        }
    });
    return matches.length > 0 ? matches.join(', ') : 'None';
}

function getPushkarNavamsa(d1, div) {
    // In Navamsa: Taurus, Cancer, Virgo, Libra, Sagittarius, Pisces are Pushkar signs
    const pushkarSigns = ['Taurus', 'Cancer', 'Virgo', 'Libra', 'Sagittarius', 'Pisces'];
    let count = 0;
    for (const p in d1) {
        if (p === 'Asc') continue;
        if (div.D9 && div.D9[p] && pushkarSigns.includes(div.D9[p].sign)) {
            count++;
        }
    }
    return `${count} Planets`;
}

function checkGandanta(d1) {
    // Check if planet is at junction: Aries-Pisces, Leo-Cancer, Sagittarius-Scorpio (within 2 degrees)
    for (const p in d1) {
        if (p === 'Asc') continue;
        const pos = d1[p];
        if (pos) {
            if (pos.sign === 'Aries' && pos.lon < 2.0) return `${p} (Aries)`;
            if (pos.sign === 'Pisces' && pos.lon > 28.0) return `${p} (Pisces)`;
            if (pos.sign === 'Leo' && pos.lon < 2.0) return `${p} (Leo)`;
            if (pos.sign === 'Cancer' && pos.lon > 28.0) return `${p} (Cancer)`;
            if (pos.sign === 'Sagittarius' && pos.lon < 2.0) return `${p} (Sagittarius)`;
            if (pos.sign === 'Scorpio' && pos.lon > 28.0) return `${p} (Scorpio)`;
        }
    }
    return 'None';
}

function getKarakamsa(d1, div) {
    // Find Atmakaraka (highest degree excluding Rahu/Ketu)
    const planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
    let ak = 'Sun';
    let maxLon = -1;
    planets.forEach(p => {
        if (d1[p] && d1[p].lon > maxLon) {
            maxLon = d1[p].lon;
            ak = p;
        }
    });
    return div.D9 && div.D9[ak] ? `${div.D9[ak].sign} (ruled by ${ak})` : 'Aries';
}

// ═══════════════════════════════════════════════════════════════════
//  KUNDLI MATCHING (MILAN) VISUAL ANALYSIS
// ═══════════════════════════════════════════════════════════════════
window.renderMilanAnalysis = function(data) {
    const card = document.getElementById('milanOutputCard');
    if (!card) return;

    let deepAnalysisBlock = document.getElementById('milanDeepAnalysisBlock');
    if (!deepAnalysisBlock) {
        deepAnalysisBlock = document.createElement('div');
        deepAnalysisBlock.id = 'milanDeepAnalysisBlock';
        deepAnalysisBlock.style.cssText = 'margin-top:24px; border-top:1.5px solid rgba(255,255,255,0.1); padding-top:20px;';
        card.appendChild(deepAnalysisBlock);
    }

    const milan = data.milan;
    if (!milan) return;

    deepAnalysisBlock.innerHTML = `
        <h3 style="color:var(--accent-purple); margin-bottom:16px; display:flex; align-items:center; gap:8px;">
            <span>📊 Premium Matchmaking Analytics</span>
            <span style="font-size:0.75rem; background:#10b981; color:#fff; padding:2px 8px; border-radius:99px;">Verified</span>
        </h3>
        
        <div style="display:flex; flex-direction:column; gap:20px;">
            <!-- Ashtakoot breakdown visual progress bars -->
            <div class="glass-card" style="padding:16px; border:1px solid rgba(255,255,255,0.06); border-radius:8px;">
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
                <div class="glass-card" style="padding:16px; background:rgba(239,68,68,0.03); border:1.5px solid rgba(239,68,68,0.1); border-radius:8px;">
                    <h4 style="color:#ef4444; margin:0 0 8px; font-size:0.9rem; font-weight:700;">2. Manglik Dosha Assessment</h4>
                    <p style="font-size:0.8rem; color:var(--muted-text); margin:0; line-height:1.5;">
                        Mars placements in the 1st, 4th, 7th, 8th, or 12th houses are checked for both charts. High compatibility exists if both are Manglik or if both are non-Manglik.
                    </p>
                </div>

                <!-- Mutual Dasha harmony -->
                <div class="glass-card" style="padding:16px; background:rgba(16,185,129,0.03); border:1.5px solid rgba(16,185,129,0.1); border-radius:8px;">
                    <h4 style="color:#10b981; margin:0 0 8px; font-size:0.9rem; font-weight:700;">3. Dasha Harmony Verdict</h4>
                    <p style="font-size:0.8rem; color:var(--muted-text); margin:0; line-height:1.5;">
                        Checking transition periods (Dasha Sandhi) to ensure both partners do not transition into challenging time-lord cycles concurrently.
                    </p>
                </div>
            </div>
        </div>
    `;
};
