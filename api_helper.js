/**
 * api_helper.js
 * Handles the API Diagnostic & Live Validation System
 * Highlights Sun's Position (Longitude, Latitude) and outputs full API payload.
 */

(function (global) {
    'use strict';

    function initApiHelper() {
        const btnOpenApiTest = document.getElementById('btnOpenApiTest');
        const apiTestPanel = document.getElementById('apiTestPanel');
        
        if (btnOpenApiTest && apiTestPanel) {
            btnOpenApiTest.addEventListener('click', () => {
                const isHidden = apiTestPanel.style.display === 'none' || !apiTestPanel.style.display;
                apiTestPanel.style.display = isHidden ? 'block' : 'none';
                
                // Initialize Geocomplete for test place input if not already done
                const apiTestPlace = document.getElementById('apiTestPlace');
                if (isHidden && apiTestPlace && !apiTestPlace.dataset.gcBound) {
                    apiTestPlace.dataset.gcBound = "true";
                    if (typeof initGeoComplete === 'function') {
                        initGeoComplete('apiTestPlace', { defaultPlace: 'New Delhi, India' });
                    }
                }
            });
        }

        const btnRunApiTest = document.getElementById('btnRunApiTest');
        if (btnRunApiTest) {
            btnRunApiTest.addEventListener('click', async () => {
                const testDate = document.getElementById('apiTestDate').value;
                const testPlace = document.getElementById('apiTestPlace').value;
                const output = document.getElementById('apiTestOutput');

                if (!testDate || !testPlace) {
                    alert("Please select Date and Place for API test.");
                    return;
                }

                output.innerHTML = `
                    <div style="display:flex; align-items:center; gap:10px; color:#818cf8; font-weight:bold; font-size:0.9rem;">
                        <span class="gc-spinner-dot"></span>
                        <span>Connecting to backend API & calculating ephemeris...</span>
                    </div>
                `;

                // URL resolution
                const apiUrl = (window.location.hostname.includes('github.io') || window.location.protocol.startsWith('file'))
                    ? 'https://sanskritai.vercel.app/api/calculate'
                    : '/api/calculate';

                try {
                    const res = await fetch(apiUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            date: testDate.replace(/-/g, '/'),
                            time: '12:00',
                            place: testPlace
                        })
                    });

                    const resJson = await res.json();

                    if (resJson.status === 'success') {
                        // Extract Sun Latitude / Longitude
                        const sunData = resJson.d1_chart && resJson.d1_chart.Sun ? resJson.d1_chart.Sun : null;
                        const lat = resJson.panchang ? resJson.panchang.latitude : null;
                        const lon = resJson.panchang ? resJson.panchang.longitude : null;
                        
                        let headerHTML = `
                            <div style="background:rgba(251,191,36,0.06); border:1.5px solid #fbbf24; border-radius:8px; padding:12px 15px; margin-bottom:15px;">
                                <h5 style="color:#fbbf24; margin:0 0 8px 0; font-size:0.95rem; font-weight:800; display:flex; align-items:center; gap:6px;">☀️ Sun & Observer Coordinates</h5>
                                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:10px; font-size:0.82rem; font-weight:700;">
                                    <div>🌅 Observer Latitude: <span style="color:#34d399;">${lat !== null ? lat : 'N/A'}</span></div>
                                    <div>🌐 Observer Longitude: <span style="color:#34d399;">${lon !== null ? lon : 'N/A'}</span></div>
                                    <div>♌ Sun Sign Placement: <span style="color:#38bdf8;">${sunData ? sunData.sign : 'N/A'}</span></div>
                                    <div>📐 Sun Longitude: <span style="color:#38bdf8;">${sunData ? sunData.lon : 'N/A'}°</span></div>
                                </div>
                            </div>
                        `;

                        let html = headerHTML;
                        html += `<table style="width:100%; border-collapse:collapse; color:#fff; font-family:monospace; font-size:0.85rem;">`;
                        html += `<tr style="border-bottom:1.5px solid rgba(255,255,255,0.1); color:#fbbf24; font-weight:700;"><td style="padding:6px;">Returned Key/Variable</td><td style="padding:6px;">Calculated Value</td></tr>`;

                        function printJson(obj, prefix = "") {
                            for (let k in obj) {
                                if (typeof obj[k] === 'object' && obj[k] !== null) {
                                    printJson(obj[k], prefix + k + ".");
                                } else {
                                    let valColor = "#cbd5e1";
                                    if (typeof obj[k] === 'number') valColor = "#34d399";
                                    if (typeof obj[k] === 'boolean') valColor = "#fb7185";
                                    html += `<tr><td style="color:#93c5fd; padding: 4px; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight:bold;">${prefix}${k}</td><td style="padding: 4px; color:${valColor}; border-bottom: 1px solid rgba(255,255,255,0.05);">${obj[k]}</td></tr>`;
                                }
                            }
                        }

                        printJson(resJson);
                        html += `</table>`;
                        output.innerHTML = html;
                    } else {
                        output.innerHTML = `<span style="color:#f87171; font-weight:bold;">Calculation error: ${resJson.detail || 'Unknown error'}</span>`;
                    }
                } catch (err) {
                    console.error(err);
                    output.innerHTML = `<span style="color:#f87171; font-weight:bold;">Failed to connect to API server. Check your connection or console logs.</span>`;
                }
            });
        }
    }

    // Export to global scope
    global.initApiHelper = initApiHelper;

    // Run automatically on content load
    document.addEventListener('DOMContentLoaded', initApiHelper);

})(window);
