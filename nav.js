/**
 * Professional Navigation System & Dynamic Menu Renderer
 * Designed for Shunyakikhoj
 */

// DOMContentLoaded is handled at the bottom of nav.js

// Pretty routing helper functions
function buildUrlPath(page, tab, queryParams) {
    if (window.location.protocol === 'file:') {
        const searchParams = new URLSearchParams();
        if (page) searchParams.set('page', page);
        if (tab) searchParams.set('tab', tab);
        for (let k in queryParams) {
            if (k !== 'page' && k !== 'tab') {
                searchParams.set(k, queryParams[k]);
            }
        }
        const searchStr = searchParams.toString();
        const currentFile = window.location.pathname.split('/').pop() || 'index.html';
        return currentFile + (searchStr ? '?' + searchStr : '');
    }

    let path = '/';
    if (page && page !== 'home') {
        path += page;
        if (tab) {
            path += '/' + tab;
        }
    } else if (tab) {
        path += 'home/' + tab;
    }
    
    const searchParams = new URLSearchParams();
    for (let k in queryParams) {
        if (k !== 'page' && k !== 'tab') {
            searchParams.set(k, queryParams[k]);
        }
    }
    const searchStr = searchParams.toString();
    return path + (searchStr ? '?' + searchStr : '');
}

function parseUrlPath(urlObj) {
    if (window.location.protocol === 'file:') {
        const page = urlObj.searchParams.get('page') || 'home';
        const tab = urlObj.searchParams.get('tab') || '';
        const queryParams = {};
        urlObj.searchParams.forEach((val, key) => {
            if (key !== 'page' && key !== 'tab') {
                queryParams[key] = val;
            }
        });
        return { page, tab, queryParams };
    }

    let pathname = urlObj.pathname;
    pathname = pathname.replace(/^\/+|\/+$/g, '');
    const parts = pathname.split('/');
    
    let page = 'home';
    let tab = '';
    
    if (parts.length > 0 && parts[0] !== '') {
        if (parts[0] === 'home') {
            page = 'home';
            if (parts.length > 1) {
                tab = parts[1];
            }
        } else {
            page = parts[0];
            if (parts.length > 1) {
                tab = parts[1];
            }
        }
    }
    
    const queryParams = {};
    urlObj.searchParams.forEach((val, key) => {
        queryParams[key] = val;
    });
    
    return { page, tab, queryParams };
}

window.buildUrlPath = buildUrlPath;
window.parseUrlPath = parseUrlPath;

