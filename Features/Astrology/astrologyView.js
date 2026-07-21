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

            <!-- Status Header Card (Shown during calculation progress) -->
            <div class="glass-card status-header-card" id="statusHeaderCard" style="display: none; flex: 1; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 40px; text-align: center; box-shadow: var(--shadow); box-sizing: border-box; flex-direction: column; align-items: center; justify-content: center; min-height: 400px;">
                <div style="font-size: 2.8rem; margin-bottom: 20px; animation: pulse 1.8s ease-in-out infinite;">🔮</div>
                <h3 style="color: var(--accent-color); margin-top: 0; margin-bottom: 12px; font-size: 1.5rem; font-weight: 800;">Casting Celestial Map</h3>
                <p id="statusMessage" style="color: var(--text-color); font-size: 1.05rem; margin-bottom: 25px; min-height: 24px; font-weight: 600;">Calculating your birth details...</p>
                <div class="progress-bar-container" style="width: 100%; max-width: 400px; height: 8px; background: rgba(255,255,255,0.08); border-radius: 4px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1);">
                    <div id="statusProgressBar" style="width: 0%; height: 100%; background: linear-gradient(90deg, #ea580c, #fbbf24); transition: width 0.1s linear; border-radius: 4px;"></div>
                </div>
            </div>

            <!-- Output Display Container (Hidden on load, flexes center) -->
            <div class="glass-card" id="outputCard" style="display: none; flex: 1; min-width: 0; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 20px; box-shadow: var(--shadow); flex-direction: column;">
                
                <!-- Mobile Report Selector (Visible on Mobile only) -->
                <div class="mobile-report-selector-container" style="margin-bottom: 15px; display: none; width: 100%;">
                    <label for="mobileReportSelector" style="font-weight: 700; color: var(--accent-color); font-size: 0.9rem; display: block; margin-bottom: 6px;">Select Astrological Report:</label>
                    <select id="mobileReportSelector" style="width: 100%; padding: 10px; background: var(--tile-bg); color: var(--text-color); border: 1.5px solid var(--border-color); border-radius: 6px; font-weight: 600;" onchange="switchReportTab(this.value)">
                        <option value="tabD1">D1 - Rashi Chart</option>
                        <option value="tabD9">D9 - Navamsa Chart</option>
                        <option value="tabD2">D2 - Hora Chart (Wealth)</option>
                        <option value="tabD3">D3 - Drekkana (Siblings)</option>
                        <option value="tabD4">D4 - Chaturthamsa (Assets)</option>
                        <option value="tabD7">D7 - Saptamsa (Children)</option>
                        <option value="tabD10">D10 - Dasamsa (Career)</option>
                        <option value="tabD12">D12 - Dwadasamsa (Parents)</option>
                        <option value="tabD16">D16 - Shodasamsa (Vehicles)</option>
                        <option value="tabD20">D20 - Vimsamsa (Spiritual)</option>
                        <option value="tabD24">D24 - Chaturvimsamsa (Education)</option>
                        <option value="tabD30">D30 - Trimsamsa (Mishaps)</option>
                        <option value="tabD40">D40 - Khavedamsa (Auspiciousness)</option>
                        <option value="tabD45">D45 - Akshavedamsa (Character)</option>
                        <option value="tabD60">D60 - Shastiamsa (Past Karma)</option>
                        <option value="tabVimshottari">Vimshottari Dasha</option>
                        <option value="tabAshtottari">Ashtottari Dasha</option>
                        <option value="tabYogini">Yogini Dasha</option>
                        <option value="tabChara">Chara Dasha</option>
                        <option value="tabShadbala">Shadbala Strengths</option>
                        <option value="tabBhavabala">Bhavabala Strengths</option>
                        <option value="tabVimsopaka">Vimsopaka Strength</option>
                        <option value="tabAspects">Planetary Aspects (Drishti)</option>
                        <option value="tabConjunctions">Planetary Conjunctions</option>
                        <option value="tabFriendships">Planetary Friendships</option>
                        <option value="tabJaimini">Jaimini Karakas</option>
                        <option value="tabSpecialLagnas">Special Lagnas</option>
                        <option value="tabUpagrahas">Upagrahas &amp; Gulika</option>
                        <option value="tabArudhas">Arudha Padas</option>
                        <option value="tabSpecialSphutas">Special Sphutas</option>
                        <option value="tabSAV">Sarvashtakavarga Matrix</option>
                        <option value="tabBAVSun">Surya Ashtakavarga (SAV)</option>
                        <option value="tabBAVMoon">Chandra Ashtakavarga (SAV)</option>
                        <option value="tabBAVMars">Mangal Ashtakavarga (SAV)</option>
                        <option value="tabBAVBudha">Budha Ashtakavarga (SAV)</option>
                        <option value="tabBAVGuru">Guru Ashtakavarga (SAV)</option>
                        <option value="tabBAVShukra">Shukra Ashtakavarga (SAV)</option>
                        <option value="tabBAVShani">Shani Ashtakavarga (SAV)</option>
                        <option value="tabPanchanga">Birth Panchanga</option>
                        <option value="tabYogas">Yogas &amp; Predictions</option>
                        <option value="tabGemstones">Gemstone &amp; Rudraksha</option>
                        <option value="tabTransitOverlay">Graha Gochar (Transit Overlay)</option>
                    </select>
                </div>

                <div class="report-dashboard-layout" style="display: flex; width: 100%; gap: 15px; min-height: 550px;">
                    <!-- Desktop Sidebar List (Hidden on Mobile) -->
                    <div class="report-sidebar-list" style="width: 220px; flex-shrink: 0; border-right: 1px solid rgba(255,255,255,0.08); padding-right: 10px; max-height: 600px; overflow-y: auto; display: flex; flex-direction: column; gap: 4px;">
                        <div style="font-weight: 800; color: var(--accent-color); font-size: 0.72rem; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.5px;">Divisional Charts</div>
                        <button class="rep-tab-btn active" id="btn-tabD1" onclick="switchReportTab('tabD1')">D1 - Rashi Chart</button>
                        <button class="rep-tab-btn" id="btn-tabD9" onclick="switchReportTab('tabD9')">D9 - Navamsa Chart</button>
                        <button class="rep-tab-btn" id="btn-tabD2" onclick="switchReportTab('tabD2')">D2 - Hora Chart</button>
                        <button class="rep-tab-btn" id="btn-tabD3" onclick="switchReportTab('tabD3')">D3 - Drekkana Chart</button>
                        <button class="rep-tab-btn" id="btn-tabD4" onclick="switchReportTab('tabD4')">D4 - Chaturthamsa</button>
                        <button class="rep-tab-btn" id="btn-tabD7" onclick="switchReportTab('tabD7')">D7 - Saptamsa Chart</button>
                        <button class="rep-tab-btn" id="btn-tabD10" onclick="switchReportTab('tabD10')">D10 - Dasamsa Chart</button>
                        <button class="rep-tab-btn" id="btn-tabD12" onclick="switchReportTab('tabD12')">D12 - Dwadasamsa</button>
                        <button class="rep-tab-btn" id="btn-tabD16" onclick="switchReportTab('tabD16')">D16 - Shodasamsa</button>
                        <button class="rep-tab-btn" id="btn-tabD20" onclick="switchReportTab('tabD20')">D20 - Vimsamsa Chart</button>
                        <button class="rep-tab-btn" id="btn-tabD24" onclick="switchReportTab('tabD24')">D24 - Chaturvimsamsa</button>
                        <button class="rep-tab-btn" id="btn-tabD30" onclick="switchReportTab('tabD30')">D30 - Trimsamsa Chart</button>
                        <button class="rep-tab-btn" id="btn-tabD40" onclick="switchReportTab('tabD40')">D40 - Khavedamsa</button>
                        <button class="rep-tab-btn" id="btn-tabD45" onclick="switchReportTab('tabD45')">D45 - Akshavedamsa</button>
                        <button class="rep-tab-btn" id="btn-tabD60" onclick="switchReportTab('tabD60')">D60 - Shastiamsa</button>

                        <div style="font-weight: 800; color: var(--accent-color); font-size: 0.72rem; text-transform: uppercase; margin: 12px 0 6px 0; letter-spacing: 0.5px;">Dasha Cycles</div>
                        <button class="rep-tab-btn" id="btn-tabVimshottari" onclick="switchReportTab('tabVimshottari')">Vimshottari Dasha</button>
                        <button class="rep-tab-btn" id="btn-tabAshtottari" onclick="switchReportTab('tabAshtottari')">Ashtottari Dasha</button>
                        <button class="rep-tab-btn" id="btn-tabYogini" onclick="switchReportTab('tabYogini')">Yogini Dasha</button>
                        <button class="rep-tab-btn" id="btn-tabChara" onclick="switchReportTab('tabChara')">Chara Dasha</button>

                        <div style="font-weight: 800; color: var(--accent-color); font-size: 0.72rem; text-transform: uppercase; margin: 12px 0 6px 0; letter-spacing: 0.5px;">Strengths &amp; Aspects</div>
                        <button class="rep-tab-btn" id="btn-tabShadbala" onclick="switchReportTab('tabShadbala')">Shadbala Strengths</button>
                        <button class="rep-tab-btn" id="btn-tabBhavabala" onclick="switchReportTab('tabBhavabala')">Bhavabala Strengths</button>
                        <button class="rep-tab-btn" id="btn-tabVimsopaka" onclick="switchReportTab('tabVimsopaka')">Vimsopaka Strength</button>
                        <button class="rep-tab-btn" id="btn-tabAspects" onclick="switchReportTab('tabAspects')">Planetary Aspects</button>
                        <button class="rep-tab-btn" id="btn-tabConjunctions" onclick="switchReportTab('tabConjunctions')">Conjunctions</button>
                        <button class="rep-tab-btn" id="btn-tabFriendships" onclick="switchReportTab('tabFriendships')">Planetary Friendships</button>

                        <div style="font-weight: 800; color: var(--accent-color); font-size: 0.72rem; text-transform: uppercase; margin: 12px 0 6px 0; letter-spacing: 0.5px;">Special Calculations</div>
                        <button class="rep-tab-btn" id="btn-tabJaimini" onclick="switchReportTab('tabJaimini')">Jaimini Karakas</button>
                        <button class="rep-tab-btn" id="btn-tabSpecialLagnas" onclick="switchReportTab('tabSpecialLagnas')">Special Lagnas</button>
                        <button class="rep-tab-btn" id="btn-tabUpagrahas" onclick="switchReportTab('tabUpagrahas')">Upagrahas &amp; Gulika</button>
                        <button class="rep-tab-btn" id="btn-tabArudhas" onclick="switchReportTab('tabArudhas')">Arudha Padas</button>
                        <button class="rep-tab-btn" id="btn-tabSpecialSphutas" onclick="switchReportTab('tabSpecialSphutas')">Special Sphutas</button>

                        <div style="font-weight: 800; color: var(--accent-color); font-size: 0.72rem; text-transform: uppercase; margin: 12px 0 6px 0; letter-spacing: 0.5px;">Ashtakavarga</div>
                        <button class="rep-tab-btn" id="btn-tabSAV" onclick="switchReportTab('tabSAV')">SAV Matrix</button>
                        <button class="rep-tab-btn" id="btn-tabBAVSun" onclick="switchReportTab('tabBAVSun')">Surya BAV</button>
                        <button class="rep-tab-btn" id="btn-tabBAVMoon" onclick="switchReportTab('tabBAVMoon')">Chandra BAV</button>
                        <button class="rep-tab-btn" id="btn-tabBAVMars" onclick="switchReportTab('tabBAVMars')">Mangal BAV</button>
                        <button class="rep-tab-btn" id="btn-tabBAVBudha" onclick="switchReportTab('tabBAVBudha')">Budha BAV</button>
                        <button class="rep-tab-btn" id="btn-tabBAVGuru" onclick="switchReportTab('tabBAVGuru')">Guru BAV</button>
                        <button class="rep-tab-btn" id="btn-tabBAVShukra" onclick="switchReportTab('tabBAVShukra')">Shukra BAV</button>
                        <button class="rep-tab-btn" id="btn-tabBAVShani" onclick="switchReportTab('tabBAVShani')">Shani BAV</button>

                        <div style="font-weight: 800; color: var(--accent-color); font-size: 0.72rem; text-transform: uppercase; margin: 12px 0 6px 0; letter-spacing: 0.5px;">Astrological Analysis</div>
                        <button class="rep-tab-btn" id="btn-tabPanchanga" onclick="switchReportTab('tabPanchanga')">Birth Panchanga</button>
                        <button class="rep-tab-btn" id="btn-tabYogas" onclick="switchReportTab('tabYogas')">Yogas &amp; Predictions</button>
                        <button class="rep-tab-btn" id="btn-tabGemstones" onclick="switchReportTab('tabGemstones')">Gemstone &amp; Rudraksha</button>
                        <button class="rep-tab-btn" id="btn-tabTransitOverlay" onclick="switchReportTab('tabTransitOverlay')">Transit Overlay</button>
                    </div>

                    <!-- Right Display Pane -->
                    <div class="report-content-pane" style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 15px;">
                        <!-- Heading of selected view -->
                        <h3 id="reportTitle" style="color: var(--title-color); margin-top: 0; border-bottom: 1.5px solid rgba(255,255,255,0.06); padding-bottom: 8px;">D1 - Rashi Chart</h3>
                        
                        <!-- Content injection viewport -->
                        <div id="reportViewport" style="flex: 1; min-height: 480px; overflow-y: auto;"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. Graha Gochar Section -->
    <div id="gocharSection" class="main-section">
        <div class="dashboard-grid" style="display: flex; gap: 20px; align-items: start; box-sizing: border-box; width: 100%;">
            <!-- Transit Input Details -->
            <div class="birth-details-card" style="flex: 1; max-width: 320px; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 20px; box-sizing: border-box;">
                <h3 style="color: var(--accent-purple); margin-top: 0; margin-bottom: 1rem;">Transit Location</h3>
                <div class="form-group" style="margin-bottom: 12px;">
                    <label for="gocharDate" style="display:block; margin-bottom:4px; font-weight:600; color:var(--text-color); font-size: 0.85rem;">Date (तारीख)</label>
                    <input type="date" id="gocharDate" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); font-size: 0.85rem;">
                </div>
                <div class="form-group" style="margin-bottom: 12px;">
                    <label for="gocharTime" style="display:block; margin-bottom:4px; font-weight:600; color:var(--text-color); font-size: 0.85rem;">Time (समय)</label>
                    <input type="time" id="gocharTime" value="12:00" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); font-size: 0.85rem;">
                </div>
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="gocharPlace" style="display:block; margin-bottom:4px; font-weight:600; color:var(--text-color); font-size: 0.85rem;">Place (स्थान)</label>
                    <input type="text" id="gocharPlace" value="New Delhi, India" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); font-size: 0.85rem;">
                </div>
                <button class="btn-submit" id="btnGochar" style="width:100%; padding:10px; font-size:0.9rem; font-weight:700; border-radius:6px;">🪐 Cast Transits</button>
            </div>

            <!-- Transit Outputs -->
            <div class="glass-card" id="gocharOutputCard" style="display: none; flex: 2; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 20px; box-shadow: var(--shadow);">
                <h3 style="color: var(--title-color); margin-top: 0; border-bottom: 1.5px solid rgba(255,255,255,0.06); padding-bottom: 8px;">Real-time Graha Gochar</h3>
                
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div style="flex: 1.2; min-width: 280px; text-align: center;">
                        <h4 style="color: var(--accent-color); margin-bottom: 10px;">Transit Map (D1)</h4>
                        <div id="gocharLagnaChartContainer" style="display: inline-block; border-radius: 8px; overflow: hidden; background: rgba(0,0,0,0.12); padding: 5px;"></div>
                    </div>
                    <div style="flex: 1.8; min-width: 300px;">
                        <h4 style="color: var(--accent-color); margin-bottom: 10px;">Transiting Planetary Positions</h4>
                        <div style="overflow-x: auto; background: rgba(0,0,0,0.1); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; max-height: 380px; overflow-y: auto;">
                            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.8rem;">
                                <thead>
                                    <tr style="border-bottom: 1.5px solid var(--border-color); color: var(--accent-color);">
                                        <th style="padding: 6px;">Planet</th>
                                        <th style="padding: 6px;">Sign</th>
                                        <th style="padding: 6px;">Longitude</th>
                                        <th style="padding: 6px;">Nakshatra</th>
                                        <th style="padding: 6px;">Pada</th>
                                    </tr>
                                </thead>
                                <tbody id="gocharPlanets"></tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <div style="margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px;">
                    <h4 style="color: var(--accent-color); margin-bottom: 10px;">Transit Panchanga</h4>
                    <div id="gocharPanchangBody" style="font-size: 0.85rem; line-height: 1.6; color: var(--text-color); display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;"></div>
                </div>
            </div>
        </div>
    </div>
</div>`;
}
