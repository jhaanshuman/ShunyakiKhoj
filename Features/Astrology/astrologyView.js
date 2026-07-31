/**
 * Dynamic View Builder for Astrology Suite
 */
function renderAstrologyView() {
    return `<div class="container astrology-container" style="width: 80% !important; max-width: 1400px !important; margin: 0 auto !important;">
    <div id="breadcrumbs" class="breadcrumbs-container"></div>

    <!-- Floating Left Toggle Button for Custom Kundali Settings -->
    <button id="btnCustomKundaliToggle" onclick="if(typeof window.toggleSettingsSidebar==='function'){window.toggleSettingsSidebar(true);}" onmouseenter="if(typeof window.toggleSettingsSidebar==='function'){window.toggleSettingsSidebar(true);}" style="position: fixed; top: 85px; left: 0; z-index: 9990; background: linear-gradient(135deg, #a23922 0%, #7c1a08 100%); color: #ffffff; border: 1px solid #f59e0b; border-left: none; border-radius: 0 8px 8px 0; padding: 8px 14px; font-weight: 800; font-size: 0.82rem; cursor: pointer; box-shadow: 4px 0 15px rgba(0,0,0,0.4); display: flex; align-items: center; gap: 6px; transition: all 0.2s;">⚙️ &gt; Custom Kundali</button>

    <!-- Left Collapsible Settings Sidebar (Slides out to the right on click/hover, collapses on mouseleave) -->
    <div id="astrologySettingsSidebar" class="settings-sidebar" onmouseleave="if(typeof window.toggleSettingsSidebar==='function'){window.toggleSettingsSidebar(false);}" style="position: fixed; top: 70px; left: -320px; width: 300px; height: calc(100vh - 70px); background: rgba(15,23,42,0.97); backdrop-filter: blur(10px); border-right: 2px solid #a23922; z-index: 9995; padding: 20px; box-shadow: 8px 0 25px rgba(0,0,0,0.6); transition: left 0.35s cubic-bezier(0.4, 0, 0.2, 1); overflow-y: auto; color: #f8fafc; box-sizing: border-box;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #334155; padding-bottom: 10px;">
            <span style="font-weight: 800; color: #fbbf24; font-size: 0.95rem;">⚙️ Custom Settings</span>
            <button onclick="if(typeof window.toggleBirthModal==='function'){window.toggleBirthModal(true);}" title="Edit Birth Details" style="background: #334155; border: 1.5px solid #f59e0b; color: #fbbf24; padding: 5px 10px; border-radius: 6px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 5px; font-size: 0.8rem;">✏️ Edit Details</button>
        </div>
        
        <div style="display: flex; flex-direction: column; gap: 12px;">
            <div style="display:flex; flex-direction:column;">
                <label style="font-weight:600; color:#cbd5e1; margin-bottom:4px; font-size:0.8rem;">Chart Style</label>
                <select id="selChartStyle" style="padding:8px; background:#1e293b; color:#f8fafc; border:1px solid #475569; border-radius:6px; font-size:0.82rem;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                    <option value="North" selected>North Indian (Lagna)</option>
                    <option value="South">South Indian</option>
                </select>
            </div>
            <div style="display:flex; flex-direction:column;">
                <label style="font-weight:600; color:#cbd5e1; margin-bottom:4px; font-size:0.8rem;">Ayanamsa</label>
                <select id="selAyanamsa" style="padding:8px; background:#1e293b; color:#f8fafc; border:1px solid #475569; border-radius:6px; font-size:0.82rem;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                    <option value="Lahiri" selected>Lahiri (Chitra Paksha)</option>
                    <option value="Raman">B.V. Raman</option>
                    <option value="KP">Krishnamurti (KP)</option>
                    <option value="Tropical">Tropical (No Ayanamsa)</option>
                    <option value="Fagan">Fagan-Bradley</option>
                    <option value="Pushya">Pushya-paksha</option>
                </select>
            </div>
            <div style="display:flex; flex-direction:column;">
                <label style="font-weight:600; color:#cbd5e1; margin-bottom:4px; font-size:0.8rem;">Rahu/Ketu Node</label>
                <select id="selNode" style="padding:8px; background:#1e293b; color:#f8fafc; border:1px solid #475569; border-radius:6px; font-size:0.82rem;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                    <option value="True" selected>True Node</option>
                    <option value="Mean">Mean Node</option>
                </select>
            </div>
            <div style="display:flex; flex-direction:column;">
                <label style="font-weight:600; color:#cbd5e1; margin-bottom:4px; font-size:0.8rem;">Rashi Numbers</label>
                <select id="selRashiVisibility" style="padding:8px; background:#1e293b; color:#f8fafc; border:1px solid #475569; border-radius:6px; font-size:0.82rem;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                    <option value="Visible" selected>Visible</option>
                    <option value="Hidden">Hidden</option>
                </select>
            </div>
            <div style="display:flex; flex-direction:column;">
                <label style="font-weight:600; color:#cbd5e1; margin-bottom:4px; font-size:0.8rem;">Outer Planets</label>
                <select id="selOuterPlanets" style="padding:8px; background:#1e293b; color:#f8fafc; border:1px solid #475569; border-radius:6px; font-size:0.82rem;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                    <option value="Hidden" selected>Hidden</option>
                    <option value="Visible">Visible</option>
                </select>
            </div>
            <div style="display:flex; flex-direction:column;">
                <label style="font-weight:600; color:#cbd5e1; margin-bottom:4px; font-size:0.8rem;">Terminology</label>
                <select id="selTerminology" style="padding:8px; background:#1e293b; color:#f8fafc; border:1px solid #475569; border-radius:6px; font-size:0.82rem;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                    <option value="Vedic" selected>Vedic (Guru/Shukra)</option>
                    <option value="Western">Western (Jup/Ven)</option>
                </select>
            </div>
            <div style="display:flex; flex-direction:column;">
                <label style="font-weight:600; color:#cbd5e1; margin-bottom:4px; font-size:0.8rem;">House System</label>
                <select id="selHouseSystem" style="padding:8px; background:#1e293b; color:#f8fafc; border:1px solid #475569; border-radius:6px; font-size:0.82rem;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                    <option value="Whole Sign" selected>Whole Sign</option>
                    <option value="Equal">Equal House</option>
                    <option value="Sripati">Sripati</option>
                    <option value="Bhava Chalit">Bhava Chalit</option>
                    <option value="KP">KP System</option>
                    <option value="Placidus">Placidus</option>
                </select>
            </div>
            <div style="display:flex; flex-direction:column;">
                <label style="font-weight:600; color:#cbd5e1; margin-bottom:4px; font-size:0.8rem;">Longitude Format</label>
                <select id="selLongStyle" style="padding:8px; background:#1e293b; color:#f8fafc; border:1px solid #475569; border-radius:6px; font-size:0.82rem;" onchange="if(typeof triggerAdvancedCalc==='function'){triggerAdvancedCalc();}">
                    <option value="DMS" selected>Deg-Min-Sec</option>
                    <option value="Decimal">Decimal Degrees</option>
                </select>
            </div>
        </div>
    </div>

    <!-- Settings managed exclusively via left collapsible astrologySettingsSidebar -->

    <!-- Center Screen Pop-up Modal for Birth Details -->
    <div id="birthDetailsModal" class="modal-backdrop" onclick="if(event.target===this) if(typeof window.toggleBirthModal==='function') window.toggleBirthModal(false);" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.75); backdrop-filter: blur(6px); z-index: 9999; justify-content: center; align-items: center; padding: 15px; box-sizing: border-box;">
        <div class="birth-details-card" style="flex: 1; max-width: 520px; width: 100%; background: #1e293b; border: 1.5px solid #a23922; border-radius: 12px; padding: 25px; box-sizing: border-box; position: relative; box-shadow: 0 15px 35px rgba(0,0,0,0.6); max-height: 90vh; overflow-y: auto; color: #f8fafc;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; border-bottom: 1px solid #334155; padding-bottom: 10px;">
                <h3 style="color: #fbbf24; margin: 0; font-size: 1.2rem; font-weight: 800;">✏️ Edit Birth Details</h3>
                <button onclick="if(typeof window.toggleBirthModal==='function') window.toggleBirthModal(false);" style="background: transparent; border: none; color: #94a3b8; font-size: 1.4rem; cursor: pointer; font-weight: 700;">✕</button>
            </div>

            <div class="form-group" style="margin-bottom: 15px;">
                <label for="birthName" style="display:block; margin-bottom:6px; font-weight:600; color:#cbd5e1; font-size:0.85rem;">Name (नाम)</label>
                <input type="text" id="birthName" value="Native" style="width:100%; padding:10px; border-radius:6px; background:#0f172a; color:#f8fafc; border:1px solid #475569; font-size:0.9rem;">
            </div>
            <div class="form-group" style="margin-bottom: 15px;">
                <label for="birthDate" style="display:block; margin-bottom:6px; font-weight:600; color:#cbd5e1; font-size:0.85rem;">Date of Birth (जन्म तिथि)</label>
                <input type="date" id="birthDate" value="1994-01-05" style="width:100%; padding:10px; border-radius:6px; background:#0f172a; color:#f8fafc; border:1px solid #475569; font-size:0.9rem;">
            </div>
            <div class="form-group" style="margin-bottom: 15px;">
                <label for="birthTime" style="display:block; margin-bottom:6px; font-weight:600; color:#cbd5e1; font-size:0.85rem;">Time of Birth (जन्म समय)</label>
                <input type="time" id="birthTime" value="20:00" style="width:100%; padding:10px; border-radius:6px; background:#0f172a; color:#f8fafc; border:1px solid #475569; font-size:0.9rem;">
            </div>
            <div class="form-group" style="margin-bottom: 15px;">
                <label for="birthPlace" style="display:block; margin-bottom:6px; font-weight:600; color:#cbd5e1; font-size:0.85rem;">Place of Birth (जन्म स्थान)</label>
                <input type="text" id="birthPlace" value="Patna, Bihar, India" style="width:100%; padding:10px; border-radius:6px; background:#0f172a; color:#f8fafc; border:1px solid #475569; font-size:0.9rem;">
                <a href="javascript:void(0)" onclick="toggleBirthMap()" style="font-size:0.8rem; color:#fbbf24; text-decoration:none; margin-top: 5px; display:inline-block;">🗺️ Pinpoint on Map for Coordinates</a>
                <div id="birthMap" style="height: 180px; margin-top: 10px; border-radius: 8px; border: 1px solid #475569; display: none;"></div>
            </div>
            
            <div class="form-row" style="display:flex; gap:10px; margin-bottom:20px;">
                <div class="form-group" style="flex:1;">
                    <label for="birthLat" style="display:block; margin-bottom:4px; font-size:0.8rem; color:#94a3b8;">Latitude</label>
                    <input type="number" step="any" id="birthLat" value="25.5941" style="width:100%; padding:8px; border-radius:6px; background:#0f172a; color:#f8fafc; border:1px solid #475569;">
                </div>
                <div class="form-group" style="flex:1;">
                    <label for="birthLon" style="display:block; margin-bottom:4px; font-size:0.8rem; color:#94a3b8;">Longitude</label>
                    <input type="number" step="any" id="birthLon" value="85.1376" style="width:100%; padding:8px; border-radius:6px; background:#0f172a; color:#f8fafc; border:1px solid #475569;">
                </div>
            </div>
            
            <button class="btn-submit" id="btnCalculate" onclick="if(typeof window.handleKundliCalculation==='function'){window.handleKundliCalculation(event);}" style="width:100%; padding:12px; font-size:1rem; font-weight:700; border-radius:8px; cursor:pointer; background:linear-gradient(135deg, #a23922 0%, #7c1a08 100%); color:#fff; border:1px solid #f59e0b;">🔮 Generate Kundali</button>
            
            <div id="extraSidebarDetails" style="display:none; margin-top:20px; border-top:1px solid rgba(255,255,255,0.08); padding-top:15px;">
                <button class="btn-submit" id="btnShowRawData" onclick="toggleRawPayloadModal()" style="width:100%; padding:10px; font-size:0.85rem; font-weight:700; border-radius:8px; cursor:pointer; margin-bottom:10px;">📋 Show Raw JSON Data</button>
                <div id="rawPayloadBox" style="display:none; max-height:200px; overflow-y:auto; background:#0d1117; padding:10px; border-radius:6px; font-family:monospace; font-size:0.75rem; border:1px solid var(--border-color); color:#4ade80;"></div>
            </div>
        </div>
    </div>

    <!-- Hidden Top Nav Tabs (Section navigation buttons removed as requested) -->
    <div class="top-nav-tabs" style="display: none !important;">
    </div>

    <!-- 1. Personalized Kundli Section -->
    <div id="personalKundliSection" class="main-section active">
        <div class="dashboard-grid" style="display: flex; gap: 20px; align-items: start; box-sizing: border-box; width: 100%;">

            <!-- Status Header Card (Shown during calculation progress) -->
            <div class="glass-card status-header-card" id="statusHeaderCard" style="display: none; flex: 1; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 40px; text-align: center; box-shadow: var(--shadow); box-sizing: border-box; flex-direction: column; align-items: center; justify-content: center; min-height: 400px;">
                <div style="font-size: 2.8rem; margin-bottom: 20px; animation: pulse 1.8s ease-in-out infinite;">🔮</div>
                <h3 style="color: var(--accent-color); margin-top: 0; margin-bottom: 12px; font-size: 1.5rem; font-weight: 800;">Casting Celestial Map</h3>
                <p id="statusMessage" style="color: var(--text-color); font-size: 1.05rem; margin-bottom: 25px; min-height: 24px; font-weight: 600;">Calculating your birth details...</p>
                <div class="progress-bar-container" style="width: 100%; max-width: 400px; height: 8px; background: rgba(255,255,255,0.08); border-radius: 4px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1);">
                    <div id="statusProgressBar" style="width: 0%; height: 100%; background: linear-gradient(90deg, #ea580c, #fbbf24); transition: width 0.1s linear; border-radius: 4px;"></div>
                </div>
            </div>

            <!-- Output Display Container (Scrollable & High Contrast Dark Theme) -->
            <div class="glass-card" id="outputCard" style="display: flex; flex: 1; min-width: 0; background: #0f172a; border: 1px solid rgba(255,255,255,0.15); border-radius: 12px; padding: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); flex-direction: column; max-height: 82vh; overflow-y: auto; color: #f8fafc;">
                
                <!-- Mobile Report Selector (Visible on Mobile only) -->
                <div class="mobile-report-selector-container" style="margin-bottom: 15px; display: none; width: 100%;">
                    <label for="mobileReportSelector" style="font-weight: 700; color: #fbbf24; font-size: 0.9rem; display: block; margin-bottom: 6px;">Select Astrological Report:</label>
                    <select id="mobileReportSelector" style="width: 100%; padding: 10px; background: #1e293b; color: #f8fafc; border: 1.5px solid #475569; border-radius: 6px; font-weight: 600; max-height: 300px; overflow-y: auto;" onchange="switchReportTab(this.value)">
                        <option value="tabD1">D1 - Rashi Chart (Lagna)</option>
                        <option value="tabD2">D2 - Hora Chart (Wealth)</option>
                        <option value="tabD3">D3 - Drekkana (Siblings)</option>
                        <option value="tabD4">D4 - Chaturthamsa (Assets)</option>
                        <option value="tabD5">D5 - Panchamsa (Fame &amp; Power)</option>
                        <option value="tabD6">D6 - Shasthamsa (Health &amp; Obstacles)</option>
                        <option value="tabD7">D7 - Saptamsa (Children)</option>
                        <option value="tabD8">D8 - Ashtamsa (Longevity)</option>
                        <option value="tabD9">D9 - Navamsa Chart (Spouse &amp; Karma)</option>
                        <option value="tabD10">D10 - Dasamsa (Career &amp; Power)</option>
                        <option value="tabD11">D11 - Rudramsa (Gains &amp; Victory)</option>
                        <option value="tabD12">D12 - Dwadasamsa (Parents)</option>
                        <option value="tabD16">D16 - Shodasamsa (Vehicles &amp; Comforts)</option>
                        <option value="tabD20">D20 - Vimsamsa (Spiritual Practice)</option>
                        <option value="tabD24">D24 - Chaturvimsamsa (Education &amp; Learning)</option>
                        <option value="tabD27">D27 - Saptavimsamsa (Stamina &amp; Strengths)</option>
                        <option value="tabD30">D30 - Trimsamsa (Mishaps &amp; Evils)</option>
                        <option value="tabD40">D40 - Khavedamsa (Auspiciousness)</option>
                        <option value="tabD45">D45 - Akshavedamsa (Character)</option>
                        <option value="tabD60">D60 - Shastiamsa (Past Karma)</option>
                        <option value="tabD81">D81 - Navanavamsa (Micro Karma Root)</option>
                        <option value="tabD108">D108 - Ashtottaramsa (Divine Root)</option>
                        <option value="tabD144">D144 - Dwadasadvadasamsa (Ultimate Matrix)</option>
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

                <!-- Dropdown Category Selector (Replaces Scrolling Button Bar) -->
                <div class="report-category-selector-wrapper" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 15px; border-bottom: 2px solid #334155; padding-bottom: 12px; width: 100%;">
                    <label for="selReportCategory" style="font-size: 0.9rem; font-weight: 800; color: #fbbf24; white-space: nowrap;">📊 Astrological Category:</label>
                    <select id="selReportCategory" onchange="switchReportCategory(this.value)" style="flex: 1; max-width: 480px; background: #1e293b; color: #f8fafc; border: 1.5px solid #a23922; border-radius: 8px; padding: 8px 14px; font-size: 0.9rem; font-weight: 700; cursor: pointer; outline: none; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                        <option value="charts">🗺️ Divisional Charts (D1 - D144)</option>
                        <option value="dasha">⏳ Dasha Cycles (19 Systems)</option>
                        <option value="strength">⚖️ Strengths &amp; Dignity</option>
                        <option value="aspects">👁️ Aspects &amp; Conjunctions</option>
                        <option value="ashtakavarga">📊 Ashtakavarga Matrix</option>
                        <option value="panchanga">🕉️ Panchanga &amp; Astronomy</option>
                        <option value="yogas">🧘 Yogas &amp; Doshas</option>
                        <option value="jaimini_kp">🎯 Jaimini &amp; KP Systems</option>
                        <option value="domains">🔮 27 Life Domains</option>
                        <option value="ai_workspace">🤖 AI Intelligence Workspace</option>
                        <option value="graphs_tables">📈 Graphs &amp; Tables</option>
                        <option value="developer_tools">🛠️ Developer Audit</option>
                    </select>
                </div>

                <!-- 1. Divisional Charts Sub-Group: Searchable Selector & Side Panel -->
                <div id="subTabs-charts" class="sub-tabs-group" style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px; background: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #334155;">
                    <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                        <label for="selDivisionalChart" style="font-weight: 700; color: #fbbf24; font-size: 0.88rem;">Select Divisional Chart (D1 to D144):</label>
                        <select id="selDivisionalChart" style="flex: 1; min-width: 250px; padding: 8px 12px; background: #0f172a; color: #f8fafc; border: 1px solid #475569; border-radius: 6px; font-size: 0.85rem; font-weight: 700; max-height: 300px; overflow-y: auto;" onchange="switchReportTab(this.value)">
                            <option value="tabD1" selected>D1 - Rashi Chart (Lagna &amp; General Destiny)</option>
                            <option value="tabD2">D2 - Hora Chart (Wealth, Treasury &amp; Financial Assets)</option>
                            <option value="tabD3">D3 - Drekkana (Siblings, Courage &amp; Energy)</option>
                            <option value="tabD4">D4 - Chaturthamsa (Properties, Assets &amp; Luck)</option>
                            <option value="tabD5">D5 - Panchamsa (Power, Fame &amp; Intellect)</option>
                            <option value="tabD6">D6 - Shasthamsa (Health, Debts &amp; Obstacles)</option>
                            <option value="tabD7">D7 - Saptamsa (Progeny, Children &amp; Successors)</option>
                            <option value="tabD8">D8 - Ashtamsa (Longevity, Sudden Events &amp; Transformation)</option>
                            <option value="tabD9">D9 - Navamsa (Spouse, Dharma &amp; Micro Destiny)</option>
                            <option value="tabD10">D10 - Dasamsa (Career, Profession &amp; Public Renown)</option>
                            <option value="tabD11">D11 - Rudramsa (Gains, Victory &amp; Windfalls)</option>
                            <option value="tabD12">D12 - Dwadasamsa (Parents &amp; Ancestral Lineage)</option>
                            <option value="tabD16">D16 - Shodasamsa (Vehicles, Comforts &amp; Happiness)</option>
                            <option value="tabD20">D20 - Vimsamsa (Spiritual Devotion &amp; Sadhana)</option>
                            <option value="tabD24">D24 - Chaturvimsamsa (Higher Learning &amp; Wisdom)</option>
                            <option value="tabD27">D27 - Saptavimsamsa (Physical Strengths &amp; Stamina)</option>
                            <option value="tabD30">D30 - Trimsamsa (Evils, Misfortunes &amp; Karmic Liabilities)</option>
                            <option value="tabD40">D40 - Khavedamsa (Maternal Lineage &amp; Auspiciousness)</option>
                            <option value="tabD45">D45 - Akshavedamsa (Character Purity &amp; Integrity)</option>
                            <option value="tabD60">D60 - Shastiamsa (Past Life Karma &amp; Root Destiny)</option>
                            <option value="tabD81">D81 - Navanavamsa (Micro Karma Roots)</option>
                            <option value="tabD108">D108 - Ashtottaramsa (Divine Blessing Matrix)</option>
                            <option value="tabD144">D144 - Dwadasadvadasamsa (Ultimate Cosmic Matrix)</option>
                        </select>
                    </div>
                </div>

                <!-- 2. Scalable Dasha Selector Sub-Group (All 19 Dashas) -->
                <div id="subTabs-dasha" class="sub-tabs-group" style="display: none; flex-direction: column; gap: 12px; margin-bottom: 20px; background: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #334155;">
                    <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                        <label for="selDashaSystem" style="font-weight: 700; color: #fbbf24; font-size: 0.88rem;">Select Planetary Dasha System (19 Systems):</label>
                        <select id="selDashaSystem" style="flex: 1; min-width: 250px; padding: 8px 12px; background: #0f172a; color: #f8fafc; border: 1px solid #475569; border-radius: 6px; font-size: 0.85rem; font-weight: 700; max-height: 300px; overflow-y: auto;" onchange="switchReportTab(this.value)">
                            <option value="tabVimshottari" selected>Vimshottari Dasha (120 Years - Universal)</option>
                            <option value="tabYogini">Yogini Dasha (36 Years - Nakshatra Cycle)</option>
                            <option value="tabAshtottari">Ashtottari Dasha (108 Years - Non-Rahu)</option>
                            <option value="tabKalachakra">Kalachakra Dasha (Wheel of Time)</option>
                            <option value="tabChara">Jaimini Chara Dasha (Sign Based)</option>
                            <option value="tabSthira">Sthira Dasha (Fixed Sign Cycle)</option>
                            <option value="tabNarayana">Narayana Dasha (Padakrama Progression)</option>
                            <option value="tabShoola">Shoola Dasha (Trik House Hazard Cycle)</option>
                            <option value="tabMandooka">Mandooka Dasha (Frog Leap Sign Cycle)</option>
                            <option value="tabPanchottari">Panchottari Dasha (105 Years - Anuradha)</option>
                            <option value="tabDwadashottari">Dwadashottari Dasha (112 Years - Sun Lagna)</option>
                            <option value="tabShatabdika">Shatabdika Dasha (100 Years - Vargottama)</option>
                            <option value="tabChaturashitiSama">Chaturashiti-sama Dasha (84 Years - 10th Lord)</option>
                            <option value="tabDwisaptatiSama">Dwisaptati-sama Dasha (72 Years - Lagna Lord 7th)</option>
                            <option value="tabShodashottari">Shodashottari Dasha (116 Years - Krishna Paksha)</option>
                            <option value="tabTara">Tara Dasha (Nakshatra Tara Cycle)</option>
                            <option value="tabNaisargika">Naisargika Dasha (Natural Age Maturation)</option>
                            <option value="tabLagnaKendradi">Lagna Kendradi Dasha (Kendra Progression)</option>
                            <option value="tabSudarshanaChakra">Sudarshana Chakra Dasha (Tri-Lagna Progression)</option>
                        </select>
                    </div>
                </div>

                <!-- 3. Strengths & Dignity Sub-Group -->
                <div id="subTabs-strength" class="sub-tabs-group" style="display: none; gap: 6px; flex-wrap: wrap; margin-bottom: 20px; background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <button class="rep-tab-btn" id="btn-tabShadbala" onclick="switchReportTab('tabShadbala')">Shadbala (6-Fold Strength)</button>
                    <button class="rep-tab-btn" id="btn-tabBhavabala" onclick="switchReportTab('tabBhavabala')">Bhavabala (House Strengths)</button>
                    <button class="rep-tab-btn" id="btn-tabVimsopaka" onclick="switchReportTab('tabVimsopaka')">Vimsopaka Bala (Divisional Dignity)</button>
                    <button class="rep-tab-btn" id="btn-tabDignityAvasthas" onclick="switchReportTab('tabDignityAvasthas')">Dignity &amp; Avasthas</button>
                    <button class="rep-tab-btn" id="btn-tabPlanetRanking" onclick="switchReportTab('tabPlanetRanking')">Planet Ranking &amp; Power</button>
                    <button class="rep-tab-btn" id="btn-tabCombustionWar" onclick="switchReportTab('tabCombustionWar')">Combustion &amp; Graha Yuddha</button>
                    <button class="rep-tab-btn" id="btn-tabFriendships" onclick="switchReportTab('tabFriendships')">Panchadha Sambandha Matrix</button>
                </div>

                <!-- 4. Aspects & Conjunctions Sub-Group -->
                <div id="subTabs-aspects" class="sub-tabs-group" style="display: none; gap: 6px; flex-wrap: wrap; margin-bottom: 20px; background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <button class="rep-tab-btn active" id="btn-tabAspects" onclick="switchReportTab('tabAspects')">Planetary Aspects (Graha Drishti)</button>
                    <button class="rep-tab-btn" id="btn-tabHouseAspects" onclick="switchReportTab('tabHouseAspects')">House Aspects</button>
                    <button class="rep-tab-btn" id="btn-tabRashiDrishti" onclick="switchReportTab('tabRashiDrishti')">Rashi Drishti (Jaimini)</button>
                    <button class="rep-tab-btn" id="btn-tabConjunctions" onclick="switchReportTab('tabConjunctions')">Conjunctions &amp; Stelliums</button>
                </div>

                <!-- 5. Ashtakavarga Sub-Group -->
                <div id="subTabs-ashtakavarga" class="sub-tabs-group" style="display: none; gap: 6px; flex-wrap: wrap; margin-bottom: 20px; background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <button class="rep-tab-btn active" id="btn-tabSAV" onclick="switchReportTab('tabSAV')">SAV Matrix (Sarvashtakavarga)</button>
                    <button class="rep-tab-btn" id="btn-tabBAVGrids" onclick="switchReportTab('tabBAVGrids')">BAV Grids (Individual Planets)</button>
                    <button class="rep-tab-btn" id="btn-tabAshtakavargaReductions" onclick="switchReportTab('tabAshtakavargaReductions')">Trikona &amp; Ekadhipatya Shodhana</button>
                    <button class="rep-tab-btn" id="btn-tabPindaSadhana" onclick="switchReportTab('tabPindaSadhana')">Pinda Sadhana (Shodhaya Pinda)</button>
                </div>

                <!-- 6. Panchanga & Astronomy Sub-Group -->
                <div id="subTabs-panchanga" class="sub-tabs-group" style="display: none; gap: 6px; flex-wrap: wrap; margin-bottom: 20px; background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <button class="rep-tab-btn active" id="btn-tabPanchanga" onclick="switchReportTab('tabPanchanga')">Birth Panchanga Limbs</button>
                    <button class="rep-tab-btn" id="btn-tabAstronomyDetail" onclick="switchReportTab('tabAstronomyDetail')">Astronomical Data &amp; Obliquity</button>
                    <button class="rep-tab-btn" id="btn-tabTransitOverlay" onclick="switchReportTab('tabTransitOverlay')">Transit Overlay &amp; Sade Sati</button>
                </div>

                <!-- 7. Yogas & Doshas Sub-Group -->
                <div id="subTabs-yogas" class="sub-tabs-group" style="display: none; gap: 6px; flex-wrap: wrap; margin-bottom: 20px; background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <button class="rep-tab-btn active" id="btn-tabYogas" onclick="switchReportTab('tabYogas')">Categorized Yogas (300+)</button>
                    <button class="rep-tab-btn" id="btn-tabDoshas" onclick="switchReportTab('tabDoshas')">Dosha Analysis &amp; Cancellations</button>
                    <button class="rep-tab-btn" id="btn-tabGemstones" onclick="switchReportTab('tabGemstones')">Gemstone &amp; Rudraksha Remedies</button>
                </div>

                <!-- 8. Jaimini & KP Paddhati Sub-Group -->
                <div id="subTabs-jaimini_kp" class="sub-tabs-group" style="display: none; gap: 6px; flex-wrap: wrap; margin-bottom: 20px; background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <button class="rep-tab-btn active" id="btn-tabJaimini" onclick="switchReportTab('tabJaimini')">Jaimini Karakas (7/8 Scheme)</button>
                    <button class="rep-tab-btn" id="btn-tabSpecialLagnas" onclick="switchReportTab('tabSpecialLagnas')">Special Lagnas &amp; Arudhas</button>
                    <button class="rep-tab-btn" id="btn-tabUpagrahas" onclick="switchReportTab('tabUpagrahas')">Upagrahas &amp; Gulika</button>
                    <button class="rep-tab-btn" id="btn-tabKPSystem" onclick="switchReportTab('tabKPSystem')">KP System (Cusps &amp; Significators)</button>
                </div>

                <!-- 9. 27 Life Domains & Predictions Sub-Group -->
                <div id="subTabs-domains" class="sub-tabs-group" style="display: none; gap: 6px; flex-wrap: wrap; margin-bottom: 20px; background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <button class="rep-tab-btn active" id="btn-tabLifeDomains" onclick="switchReportTab('tabLifeDomains')">27 Life Domains Explorer</button>
                    <button class="rep-tab-btn" id="btn-tabEventIndicators" onclick="switchReportTab('tabEventIndicators')">Event Indicators &amp; Timing</button>
                    <button class="rep-tab-btn" id="btn-tabPredictionIndex" onclick="switchReportTab('tabPredictionIndex')">Prediction Index Summary</button>
                </div>

                <!-- 10. AI Intelligence Workspace Sub-Group -->
                <div id="subTabs-ai_workspace" class="sub-tabs-group" style="display: none; gap: 6px; flex-wrap: wrap; margin-bottom: 20px; background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <button class="rep-tab-btn active" id="btn-tabAIExecutive" onclick="switchReportTab('tabAIExecutive')">AI Executive Summary</button>
                    <button class="rep-tab-btn" id="btn-tabAISWOC" onclick="switchReportTab('tabAISWOC')">SWOC Analysis (Strengths/Weaknesses)</button>
                    <button class="rep-tab-btn" id="btn-tabAIFAQs" onclick="switchReportTab('tabAIFAQs')">AI Guidance FAQs</button>
                </div>

                <!-- 11. Graphs & Tables Sub-Group -->
                <div id="subTabs-graphs_tables" class="sub-tabs-group" style="display: none; gap: 6px; flex-wrap: wrap; margin-bottom: 20px; background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <button class="rep-tab-btn active" id="btn-tabVisualGraphs" onclick="switchReportTab('tabVisualGraphs')">Visual Analytics Graphs</button>
                    <button class="rep-tab-btn" id="btn-tabDataTables" onclick="switchReportTab('tabDataTables')">Structured Data Tables</button>
                </div>

                <!-- 12. Developer Audit Tools Sub-Group -->
                <div id="subTabs-developer_tools" class="sub-tabs-group" style="display: none; gap: 6px; flex-wrap: wrap; margin-bottom: 20px; background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <button class="rep-tab-btn active" id="btn-tabSchemaAudit" onclick="switchReportTab('tabSchemaAudit')">Schema Audit &amp; Engine Metadata</button>
                    <button class="rep-tab-btn" id="btn-tabRuleEngine" onclick="switchReportTab('tabRuleEngine')">Rule Engine Matches</button>
                    <button class="rep-tab-btn" id="btn-tabDataFolder" onclick="switchReportTab('tabDataFolder')">Data/ Folder Datasets</button>
                </div>

                <div class="report-dashboard-layout" style="display: flex; width: 100%; gap: 15px; min-height: 550px;">
                    <!-- Right Display Pane -->
                    <div class="report-content-pane" style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 15px; background: #192333;">
                        <!-- Heading of selected view -->
                        <h3 id="reportTitle" style="color: #fbbf24; margin-top: 0; border-bottom: 2px solid #334155; padding-bottom: 8px; font-weight: 800; font-size: 1.2rem;">D1 - Rashi Chart</h3>
                        
                        <!-- Content injection viewport -->
                        <div id="reportViewport" style="flex: 1; min-height: 480px; overflow-y: auto; background: #192333; padding: 15px; border-radius: 8px; border: 1px solid #334155; color: #f8fafc;"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 2. Graha Gochar Section -->
    <div id="gocharSection" class="main-section" style="display: none;">
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
                <button class="btn-submit" id="btnGochar" onclick="if(typeof calculateGochar==='function'){calculateGochar();}else if(typeof window.calculateGochar==='function'){window.calculateGochar();}" style="width:100%; padding:10px; font-size:0.9rem; font-weight:700; border-radius:6px; cursor:pointer;">🪐 Cast Transits</button>
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
                        <div id="gocharPlanets" style="overflow-x: auto; background: rgba(0,0,0,0.1); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; max-height: 380px; overflow-y: auto;"></div>
                    </div>
                </div>

                <div style="margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px;">
                    <h4 style="color: var(--accent-color); margin-bottom: 10px;">Transit Panchanga</h4>
                    <div id="gocharPanchangBody" style="font-size: 0.85rem; line-height: 1.6; color: var(--text-color); display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px;"></div>
                </div>

                <div style="margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px;">
                    <h4 style="color: var(--accent-color); margin-bottom: 10px;">Transit Choghadiya (Auspicious Muhurtas)</h4>
                    <div style="overflow-x: auto; background: rgba(0,0,0,0.1); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px;">
                        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.8rem; line-height: 1.6;">
                            <thead>
                                <tr style="border-bottom: 1.5px solid var(--border-color); color: var(--accent-color); font-weight: 800;">
                                    <th style="padding: 6px;">Part</th>
                                    <th style="padding: 6px;">Time Range</th>
                                    <th style="padding: 6px;">Choghadiya</th>
                                    <th style="padding: 6px;">Quality</th>
                                </tr>
                            </thead>
                            <tbody id="gocharChoghadiyaBody"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 3. Kundli Milan Section -->
    <div id="milanSection" class="main-section" style="display: none;">
        <div class="dashboard-grid" style="display: flex; gap: 20px; align-items: start; box-sizing: border-box; width: 100%; flex-wrap: wrap;">
            
            <!-- Milan Inputs Form Card -->
            <div class="birth-details-card" style="flex: 1; max-width: 450px; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 25px; box-sizing: border-box;">
                <h3 style="color: var(--accent-purple); margin-top:0; margin-bottom: 1.5rem;">💞 Kundli Milan Matching</h3>
                
                <!-- Groom (Boy) Details -->
                <div style="background: rgba(0,0,0,0.12); padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.05);">
                    <h4 style="margin: 0 0 10px 0; color: var(--accent-color); font-size: 0.95rem;">🤵 Groom (Boy) Details</h4>
                    <div class="form-group" style="margin-bottom: 10px;">
                        <label style="display:block; margin-bottom:4px; font-size:0.78rem; color:var(--text-color);">Date of Birth</label>
                        <input type="date" id="boyDate" value="1994-01-05" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); font-size:0.85rem;">
                    </div>
                    <div class="form-group" style="margin-bottom: 10px;">
                        <label style="display:block; margin-bottom:4px; font-size:0.78rem; color:var(--text-color);">Time of Birth</label>
                        <input type="time" id="boyTime" value="20:00" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); font-size:0.85rem;">
                    </div>
                    <div class="form-group" style="margin-bottom: 5px;">
                        <label style="display:block; margin-bottom:4px; font-size:0.78rem; color:var(--text-color);">Place of Birth</label>
                        <input type="text" id="boyPlace" value="New Delhi, India" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); font-size:0.85rem;">
                    </div>
                </div>

                <!-- Bride (Girl) Details -->
                <div style="background: rgba(0,0,0,0.12); padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05);">
                    <h4 style="margin: 0 0 10px 0; color: var(--accent-color); font-size: 0.95rem;">👰 Bride (Girl) Details</h4>
                    <div class="form-group" style="margin-bottom: 10px;">
                        <label style="display:block; margin-bottom:4px; font-size:0.78rem; color:var(--text-color);">Date of Birth</label>
                        <input type="date" id="girlDate" value="1995-03-10" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); font-size:0.85rem;">
                    </div>
                    <div class="form-group" style="margin-bottom: 10px;">
                        <label style="display:block; margin-bottom:4px; font-size:0.78rem; color:var(--text-color);">Time of Birth</label>
                        <input type="time" id="girlTime" value="08:30" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); font-size:0.85rem;">
                    </div>
                    <div class="form-group" style="margin-bottom: 5px;">
                        <label style="display:block; margin-bottom:4px; font-size:0.78rem; color:var(--text-color);">Place of Birth</label>
                        <input type="text" id="girlPlace" value="New Delhi, India" style="width:100%; padding:8px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); font-size:0.85rem;">
                    </div>
                </div>

                <button class="btn-submit" id="btnMatch" onclick="if(typeof calculateMilan==='function'){calculateMilan();}else if(typeof window.calculateMilan==='function'){window.calculateMilan();}" style="width:100%; padding:12px; font-size:1rem; font-weight:700; border-radius:8px; cursor:pointer;">💞 Calculate Guna Milan</button>
            </div>

            <!-- Milan Outputs Display Card -->
            <div class="glass-card" id="milanOutputCard" style="display: none; flex: 1.5; min-width: 320px; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 25px; box-shadow: var(--shadow);">
                <h3 style="color: var(--title-color); margin-top: 0; border-bottom: 1.5px solid rgba(255,255,255,0.06); padding-bottom: 8px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <span>Guna Milan Report</span>
                    <span id="milanScoreBadge" class="result-badge" style="font-size: 0.95rem; font-weight: 800; padding: 4px 12px; border-radius: 99px;">0 / 36</span>
                </h3>

                <!-- Boy / Girl Nakshatra Rashi Info -->
                <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 20px; flex-wrap: wrap;">
                    <div style="flex: 1; background: rgba(0,0,0,0.15); padding: 12px; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                        <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 4px;">Groom Nakshatra &amp; Rashi</div>
                        <div id="boyResultInfo" style="font-weight: 700; color: #fff; font-size: 0.95rem;">--</div>
                    </div>
                    <div style="flex: 1; background: rgba(0,0,0,0.15); padding: 12px; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                        <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 4px;">Bride Nakshatra &amp; Rashi</div>
                        <div id="girlResultInfo" style="font-weight: 700; color: #fff; font-size: 0.95rem;">--</div>
                    </div>
                </div>

                <div style="overflow-x: auto; background: rgba(0,0,0,0.12); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px;">
                    <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; line-height: 1.6;">
                        <thead>
                            <tr style="border-bottom: 1.5px solid var(--border-color); color: var(--accent-color); font-weight: 800;">
                                <th style="padding: 8px 10px;">Koota (Factor)</th>
                                <th style="padding: 8px 10px;">Max Points</th>
                                <th style="padding: 8px 10px;">Obtained Points</th>
                            </tr>
                        </thead>
                        <tbody id="milanTableBody"></tbody>
                    </table>
                </div>

                <!-- Deep Analysis Container populated dynamically -->
                <div id="milanDeepAnalysisBlock"></div>
            </div>
        </div>
    </div>

    <!-- 4. Prashna Kundali Section -->
    <div id="prashnaSection" class="main-section" style="display: none;">
        <div class="dashboard-grid" style="display: flex; gap: 20px; align-items: start; box-sizing: border-box; width: 100%; flex-wrap: wrap;">
            
            <!-- Prashna Inputs Form Card -->
            <div class="birth-details-card" style="flex: 1; max-width: 450px; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 25px; box-sizing: border-box;">
                <h3 style="color: var(--accent-purple); margin-top:0; margin-bottom: 1.5rem;">🔮 Prashna Kundali (Horary)</h3>
                
                <div class="form-group" style="margin-bottom: 15px;">
                    <label style="display:block; margin-bottom:6px; font-weight:600; color:var(--text-color);">Query Category (प्रश्न श्रेणी)</label>
                    <select id="prashnaCategory" style="width:100%; padding:10px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color); font-weight:700;">
                        <option value="career">💼 Career & Job (नौकरी / व्यवसाय)</option>
                        <option value="marriage">💞 Love & Marriage (प्रेम / विवाह)</option>
                        <option value="health">🏥 Health & Recovery (स्वास्थ्य / रोग)</option>
                        <option value="wealth">💰 Wealth & Property (धन / संपत्ति)</option>
                        <option value="travel">✈️ Travel & Relocation (यात्रा / स्थानांतरण)</option>
                        <option value="general" selected>🔮 General Guidance (सामान्य प्रश्न)</option>
                    </select>
                </div>

                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="prashnaQuestion" style="display:block; margin-bottom:6px; font-weight:600; color:var(--text-color);">Your Question (आपका प्रश्न)</label>
                    <input type="text" id="prashnaQuestion" placeholder="e.g. Will I get a job in next 3 months?" style="width:100%; padding:10px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color);">
                </div>

                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="prashnaDate" style="display:block; margin-bottom:6px; font-weight:600; color:var(--text-color);">Date of Query (प्रश्न तिथि)</label>
                    <input type="date" id="prashnaDate" style="width:100%; padding:10px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color);">
                </div>

                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="prashnaTime" style="display:block; margin-bottom:6px; font-weight:600; color:var(--text-color);">Time of Query (प्रश्न समय)</label>
                    <input type="time" id="prashnaTime" style="width:100%; padding:10px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color);">
                </div>

                <div class="form-group" style="margin-bottom: 20px;">
                    <label for="prashnaPlace" style="display:block; margin-bottom:6px; font-weight:600; color:var(--text-color);">Place of Query (प्रश्न स्थान)</label>
                    <input type="text" id="prashnaPlace" value="New Delhi, India" style="width:100%; padding:10px; border-radius:6px; background:var(--tile-bg); color:var(--text-color); border:1px solid var(--border-color);">
                </div>

                <button class="btn-submit" id="btnPrashna" onclick="if(typeof calculatePrashna==='function'){calculatePrashna();}else if(typeof window.calculatePrashna==='function'){window.calculatePrashna();}" style="width:100%; padding:12px; font-size:1rem; font-weight:700; border-radius:8px; cursor:pointer;">🔮 Cast Prashna Chart</button>
            </div>

            <!-- Prashna Outputs Display Card -->
            <div class="glass-card" id="prashnaOutputCard" style="display: none; flex: 1.5; min-width: 320px; background: var(--card-bg); border: var(--card-border); border-radius: 12px; padding: 25px; box-shadow: var(--shadow);">
                <h3 style="color: var(--title-color); margin-top: 0; border-bottom: 1.5px solid rgba(255,255,255,0.06); padding-bottom: 8px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <span>Horary (Prashna) Report</span>
                    <span id="prashnaVerdictBadge" class="result-badge success" style="font-size: 0.95rem; font-weight: 800; padding: 4px 12px; border-radius: 99px;">Auspicious</span>
                </h3>

                <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; border-bottom: 1px solid rgba(0,0,0,0.08); padding-bottom: 15px;">
                    <div style="flex: 1; min-width: 200px; text-align: center;">
                        <h4 style="color: var(--accent-color); margin: 0 0 10px 0;">Prashna Lagna (D1)</h4>
                        <div id="prashnaChartContainer" style="display: inline-block; border-radius: 8px; overflow: hidden; background: rgba(0,0,0,0.05); padding: 5px;"></div>
                    </div>
                    <div style="flex: 1.2; min-width: 240px;">
                        <h4 style="color: var(--accent-color); margin: 0 0 10px 0;">Query Moment Panchang</h4>
                        <div id="prashnaPanchang" style="font-size: 0.82rem; line-height: 1.6; color: var(--text-color);"></div>
                    </div>
                </div>

                <div style="margin-top: 15px; border-bottom: 1px solid rgba(0,0,0,0.08); padding-bottom: 15px;">
                    <h4 style="color: var(--accent-color); margin: 0 0 10px 0;">Planetary Placements</h4>
                    <div style="overflow-x: auto; background: rgba(0,0,0,0.03); border: 1px solid var(--border-color); border-radius: 8px; padding: 8px;">
                        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.8rem; line-height: 1.5;">
                            <thead>
                                <tr style="border-bottom: 1.5px solid var(--border-color); color: var(--accent-color); font-weight: 800;">
                                    <th style="padding: 6px;">Planet</th>
                                    <th style="padding: 6px;">Rashi</th>
                                    <th style="padding: 6px;">Longitude</th>
                                    <th style="padding: 6px;">Nakshatra</th>
                                    <th style="padding: 6px;">House</th>
                                </tr>
                            </thead>
                            <tbody id="prashnaPlanetsBody"></tbody>
                        </table>
                    </div>
                </div>

                <!-- Extensive Horary Analysis Panel -->
                <div id="prashnaAnalysisBlock" style="margin-top: 15px;"></div>
            </div>

        </div>
    </div>
</div>`;
}
