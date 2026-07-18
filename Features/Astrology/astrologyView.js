/**
 * Dynamic View Builder for Astrology Suite
 */
function renderAstrologyView() {
    return `<div class="container">
    <div id="breadcrumbs" class="breadcrumbs-container"></div>

    <!-- Top Navigation Tabs -->
    <div class="top-nav-tabs">
        <button class="top-tab-btn active" onclick="switchTopTab(event, 'personalKundliSection')">Personalized Kundli</button>
        <button class="top-tab-btn" onclick="switchTopTab(event, 'gocharSection')">Graha Gochar (Transits)</button>
    </div>

    <!-- 1. Personalized Kundli Section -->
    <div id="personalKundliSection" class="main-section active">
        <div class="dashboard-grid">
            <div class="glass-card">
                <h3 style="color: var(--accent-purple); margin-bottom: 1.5rem;">Enter Birth Details</h3>
                <div class="form-group">
                    <label for="birthDate">Date of Birth</label>
                    <input type="date" id="birthDate" value="1994-01-05">
                </div>
                <div class="form-group">
                    <label for="birthTime">Time of Birth</label>
                    <input type="time" id="birthTime" value="20:00">
                </div>
                <div class="form-group">
                    <label for="birthPlace">Place of Birth</label>
                    <input type="text" id="birthPlace" value="Patna, Bihar, India">
                </div>
                <button class="btn-submit" id="btnCalculate">Generate Kundli</button>
            </div>

            <!-- Output Display -->
            <div class="glass-card" id="outputCard" style="display: none;">
                <div class="tabs">
                    <button class="tab-btn active" onclick="switchTab(event, 'tabDivisional')">Divisional Charts</button>
                    <button class="tab-btn" onclick="switchTab(event, 'tabDasha')">Vimshottari Dasha</button>
                    <button class="tab-btn" onclick="switchTab(event, 'tabGemstone')">Gemstones</button>
                    <button class="tab-btn" onclick="switchTab(event, 'tabRudraksha')">Rudraksha</button>
                    <button class="tab-btn" onclick="switchTab(event, 'tabPrashna')">🔮 Prashna</button>
                    <button class="tab-btn" onclick="switchTab(event, 'tabAnalysis')">📊 Analysis</button>
                </div>

                <!-- Tab Divisional Charts -->
                <div id="tabDivisional" class="tab-content active">
                    <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem;">
                        <label for="vargaSelect" style="font-weight: 600; color: var(--muted-text);">Choose Varga (Division):</label>
                        <select id="vargaSelect" style="width: 250px; background: var(--tile-bg); border: 1px solid var(--border-color); color: var(--text-color); padding: 0.5rem; border-radius: 6px;" onchange="updateVargaCharts()">
                            <option value="D1">D1 (Rashi) - Natal Chart</option>
                            <option value="D2">D2 (Hora) - Wealth</option>
                            <option value="D3">D3 (Drekkana) - Siblings</option>
                            <option value="D4">D4 (Chaturthamsa) - Destiny/House</option>
                            <option value="D7">D7 (Saptamsa) - Progeny</option>
                            <option value="D9" selected>D9 (Navamsa) - Marriage/Spouse</option>
                            <option value="D10">D10 (Dasamsa) - Career/Profession</option>
                            <option value="D12">D12 (Dwadasamsa) - Parents</option>
                            <option value="D16">D16 (Shodasamsa) - Vehicles/Luxuries</option>
                            <option value="D20">D20 (Vimsamsa) - Spiritual Progress</option>
                            <option value="D24">D24 (Chaturvimsamsa) - Learning/Knowledge</option>
                            <option value="D30">D30 (Trimsamsa) - Evil Effects</option>
                            <option value="D40">D40 (Khavedamsa) - Auspiciousness</option>
                            <option value="D45">D45 (Akshavedamsa) - Character</option>
                            <option value="D60">D60 (Shastiamsa) - Past Karma</option>
                        </select>
                    </div>

                    <div class="charts-row">
                        <div class="chart-box">
                            <h4 id="vargaNorthTitle">North Indian Chart (D9)</h4>
                            <div id="vargaNorth"></div>
                        </div>
                        <div class="chart-box">
                            <h4 id="vargaSouthTitle">South Indian Chart (D9)</h4>
                            <div id="vargaSouth"></div>
                        </div>
                    </div>
                    <h3 style="margin-top: 2rem; color: var(--accent-purple);">Planetary Placements</h3>
                    <div class="planet-grid" id="d1Planets"></div>
                </div>

                <!-- Tab Dasha -->
                <div id="tabDasha" class="tab-content">
                    <h3 style="color: var(--accent-purple); margin-bottom: 0.5rem;" id="dashaHeader">Vimshottari Dasha Timeline</h3>
                    <p style="color: var(--muted-text); font-size: 0.85rem; margin-bottom: 1rem;">Your Mahadasha and Antardasha periods based on Moon Nakshatra at birth.</p>
                    <!-- Dasha Timeline Bar -->
                    <div id="dashaTimelineBar" style="margin-bottom: 1.5rem;"></div>
                    <!-- Dasha Tree -->
                    <div class="dasha-list" id="dashaContainer"></div>
                </div>

                <!-- Tab Gemstone -->
                <div id="tabGemstone" class="tab-content">
                    <h3 style="color: var(--accent-purple); margin-bottom: 1rem;">Gemstone Recommendation</h3>
                    <div id="gemstoneContainer"></div>
                </div>

                <!-- Tab Rudraksha -->
                <div id="tabRudraksha" class="tab-content">
                    <h3 style="color: var(--accent-purple); margin-bottom: 1rem;">Rudraksha Suggestion</h3>
                    <div id="rudrakshaContainer"></div>
                </div>

                <!-- Tab Prashna Kundali -->
                <div id="tabPrashna" class="tab-content">
                    <div style="background:rgba(99,102,241,0.1);border:1.5px solid rgba(99,102,241,0.3);border-radius:12px;padding:18px;margin-bottom:1.5rem;">
                        <h3 style="color:#a5b4fc;margin:0 0 8px;">🔮 Prashna Kundali (Horary Astrology)</h3>
                        <p style="color:var(--muted-text);font-size:0.9rem;margin:0;">In Prashna, the <strong style="color:#c4b5fd;">moment you ask the question</strong> becomes the birth chart. Enter the current date, time and your location — then click <strong style="color:#c4b5fd;">Cast Prashna</strong> to read the answer from the planets.</p>
                    </div>
                    <div class="form-row" style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem;">
                        <div class="form-group" style="flex:1;min-width:160px;">
                            <label for="prashnaDate">Query Date</label>
                            <input type="date" id="prashnaDate" style="width:100%;">
                        </div>
                        <div class="form-group" style="flex:1;min-width:130px;">
                            <label for="prashnaTime">Query Time</label>
                            <input type="time" id="prashnaTime" style="width:100%;">
                        </div>
                        <div class="form-group" style="flex:2;min-width:200px;">
                            <label for="prashnaPlace">Your Location</label>
                            <input type="text" id="prashnaPlace" value="New Delhi, India" style="width:100%;">
                        </div>
                        <div class="form-group" style="flex:1;min-width:140px;">
                            <label for="prashnaQuestion">Question (optional)</label>
                            <input type="text" id="prashnaQuestion" placeholder="e.g. Career, Marriage..." style="width:100%;">
                        </div>
                        <div style="display:flex;align-items:flex-end;">
                            <button class="btn-submit" id="btnPrashna" style="white-space:nowrap;">🔮 Cast Prashna</button>
                        </div>
                    </div>
                    <!-- Prashna Output -->
                    <div id="prashnaOutputCard" style="display:none;">
                        <div class="charts-row">
                            <div class="chart-box">
                                <h4 id="prashnaNorthTitle">Prashna North Indian Chart</h4>
                                <div id="prashnaNorth"></div>
                            </div>
                            <div class="chart-box">
                                <h4 id="prashnaSouthTitle">Prashna South Indian Chart</h4>
                                <div id="prashnaSouth"></div>
                            </div>
                        </div>
                        <div id="prashnaInterpretation" style="margin-top:1.5rem;"></div>
                    </div>
                </div>

                <!-- Tab Analysis -->
                <div id="tabAnalysis" class="tab-content">
                    <div id="analysisContainer">
                        <div style="text-align:center;padding:2rem;color:var(--muted-text);">Generate your Kundli above to see detailed analysis, statistics and charts.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. Graha Gochar Section -->
    <div id="gocharSection" class="main-section">
        <div class="dashboard-grid">
            <div class="glass-card">
                <h3 style="color: var(--accent-purple); margin-bottom: 1.5rem;">Select Gochar Date</h3>
                <div class="form-group">
                    <label for="gocharDate">Date</label>
                    <input type="date" id="gocharDate">
                </div>
                <div class="form-group">
                    <label for="gocharTime">Time</label>
                    <input type="time" id="gocharTime" value="12:00">
                </div>
                <div class="form-group">
                    <label for="gocharPlace">Place</label>
                    <input type="text" id="gocharPlace" value="New Delhi, India">
                </div>
                <button class="btn-submit" id="btnGochar">View Gochar</button>
            </div>

            <!-- Gochar Output -->
            <div class="glass-card" id="gocharOutputCard" style="display: none;">
                <div class="tabs">
                    <button class="tab-btn active" onclick="switchTab(event, 'tabGocharD1')">Gochar Charts</button>
                    <button class="tab-btn" onclick="switchTab(event, 'tabGocharPanchang')">Panchang</button>
                    <button class="tab-btn" onclick="switchTab(event, 'tabGocharMuhurtas')">Muhurtas</button>
                </div>

                <div id="tabGocharD1" class="tab-content active">
                    <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1rem;">
                        <label for="gocharVargaSelect" style="font-weight: 600; color: var(--muted-text);">Choose Varga (Transit):</label>
                        <select id="gocharVargaSelect" style="width: 250px; background: var(--tile-bg); border: 1px solid var(--border-color); color: var(--text-color); padding: 0.5rem; border-radius: 6px;" onchange="updateGocharVargaCharts()">
                            <option value="D1" selected>D1 (Rashi) - Natal Chart</option>
                            <option value="D9">D9 (Navamsa) - Marriage/Spouse</option>
                        </select>
                    </div>

                    <div class="charts-row">
                        <div class="chart-box">
                            <h4 id="gocharVargaNorthTitle">Gochar North Indian</h4>
                            <div id="gocharNorth"></div>
                        </div>
                        <div class="chart-box">
                            <h4 id="gocharVargaSouthTitle">Gochar South Indian</h4>
                            <div id="gocharSouth"></div>
                        </div>
                    </div>
                    <h3 style="margin-top: 2rem; color: var(--accent-purple);">Gochar Transit Degrees</h3>
                    <div class="planet-grid" id="gocharPlanets"></div>
                </div>

                <div id="tabGocharPanchang" class="tab-content">
                    <h3 style="color: var(--accent-purple); margin-bottom: 1rem;">Gochar Panchang</h3>
                    <table class="panchang-table">
                        <tbody id="gocharPanchangBody"></tbody>
                    </table>
                </div>

                <div id="tabGocharMuhurtas" class="tab-content">
                    <h3 class="muhurta-section-title">Choghadiya Timings (Transit)</h3>
                    <table class="panchang-table">
                        <thead>
                            <tr style="color: var(--accent-purple); text-align: left; font-weight: 700;">
                                <th style="padding: 0.5rem;">Period</th>
                                <th style="padding: 0.5rem;">Time Span</th>
                                <th style="padding: 0.5rem;">Choghadiya</th>
                                <th style="padding: 0.5rem;">Quality</th>
                            </tr>
                        </thead>
                        <tbody id="gocharChoghadiyaBody"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- 3. Match Making Section -->
    <div id="milanSection" class="main-section">
        <div class="glass-card" style="margin-bottom: 2rem;">
            <h3 style="color: var(--accent-purple); margin-bottom: 1.5rem; text-align: center;">Kundli Milan (Ashtakoot Compatibility)</h3>
            <div class="milan-grid">
                <!-- Boy Details -->
                <div>
                    <h4 style="color: var(--accent-gold); margin-bottom: 1rem;">Groom (Boy) Birth Details</h4>
                    <div class="form-group">
                        <label for="boyDate">Date of Birth</label>
                        <input type="date" id="boyDate" value="1994-01-05">
                    </div>
                    <div class="form-group">
                        <label for="boyTime">Time of Birth</label>
                        <input type="time" id="boyTime" value="20:00">
                    </div>
                    <div class="form-group">
                        <label for="boyPlace">Place of Birth</label>
                        <input type="text" id="boyPlace" value="Patna, Bihar, India">
                    </div>
                </div>
                <!-- Girl Details -->
                <div>
                    <h4 style="color: var(--accent-gold); margin-bottom: 1rem;">Bride (Girl) Birth Details</h4>
                    <div class="form-group">
                        <label for="girlDate">Date of Birth</label>
                        <input type="date" id="girlDate" value="1995-03-10">
                    </div>
                    <div class="form-group">
                        <label for="girlTime">Time of Birth</label>
                        <input type="time" id="girlTime" value="08:30">
                    </div>
                    <div class="form-group">
                        <label for="girlPlace">Place of Birth</label>
                        <input type="text" id="girlPlace" value="Patna, Bihar, India">
                    </div>
                </div>
            </div>
            <button class="btn-submit" id="btnMatch" style="margin-top: 1.5rem;">Calculate Match Compatibility</button>
        </div>

        <!-- Match Output Card -->
        <div class="glass-card" id="milanOutputCard" style="display: none;">
            <h3 style="color: var(--accent-purple); margin-bottom: 1.5rem; text-align: center;">Guna Milan Results</h3>
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 1.2rem; color: var(--muted-text);">
                    Boy: <strong id="boyResultInfo" style="color: #fff;"></strong> | Girl: <strong id="girlResultInfo" style="color: #fff;"></strong>
                </div>
                <div id="milanScoreBadge" class="result-badge"></div>
            </div>

            <table class="panchang-table">
                <thead>
                    <tr style="border-bottom: 2px solid var(--border-color); text-align: left; font-weight: 700; color: var(--accent-purple);">
                        <th style="padding: 0.75rem 1rem;">Koot parameter</th>
                        <th style="padding: 0.75rem 1rem;">Max points</th>
                        <th style="padding: 0.75rem 1rem;">Obtained points</th>
                    </tr>
                </thead>
                <tbody id="milanTableBody"></tbody>
            </table>
        </div>
    </div>
    
    <!-- 4. Maasik / Monthly Panchang Section -->
    <div id="maasikSection" class="main-section">
        <!-- Unified Panchang Header (shared with dainik, shows month) -->
        <div class="panchang-unified-header" id="maasikPancHeader">
            <div>
                <div class="ph-title" id="phTitleMaasik">Maasik Panchang</div>
                <div class="ph-subtitle" id="phSubMaasik">Loading...</div>
            </div>
            <div class="ph-controls">
                <div class="ph-view-toggle">
                    <button class="ph-view-btn" id="phViewDayBtnM" onclick="switchPancView('day')">Day</button>
                    <button class="ph-view-btn active" id="phViewMonthBtnM" onclick="switchPancView('month')">Month</button>
                </div>
                <button class="ph-nav-btn" id="maasikPrevBtn" title="Previous Month">&#8249;</button>
                <input type="month" class="ph-date-input" id="maasikMonthInput" style="min-width:140px;">
                <button class="ph-nav-btn" id="maasikNextBtn" title="Next Month">&#8250;</button>
                <button class="ph-today-btn" id="maasikTodayBtn">This Month</button>
                <input type="text" class="ph-place-input" id="maasikPlaceInput" value="New Delhi, India" placeholder="Place...">
            </div>
        </div>

        <!-- Calendar Grid + Sidebar Wrapper -->
        <div class="monthly-panchang-wrapper">
            <!-- Main Calendar Grid -->
            <div class="monthly-cal-main">
                <div class="cal-grid-header">
                    <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
                </div>
                <div class="cal-grid" id="maasikCalGrid">
                    <div class="cal-month-loading">Select a month to view the calendar...</div>
                </div>
            </div>

            <!-- Sidebar Details -->
            <div class="monthly-cal-sidebar" id="maasikSidebar">
                <div class="sidebar-title" id="maasikSidebarTitle">Select a date for details</div>
                <div id="maasikSidebarContent">
                    <div style="color: var(--muted-text); font-size: 0.85rem; text-align: center; padding: 2rem 0;">Click any date in the calendar to view its full Panchang details.</div>
                </div>
            </div>
        </div>
        
        <!-- Monthly Panchang Footer Widgets -->
        <div style="padding: 20px; border-top: 2px solid rgba(162,57,34,0.2); background: rgba(0,0,0,0.15); display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-top: 15px;">
            <div class="glass-card widget-box dainik-layout-card" style="padding: 15px; background: var(--card-bg); border: var(--card-border); border-radius: 8px;">
                <h4 style="color:var(--title-color); margin-top:0; border-bottom:var(--card-border); padding-bottom:6px; font-size:0.95rem;">🪐 Planetary Events</h4>
                <div id="planetaryEventsContainer_maasik" style="display:flex; flex-direction:column; gap:8px;">
                    Loading...
                </div>
            </div>
            
            <div class="glass-card widget-box dainik-layout-card" style="padding: 15px; background: var(--card-bg); border: var(--card-border); border-radius: 8px;">
                <h4 style="color:var(--title-color); margin-top:0; border-bottom:var(--card-border); padding-bottom:6px; font-size:0.95rem;">🦁 Rashifal (Horoscope)</h4>
                <div id="rashifalTodayContainer_maasik" style="max-height:300px; overflow-y:auto; padding-right:4px;">
                    Loading...
                </div>
            </div>
            
            <div class="glass-card widget-box dainik-layout-card" style="padding: 15px; background: var(--card-bg); border: var(--card-border); border-radius: 8px;">
                <h4 style="color:var(--title-color); margin-top:0; border-bottom:var(--card-border); padding-bottom:6px; font-size:0.95rem;">📅 Upavas & Festivals</h4>
                <div id="upcomingFestivalsContainer_maasik" style="max-height:300px; overflow-y:auto; padding-right:4px;">
                    Loading...
                </div>
            </div>
        </div>
    </div>

    <!-- Footer diagnostic API panel -->
    <footer style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border-color); text-align: center; font-size: 0.9rem; color: var(--muted-text);">
        <p>© 2026 Sanskrit AI Astrological Suite. Enterprise Grade.</p>
        <button id="btnOpenApiTest" style="background: rgba(124, 45, 18, 0.2); border: 1.5px solid #a23922; color: #fff; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; margin-top: 10px; transition: all 0.2s;">⚙️ Open API Diagnostic Panel</button>
        
        <div id="apiTestPanel" style="display: none; background: rgba(0,0,0,0.4); border: 2px solid #a23922; border-radius: 8px; padding: 20px; margin-top: 1.5rem; text-align: left;">
            <h4 style="color: var(--accent-gold); margin-top:0; border-bottom: 1.5px solid var(--border-color); padding-bottom: 6px;">⚙️ API Diagnostic & Live Validation System</h4>
            <div style="display: flex; gap: 15px; flex-wrap: wrap; margin-bottom: 15px;">
                <div style="flex:1; min-width:200px;">
                    <label style="display:block; margin-bottom:5px; font-weight:600;">Date</label>
                    <input type="date" id="apiTestDate" value="2026-07-14" style="width:100%; padding:8px; border:1px solid var(--border-color); border-radius:4px; background:#1e1b4b; color:#fff;">
                </div>
                <div style="flex:1; min-width:200px;">
                    <label style="display:block; margin-bottom:5px; font-weight:600;">Place</label>
                    <input type="text" id="apiTestPlace" value="New Delhi, India" style="width:100%; padding:8px; border:1px solid var(--border-color); border-radius:4px; background:#1e1b4b; color:#fff;">
                </div>
                <div style="display:flex; align-items:flex-end;">
                    <button id="btnRunApiTest" style="background:#a23922; border:none; color:#fff; padding:10px 20px; border-radius:4px; font-weight:700; cursor:pointer;">Run API Test</button>
                </div>
            </div>
            <div id="apiTestOutput" style="max-height: 350px; overflow-y: auto; background: rgba(0,0,0,0.6); padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.85rem; border: 1px solid var(--border-color);">
                Click "Run API Test" to load live dynamic calculation response.
            </div>
        </div>
    </footer>
</div>`;
}
