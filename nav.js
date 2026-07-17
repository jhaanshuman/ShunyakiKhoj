/**
 * Professional Navigation System & Dynamic Menu Renderer
 * Designed for Shunyakikhoj
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
});

let menuConfig = null;
let currentActiveItem = null;

async function initNavigation() {
    try {
        // Find if config path needs context prefix
        const configPath = window.location.pathname.includes('/Features/') ? '../../nav_config.json' : './nav_config.json';
        const res = await fetch(configPath);
        menuConfig = await res.json();
        
        // Render menus
        renderDesktopNav(menuConfig.menu);
        renderMobileNav(menuConfig.menu);
        
        // Setup Search, Theme Toggle, Breadcrumbs & Accessibility
        setupSearch(menuConfig.menu);
        setupThemeToggle();
        setupBreadcrumbs(menuConfig.menu);
        setupKeyboardAccessibility();
        highlightActiveMenu();
    } catch (e) {
        console.error("Failed to load navigation configuration:", e);
    }
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
function renderMobileNav(menuItems) {
    const mobileMenuContainer = document.querySelector('.mobile-menu');
    if (!mobileMenuContainer) return;

    // Clear existing static items
    mobileMenuContainer.innerHTML = '';

    const header = document.createElement('div');
    header.className = 'mobile-menu-header';
    header.innerHTML = `
        <h3>Navigation Menu</h3>
        <button id="mobileMenuClose" aria-label="Close mobile menu">✕</button>
    `;
    mobileMenuContainer.appendChild(header);

    const accordion = document.createElement('div');
    accordion.className = 'mobile-accordion';

    menuItems.forEach((item, idx) => {
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
                const a = document.createElement('a');
                a.href = adjustUrlPath(sub.url);
                a.target = '_blank';
                a.innerHTML = `${sub.icon || '🔸'} ${sub.label}`;
                li.appendChild(a);
                ul.appendChild(li);
            });
            content.appendChild(ul);
        } else if (item.type === 'megamenu' && item.columns) {
            item.columns.forEach(col => {
                const colTitle = document.createElement('div');
                colTitle.className = 'accordion-col-title';
                colTitle.innerText = col.title || '';
                content.appendChild(colTitle);

                const ul = document.createElement('ul');
                col.items.forEach(sub => {
                    const li = document.createElement('li');
                    const a = document.createElement('a');
                    a.href = adjustUrlPath(sub.url);
                    a.target = '_blank';
                    a.innerHTML = `${sub.icon || '🔸'} ${sub.label}`;
                    li.appendChild(a);
                    ul.appendChild(li);
                });
                content.appendChild(ul);
            });
        } else {
            // direct link
            trigger.onclick = () => { window.location.href = adjustUrlPath(item.url); };
        }

        group.appendChild(content);
        accordion.appendChild(group);

        // Toggle Accordion Click
        trigger.addEventListener('click', () => {
            const isActive = group.classList.contains('active');
            // collapse others
            document.querySelectorAll('.accordion-group').forEach(g => g.classList.remove('active'));
            if (!isActive) {
                group.classList.add('active');
            }
        });
    });

    mobileMenuContainer.appendChild(accordion);

    // Setup hamburger trigger toggle
    const hamburgerBtn = document.querySelector('.menu-icon');
    const overlay = document.querySelector('.menu-overlay');

    if (hamburgerBtn && overlay) {
        hamburgerBtn.onclick = () => {
            mobileMenuContainer.classList.add('active');
            overlay.classList.add('active');
        };

        overlay.onclick = () => {
            mobileMenuContainer.classList.remove('active');
            overlay.classList.remove('active');
        };

        const closeBtn = document.getElementById('mobileMenuClose');
        if (closeBtn) {
            closeBtn.onclick = () => {
                mobileMenuContainer.classList.remove('active');
                overlay.classList.remove('active');
            };
        }
    }
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
    document.body.appendChild(overlay);

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
    document.body.classList.remove('theme-dark', 'theme-manuscript', 'theme-bright', 'theme-focus', 'theme-pale', 'theme-indigo', 'dark-theme');
    document.body.classList.add(themeId);
    if (['theme-dark', 'theme-focus', 'theme-indigo'].includes(themeId)) {
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

    const savedTheme = localStorage.getItem('shunya-theme-name') || 'theme-focus';
    applyTheme(savedTheme);

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
            { id: 'theme-dark', name: '🌌 Dark Mode', bg: '#0d1117' },
            { id: 'theme-manuscript', name: '📜 Yellow Manuscript', bg: '#fdfaf2' },
            { id: 'theme-bright', name: '☀️ Bright & Clean', bg: '#f8fafc' },
            { id: 'theme-focus', name: '👁️ Focus Mode', bg: '#09090b' },
            { id: 'theme-pale', name: '🍃 Slightly Pale', bg: '#fafafa' },
            { id: 'theme-indigo', name: '🍇 Royal Indigo', bg: '#030712' }
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
        dropdown.style.top = `${rect.bottom + window.scrollY + 10}px`;
        dropdown.style.left = `${rect.left + window.scrollX - 100}px`;
        
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