const DEFAULT_NAV_CONFIG = {
  "menu": [
    {
      "label": "Hindu Panchang",
      "type": "dropdown",
      "icon": "🕉️",
      "items": [
        { "label": "Dainik Panchang", "url": "index.html?tab=panchang", "icon": "☀️" },
        { "label": "Bengali Panjika", "url": "index.html?tab=panchang&region=bengali", "icon": "🎷" },
        { "label": "Tamil Panchangam", "url": "index.html?tab=panchang&region=tamil", "icon": "🐚" },
        { "label": "Telugu Panchangam", "url": "index.html?tab=panchang&region=telugu", "icon": "🌺" },
        { "label": "Malayalam Panchangam", "url": "index.html?tab=panchang&region=malayalam", "icon": "🌴" }
      ]
    },
    {
      "label": "Vedic Calendars",
      "type": "dropdown",
      "icon": "📅",
      "items": [
        { "label": "Maasik Hindu Calendar", "url": "index.html?tab=maasik", "icon": "🗓️" },
        { "label": "National Indian Calendar", "url": "index.html?tab=maasik", "icon": "🇮🇳" },
        { "label": "Tamil Calendar", "url": "index.html?tab=maasik", "icon": "🐚" },
        { "label": "Telugu Calendar", "url": "index.html?tab=maasik", "icon": "🌿" }
      ]
    },
    {
      "label": "Jyotish Utilities",
      "type": "dropdown",
      "icon": "🔮",
      "items": [
        { "label": "Personalised Kundli D1/D9", "url": "Features/Astrology/astrology.html?tab=kundli", "icon": "🧘" },
        { "label": "Gemstone Recommendation", "url": "Features/Astrology/astrology.html?tab=gemstone", "icon": "💎" },
        { "label": "Rudraksha Suggestion", "url": "Features/Astrology/astrology.html?tab=rudraksha", "icon": "📿" },
        { "label": "Kundli Matching (Milan)", "url": "Features/Astrology/astrology.html?tab=milan", "icon": "💞" },
        { "label": "Prashna Kundali", "url": "Features/Astrology/astrology.html?tab=prashna", "icon": "❓" },
        { "label": "Daily Rashifal Predictions", "url": "Features/Astrology/astrology.html?tab=rashifal", "icon": "🦁" },
        { "label": "Weekly Horoscope Signs", "url": "Features/Astrology/astrology.html?tab=weekly", "icon": "📈" },
        { "label": "Monthly Rashi Transits", "url": "Features/Astrology/astrology.html?tab=maasik", "icon": "🪐" },
        { "label": "Yearly Predictions 2026", "url": "Features/Astrology/astrology.html?tab=yearly", "icon": "📅" }
      ]
    },
    {
      "label": "Hindu Festivals",
      "type": "dropdown",
      "icon": "🎉",
      "items": [
        { "label": "Diwali Shubh Muhurtas", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🪔" },
        { "label": "Raksha Bandhan Thread Time", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🎗️" },
        { "label": "Maha Shivaratri Nishita", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🔱" },
        { "label": "Ganesha Chaturthi Murti Sthapna", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🐘" }
      ]
    },
    {
      "label": "Panchang Utilities",
      "type": "dropdown",
      "icon": "🌾",
      "items": [
        { "label": "Rahu Kala Timings", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "⚠️" },
        { "label": "Panchak Boundary Times", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🚫" },
        { "label": "Bhadra Vishti Karana Span", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "⏳" },
        { "label": "Ganda Mool constellations", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "⭐" }
      ]
    },
    {
      "label": "Yoga in Astrology",
      "type": "dropdown",
      "icon": "🎗️",
      "items": [
        { "label": "Gurupushyamrut Yoga", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🌟" },
        { "label": "Sarvarthasiddhi Yoga", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🕉️" },
        { "label": "Dwipushkar Yoga", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "💫" },
        { "label": "Ravi Pushya Yoga", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "☀️" }
      ]
    },
    {
      "label": "Vrat and Upavas",
      "type": "dropdown",
      "icon": "🛐",
      "items": [
        { "label": "Sankashti Chaturthi moonrise", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🌙" },
        { "label": "Vinayaka Chaturthi timings", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🐘" },
        { "label": "Ekadashi Dates list", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🥦" },
        { "label": "Pradosham Fasting slots", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🔱" }
      ]
    },
    {
      "label": "Vrat Katha",
      "type": "dropdown",
      "icon": "📜",
      "items": [
        { "label": "Satyanarayana Vrat Katha", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "📖" },
        { "label": "Ekadashi Vrat Katha", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🥬" },
        { "label": "Karwa Chauth Vrat Katha", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🪔" },
        { "label": "Ahoi Ashtami Vrat Katha", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "✨" }
      ]
    },
    {
      "label": "Hindu Astronomy",
      "type": "dropdown",
      "icon": "🔭",
      "items": [
        { "label": "Solar Eclipse calculations", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🌑" },
        { "label": "Lunar Eclipse timings", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🌖" },
        { "label": "Eclipse Dates database", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "📅" },
        { "label": "Winter Solstice alignment", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "❄️" }
      ]
    },
    {
      "label": "Puja Vidhi",
      "type": "dropdown",
      "icon": "🔥",
      "items": [
        { "label": "Ganesha Puja Vidhi steps", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🐘" },
        { "label": "Lakshmi Puja Vidhi Deepavali", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🪔" },
        { "label": "Shivaratri Abhishekam Vidhi", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🔱" }
      ]
    },
    {
      "label": "Vedic Mantras",
      "type": "dropdown",
      "icon": "☀️",
      "items": [
        { "label": "Maha Lakshmi Ashtakam", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🌸" },
        { "label": "Navdurga forms list", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🛡️" },
        { "label": "Dasha Mahavidya sadhana", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🔥" },
        { "label": "Saraswati stotrams", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🎼" },
        { "label": "Gayatri Mantra meaning", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "☀️" },
        { "label": "Mahamrityunjaya Mantra", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "💀" },
        { "label": "Shanti Path translations", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🕊️" }
      ]
    },
    {
      "label": "Deities Yantra",
      "type": "dropdown",
      "icon": "🛡️",
      "items": [
        { "label": "Shri Yantra geometric logic", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "☸️" },
        { "label": "Kubera Yantra installation", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "💰" },
        { "label": "Mahavidya Yantra protection", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🛡️" }
      ]
    },
    {
      "label": "Hindu Rituals",
      "type": "dropdown",
      "icon": "🌊",
      "items": [
        { "label": "Kumbha Mela bathing dates", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🌊" },
        { "label": "Shradh Karma Pitru Paksha", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🕯️" },
        { "label": "Vivah Sanskar 7 rounds", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🤝" }
      ]
    },
    {
      "label": "Devotional Lyrics",
      "type": "dropdown",
      "icon": "🎼",
      "items": [
        { "label": "Ganesh Aarti & Chalisa", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🐘" },
        { "label": "Sundarkand Paath lyrics", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "📖" },
        { "label": "Vishnu Sahasranama Stotram", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🕉️" },
        { "label": "Shri Durga Saptashati text", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🛡️" }
      ]
    },
    {
      "label": "Art Gallery",
      "type": "dropdown",
      "icon": "🎨",
      "items": [
        { "label": "Rangoli Collection designs", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🎨" },
        { "label": "Mehandi Designs traditional", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "🌿" },
        { "label": "Festivals greetings templates", "url": "Features/Astrology/astrology.html?tab=panchang", "icon": "✉️" }
      ]
    },
    {
      "label": "Wisdom Library",
      "url": "./Static/index.html",
      "icon": "📿"
    }
  ]
};

let menuConfig = null;
let currentActiveItem = null;

async function initNavigation() {
    try {
        const configPath = window.location.pathname.includes('/Features/') ? '../../nav_config.json' : './nav_config.json';
        const res = await fetch(configPath);
        menuConfig = await res.json();
    } catch (e) {
        console.warn("Failed to load navigation configuration from JSON, falling back to local copy.", e);
        menuConfig = DEFAULT_NAV_CONFIG;
    }
    
    // Render menus
    renderMobileNav(menuConfig.menu);
    
    // Setup Search, Theme Toggle, Breadcrumbs & Accessibility
    setupSearch(menuConfig.menu);
    setupThemeToggle();
    setupBreadcrumbs(menuConfig.menu);
    setupKeyboardAccessibility();
    highlightActiveMenu();
}

// ==========================================
// DESKTOP NAVIGATION RENDERING
// ==========================================
function renderDesktopNav(menuItems) {
    const navContainer = document.querySelector('.header');
    if (!navContainer) return;

    // Create Navigation Bar inside Header
    const navBar = document.createElement('nav');
    navBar.className = 'desktop-navbar';
    navBar.setAttribute('role', 'navigation');
    navBar.setAttribute('aria-label', 'Primary Navigation');

    const navList = document.createElement('ul');
    navList.className = 'nav-menu-list';

    menuItems.forEach((item, index) => {
        const li = document.createElement('li');
        li.className = 'nav-menu-item';
        if (item.type === 'megamenu') li.classList.add('has-megamenu');
        else if (item.type === 'dropdown') li.classList.add('has-dropdown');

        const a = document.createElement('a');
        a.href = item.url || 'javascript:void(0)';
        a.className = 'nav-menu-link';
        a.innerHTML = `<span class="menu-emoji">${item.icon}</span> ${item.label}`;
        a.setAttribute('aria-haspopup', item.type ? 'true' : 'false');
        a.setAttribute('aria-expanded', 'false');
        
        li.appendChild(a);

        // Render Dropdown / Megamenu
        if (item.type === 'dropdown' && item.items) {
            const dropdown = document.createElement('div');
            dropdown.className = 'dropdown-panel';
            const ul = document.createElement('ul');
            item.items.forEach(sub => {
                const subLi = document.createElement('li');
                const subA = document.createElement('a');
                // Adjust url relative path if on child pages
                subA.href = adjustUrlPath(sub.url);
                subA.target = '_blank';
                subA.innerHTML = `<span class="sub-emoji">${sub.icon || '🔸'}</span> ${sub.label}`;
                subLi.appendChild(subA);
                ul.appendChild(subLi);
            });
            dropdown.appendChild(ul);
            li.appendChild(dropdown);
        } else if (item.type === 'megamenu' && item.columns) {
            const megamenu = document.createElement('div');
            megamenu.className = 'megamenu-panel';
            
            const columnsContainer = document.createElement('div');
            columnsContainer.className = 'megamenu-columns';

            item.columns.forEach(col => {
                const column = document.createElement('div');
                column.className = 'megamenu-column';
                if (col.title) {
                    const h4 = document.createElement('h4');
                    h4.innerText = col.title;
                    column.appendChild(h4);
                }

                const ul = document.createElement('ul');
                col.items.forEach(sub => {
                    const subLi = document.createElement('li');
                    const subA = document.createElement('a');
                    subA.href = adjustUrlPath(sub.url);
                    subA.className = 'megamenu-item-link';
                    subA.target = '_blank';
                    
                    const itemContent = `
                        <div class="megamenu-item-header">
                            <span class="sub-emoji">${sub.icon || '🔸'}</span>
                            <span class="megamenu-item-title">${sub.label}</span>
                        </div>
                        ${sub.description ? `<p class="megamenu-item-desc">${sub.description}</p>` : ''}
                    `;
                    subA.innerHTML = itemContent;
                    subLi.appendChild(subA);
                    ul.appendChild(subLi);
                });
                column.appendChild(ul);
                columnsContainer.appendChild(column);
            });
            megamenu.appendChild(columnsContainer);
            
            // Add popular/recommended sidebar panel inside megamenu
            const sidebar = document.createElement('div');
            sidebar.className = 'megamenu-sidebar';
            sidebar.innerHTML = `
                <h5>💡 Recommended Tools</h5>
                <a href="${adjustUrlPath('./Features/Astrology/astrology.html?tab=panchang')}" class="rec-tool">☀️ Dainik Panchang</a>
                <a href="${adjustUrlPath('./Features/Astrology/astrology.html?tab=divisional&varga=D9')}" class="rec-tool">❤️ D9 Navamsa Chart</a>
                <a href="${adjustUrlPath('./Features/Astrology/astrology.html?tab=muhurtas')}" class="rec-tool">✨ Abhijit Muhurta</a>
            `;
            megamenu.appendChild(sidebar);
            li.appendChild(megamenu);
        }

        // Hover close delays and animations handler
        let closeTimeout = null;

        li.addEventListener('mouseenter', () => {
            clearTimeout(closeTimeout);
            // Close other menus instantly
            document.querySelectorAll('.nav-menu-item').forEach(other => {
                if (other !== li) {
                    other.classList.remove('menu-active');
                    other.querySelector('.nav-menu-link')?.setAttribute('aria-expanded', 'false');
                }
            });
            li.classList.add('menu-active');
            a.setAttribute('aria-expanded', 'true');
        });

        li.addEventListener('mouseleave', () => {
            closeTimeout = setTimeout(() => {
                li.classList.remove('menu-active');
                a.setAttribute('aria-expanded', 'false');
            }, 200); // 200ms delay to prevent accidental mouseout closures
        });

        navList.appendChild(li);
    });

    // Replace or insert menu inside Header before controls
    const headerIcons = document.querySelector('.header-icons');
    if (headerIcons) {
        navContainer.insertBefore(navBar, headerIcons);
        navBar.appendChild(navList);
    }
}

// ==========================================
// MOBILE ACCORDION HAMBURGER MENU RENDERING
// ==========================================
// ==========================================
// MOBILE ACCORDION HAMBURGER MENU RENDERING
// ==========================================
let favorites = JSON.parse(localStorage.getItem('shunya-favorites')) || [
    { label: "Dainik Panchang", url: "/home/panchang", icon: "☀️" },
    { label: "Month Panchang", url: "/home/maasik", icon: "🗓️" },
    { label: "Personalized Kundli", url: "/astrology/personal", icon: "🧘" }
];

function getPrettyUrl(rawUrl) {
    if (!rawUrl || rawUrl === '#') return '#';
    try {
        const base = window.location.protocol === 'file:' ? window.location.href : window.location.origin;
        let cleanUrl = rawUrl;
        if (window.location.protocol === 'file:' && rawUrl.startsWith('/')) {
            cleanUrl = '.' + rawUrl;
        }
        const url = new URL(cleanUrl, base);
        const path = url.pathname;
        const tab = url.searchParams.get('tab') || '';
        const region = url.searchParams.get('region') || '';
        const varga = url.searchParams.get('varga') || '';
        
        if (window.location.protocol === 'file:') {
            if (path.includes('Static') && path.includes('index.html')) {
                return 'Static/index.html';
            }
            if (path.includes('Dictionary.html')) {
                return 'Features/Dictionary/Dictionary.html';
            }
            let query = '';
            if (tab) {
                query = `?tab=${tab}`;
            } else if (path.includes('astrology.html')) {
                query = `?tab=panchang`;
            }
            if (region) query += (query ? '&' : '?') + `region=${region}`;
            if (varga) query += (query ? '&' : '?') + `varga=${varga}`;
            return 'index.html' + query;
        }

        let pretty = '/';
        if (path.includes('astrology.html')) {
            if (tab === 'panchang' || tab === 'maasik' || tab === 'muhurtas') {
                pretty = `/home/${tab}`;
            } else {
                pretty = `/astrology/${tab || 'personal'}`;
            }
        } else if (path.includes('Dictionary.html')) {
            pretty = '/dictionary';
        } else if (path.includes('/Static/') && path.includes('index.html')) {
            pretty = '/wisdom';
        }
        
        const q = [];
        if (region) q.push(`region=${region}`);
        if (varga) q.push(`varga=${varga}`);
        if (q.length > 0) {
            pretty += '?' + q.join('&');
        }
        return pretty;
    } catch(e) {
        return rawUrl;
    }
}

function saveFavorites() {
    localStorage.setItem('shunya-favorites', JSON.stringify(favorites));
}

function isFavorite(url) {
    return favorites.some(f => f.url === url);
}

function toggleFavorite(item) {
    const idx = favorites.findIndex(f => f.url === item.url);
    if (idx > -1) {
        favorites.splice(idx, 1);
    } else {
        favorites.push({ label: item.label, url: item.url, icon: item.icon });
    }
    saveFavorites();
    const accordion = document.getElementById('drawerAccordion');
    if (accordion && window.lastMenuItems) {
        renderDrawerContent(accordion, window.lastMenuItems);
    }
    const sidebarAccordion = document.getElementById('sidebarAccordion');
    if (sidebarAccordion && window.lastMenuItems) {
        renderDrawerContent(sidebarAccordion, window.lastMenuItems);
    }
}

function renderDrawerContent(accordionContainer, menuItems) {
    accordionContainer.innerHTML = '';

    // 1. Favourites Section
    const favGroup = document.createElement('div');
    favGroup.className = 'accordion-group active'; // Expand by default

    const favTrigger = document.createElement('button');
    favTrigger.className = 'accordion-trigger';
    favTrigger.style.background = 'rgba(251,191,36,0.06)';
    favTrigger.innerHTML = `<span style="color:#fbbf24; font-weight:800;">⭐ Favourites</span> <span class="arrow">▼</span>`;
    favGroup.appendChild(favTrigger);

    const favContent = document.createElement('div');
    favContent.className = 'accordion-content';
    favContent.style.display = 'block';

    if (favorites.length === 0) {
        favContent.innerHTML = `<div style="padding:12px 15px; font-size:0.8rem; color:var(--text-muted); font-style:italic;">No favorites added yet. Right-click any link or tap the star icon to add.</div>`;
    } else {
        const ul = document.createElement('ul');
        ul.className = 'favorites-list';
        favorites.forEach(f => {
            const li = document.createElement('li');
            li.className = 'fav-draggable-item';
            li.setAttribute('draggable', 'true');
            li.setAttribute('data-url', f.url);
            li.style.cssText = 'display:flex; align-items:center; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:8px 12px; margin-bottom:6px; border-radius:6px; cursor:grab;';
            
            li.innerHTML = `
                <span class="drag-handle" style="margin-right:8px; cursor:move; color:rgba(255,255,255,0.25); user-select:none;">☰</span>
                <a href="${f.url}" class="accordion-subitem-link" data-label="${f.label}" data-icon="${f.icon}" style="flex:1; display:flex; align-items:center; text-decoration:none; color:var(--text-color); font-size:0.85rem; font-weight:600;">
                    <span style="margin-right:6px;">${f.icon}</span> ${f.label}
                </a>
                <span class="star-toggle" data-url="${f.url}" data-label="${f.label}" data-icon="${f.icon}" style="cursor:pointer; color:#fbbf24; font-size:1.15rem; padding: 2px 5px;">★</span>
            `;
            ul.appendChild(li);
        });
        favContent.appendChild(ul);
    }
    favGroup.appendChild(favContent);
    accordionContainer.appendChild(favGroup);

    // 2. Add Regular Categories
    menuItems.forEach((item) => {
        const group = document.createElement('div');
        group.className = 'accordion-group';

        const trigger = document.createElement('button');
        trigger.className = 'accordion-trigger';
        trigger.innerHTML = `<span>${item.icon} ${item.label}</span> <span class="arrow">▼</span>`;
        group.appendChild(trigger);

        const content = document.createElement('div');
        content.className = 'accordion-content';

        if (item.type === 'dropdown' && item.items) {
            const ul = document.createElement('ul');
            item.items.forEach(sub => {
                const li = document.createElement('li');
                const pretty = getPrettyUrl(sub.url);
                const isFav = isFavorite(pretty);
                
                li.style.cssText = 'display:flex; align-items:center; justify-content:space-between; padding:4px 0;';
                li.innerHTML = `
                    <a href="${pretty}" class="accordion-subitem-link" data-label="${sub.label}" data-icon="${sub.icon || '🔸'}" style="flex:1; display:flex; align-items:center; text-decoration:none; color:var(--text-color); font-size:0.85rem; font-weight:600; padding:6px 0;">
                        <span style="margin-right:6px;">${sub.icon || '🔸'}</span> ${sub.label}
                    </a>
                    <span class="star-toggle" data-url="${pretty}" data-label="${sub.label}" data-icon="${sub.icon || '🔸'}" style="cursor:pointer; color:${isFav ? '#fbbf24' : 'rgba(255,255,255,0.15)'}; font-size:1.15rem; padding: 2px 5px;">${isFav ? '★' : '☆'}</span>
                `;
                ul.appendChild(li);
            });
            content.appendChild(ul);
        } else if (item.type === 'megamenu' && item.columns) {
            item.columns.forEach(col => {
                const colTitle = document.createElement('div');
                colTitle.className = 'accordion-col-title';
                colTitle.style.cssText = 'font-size:0.75rem; text-transform:uppercase; color:var(--accent-color); font-weight:800; padding:8px 0 4px; border-bottom:1px solid rgba(255,255,255,0.05); margin-bottom:6px;';
                colTitle.innerText = col.title || '';
                content.appendChild(colTitle);

                const ul = document.createElement('ul');
                col.items.forEach(sub => {
                    const li = document.createElement('li');
                    const pretty = getPrettyUrl(sub.url);
                    const isFav = isFavorite(pretty);
                    
                    li.style.cssText = 'display:flex; align-items:center; justify-content:space-between; padding:4px 0;';
                    li.innerHTML = `
                        <a href="${pretty}" class="accordion-subitem-link" data-label="${sub.label}" data-icon="${sub.icon || '🔸'}" style="flex:1; display:flex; align-items:center; text-decoration:none; color:var(--text-color); font-size:0.85rem; font-weight:600; padding:6px 0;">
                            <span style="margin-right:6px;">${sub.icon || '🔸'}</span> ${sub.label}
                        </a>
                        <span class="star-toggle" data-url="${pretty}" data-label="${sub.label}" data-icon="${sub.icon || '🔸'}" style="cursor:pointer; color:${isFav ? '#fbbf24' : 'rgba(255,255,255,0.15)'}; font-size:1.15rem; padding: 2px 5px;">${isFav ? '★' : '☆'}</span>
                    `;
                    ul.appendChild(li);
                });
                content.appendChild(ul);
            });
        } else {
            // direct link
            const pretty = getPrettyUrl(item.url);
            const isFav = isFavorite(pretty);
            trigger.innerHTML = `
                <a href="${pretty}" class="accordion-subitem-link" data-label="${item.label}" data-icon="${item.icon}" style="flex:1; display:flex; align-items:center; text-decoration:none; color:var(--title-color); font-weight:800;">
                    <span style="margin-right:8px;">${item.icon}</span> ${item.label}
                </a>
                <span class="star-toggle" data-url="${pretty}" data-label="${item.label}" data-icon="${item.icon}" style="cursor:pointer; color:${isFav ? '#fbbf24' : 'rgba(255,255,255,0.15)'}; font-size:1.15rem; padding: 2px 5px; margin-left:auto;">${isFav ? '★' : '☆'}</span>
            `;
            trigger.style.display = 'flex';
            trigger.style.alignItems = 'center';
        }

        group.appendChild(content);
        accordionContainer.appendChild(group);

        // Accordion Header Toggle logic
        trigger.addEventListener('click', (e) => {
            if (e.target.closest('.star-toggle') || e.target.closest('a')) return;
            const isActive = group.classList.contains('active');
            
            // Collapse other accordion groups (excluding favorites if it's the target)
            accordionContainer.querySelectorAll('.accordion-group').forEach(g => {
                if (g !== group) {
                    g.classList.remove('active');
                    const c = g.querySelector('.accordion-content');
                    if (c) c.style.display = 'none';
                }
            });
            
            if (isActive) {
                group.classList.remove('active');
                content.style.display = 'none';
            } else {
                group.classList.add('active');
                content.style.display = 'block';
            }
        });
    });

    // Attach click triggers to star-toggles
    accordionContainer.querySelectorAll('.star-toggle').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const url = btn.getAttribute('data-url');
            const label = btn.getAttribute('data-label');
            const icon = btn.getAttribute('data-icon');
            toggleFavorite({ label, url, icon });
        });
    });

    // Attach Drag and Drop handlers
    const dragItems = accordionContainer.querySelectorAll('.fav-draggable-item');
    dragItems.forEach(item => {
        item.addEventListener('dragstart', handleDragStart, false);
        item.addEventListener('dragenter', handleDragEnter, false);
        item.addEventListener('dragover', handleDragOver, false);
        item.addEventListener('dragleave', handleDragLeave, false);
        item.addEventListener('drop', handleDrop, false);
        item.addEventListener('dragend', handleDragEnd, false);
    });
}

function handleDragStart(e) {
    window.dragSrcEl = this;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
    this.style.opacity = '0.4';
}

function handleDragOver(e) {
    if (e.preventDefault) e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    return false;
}

function handleDragEnter(e) {
    this.classList.add('over');
}

function handleDragLeave(e) {
    this.classList.remove('over');
}

function handleDrop(e) {
    e.stopPropagation();
    e.preventDefault();
    if (window.dragSrcEl !== this) {
        const srcUrl = window.dragSrcEl.getAttribute('data-url');
        const targetUrl = this.getAttribute('data-url');
        
        const srcIdx = favorites.findIndex(f => f.url === srcUrl);
        const targetIdx = favorites.findIndex(f => f.url === targetUrl);
        
        if (srcIdx > -1 && targetIdx > -1) {
            const temp = favorites[srcIdx];
            favorites.splice(srcIdx, 1);
            favorites.splice(targetIdx, 0, temp);
            saveFavorites();
            const accordion = document.getElementById('drawerAccordion');
            if (accordion && window.lastMenuItems) {
                renderDrawerContent(accordion, window.lastMenuItems);
            }
            const sidebarAccordion = document.getElementById('sidebarAccordion');
            if (sidebarAccordion && window.lastMenuItems) {
                renderDrawerContent(sidebarAccordion, window.lastMenuItems);
            }
        }
    }
    return false;
}

function handleDragEnd(e) {
    this.style.opacity = '1.0';
    document.querySelectorAll('.fav-draggable-item').forEach(item => {
        item.classList.remove('over');
    });
}

function renderMobileNav(menuItems) {
    window.lastMenuItems = menuItems;
    const accordion = document.getElementById('drawerAccordion');
    if (accordion) {
        renderDrawerContent(accordion, menuItems);
    }

    const sidebarAccordion = document.getElementById('sidebarAccordion');
    if (sidebarAccordion) {
        renderDrawerContent(sidebarAccordion, menuItems);
    }

    // Setup Hamburger and Drawer triggers
    const hamburgerBtn = document.querySelector('.menu-icon');
    const drawerMenu = document.getElementById('leftDrawerMenu');
    const overlay = document.getElementById('leftDrawerOverlay');
    const closeBtn = document.getElementById('leftDrawerCloseBtn');

    if (hamburgerBtn && drawerMenu && overlay) {
        hamburgerBtn.onclick = (e) => {
            e.preventDefault();
            if (window.innerWidth > 900) {
                const grid = document.querySelector('.homepage-three-column-grid');
                const sidebar = document.getElementById('leftMenuSidebar');
                if (grid && sidebar) {
                    const isCollapsed = sidebar.classList.toggle('collapsed');
                    grid.classList.toggle('sidebar-collapsed', isCollapsed);
                    localStorage.setItem('sidebar-collapsed', isCollapsed ? 'true' : 'false');
                }
            } else {
                drawerMenu.classList.add('active');
                overlay.classList.add('active');
            }
        };

        const closeDrawer = () => {
            drawerMenu.classList.remove('active');
            overlay.classList.remove('active');
        };

        overlay.onclick = closeDrawer;
        if (closeBtn) closeBtn.onclick = closeDrawer;
    }

    // Persistent sidebar collapse state on load for desktop
    if (window.innerWidth > 900) {
        const grid = document.querySelector('.homepage-three-column-grid');
        const sidebar = document.getElementById('leftMenuSidebar');
        if (grid && sidebar) {
            const savedCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
            if (savedCollapsed) {
                sidebar.classList.add('collapsed');
                grid.classList.add('sidebar-collapsed');
            }
        }
    }
    
    // Right Click Custom Context Menu for Desktop
    document.addEventListener('contextmenu', (e) => {
        const link = e.target.closest('.accordion-subitem-link');
        if (link && drawerMenu.classList.contains('active')) {
            e.preventDefault();
            const url = link.getAttribute('href');
            const label = link.dataset.label;
            const icon = link.dataset.icon;
            
            const ctxMenu = document.getElementById('customContextMenu');
            if (ctxMenu) {
                ctxMenu.style.display = 'block';
                ctxMenu.style.left = `${e.clientX}px`;
                ctxMenu.style.top = `${e.clientY}px`;
                
                const isFav = isFavorite(url);
                const act = document.getElementById('ctxFavAction');
                if (act) {
                    act.textContent = isFav ? '⭐ Remove from Favourites' : '⭐ Add to Favourites';
                    act.onclick = () => {
                        toggleFavorite({ label, url, icon });
                        ctxMenu.style.display = 'none';
                    };
                }
            }
        } else {
            const ctxMenu = document.getElementById('customContextMenu');
            if (ctxMenu) ctxMenu.style.display = 'none';
        }
    });

    document.addEventListener('click', () => {
        const ctxMenu = document.getElementById('customContextMenu');
        if (ctxMenu) ctxMenu.style.display = 'none';
    });
}

// Adjust URL path dynamically depending on current page level (root vs Features/Astrology/)
function adjustUrlPath(url) {
    if (!url || url === '#') return '#';
    const isFeaturesPage = window.location.pathname.includes('/Features/');
    if (isFeaturesPage) {
        // If url starts with "./Features/", strip the dot and prefix with "../"
        if (url.startsWith('./Features/')) {
            return url.replace('./Features/', '../');
        }
        // If url starts with "./", replace with "../../"
        if (url.startsWith('./')) {
            return url.replace('./', '../../');
        }
    }
    return url;
}

// ==========================================
// BREADCRUMBS GENERATION
// ==========================================
function setupBreadcrumbs(menuItems) {
    // Target the header breadcrumb element
    let container = document.getElementById('header-breadcrumb');
    if (!container) return;

    const currentUrl = window.location.href;
    const currentTab = getQueryParam('tab');
    const currentVarga = getQueryParam('varga');
    const currentRegion = getQueryParam('region');

    let crumbs = [{ label: '🏠 Home', url: adjustUrlPath('./index.html') }];
    let found = false;

    // Search inside menu items to find match
    for (const item of menuItems) {
        if (item.type === 'dropdown' && item.items) {
            for (const sub of item.items) {
                if (urlMatches(sub.url, currentUrl, currentTab, currentVarga, currentRegion)) {
                    crumbs.push({ label: item.label, url: 'javascript:void(0)' });
                    crumbs.push({ label: sub.label, url: adjustUrlPath(sub.url) });
                    found = true;
                    break;
                }
            }
        } else if (item.type === 'megamenu' && item.columns) {
            for (const col of item.columns) {
                for (const sub of col.items) {
                    if (urlMatches(sub.url, currentUrl, currentTab, currentVarga, currentRegion)) {
                        crumbs.push({ label: item.label, url: 'javascript:void(0)' });
                        if (col.title) crumbs.push({ label: col.title, url: 'javascript:void(0)' });
                        crumbs.push({ label: sub.label, url: adjustUrlPath(sub.url) });
                        found = true;
                        break;
                    }
                }
                if (found) break;
            }
        }
        if (found) break;
    }

    // Render breadcrumbs
    container.innerHTML = crumbs.map((c, idx) => {
        const isLast = idx === crumbs.length - 1;
        if (isLast) return `<span class="crumb-active" aria-current="page" style="color: var(--accent-color); font-weight: 700;">${c.label}</span>`;
        return `<a href="${c.url}" class="crumb-link" style="color: var(--text-muted); text-decoration: none;">${c.label}</a> <span class="crumb-sep" style="margin: 0 4px; color: var(--text-muted);">/</span>`;
    }).join(' ');
}

function urlMatches(menuUrl, currentUrl, tab, varga, region) {
    if (!menuUrl || menuUrl === '#') return false;
    
    const menuTab = getUrlParam(menuUrl, 'tab');
    const menuVarga = getUrlParam(menuUrl, 'varga');
    const menuRegion = getUrlParam(menuUrl, 'region');

    if (menuTab !== tab) return false;
    if (menuVarga && menuVarga !== varga) return false;
    if (menuRegion && menuRegion !== region) return false;
    
    return true;
}

function getQueryParam(param) {
    return new URLSearchParams(window.location.search).get(param);
}

function getUrlParam(urlStr, param) {
    try {
        const qIndex = urlStr.indexOf('?');
        if (qIndex === -1) return null;
        const searchParams = new URLSearchParams(urlStr.substring(qIndex));
        return searchParams.get(param);
    } catch (e) {
        return null;
    }
}

// ==========================================
// GLOBAL SEARCH OVERLAY & RESULTS ENGINE
// ==========================================
function setupSearch(menuItems) {
    // Inject Search Overlay modal
    const overlay = document.createElement('div');
    overlay.id = 'globalSearchOverlay';
    overlay.className = 'search-overlay-modal';
    overlay.innerHTML = `
        <div class="search-overlay-card">
            <div class="search-overlay-header">
                <h3>🔍 Jyotish Knowledge Search</h3>
                <button id="closeSearchBtn">✕</button>
            </div>
            <div class="search-overlay-input-wrap">
                <input type="text" id="globalSearchInput" placeholder="Search Panchang terms, Yogas, Dashas, Planets, Nakshatras..." autofocus>
            </div>
            <div id="globalSearchResults" class="search-results-list">
                <div class="search-placeholder-msg">Type to search across the entire Jyotish research suite...</div>
            </div>
        </div>
    `;
    const header = document.querySelector('header');
    if (header) {
        header.insertAdjacentElement('afterend', overlay);
    } else {
        document.body.appendChild(overlay);
    }

    const searchInput = document.getElementById('globalSearchInput');
    const resultsContainer = document.getElementById('globalSearchResults');

    // Gather flat list of all searchable links
    const flatItems = [];
    menuItems.forEach(item => {
        if (item.type === 'dropdown' && item.items) {
            item.items.forEach(sub => {
                flatItems.push({ label: sub.label, url: sub.url, category: item.label, description: sub.description || `Access the ${sub.label} tool` });
            });
        } else if (item.type === 'megamenu' && item.columns) {
            item.columns.forEach(col => {
                col.items.forEach(sub => {
                    flatItems.push({ label: sub.label, url: sub.url, category: `${item.label} (${col.title || ''})`, description: sub.description || `Access the ${sub.label} tool` });
                });
            });
        } else {
            flatItems.push({ label: item.label, url: item.url, category: 'Main', description: `Explore ${item.label}` });
        }
    });

    // Add extra commonly searched terms to improve matches
    flatItems.push(
        { label: "Rahu Kalam", url: "./Features/Astrology/astrology.html?tab=muhurtas", category: "Muhurta", description: "Vedic daily Rahu duration periods" },
        { label: "Brahma Muhurta", url: "./Features/Astrology/astrology.html?tab=muhurtas", category: "Muhurta", description: "Vedic spiritual hours before dawn" },
        { label: "Abhijit Muhurta", url: "./Features/Astrology/astrology.html?tab=muhurtas", category: "Muhurta", description: "Most auspicious midday solar hour" },
        { label: "D9 Navamsa Chart", url: "./Features/Astrology/astrology.html?tab=divisional&varga=D9", category: "Kundli (Divisional Charts)", description: "Marriage, spouse & path of destiny" },
        { label: "Vimshottari Dasha", url: "./Features/Astrology/astrology.html?tab=dasha", category: "Dasha", description: "120-year planetary progression cycle calculations" }
    );

    // Bind Search input keyup
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim().toLowerCase();
        if (!query) {
            resultsContainer.innerHTML = `<div class="search-placeholder-msg">Type to search across the entire Jyotish research suite...</div>`;
            return;
        }

        const filtered = flatItems.filter(item => 
            item.label.toLowerCase().includes(query) || 
            item.category.toLowerCase().includes(query) || 
            item.description.toLowerCase().includes(query)
        );

        if (filtered.length === 0) {
            resultsContainer.innerHTML = `<div class="search-empty-msg">No results matching "${searchInput.value}" found. Try search keys like "D9", "Tithi", "Rahu", "Muhurta".</div>`;
            return;
        }

        resultsContainer.innerHTML = filtered.map(item => `
            <a href="${adjustUrlPath(item.url)}" class="search-result-item" target="_blank">
                <div class="result-badge">${item.category}</div>
                <div class="result-title">${item.label}</div>
                <div class="result-desc">${item.description}</div>
            </a>
        `).join('');
    });

    // Bind Toggle Button click
    // Scan headers inside index.html and children to bind search buttons dynamically
    const bindSearchButtons = () => {
        const searchSpans = document.querySelectorAll('.header-icons span, .header-icons i, #searchBtn');
        searchSpans.forEach(span => {
            if (span.innerText === '🔍' || span.classList.contains('fa-search') || span.id === 'searchBtn') {
                span.style.cursor = 'pointer';
                span.onclick = (e) => {
                    e.preventDefault();
                    overlay.classList.add('active');
                    searchInput.value = '';
                    resultsContainer.innerHTML = `<div class="search-placeholder-msg">Type to search across the entire Jyotish research suite...</div>`;
                    setTimeout(() => searchInput.focus(), 150);
                };
            }
        });
    };

    bindSearchButtons();
    
    // Close handles
    document.getElementById('closeSearchBtn').onclick = () => overlay.classList.remove('active');
    overlay.onclick = (e) => { if (e.target === overlay) overlay.classList.remove('active'); };
}

// ==========================================
// DARK THEME / LIGHT THEME TOGGLE ENGINE
// ==========================================
function applyTheme(themeId) {
    document.body.classList.remove('theme-dark', 'theme-bright', 'dark-theme');
    document.body.classList.add(themeId);
    if (themeId === 'theme-dark') {
        document.body.classList.add('dark-theme');
    }
    localStorage.setItem('shunya-theme-name', themeId);
}

function setupThemeToggle() {
    const headerIcons = document.querySelector('.header-icons');
    if (!headerIcons) return;

    let themeToggleBtn = document.getElementById('themeToggleBtn');
    if (!themeToggleBtn) {
        themeToggleBtn = document.createElement('span');
        themeToggleBtn.id = 'themeToggleBtn';
        themeToggleBtn.style.cursor = 'pointer';
        themeToggleBtn.innerText = '🌓';
        headerIcons.insertBefore(themeToggleBtn, headerIcons.firstChild);
    }

    const hr = new Date().getHours();
    const autoDefaultTheme = (hr >= 6 && hr < 18) ? 'theme-bright' : 'theme-dark';
    const savedTheme = localStorage.getItem('shunya-theme-name');
    const activeTheme = ['theme-bright', 'theme-dark'].includes(savedTheme) ? savedTheme : autoDefaultTheme;
    applyTheme(activeTheme);

    themeToggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        
        let existingDropdown = document.querySelector('.theme-dropdown-panel');
        if (existingDropdown) {
            existingDropdown.remove();
            return;
        }

        const dropdown = document.createElement('div');
        dropdown.className = 'theme-dropdown-panel';
        
        const themesList = [
            { id: 'theme-bright', name: '☀️ Surya Aarti (Bright)', bg: '#fff8dc' },
            { id: 'theme-dark', name: '🌌 Dark Mode', bg: '#0d1117' }
        ];

        themesList.forEach(t => {
            const item = document.createElement('div');
            item.className = 'theme-dropdown-item';
            item.innerHTML = `
                <span class="theme-preview-dot" style="background: ${t.bg}; border: 1px solid rgba(255,255,255,0.2); width: 14px; height: 14px; border-radius: 50%; display: inline-block;"></span>
                <span>${t.name}</span>
            `;
            item.addEventListener('click', () => {
                applyTheme(t.id);
                showSnackbarNotification(`${t.name} Activated`);
                dropdown.remove();
            });
            dropdown.appendChild(item);
        });

        document.body.appendChild(dropdown);

        const rect = themeToggleBtn.getBoundingClientRect();
        dropdown.style.top = `${rect.bottom + 8}px`;
        dropdown.style.left = `${Math.max(8, rect.right - 210)}px`;
        
        const closeDropdown = (event) => {
            if (!dropdown.contains(event.target) && event.target !== themeToggleBtn) {
                dropdown.remove();
                document.removeEventListener('click', closeDropdown);
            }
        };
        document.addEventListener('click', closeDropdown);
    });
}

function showSnackbarNotification(msg) {
    let snack = document.getElementById('shunya-snackbar');
    if (!snack) {
        snack = document.createElement('div');
        snack.id = 'shunya-snackbar';
        snack.className = 'shunya-snackbar-element';
        document.body.appendChild(snack);
    }
    snack.innerText = msg;
    snack.classList.add('show');
    setTimeout(() => { snack.classList.remove('show'); }, 3000);
}

// ==========================================
// ACTIVE NAVIGATION HIGHLIGHT ENGINE
// ==========================================
function highlightActiveMenu() {
    const currentUrl = window.location.href;
    const currentTab = getQueryParam('tab');
    const currentVarga = getQueryParam('varga');
    const currentRegion = getQueryParam('region');

    const navLinks = document.querySelectorAll('.nav-menu-link, .megamenu-item-link, .dropdown-panel a');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (urlMatches(href, currentUrl, currentTab, currentVarga, currentRegion)) {
            link.classList.add('active');
            
            // Traverse up to find parent navigation list items and highlight them
            let parentMenu = link.closest('.nav-menu-item');
            if (parentMenu) {
                parentMenu.classList.add('parent-active');
                const mainLink = parentMenu.querySelector('.nav-menu-link');
                if (mainLink) mainLink.classList.add('parent-active');
            }
        }
    });
}

// ==========================================
// ACCESSIBILITY & KEYBOARD NAVIGATION (WCAG / ARIA)
// ==========================================
function setupKeyboardAccessibility() {
    // Close overlay searches or dropdowns with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.getElementById('globalSearchOverlay')?.classList.remove('active');
            document.querySelectorAll('.nav-menu-item').forEach(item => {
                item.classList.remove('menu-active');
                item.querySelector('.nav-menu-link')?.setAttribute('aria-expanded', 'false');
            });
        }
    });

    const menuLinks = document.querySelectorAll('.nav-menu-link');
    menuLinks.forEach((link, idx) => {
        link.addEventListener('keydown', (e) => {
            const parent = link.parentElement;
            
            if (e.key === 'ArrowDown' || e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                parent.classList.add('menu-active');
                link.setAttribute('aria-expanded', 'true');
                
                // Focus first sub-item
                const firstSub = parent.querySelector('.dropdown-panel a, .megamenu-item-link');
                if (firstSub) firstSub.focus();
            }

            if (e.key === 'ArrowRight' && idx < menuLinks.length - 1) {
                e.preventDefault();
                menuLinks[idx + 1].focus();
            }

            if (e.key === 'ArrowLeft' && idx > 0) {
                e.preventDefault();
                menuLinks[idx - 1].focus();
            }
        });
    });
}

// ==========================================
// SPA ROUTER IMPLEMENTATION
// ==========================================
let originalHomeHTML = null;

function navigateToPage(page, tab = '', queryParams = {}) {
    const viewport = document.getElementById('spaViewport');
    if (!viewport) return;
    
    window.currentSPAState = { page, tab, queryParams };
    
    // Save original home HTML on first run
    if (!originalHomeHTML) {
        originalHomeHTML = viewport.innerHTML;
    }
    
    // Update URL query parameters for pretty URL routing
    const prettyUrl = buildUrlPath(page, tab, queryParams);
    if (window.location.protocol !== 'file:') {
        try {
            window.history.pushState({}, '', prettyUrl);
        } catch (e) {
            console.warn("pushState blocked under CORS context:", e);
        }
    }
    
    // Toggle displays
    const leftSidebar = document.querySelector('.left-ad-sidebar');
    const rightSidebar = document.querySelector('.right-widgets-sidebar');
    
    // Render the view
    if (page === 'astrology') {
        if (leftSidebar) leftSidebar.style.display = 'none';
        if (rightSidebar) rightSidebar.style.display = 'none';
        
        if (typeof renderAstrologyView === 'function') {
            viewport.innerHTML = renderAstrologyView();
            // Bind all event listeners inside astrology.js
            if (typeof initAstrology === 'function') {
                initAstrology(tab, queryParams);
            }
        }
    } else if (page === 'dictionary') {
        if (leftSidebar) leftSidebar.style.display = 'none';
        if (rightSidebar) rightSidebar.style.display = 'none';
        
        if (typeof renderDictionaryView === 'function') {
            viewport.innerHTML = renderDictionaryView();
            if (typeof initDictionary === 'function') {
                initDictionary();
            }
        }
    } else if (page === 'wisdom') {
        if (leftSidebar) leftSidebar.style.display = 'none';
        if (rightSidebar) rightSidebar.style.display = 'none';
        
        if (typeof renderWisdomView === 'function') {
            viewport.innerHTML = renderWisdomView();
            if (typeof initWisdom === 'function') {
                initWisdom();
            }
        }
    } else {
        // 'home' page
        if (leftSidebar) leftSidebar.style.display = 'block';
        if (rightSidebar) rightSidebar.style.display = 'block';
        
        viewport.innerHTML = originalHomeHTML;
        
        // Re-bind autocomplete inputs and API test events
        if (typeof initGeoComplete === 'function') {
            if (document.getElementById('panchangPlaceInput')) {
                initGeoComplete('panchangPlaceInput', { defaultPlace: 'New Delhi, India' });
            }
            if (document.getElementById('maasikPlaceInput')) {
                initGeoComplete('maasikPlaceInput', { defaultPlace: 'New Delhi, India' });
            }
        }
        if (typeof initApiHelper === 'function') {
            initApiHelper();
        }
        
        // Re-run astrology features binding for panchang on home page
        if (typeof initAstrology === 'function') {
            initAstrology(tab, queryParams);
        }
        
        if (menuConfig && menuConfig.menu) {
            renderMobileNav(menuConfig.menu);
        }
        
        if (tab === 'panchang' || tab === 'maasik' || tab === 'muhurtas') {
            const welcome = document.getElementById('homeWelcomeSection');
            if (welcome) welcome.style.display = 'none';
            const controlsCard = document.querySelector('.controls-card');
            const routerHeader = document.querySelector('.panchang-unified-header');
            if (controlsCard) controlsCard.style.display = 'flex';
            if (routerHeader) routerHeader.style.display = 'flex';
            
            if (tab === 'panchang') {
                if (typeof switchPancView === 'function') switchPancView('day');
            } else if (tab === 'maasik') {
                if (typeof switchPancView === 'function') switchPancView('month');
            } else if (tab === 'muhurtas') {
                if (typeof switchPancView === 'function') switchPancView('muhurtas');
            }
        } else {
            const welcome = document.getElementById('homeWelcomeSection');
            if (welcome) welcome.style.display = 'block';
            const controlsCard = document.querySelector('.controls-card');
            const routerHeader = document.querySelector('.panchang-unified-header');
            const dayViewHome = document.getElementById('dayViewContainer');
            const maasikViewHome = document.getElementById('maasikViewContainer');
            const muhurtasViewHome = document.getElementById('muhurtasViewContainer');
            
            if (controlsCard) controlsCard.style.display = 'none';
            if (routerHeader) routerHeader.style.display = 'none';
            if (dayViewHome) dayViewHome.style.display = 'none';
            if (maasikViewHome) maasikViewHome.style.display = 'none';
            if (muhurtasViewHome) muhurtasViewHome.style.display = 'none';
        }
    }
    
    highlightActiveMenu();
}

// Global popstate history back/forward support
window.addEventListener('popstate', () => {
    const parsed = parseUrlPath(new URL(window.location.href));
    navigateToPage(parsed.page, parsed.tab, parsed.queryParams);
});

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    
    // Read page from URL path on load
    const parsed = parseUrlPath(new URL(window.location.href));
    
    setTimeout(() => {
        navigateToPage(parsed.page, parsed.tab, parsed.queryParams);
    }, 100);

    // Dynamic SEO about-panchang-box click bindings
    document.addEventListener('click', (e) => {
        const aboutBox = document.querySelector('.about-panchang-box');
        if (aboutBox) {
            if (aboutBox.contains(e.target)) {
                aboutBox.classList.add('expanded');
            } else {
                aboutBox.classList.remove('expanded');
            }
        }
    });
});

// Intercept clicks on links for SPA
document.addEventListener('click', (e) => {
    const anchor = e.target.closest('a');
    if (!anchor) return;
    
    const href = anchor.getAttribute('href');
    if (!href) return;
    
    // Skip external links or target=_blank links
    if (anchor.getAttribute('target') === '_blank') return;

    // Check if it's an internal link managed by our SPA pretty URLs
    let isInternal = false;
    try {
        const base = window.location.protocol === 'file:' ? window.location.href : window.location.origin;
        const parsed = new URL(href, base);
        const parsedOrigin = parsed.protocol === 'file:' ? 'file:' : parsed.origin;
        const localOrigin = window.location.protocol === 'file:' ? 'file:' : window.location.origin;
        
        if (parsedOrigin === localOrigin) {
            const path = parsed.pathname.toLowerCase();
            // Exclude assets, robots, sitemap, auth, and list_events
            if (!path.includes('.') || path.endsWith('.html') || path.endsWith('.htm')) {
                if (!path.includes('/api/') && !path.includes('/userlog/') && !path.includes('list_events.html')) {
                    isInternal = true;
                }
            }
        }
    } catch(err) {
        if (!href.startsWith('http') && !href.startsWith('mailto:') && !href.startsWith('tel:') && href !== '#') {
            isInternal = true;
        }
    }
    
    if (isInternal) {
        e.preventDefault();
        try {
            const base = window.location.protocol === 'file:' ? window.location.href : window.location.origin;
            const parsed = new URL(href, base);
            const { page, tab, queryParams } = parseUrlPath(parsed);
            navigateToPage(page, tab, queryParams);
        } catch(err) {
            console.error("Navigation click handling failed:", err);
        }
    }
});
