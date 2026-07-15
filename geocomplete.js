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
            const q = originalInput.value.trim();
            if (q.length < 2) { closeDropdown(); return; }
            clearTimeout(debounceTimer);
            showSearching();
            debounceTimer = setTimeout(async () => {
                const results = await fetchPlaces(q);
                renderResults(results);
            }, 320); // 320ms debounce — respects Nominatim 1 req/sec policy
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
