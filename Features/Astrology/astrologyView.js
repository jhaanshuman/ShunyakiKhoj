/**
 * Dynamic View Builder for Astrology Suite
 */
function renderAstrologyView() {
    return `<div class="container astrology-container">
    <div id="breadcrumbs" class="breadcrumbs-container"></div>

    <!-- Settings & Customization Header Bar -->
    <div class="astrology-settings-bar" style="display: flex; gap: 10px; flex-wrap: wrap; background: rgba(15,18,29,0.8); border: 1px solid rgba(255,255,255,0.08); padding: 12px 15px; border-radius: 8px; margin-bottom: 20px; font-size: 0.8rem; box-sizing: border-box; width: 100%;">
        <div style="display:flex; flex-direction:column; min-width:110px;">
            <label style="font-weight:600; color:var(--text-muted); margin-bottom:4px;">Chart Style</label>
            <select id="selChartStyle" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                <option value="North" selected>North Indian (Lagna)</option>
                <option value="South">South Indian</option>
            </select>
        </div>
        <div style="display:flex; flex-direction:column; min-width:110px;">
            <label style="font-weight:600; color:var(--text-muted); margin-bottom:4px;">Ayanamsa</label>
            <select id="selAyanamsa" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                <option value="Lahiri" selected>Lahiri (Chitra Paksha)</option>
                <option value="Raman">B.V. Raman</option>
                <option value="KP">Krishnamurti (KP)</option>
                <option value="Tropical">Tropical (No Ayanamsa)</option>
                <option value="Fagan">Fagan-Bradley</option>
                <option value="Pushya">Pushya-paksha</option>
            </select>
        </div>
        <div style="display:flex; flex-direction:column; min-width:100px;">
            <label style="font-weight:600; color:var(--text-muted); margin-bottom:4px;">Rahu/Ketu</label>
            <select id="selNode" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                <option value="True" selected>True Node</option>
                <option value="Mean">Mean Node</option>
            </select>
        </div>
        <div style="display:flex; flex-direction:column; min-width:100px;">
            <label style="font-weight:600; color:var(--text-muted); margin-bottom:4px;">Rashi Numbers</label>
            <select id="selRashiVisibility" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                <option value="Visible" selected>Visible</option>
                <option value="Hidden">Hidden</option>
            </select>
        </div>
        <div style="display:flex; flex-direction:column; min-width:100px;">
            <label style="font-weight:600; color:var(--text-muted); margin-bottom:4px;">Outer Planets</label>
            <select id="selOuterPlanets" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                <option value="Hidden" selected>Hidden</option>
                <option value="Visible">Visible</option>
            </select>
        </div>
        <div style="display:flex; flex-direction:column; min-width:100px;">
            <label style="font-weight:600; color:var(--text-muted); margin-bottom:4px;">Terminology</label>
            <select id="selTerminology" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                <option value="Vedic" selected>Vedic (Guru/Shukra)</option>
                <option value="Western">Western (Jup/Ven)</option>
            </select>
        </div>
        <div style="display:flex; flex-direction:column; min-width:110px;">
            <label style="font-weight:600; color:var(--text-muted); margin-bottom:4px;">Longitude Format</label>
            <select id="selLongStyle" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                <option value="DMS" selected>Deg-Min-Sec</option>
                <option value="Decimal">Decimal Degrees</option>
            </select>
        </div>
    </div>

    <!-- Top Tabs for switching sections -->
    <div class="top-nav-tabs" style="margin-bottom: 20px;">
        <button class="top-tab-btn active" onclick="switchTopTab(event, 'personalKundliSection')">Personalized Kundli</button>
        <button class="top-tab-btn" onclick="switchTopTab(event, 'gocharSection')">Graha Gochar (Transits)</button>
    </div>

    <!-- 1. Personalized Kundli Section -->
    <div id="personalKundliSection" class="main-section active">
        <div class="dashboard-grid" style="display: flex; gap: 20px; align-items: start; box-sizing: border-box; width: 100%;">
            
            <!-- Birth Details Card (Starts wide, slides to left sidebar) -->
            <div class="birth-details-card" style="flex: 1; max-width: 600px; margin: 0 auto; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 25px; transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1); box-sizing: border-box; overflow: hidden; position: relative;">
                <h3 style="color: var(--accent-purple); margin-top:0; margin-bottom: 1.5rem;">Enter Birth Details</h3>
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="birthName" style="display:block; margin-bottom:6px; font-weight:600; color:var(--text-color);">Name (नाम)</label>
                    <input type="text" id="birthName" value="Native" style="width:100%; padding:10px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color);">
                </div>
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="birthDate" style="display:block; margin-bottom:6px; font-weight:600; color:var(--text-color);">Date of Birth (जन्म तिथि)</label>
                    <input type="date" id="birthDate" value="1994-01-05" style="width:100%; padding:10px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color);">
                </div>
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="birthTime" style="display:block; margin-bottom:6px; font-weight:600; color:var(--text-color);">Time of Birth (जन्म समय)</label>
                    <input type="time" id="birthTime" value="20:00" style="width:100%; padding:10px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color);">
                </div>
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="birthPlace" style="display:block; margin-bottom:6px; font-weight:600; color:var(--text-color);">Place of Birth (जन्म स्थान)</label>
                    <input type="text" id="birthPlace" value="Patna, Bihar, India" style="width:100%; padding:10px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color);">
                    <a href="javascript:void(0)" onclick="toggleBirthMap()" style="font-size:0.8rem; color:var(--accent-color); text-decoration:none; margin-top: 5px; display:inline-block;">🗺️ Pinpoint on Map for Coordinates</a>
                    <div id="birthMap" style="height: 180px; margin-top: 10px; border-radius: 8px; border: 1px solid var(--border-color); display: none;"></div>
                </div>
                
                <div class="form-row" style="display:flex; gap:10px; margin-bottom:20px;">
                    <div class="form-group" style="flex:1;">
                        <label for="birthLat" style="display:block; margin-bottom:4px; font-size:0.8rem; color:var(--text-muted);">Latitude</label>
                        <input type="number" step="any" id="birthLat" value="25.5941" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color);">
                    </div>
                    <div class="form-group" style="flex:1;">
                        <label for="birthLon" style="display:block; margin-bottom:4px; font-size:0.8rem; color:var(--text-muted);">Longitude</label>
                        <input type="number" step="any" id="birthLon" value="85.1376" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color);">
                    </div>
                </div>
                
                <button class="btn-submit" id="btnCalculate" style="width:100%; padding:12px; font-size:1rem; font-weight:700; border-radius:8px;">🔮 Generate Kundali</button>
                
                <!-- Raw Data & Extra Details (Hidden on load) -->
                <div id="extraSidebarDetails" style="display:none; margin-top:20px; border-top:1px solid rgba(255,255,255,0.08); padding-top:15px;">
                    <button class="ph-today-btn" id="btnShowRawData" onclick="toggleRawPayloadModal()" style="width:100%; font-size:0.8rem; padding:8px 12px; background:rgba(255,255,255,0.05); color:#fff; border:1px solid var(--border-color); margin-bottom:10px;">📋 Show Raw JSON Data</button>
                    <div id="rawPayloadBox" style="display:none; max-height:200px; overflow-y:auto; background:#0d1117; padding:10px; border-radius:6px; font-family:monospace; font-size:0.75rem; border:1px solid var(--border-color); color:#4ade80;"></div>
                </div>
            </div>

            <!-- Output Display Container (Hidden on load, flexes center) -->
            <div class="glass-card" id="outputCard" style="display: none; flex: 1; min-width: 0; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 25px; box-shadow: var(--shadow);">
                <div class="tabs" style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px;">
                    <button class="tab-btn active" onclick="switchKundliTab(event, 'tabChart')">Chart (कुण्डली)</button>
                    <button class="tab-btn" onclick="switchKundliTab(event, 'tabDasha')">Dasha (महादशा)</button>
                    <button class="tab-btn" onclick="switchKundliTab(event, 'tabStrength')">Strength (बल)</button>
                    <button class="tab-btn" onclick="switchKundliTab(event, 'tabAshtakvarga')">Ashtakvarga (अष्टकवर्ग)</button>
                    <button class="tab-btn" onclick="switchKundliTab(event, 'tabPanchanga')">Panchanga (पञ्चाङ्ग)</button>
                </div>

                <!-- 1. Chart Tab -->
                <div id="tabChart" class="tab-content active">
                    <div class="chart-controls-bar" style="display:flex; gap:12px; align-items:center; margin-bottom:15px; flex-wrap:wrap;">
                        <div style="display:flex; align-items:center; gap:8px;">
                            <label style="font-weight:600; color:var(--text-muted); font-size:0.85rem;">Center Chart:</label>
                            <select id="selChartCenter" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                                <option value="Asc" selected>Ascendant / Lagna</option>
                                <option value="Sun">Surya Lagna (Sun)</option>
                                <option value="Moon">Chandra Lagna (Moon)</option>
                            </select>
                        </div>
                    </div>

                    <!-- Inner sub-tabs: Rashi | Navamsa | Bhava | Others -->
                    <div class="sub-tabs" style="display:flex; gap:6px; margin-bottom:15px; border-bottom:1px dashed rgba(255,255,255,0.06); padding-bottom:6px;">
                        <button class="sub-tab-btn active" onclick="switchSubChartTab(event, 'D1')">Rashi (D1)</button>
                        <button class="sub-tab-btn" onclick="switchSubChartTab(event, 'D9')">Navamsa (D9)</button>
                        <button class="sub-tab-btn" onclick="switchSubChartTab(event, 'Bhava')">Bhava (Sripathy)</button>
                        <button class="sub-tab-btn" onclick="switchSubChartTab(event, 'Others')">Others (D1-60)</button>
                    </div>

                    <!-- Divisional others selector (Visible only in others sub-tab) -->
                    <div id="othersVargaDropdownSelector" style="display:none; align-items:center; gap:8px; margin-bottom:15px;">
                        <label style="font-weight:600; color:var(--text-muted); font-size:0.85rem;">Divisional Chart (Varga):</label>
                        <select id="selOthersVarga" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="updateOthersVargaView()">
                            <option value="D2">D2 (Hora) - Wealth</option>
                            <option value="D3">D3 (Drekkana) - Siblings</option>
                            <option value="D4">D4 (Chaturthamsa) - Home/Destiny</option>
                            <option value="D7">D7 (Saptamsa) - Progeny</option>
                            <option value="D10">D10 (Dasamsa) - Profession</option>
                            <option value="D12">D12 (Dwadasamsa) - Parents</option>
                            <option value="D16">D16 (Shodasamsa) - Vehicles/Luxuries</option>
                            <option value="D20">D20 (Vimsamsa) - Spirituality</option>
                            <option value="D24">D24 (Chaturvimsamsa) - Learning</option>
                            <option value="D30">D30 (Trimsamsa) - Evils</option>
                            <option value="D40">D40 (Khavedamsa) - Auspiciousness</option>
                            <option value="D45">D45 (Akshavedamsa) - Character</option>
                            <option value="D60">D60 (Shastiamsa) - Past Karma</option>
                        </select>
                    </div>

                    <!-- SVGs Display -->
                    <div class="charts-row" style="display:flex; gap:20px; flex-wrap:wrap; margin-bottom:20px;">
                        <div class="chart-box" style="flex:1.2; min-width:320px; text-align:center;">
                            <h4 id="lagnaChartTitle" style="color:var(--title-color); margin-top:0; margin-bottom:10px;">Lagna Chart (D1)</h4>
                            <div id="lagnaChartContainer" style="display:inline-block; border-radius:8px; overflow:hidden;"></div>
                        </div>
                        
                        <div class="chart-box" style="flex:1.8; min-width:320px;">
                            <!-- List Tabs: Planets | Upagraha | Arudha | Others -->
                            <div class="list-tabs" style="display:flex; gap:6px; margin-bottom:12px;">
                                <button class="list-tab-btn active" onclick="switchListTab(event, 'listPlanets')">Planets</button>
                                <button class="list-tab-btn" onclick="switchListTab(event, 'listUpagraha')">Upagraha</button>
                                <button class="list-tab-btn" onclick="switchListTab(event, 'listArudha')">Arudha</button>
                                <button class="list-tab-btn" onclick="switchListTab(event, 'listOthers')">Others</button>
                            </div>

                            <!-- List Tables Container -->
                            <div id="chartListTableContainer" style="overflow-x:auto; background:rgba(0,0,0,0.1); border:1px solid var(--border-color); border-radius:8px; padding:10px; max-height: 380px; overflow-y: auto;">
                                <!-- Loaded dynamically -->
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. Dasha Tab -->
                <div id="tabDasha" class="tab-content" style="display:none;">
                    <div style="display:flex; gap:15px; flex-wrap:wrap; align-items:center; margin-bottom:15px;">
                        <div style="display:flex; flex-direction:column; min-width:140px;">
                            <label style="font-weight:600; color:var(--text-muted); font-size:0.8rem; margin-bottom:4px;">Dasha System</label>
                            <select id="selDashaSystem" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="updateDashaView()">
                                <option value="Vimshottari" selected>Vimshottari Dasha</option>
                                <option value="Ashtottari">Ashtottari Dasha</option>
                                <option value="Yogini">Yogini Dasha</option>
                                <option value="Chara">Chara Dasha</option>
                                <option value="Tribhagi">Tribhagi Vimshottari</option>
                                <option value="Divisional">Divisional Planetwise</option>
                            </select>
                        </div>
                        <div style="display:flex; flex-direction:column; min-width:140px;">
                            <label style="font-weight:600; color:var(--text-muted); font-size:0.8rem; margin-bottom:4px;">Year Length Mode</label>
                            <select id="selDashaYear" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="updateDashaView()">
                                <option value="Sidereal" selected>Mean Sidereal Year</option>
                                <option value="Tropical">Mean Tropical Year</option>
                                <option value="365.25">365.25 Days Year</option>
                                <option value="365">365 Days Year</option>
                                <option value="Savana">Savana Year (360 Days)</option>
                            </select>
                        </div>
                    </div>
                    
                    <div id="dashaTimelineContainer" style="overflow-x:auto; background:rgba(0,0,0,0.1); border:1px solid var(--border-color); border-radius:8px; padding:15px;">
                        <!-- Loaded dynamically -->
                    </div>
                </div>

                <!-- 3. Strength Tab -->
                <div id="tabStrength" class="tab-content" style="display:none;">
                    <!-- Strength sub-tabs: Shadbala | Bhavabala | Vimsopaka -->
                    <div class="strength-tabs" style="display:flex; gap:6px; margin-bottom:15px; border-bottom:1px dashed rgba(255,255,255,0.06); padding-bottom:6px;">
                        <button class="strength-tab-btn active" onclick="switchStrengthTab(event, 'Shadbala')">Shadbala</button>
                        <button class="strength-tab-btn" onclick="switchStrengthTab(event, 'Bhavabala')">Bhavabala</button>
                        <button class="strength-tab-btn" onclick="switchStrengthTab(event, 'Vimsopaka')">Vimsopaka</button>
                    </div>

                    <!-- Sub Tab Viewport -->
                    <div id="strengthSubContent">
                        <!-- Bar chart canvas + table data loaded dynamically -->
                    </div>
                </div>

                <!-- 4. Ashtakavarga Tab -->
                <div id="tabAshtakvarga" class="tab-content" style="display:none;">
                    <div style="display:flex; gap:15px; flex-wrap:wrap; align-items:center; margin-bottom:15px;">
                        <div style="display:flex; flex-direction:column; min-width:140px;">
                            <label style="font-weight:600; color:var(--text-muted); font-size:0.8rem; margin-bottom:4px;">Varga Division</label>
                            <select id="selAshtakVarga" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="updateAshtakavargaView()">
                                <option value="D1" selected>D1 (Rashi)</option>
                                <option value="D9">D9 (Navamsa)</option>
                                <option value="D10">D10 (Dasamsa)</option>
                            </select>
                        </div>
                        <div style="display:flex; flex-direction:column; min-width:140px;">
                            <label style="font-weight:600; color:var(--text-muted); font-size:0.8rem; margin-bottom:4px;">Ashtakavarga Type</label>
                            <select id="selAshtakPlanet" style="padding:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); border-radius:4px;" onchange="updateAshtakavargaView()">
                                <option value="Sarvashtakavarga" selected>Sarvashtakavarga (SAV)</option>
                                <option value="Sun">Sun BAV</option>
                                <option value="Moon">Moon BAV</option>
                                <option value="Mars">Mars BAV</option>
                                <option value="Mercury">Mercury BAV</option>
                                <option value="Jupiter">Jupiter BAV</option>
                                <option value="Venus">Venus BAV</option>
                                <option value="Saturn">Saturn BAV</option>
                            </select>
                        </div>
                    </div>

                    <div class="ashtak-row" style="display:flex; gap:20px; flex-wrap:wrap;">
                        <div style="flex:1.2; min-width:280px; text-align:center;">
                            <div id="ashtakChartContainer" style="display:inline-block;"></div>
                        </div>
                        <div style="flex:1.8; min-width:320px; overflow-x:auto;">
                            <div id="ashtakTableContainer"></div>
                        </div>
                    </div>
                </div>

                <!-- 5. Panchanga Tab -->
                <div id="tabPanchanga" class="tab-content" style="display:none;">
                    <h4 style="color:var(--title-color); margin-top:0;">Native Birth Panchanga Limb Table</h4>
                    <div id="birthPanchangTableContainer" style="overflow-x:auto;">
                        <!-- Loaded dynamically -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. Graha Gochar Section -->
    <div id="gocharSection" class="main-section">
        <div class="dashboard-grid">
            <div class="glass-card">
                <h3 style="color: var(--accent-purple); margin-bottom: 1.5rem;">Vedic Transits &amp; Planets</h3>
                <p style="color: var(--text-color);">Dynamic real-time transit calculation viewport based on current coordinates.</p>
            </div>
        </div>
    </div>
</div>`;
}
