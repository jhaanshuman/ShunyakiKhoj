/**
 * geocomplete.js — Global City Autocomplete via OpenStreetMap Nominatim
 * Provides a beautiful dropdown city-search for any place input on the platform.
 * Usage:  initGeoComplete('inputId')
 *         initGeoComplete('mPlace')
 *         initGeoComplete('mBoyPlace')
 * No API key required. Respects Nominatim usage policy (1 req/sec, debounced).
 */

(function (global) {
    'use strict';

    /* ── Local Geo Lat-Lon Database for Instant Search ────────────────────── */
    const LOCAL_GEO_DB = [
        { name: "New Delhi", display_name: "New Delhi, Delhi, India", lat: "28.6139", lon: "77.2090", type: "city", address: { city: "New Delhi", state: "Delhi", country: "India", country_code: "in" } },
        { name: "Delhi", display_name: "Delhi, India", lat: "28.6538", lon: "77.2282", type: "city", address: { city: "Delhi", state: "Delhi", country: "India", country_code: "in" } },
        { name: "Mumbai", display_name: "Mumbai, Maharashtra, India", lat: "19.0760", lon: "72.8777", type: "city", address: { city: "Mumbai", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Bombay", display_name: "Mumbai, Maharashtra, India", lat: "19.0760", lon: "72.8777", type: "city", address: { city: "Mumbai", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Bengaluru", display_name: "Bengaluru, Karnataka, India", lat: "12.9716", lon: "77.5946", type: "city", address: { city: "Bengaluru", state: "Karnataka", country: "India", country_code: "in" } },
        { name: "Bangalore", display_name: "Bengaluru, Karnataka, India", lat: "12.9716", lon: "77.5946", type: "city", address: { city: "Bengaluru", state: "Karnataka", country: "India", country_code: "in" } },
        { name: "Kolkata", display_name: "Kolkata, West Bengal, India", lat: "22.5726", lon: "88.3639", type: "city", address: { city: "Kolkata", state: "West Bengal", country: "India", country_code: "in" } },
        { name: "Calcutta", display_name: "Kolkata, West Bengal, India", lat: "22.5726", lon: "88.3639", type: "city", address: { city: "Kolkata", state: "West Bengal", country: "India", country_code: "in" } },
        { name: "Chennai", display_name: "Chennai, Tamil Nadu, India", lat: "13.0827", lon: "80.2707", type: "city", address: { city: "Chennai", state: "Tamil Nadu", country: "India", country_code: "in" } },
        { name: "Madras", display_name: "Chennai, Tamil Nadu, India", lat: "13.0827", lon: "80.2707", type: "city", address: { city: "Chennai", state: "Tamil Nadu", country: "India", country_code: "in" } },
        { name: "Hyderabad", display_name: "Hyderabad, Telangana, India", lat: "17.3850", lon: "78.4867", type: "city", address: { city: "Hyderabad", state: "Telangana", country: "India", country_code: "in" } },
        { name: "Pune", display_name: "Pune, Maharashtra, India", lat: "18.5204", lon: "73.8567", type: "city", address: { city: "Pune", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Ahmedabad", display_name: "Ahmedabad, Gujarat, India", lat: "23.0225", lon: "72.5714", type: "city", address: { city: "Ahmedabad", state: "Gujarat", country: "India", country_code: "in" } },
        { name: "Patna", display_name: "Patna, Bihar, India", lat: "25.5941", lon: "85.1376", type: "city", address: { city: "Patna", state: "Bihar", country: "India", country_code: "in" } },
        { name: "Jaipur", display_name: "Jaipur, Rajasthan, India", lat: "26.9124", lon: "75.7873", type: "city", address: { city: "Jaipur", state: "Rajasthan", country: "India", country_code: "in" } },
        { name: "Surat", display_name: "Surat, Gujarat, India", lat: "21.1702", lon: "72.8311", type: "city", address: { city: "Surat", state: "Gujarat", country: "India", country_code: "in" } },
        { name: "Lucknow", display_name: "Lucknow, Uttar Pradesh, India", lat: "26.8467", lon: "80.9462", type: "city", address: { city: "Lucknow", state: "Uttar Pradesh", country: "India", country_code: "in" } },
        { name: "Kanpur", display_name: "Kanpur, Uttar Pradesh, India", lat: "26.4499", lon: "80.3319", type: "city", address: { city: "Kanpur", state: "Uttar Pradesh", country: "India", country_code: "in" } },
        { name: "Nagpur", display_name: "Nagpur, Maharashtra, India", lat: "21.1458", lon: "79.0882", type: "city", address: { city: "Nagpur", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Indore", display_name: "Indore, Madhya Pradesh, India", lat: "22.7196", lon: "75.8577", type: "city", address: { city: "Indore", state: "Madhya Pradesh", country: "India", country_code: "in" } },
        { name: "Thane", display_name: "Thane, Maharashtra, India", lat: "19.2183", lon: "72.9781", type: "city", address: { city: "Thane", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Bhopal", display_name: "Bhopal, Madhya Pradesh, India", lat: "23.2599", lon: "77.4126", type: "city", address: { city: "Bhopal", state: "Madhya Pradesh", country: "India", country_code: "in" } },
        { name: "Visakhapatnam", display_name: "Visakhapatnam, Andhra Pradesh, India", lat: "17.6868", lon: "83.2185", type: "city", address: { city: "Visakhapatnam", state: "Andhra Pradesh", country: "India", country_code: "in" } },
        { name: "Pimpri-Chinchwad", display_name: "Pimpri-Chinchwad, Maharashtra, India", lat: "18.6298", lon: "73.7997", type: "city", address: { city: "Pimpri-Chinchwad", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Vadodara", display_name: "Vadodara, Gujarat, India", lat: "22.3072", lon: "73.1812", type: "city", address: { city: "Vadodara", state: "Gujarat", country: "India", country_code: "in" } },
        { name: "Ghaziabad", display_name: "Ghaziabad, Uttar Pradesh, India", lat: "28.6692", lon: "77.4538", type: "city", address: { city: "Ghaziabad", state: "Uttar Pradesh", country: "India", country_code: "in" } },
        { name: "Ludhiana", display_name: "Ludhiana, Punjab, India", lat: "30.9010", lon: "75.8573", type: "city", address: { city: "Ludhiana", state: "Punjab", country: "India", country_code: "in" } },
        { name: "Agra", display_name: "Agra, Uttar Pradesh, India", lat: "27.1767", lon: "78.0081", type: "city", address: { city: "Agra", state: "Uttar Pradesh", country: "India", country_code: "in" } },
        { name: "Nashik", display_name: "Nashik, Maharashtra, India", lat: "19.9975", lon: "73.7898", type: "city", address: { city: "Nashik", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Faridabad", display_name: "Faridabad, Haryana, India", lat: "28.4089", lon: "77.3178", type: "city", address: { city: "Faridabad", state: "Haryana", country: "India", country_code: "in" } },
        { name: "Meerut", display_name: "Meerut, Uttar Pradesh, India", lat: "28.9845", lon: "77.7064", type: "city", address: { city: "Meerut", state: "Uttar Pradesh", country: "India", country_code: "in" } },
        { name: "Rajkot", display_name: "Rajkot, Gujarat, India", lat: "22.3039", lon: "70.8022", type: "city", address: { city: "Rajkot", state: "Gujarat", country: "India", country_code: "in" } },
        { name: "Kalyan-Dombivli", display_name: "Kalyan-Dombivli, Maharashtra, India", lat: "19.2403", lon: "73.1305", type: "city", address: { city: "Kalyan-Dombivli", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Vasai-Virar", display_name: "Vasai-Virar, Maharashtra, India", lat: "19.3913", lon: "72.8397", type: "city", address: { city: "Vasai-Virar", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Srinagar", display_name: "Srinagar, Jammu & Kashmir, India", lat: "34.0837", lon: "74.7973", type: "city", address: { city: "Srinagar", state: "Jammu and Kashmir", country: "India", country_code: "in" } },
        { name: "Aurangabad", display_name: "Aurangabad, Maharashtra, India", lat: "19.8762", lon: "75.3433", type: "city", address: { city: "Aurangabad", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Dhanbad", display_name: "Dhanbad, Jharkhand, India", lat: "23.7957", lon: "86.4304", type: "city", address: { city: "Dhanbad", state: "Jharkhand", country: "India", country_code: "in" } },
        { name: "Amritsar", display_name: "Amritsar, Punjab, India", lat: "31.6340", lon: "74.8723", type: "city", address: { city: "Amritsar", state: "Punjab", country: "India", country_code: "in" } },
        { name: "Navi Mumbai", display_name: "Navi Mumbai, Maharashtra, India", lat: "19.0330", lon: "73.0297", type: "city", address: { city: "Navi Mumbai", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Allahabad", display_name: "Prayagraj, Uttar Pradesh, India", lat: "25.4358", lon: "81.8463", type: "city", address: { city: "Prayagraj", state: "Uttar Pradesh", country: "India", country_code: "in" } },
        { name: "Prayagraj", display_name: "Prayagraj, Uttar Pradesh, India", lat: "25.4358", lon: "81.8463", type: "city", address: { city: "Prayagraj", state: "Uttar Pradesh", country: "India", country_code: "in" } },
        { name: "Howrah", display_name: "Howrah, West Bengal, India", lat: "22.5958", lon: "88.2636", type: "city", address: { city: "Howrah", state: "West Bengal", country: "India", country_code: "in" } },
        { name: "Gwalior", display_name: "Gwalior, Madhya Pradesh, India", lat: "26.2183", lon: "78.1828", type: "city", address: { city: "Gwalior", state: "Madhya Pradesh", country: "India", country_code: "in" } },
        { name: "Jabalpur", display_name: "Jabalpur, Madhya Pradesh, India", lat: "22.1760", lon: "79.9300", type: "city", address: { city: "Jabalpur", state: "Madhya Pradesh", country: "India", country_code: "in" } },
        { name: "Coimbatore", display_name: "Coimbatore, Tamil Nadu, India", lat: "11.0168", lon: "76.9558", type: "city", address: { city: "Coimbatore", state: "Tamil Nadu", country: "India", country_code: "in" } },
        { name: "Vijayawada", display_name: "Vijayawada, Andhra Pradesh, India", lat: "16.5062", lon: "80.6480", type: "city", address: { city: "Vijayawada", state: "Andhra Pradesh", country: "India", country_code: "in" } },
        { name: "Jodhpur", display_name: "Jodhpur, Rajasthan, India", lat: "26.2389", lon: "73.0243", type: "city", address: { city: "Jodhpur", state: "Rajasthan", country: "India", country_code: "in" } },
        { name: "Madurai", display_name: "Madurai, Tamil Nadu, India", lat: "9.9252", lon: "78.1198", type: "city", address: { city: "Madurai", state: "Tamil Nadu", country: "India", country_code: "in" } },
        { name: "Raipur", display_name: "Raipur, Chhattisgarh, India", lat: "21.2514", lon: "81.6296", type: "city", address: { city: "Raipur", state: "Chhattisgarh", country: "India", country_code: "in" } },
        { name: "Kota", display_name: "Kota, Rajasthan, India", lat: "25.2138", lon: "75.8648", type: "city", address: { city: "Kota", state: "Rajasthan", country: "India", country_code: "in" } },
        { name: "Chandigarh", display_name: "Chandigarh, India", lat: "30.7333", lon: "76.7794", type: "city", address: { city: "Chandigarh", state: "Chandigarh", country: "India", country_code: "in" } },
        { name: "Guwahati", display_name: "Guwahati, Assam, India", lat: "26.1445", lon: "91.7362", type: "city", address: { city: "Guwahati", state: "Assam", country: "India", country_code: "in" } },
        { name: "Solapur", display_name: "Solapur, Maharashtra, India", lat: "17.6599", lon: "75.9064", type: "city", address: { city: "Solapur", state: "Maharashtra", country: "India", country_code: "in" } },
        { name: "Hubli", display_name: "Hubli, Karnataka, India", lat: "15.3647", lon: "75.1240", type: "city", address: { city: "Hubli", state: "Karnataka", country: "India", country_code: "in" } },
        { name: "Bareilly", display_name: "Bareilly, Uttar Pradesh, India", lat: "28.3640", lon: "79.4150", type: "city", address: { city: "Bareilly", state: "Uttar Pradesh", country: "India", country_code: "in" } },
        { name: "Mysore", display_name: "Mysuru, Karnataka, India", lat: "12.2958", lon: "76.6394", type: "city", address: { city: "Mysuru", state: "Karnataka", country: "India", country_code: "in" } },
        { name: "Mysuru", display_name: "Mysuru, Karnataka, India", lat: "12.2958", lon: "76.6394", type: "city", address: { city: "Mysuru", state: "Karnataka", country: "India", country_code: "in" } },
        { name: "Tiruchirappalli", display_name: "Tiruchirappalli, Tamil Nadu, India", lat: "10.7905", lon: "78.7047", type: "city", address: { city: "Tiruchirappalli", state: "Tamil Nadu", country: "India", country_code: "in" } },
        { name: "Tirupati", display_name: "Tirupati, Andhra Pradesh, India", lat: "13.6288", lon: "79.4192", type: "city", address: { city: "Tirupati", state: "Andhra Pradesh", country: "India", country_code: "in" } },
        { name: "Gurgaon", display_name: "Gurugram, Haryana, India", lat: "28.4595", lon: "77.0266", type: "city", address: { city: "Gurugram", state: "Haryana", country: "India", country_code: "in" } },
        { name: "Gurugram", display_name: "Gurugram, Haryana, India", lat: "28.4595", lon: "77.0266", type: "city", address: { city: "Gurugram", state: "Haryana", country: "India", country_code: "in" } },
        { name: "Noida", display_name: "Noida, Uttar Pradesh, India", lat: "28.5355", lon: "77.3910", type: "city", address: { city: "Noida", state: "Uttar Pradesh", country: "India", country_code: "in" } },
        { name: "Aligarh", display_name: "Aligarh, Uttar Pradesh, India", lat: "27.8974", lon: "78.0880", type: "city", address: { city: "Aligarh", state: "Uttar Pradesh", country: "India", country_code: "in" } },
        { name: "Jalandhar", display_name: "Jalandhar, Punjab, India", lat: "31.3260", lon: "75.5762", type: "city", address: { city: "Jalandhar", state: "Punjab", country: "India", country_code: "in" } },
        { name: "Bhubaneswar", display_name: "Bhubaneswar, Orissa, India", lat: "20.2961", lon: "85.8245", type: "city", address: { city: "Bhubaneswar", state: "Odisha", country: "India", country_code: "in" } },
        { name: "Dehradun", display_name: "Dehradun, Uttarakhand, India", lat: "30.3165", lon: "78.0322", type: "city", address: { city: "Dehradun", state: "Uttarakhand", country: "India", country_code: "in" } },
        { name: "Ranchi", display_name: "Ranchi, Jharkhand, India", lat: "23.3441", lon: "85.3096", type: "city", address: { city: "Ranchi", state: "Jharkhand", country: "India", country_code: "in" } },
        { name: "Shimla", display_name: "Shimla, Himachal Pradesh, India", lat: "31.1048", lon: "77.1734", type: "city", address: { city: "Shimla", state: "Himachal Pradesh", country: "India", country_code: "in" } },
        { name: "London", display_name: "London, England, United Kingdom", lat: "51.5074", lon: "-0.1278", type: "city", address: { city: "London", state: "England", country: "United Kingdom", country_code: "gb" } },
        { name: "New York", display_name: "New York, USA", lat: "40.7128", lon: "-74.0060", type: "city", address: { city: "New York", state: "New York", country: "United States", country_code: "us" } },
        { name: "San Francisco", display_name: "San Francisco, California, USA", lat: "37.7749", lon: "-122.4194", type: "city", address: { city: "San Francisco", state: "California", country: "United States", country_code: "us" } },
        { name: "Tokyo", display_name: "Tokyo, Japan", lat: "35.6762", lon: "139.6503", type: "city", address: { city: "Tokyo", state: "Tokyo", country: "Japan", country_code: "jp" } }
    ];

    /* ── Styles injected once ─────────────────────────────────────────────── */
    function injectStyles() {
        if (document.getElementById('_geocomplete_styles')) return;
        const style = document.createElement('style');
        style.id = '_geocomplete_styles';
        style.textContent = `
            .gc-wrapper {
                position: relative;
                width: 100%;
            }
            .gc-input-wrap {
                position: relative;
                display: flex;
                align-items: center;
            }
            .gc-pin-icon {
                position: absolute;
                left: 10px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 0.9rem;
                pointer-events: none;
                z-index: 2;
                opacity: 0.6;
            }
            .gc-input {
                width: 100%;
                padding: 9px 34px 9px 30px !important;
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.12);
                color: #fff;
                border-radius: 8px;
                font-family: inherit;
                font-size: 0.9rem;
                transition: border-color 0.2s, background 0.2s;
                box-sizing: border-box;
            }
            .gc-input:focus {
                outline: none;
                border-color: #6366f1;
                background: rgba(99,102,241,0.08);
            }
            .gc-clear-btn {
                position: absolute;
                right: 8px;
                top: 50%;
                transform: translateY(-50%);
                background: none;
                border: none;
                color: #94a3b8;
                cursor: pointer;
                font-size: 1rem;
                line-height: 1;
                padding: 2px 4px;
                border-radius: 4px;
                display: none;
                transition: color 0.15s;
                z-index: 2;
            }
            .gc-clear-btn:hover { color: #f87171; }
            .gc-dropdown {
                position: absolute;
                top: calc(100% + 4px);
                left: 0; right: 0;
                background: #0f172a;
                border: 1px solid rgba(99,102,241,0.35);
                border-radius: 10px;
                box-shadow: 0 16px 48px rgba(0,0,0,0.6), 0 0 0 1px rgba(99,102,241,0.1);
                z-index: 9999;
                overflow: hidden;
                max-height: 320px;
                overflow-y: auto;
                animation: gcFadeIn 0.15s ease;
            }
            @keyframes gcFadeIn {
                from { opacity: 0; transform: translateY(-6px); }
                to   { opacity: 1; transform: translateY(0); }
            }
            .gc-dropdown::-webkit-scrollbar { width: 4px; }
            .gc-dropdown::-webkit-scrollbar-track { background: transparent; }
            .gc-dropdown::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 2px; }

            .gc-item {
                display: flex;
                align-items: flex-start;
                gap: 10px;
                padding: 10px 14px;
                cursor: pointer;
                border-bottom: 1px solid rgba(255,255,255,0.04);
                transition: background 0.12s;
            }
            .gc-item:last-child { border-bottom: none; }
            .gc-item:hover, .gc-item.active {
                background: rgba(99,102,241,0.15);
            }
            .gc-item-icon {
                font-size: 1.05rem;
                margin-top: 1px;
                flex-shrink: 0;
            }
            .gc-item-body { flex: 1; min-width: 0; }
            .gc-item-name {
                font-size: 0.88rem;
                font-weight: 700;
                color: #e2e8f0;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .gc-item-meta {
                font-size: 0.73rem;
                color: #64748b;
                margin-top: 1px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .gc-item-coords {
                font-size: 0.68rem;
                color: #4ade80;
                font-weight: 600;
                white-space: nowrap;
                flex-shrink: 0;
                align-self: center;
            }
            .gc-status {
                padding: 12px 16px;
                font-size: 0.82rem;
                color: #64748b;
                text-align: center;
                font-style: italic;
            }
            .gc-searching {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                padding: 14px;
                color: #818cf8;
                font-size: 0.82rem;
            }
            .gc-spinner-dot {
                width: 6px; height: 6px;
                border-radius: 50%;
                background: #6366f1;
                animation: gcPulse 1s infinite ease-in-out;
                display: inline-block;
            }
            .gc-spinner-dot:nth-child(2) { animation-delay: 0.2s; }
            .gc-spinner-dot:nth-child(3) { animation-delay: 0.4s; }
            @keyframes gcPulse {
                0%, 100% { opacity: 0.3; transform: scale(0.7); }
                50%       { opacity: 1;   transform: scale(1.1); }
            }
            .gc-divider {
                padding: 4px 14px;
                font-size: 0.66rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                color: #334155;
                background: rgba(0,0,0,0.2);
            }
        `;
        document.head.appendChild(style);
    }

    /* ── Place type → icon map ─────────────────────────────────────────────── */
    function getPlaceIcon(type, cls) {
        const map = {
            city: '🏙️', town: '🏘️', village: '🏡', suburb: '🏢',
            state: '🗺️', country: '🌍', county: '📍',
            administrative: '📍', municipality: '🏙️',
            district: '🗺️', hamlet: '🏡', neighbourhood: '🏢'
        };
        const t = (type || '').toLowerCase();
        const c = (cls  || '').toLowerCase();
        return map[t] || map[c] || '📌';
    }

    /* ── Format a Nominatim result into display strings ────────────────────── */
    function formatResult(r) {
        const addr = r.address || {};
        // Primary name: city > town > village > county > state
        const primary =
            addr.city || addr.town || addr.village || addr.county ||
            addr.state_district || addr.state || r.name || r.display_name.split(',')[0];
        // Country flag (basic emoji mapping)
        const countryCode = (addr.country_code || '').toUpperCase();
        const flag = countryCode.length === 2
            ? String.fromCodePoint(...[...countryCode].map(c => c.charCodeAt(0) + 127397))
            : '';
        // Build breadcrumb: City, State, Country
        const parts = [
            addr.state || addr.state_district,
            addr.country
        ].filter(Boolean);
        const meta = flag + ' ' + parts.join(', ');
        // Compact coord string
        const lat = parseFloat(r.lat).toFixed(4);
        const lon = parseFloat(r.lon).toFixed(4);
        const coords = `${lat >= 0 ? '+' : ''}${lat}, ${lon >= 0 ? '+' : ''}${lon}`;
        // Value to put in the text input (what the backend receives)
        const inputValue = [primary, addr.state, addr.country].filter(Boolean).join(', ');
        return { primary, meta, coords, inputValue, icon: getPlaceIcon(r.type, r.class) };
    }

    /* ── Core autocomplete factory ──────────────────────────────────────────── */
    function initGeoComplete(inputId, options) {
        options = options || {};
        const defaultPlace = options.defaultPlace || 'Patna, Bihar, India';

        injectStyles();

        const originalInput = document.getElementById(inputId);
        if (!originalInput) {
            console.warn('[GeoComplete] Element not found:', inputId);
            return;
        }
        if (originalInput.dataset.gcInitialized) {
            return;
        }
        originalInput.dataset.gcInitialized = "true";

        /* Wrap the original input */
        const wrapper = document.createElement('div');
        wrapper.className = 'gc-wrapper';
        originalInput.parentNode.insertBefore(wrapper, originalInput);
        wrapper.appendChild(originalInput);

        /* Apply gc-input class while preserving existing styles */
        originalInput.classList.add('gc-input');

        /* Pin icon */
        const pin = document.createElement('span');
        pin.className = 'gc-pin-icon';
        pin.textContent = '📍';
        wrapper.appendChild(pin);

        /* Clear button */
        const clearBtn = document.createElement('button');
        clearBtn.className = 'gc-clear-btn';
        clearBtn.type = 'button';
        clearBtn.textContent = '✕';
        clearBtn.title = 'Clear';
        wrapper.appendChild(clearBtn);

        /* Wrap in relative input group */
        const inputWrap = document.createElement('div');
        inputWrap.className = 'gc-input-wrap';
        wrapper.appendChild(inputWrap);
        inputWrap.appendChild(pin);
        inputWrap.appendChild(originalInput);
        inputWrap.appendChild(clearBtn);

        /* Dropdown */
        const dropdown = document.createElement('div');
        dropdown.className = 'gc-dropdown';
        dropdown.style.display = 'none';
        wrapper.appendChild(dropdown);

        /* State */
        let debounceTimer = null;
        let activeIndex   = -1;
        let lastResults   = [];
        let selectedItem  = null;

        /* Set default value */
        if (!originalInput.value) {
            originalInput.value = defaultPlace;
        }

        /* Toggle clear button visibility */
        function updateClearBtn() {
            clearBtn.style.display = originalInput.value.trim() ? 'block' : 'none';
        }
        updateClearBtn();

        /* Close dropdown */
        function closeDropdown() {
            dropdown.style.display = 'none';
            activeIndex = -1;
        }

        /* Show searching indicator */
        function showSearching() {
            dropdown.style.display = 'block';
            dropdown.innerHTML = `
                <div class="gc-searching">
                    <span class="gc-spinner-dot"></span>
                    <span class="gc-spinner-dot"></span>
                    <span class="gc-spinner-dot"></span>
                    <span style="margin-left:6px;">Searching cities…</span>
                </div>`;
        }

        /* Render results */
        function renderResults(results) {
            lastResults = results;
            activeIndex = -1;
            if (!results || results.length === 0) {
                dropdown.innerHTML = '<div class="gc-status">No cities found. Try a different spelling.</div>';
                dropdown.style.display = 'block';
                return;
            }
            dropdown.innerHTML = '<div class="gc-divider">🌍 Global City Suggestions</div>';
            results.forEach((r, i) => {
                const f = formatResult(r);
                const item = document.createElement('div');
                item.className = 'gc-item';
                item.dataset.index = i;
                item.innerHTML = `
                    <div class="gc-item-icon">${f.icon}</div>
                    <div class="gc-item-body">
                        <div class="gc-item-name">${f.primary}</div>
                        <div class="gc-item-meta">${f.meta}</div>
                    </div>
                    <div class="gc-item-coords">${f.coords}</div>`;
                item.addEventListener('mousedown', (e) => {
                    e.preventDefault(); // prevent input blur before click fires
                    selectResult(r, f);
                });
                dropdown.appendChild(item);
            });
            dropdown.style.display = 'block';
        }

        /* Select a result */
        function selectResult(raw, formatted) {
            selectedItem = { raw, formatted };
            originalInput.value = formatted.inputValue;
            updateClearBtn();
            closeDropdown();
            // Store precise coordinates as data attrs for backend use
            originalInput.dataset.lat = raw.lat;
            originalInput.dataset.lon = raw.lon;
            originalInput.dataset.displayName = raw.display_name;
            // Fire change event so external listeners know
            originalInput.dispatchEvent(new Event('change', { bubbles: true }));
        }

        /* Keyboard navigation */
        function setActive(idx) {
            const items = dropdown.querySelectorAll('.gc-item');
            items.forEach(it => it.classList.remove('active'));
            activeIndex = Math.max(-1, Math.min(items.length - 1, idx));
            if (activeIndex >= 0) {
                items[activeIndex].classList.add('active');
                items[activeIndex].scrollIntoView({ block: 'nearest' });
            }
        }

        /* ── Fetch from Nominatim ──────────────────────────────────────────── */
        async function fetchPlaces(query) {
            const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&addressdetails=1&limit=8&featuretype=city&accept-language=en`;
            try {
                const res  = await fetch(url, {
                    headers: { 'Accept-Language': 'en', 'User-Agent': 'ShunyaKiKhojJyotish/1.0' }
                });
                const data = await res.json();
                // Filter: prefer cities, towns, administrative regions
                const preferred = data.filter(r =>
                    ['city','town','village','administrative','municipality','suburb'].includes(r.type) ||
                    ['place','boundary'].includes(r.class)
                );
                return preferred.length ? preferred : data;
            } catch (e) {
                console.warn('[GeoComplete] Nominatim error:', e);
                return [];
            }
        }

        /* ── Events ──────────────────────────────────────────────────────────── */
        originalInput.addEventListener('input', () => {
            updateClearBtn();
            const q = originalInput.value.trim().toLowerCase();
            if (q.length < 2) { closeDropdown(); return; }
            
            // ⚡ Instant Local Geo Database search
            const localMatches = LOCAL_GEO_DB.filter(city => 
                city.name.toLowerCase().startsWith(q) || 
                city.name.toLowerCase().includes(q)
            ).slice(0, 5);
            
            if (localMatches.length > 0) {
                // Instantly render local matches without debounce network delay!
                renderResults(localMatches);
            } else {
                showSearching();
            }

            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(async () => {
                // Fetch Nominatim results to complete/refine search
                const apiResults = await fetchPlaces(originalInput.value.trim());
                // Merge local matches with API results, filtering duplicates
                const merged = [...localMatches];
                apiResults.forEach(apiCity => {
                    const latDiff = 0.05;
                    const lonDiff = 0.05;
                    const isDup = localMatches.some(loc => 
                        Math.abs(parseFloat(loc.lat) - parseFloat(apiCity.lat)) < latDiff &&
                        Math.abs(parseFloat(loc.lon) - parseFloat(apiCity.lon)) < lonDiff
                    );
                    if (!isDup) merged.push(apiCity);
                });
                renderResults(merged.slice(0, 8));
            }, 320); // 320ms debounce
        });

        originalInput.addEventListener('keydown', (e) => {
            if (dropdown.style.display === 'none') return;
            if (e.key === 'ArrowDown')  { e.preventDefault(); setActive(activeIndex + 1); }
            if (e.key === 'ArrowUp')    { e.preventDefault(); setActive(activeIndex - 1); }
            if (e.key === 'Escape')     { closeDropdown(); }
            if (e.key === 'Enter') {
                e.preventDefault();
                if (activeIndex >= 0 && lastResults[activeIndex]) {
                    const f = formatResult(lastResults[activeIndex]);
                    selectResult(lastResults[activeIndex], f);
                } else {
                    closeDropdown();
                }
            }
        });

        originalInput.addEventListener('blur', () => {
            // Small delay so mousedown click on dropdown item fires first
            setTimeout(closeDropdown, 180);
        });

        clearBtn.addEventListener('click', () => {
            originalInput.value = '';
            selectedItem = null;
            delete originalInput.dataset.lat;
            delete originalInput.dataset.lon;
            updateClearBtn();
            originalInput.focus();
        });

        /* Close on outside click */
        document.addEventListener('click', (e) => {
            if (!wrapper.contains(e.target)) closeDropdown();
        });

        /* Public API */
        return {
            getSelectedRaw: () => selectedItem ? selectedItem.raw : null,
            getCoords: () => ({
                lat: originalInput.dataset.lat || null,
                lon: originalInput.dataset.lon || null
            }),
            getValue: () => originalInput.value
        };
    }

    /* ── Expose globally ─────────────────────────────────────────────────── */
    global.initGeoComplete = initGeoComplete;

}(window));
