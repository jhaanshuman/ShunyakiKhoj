// ===== DATA STORE (12+ CATEGORIES, 11,100+ WISDOM ITEMS) =====
const categories = [
    { id: 'festival', name: 'Festival Calendar', icon: '📅', color: '#FF6B35', glow: 'rgba(255, 107, 53, 0.2)', description: 'Sacred festivals, auspicious timings, and historical celebrations of Sanatana Dharma' },
    { id: 'vrat', name: 'Vrat & Upavaas', icon: '🪔', color: '#FF9500', glow: 'rgba(255, 149, 0, 0.2)', description: 'Fasting rituals and spiritual observances for purification and divine grace' },
    { id: 'vrat_katha', name: 'Vrat Katha', icon: '📖', color: '#FFD700', glow: 'rgba(255, 215, 0, 0.2)', description: 'Sacred stories, recitations, stotras, and readings of holy scriptures' },
    { id: 'puja', name: 'Puja Vidhi', icon: '🙏', color: '#AF52DE', glow: 'rgba(175, 82, 222, 0.2)', description: 'Sacred worship rituals and procedures for various deities and occasions' },
    { id: 'mantra', name: 'Vedic Mantra', icon: '📿', color: '#5856D6', glow: 'rgba(88, 86, 214, 0.2)', description: 'Sacred Sanskrit chants and hymns for meditation and spiritual power' },
    { id: 'yantra', name: 'Deity Yantra', icon: '🔯', color: '#FF2D55', glow: 'rgba(255, 45, 85, 0.2)', description: 'Sacred geometric diagrams used for meditation and spiritual practices' },
    { id: 'ritual', name: 'Sanatana Rituals', icon: '🕉️', color: '#34C759', glow: 'rgba(52, 199, 89, 0.2)', description: 'Traditional rites of passage, twilight prayers, and custom rituals' },
    { id: 'upanishads', name: 'Upanishads & Darshanas', icon: '📜', color: '#8B5CF6', glow: 'rgba(139, 92, 246, 0.2)', description: 'The ten Mukhya Upanishads and six orthodox Darshana schools of Vedic philosophy' },
    { id: 'sukta', name: 'Vedic Suktas & Samhitas', icon: '☀️', color: '#F59E0B', glow: 'rgba(245, 158, 11, 0.2)', description: 'Sacred Rigvedic, Yajurvedic, and Atharvavedic hymns for cosmic harmony and peace' },
    { id: 'kavacham', name: 'Sacred Kavachas & Shields', icon: '🛡️', color: '#10B981', glow: 'rgba(16, 185, 129, 0.2)', description: 'Protective armor stotrams for planetary peace, health, and spiritual defense' },
    { id: 'shloka', name: 'Bhagavad Gita & Epics', icon: '📖', color: '#EC4899', glow: 'rgba(236, 72, 153, 0.2)', description: 'Essential shlokas from Srimad Bhagavad Gita, Ramayana, and Mahabharata' },
    { id: 'subhashita', name: 'Subhashitani & Niti Shlokas', icon: '💡', color: '#06B6D4', glow: 'rgba(6, 182, 212, 0.2)', description: 'Timeless Sanskrit moral maxims, Chanakya Niti, and practical wisdom' }
];

// Store for loaded data
const dataStore = {};

// ===== DOM ELEMENTS =====
let categoryGrid, itemsSection, itemsGrid, itemsTitle, itemsCount, backBtn, detailModal, modalBody, modalClose, searchInput, particlesContainer;

// ===== INITIALIZATION =====
window.initWisdom = function() {
    categoryGrid = document.getElementById('categoryGrid');
    itemsSection = document.getElementById('itemsSection');
    itemsGrid = document.getElementById('itemsGrid');
    itemsTitle = document.getElementById('itemsTitle');
    itemsCount = document.getElementById('itemsCount');
    backBtn = document.getElementById('backBtn');
    detailModal = document.getElementById('detailModal');
    modalBody = document.getElementById('modalBody');
    modalClose = document.getElementById('modalClose');
    searchInput = document.getElementById('searchInput');
    particlesContainer = document.getElementById('particles');

    createParticles();
    renderCategories();
    setupEventListeners();
    setupScrollEffects();

    // Check for category query parameters to automatically open that category
    const spaState = window.currentSPAState || {};
    const urlParams = new URLSearchParams(window.location.search);
    const queryCat = (spaState.queryParams && spaState.queryParams.category) || urlParams.get('category');
    if (queryCat) {
        setTimeout(() => {
            loadCategory(queryCat);
        }, 150);
    }
};

// ===== PARTICLES =====
function createParticles() {
    if (particlesContainer) {
        particlesContainer.innerHTML = '';
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDuration = (Math.random() * 15 + 10) + 's';
            particle.style.animationDelay = Math.random() * 10 + 's';
            particle.style.width = (Math.random() * 4 + 2) + 'px';
            particle.style.height = particle.style.width;
            particle.style.opacity = Math.random() * 0.5 + 0.2;
            particlesContainer.appendChild(particle);
        }
    }
}

// ===== RENDER CATEGORIES =====
function renderCategories() {
    if (!categoryGrid) return;
    
    categoryGrid.innerHTML = categories.map((cat, index) => `
        <div class="category-tile fade-in-up stagger-${(index % 6) + 1}" 
             style="--tile-color: ${cat.color}; --tile-glow: ${cat.glow}"
             onclick="loadCategory('${cat.id}')"
             data-category="${cat.id}">
            <div class="tile-shine"></div>
            <div class="tile-icon">${cat.icon}</div>
            <h3 class="tile-name">${cat.name}</h3>
            <p class="tile-count">Loading...</p>
            <p class="tile-description">${cat.description}</p>
        </div>
    `).join('');
    
    // Load counts for each category from window.WisdomDatabase
    categories.forEach(cat => {
        loadCategoryData(cat.id).then(data => {
            const tile = document.querySelector(`[data-category="${cat.id}"] .tile-count`);
            if (tile && data && data.items) {
                tile.textContent = `${data.items.length} Sacred Entries`;
            }
        }).catch(() => {
            const tile = document.querySelector(`[data-category="${cat.id}"] .tile-count`);
            if (tile) tile.textContent = '📂 Load Failed';
        });
    });
}

// ===== LOAD CATEGORY DATA =====
async function loadCategoryData(categoryId) {
    if (dataStore[categoryId]) {
        return dataStore[categoryId];
    }
    
    // Read directly from window.WisdomDatabase without fetch API
    if (window.WisdomDatabase && window.WisdomDatabase[categoryId]) {
        dataStore[categoryId] = window.WisdomDatabase[categoryId];
        return window.WisdomDatabase[categoryId];
    }
    
    // Fallback if database script failed to load
    console.warn(`⚠️ window.WisdomDatabase not loaded, using offline fallback schema for ${categoryId}`);
    const category = categories.find(c => c.id === categoryId);
    const fallbackData = {
        category: category ? category.name : categoryId,
        icon: category ? category.icon : '📿',
        color: category ? category.color : '#5856D6',
        items: [
            {
                id: `${categoryId.substring(0, 2)}001`,
                name: `⚠️ Failed to Load Database`,
                deity: 'Check script loading',
                description: `Consolidated wisdom_database.js was not found or failed to register on the window object.`,
                benefits: ['Verify wisdom_database.js script tag in index.html', 'Check script path exists under Static/data/'],
                error: true
            }
        ]
    };
    dataStore[categoryId] = fallbackData;
    return fallbackData;
}

// ===== LOAD CATEGORY =====
async function loadCategory(categoryId) {
    const category = categories.find(c => c.id === categoryId);
    if (!category) return;
    
    // Show loading state
    if (itemsGrid) {
        itemsGrid.innerHTML = `
            <div class="loading-shimmer" style="height: 200px; border-radius: 20px;"></div>
        `.repeat(6);
    }
    
    // Hide categories, show items
    const catSection = document.querySelector('.categories-section');
    const heroSection = document.querySelector('.hero-section');
    if (catSection) catSection.style.display = 'none';
    if (heroSection) heroSection.style.display = 'none';
    if (itemsSection) itemsSection.classList.add('active');
    
    // Update header
    if (itemsTitle) {
        itemsTitle.textContent = `${category.icon} ${category.name}`;
        itemsTitle.style.color = category.color;
    }
    
    try {
        const data = await loadCategoryData(categoryId);
        if (data && data.items && data.items.length > 0) {
            if (data.items[0] && data.items[0].error) {
                if (itemsCount) itemsCount.textContent = '⚠️ Data Load Error';
                renderItems(data.items, category);
            } else {
                if (itemsCount) itemsCount.textContent = `${data.items.length} Sacred Entries`;
                renderItems(data.items, category);
            }
        } else {
            if (itemsGrid) {
                itemsGrid.innerHTML = `
                    <div class="empty-state" style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: rgba(255,255,255,0.6);">
                        <div style="font-size: 48px; margin-bottom: 20px;">📂</div>
                        <h3 style="color: white; margin-bottom: 10px;">No entries found</h3>
                    </div>
                `;
            }
        }
    } catch (error) {
        console.error('Error loading category:', error);
        if (itemsGrid) {
            itemsGrid.innerHTML = `
                <div class="error-state" style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: rgba(255,255,255,0.6);">
                    <div style="font-size: 48px; margin-bottom: 20px;">⚠️</div>
                    <h3 style="color: white; margin-bottom: 10px;">Unable to load content</h3>
                    <p>Error: ${error.message}</p>
                </div>
            `;
        }
    }
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== RENDER ITEMS =====
function renderItems(items, category) {
    if (!itemsGrid) return;
    if (!items || items.length === 0) {
        itemsGrid.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: rgba(255,255,255,0.6);">
                <div style="font-size: 48px; margin-bottom: 20px;">📿</div>
                <h3 style="color: white; margin-bottom: 10px;">No entries found</h3>
            </div>
        `;
        return;
    }
    
    itemsGrid.innerHTML = items.map((item, index) => {
        const preview = getItemPreview(item, category.id);
        const tags = getItemTags(item, category.id);
        const deityDisplay = item.deity ? `<div class="item-deity">🙏 ${item.deity}</div>` : '';
        const isError = item.error === true;
        
        return `
            <div class="item-card fade-in-up stagger-${(index % 6) + 1}" 
                 style="--item-color: ${isError ? '#FF4444' : category.color}; --item-glow: ${isError ? 'rgba(255,68,68,0.2)' : category.glow}"
                 onclick="${isError ? '' : `showDetail('${item.id}', '${category.id}')`}"
                 ${isError ? 'style="cursor: default; opacity: 0.7;"' : ''}>
                <span class="item-id">#${item.id}</span>
                <h3 class="item-name">${item.name}</h3>
                ${deityDisplay}
                <div class="item-meta">
                    ${tags}
                </div>
                <p class="item-preview">${preview}</p>
                ${isError ? '' : `<span class="item-arrow">→</span>`}
            </div>
        `;
    }).join('');
}

// ===== GET ITEM PREVIEW =====
function getItemPreview(item, categoryId) {
    if (item.error) return item.description || '⚠️ Data loading error';
    return item.hover || item.description || item.purpose || 'Sacred spiritual content';
}

// ===== GET ITEM TAGS =====
function getItemTags(item, categoryId) {
    if (item.error) return `<span class="item-tag">⚠️ Error</span>`;
    
    const tags = [];
    if (item.deity) tags.push(`🙏 ${item.deity}`);
    if (item.duration) tags.push(`⏱ ${item.duration}`);
    if (item.verses) tags.push(`📖 ${item.verses} V`);
    if (item.author) tags.push(`✍️ ${item.author}`);
    if (item.best_time) tags.push(`🌅 ${item.best_time.split(',')[0]}`);
    if (item.type) tags.push(`✨ ${item.type}`);
    
    return tags.slice(0, 3).map(tag => `<span class="item-tag">${tag}</span>`).join('');
}

// ===== SHOW DETAIL MODAL =====
async function showDetail(itemId, categoryId) {
    try {
        const data = await loadCategoryData(categoryId);
        const item = data.items.find(i => i.id === itemId);
        if (!item) {
            console.warn('Item not found:', itemId);
            return;
        }
        
        const category = categories.find(c => c.id === categoryId);
        if (modalBody && detailModal) {
            modalBody.innerHTML = generateDetailHTML(item, category);
            detailModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    } catch (error) {
        console.error('Error showing detail:', error);
    }
}

// ===== GENERATE DETAIL HTML =====
function generateDetailHTML(item, category) {
    if (item.error) {
        return `
            <div class="detail-header" style="text-align: center; padding: 40px 20px;">
                <div style="font-size: 48px; margin-bottom: 20px;">⚠️</div>
                <h2 style="color: #FF4444; margin-bottom: 10px;">Data Load Error</h2>
                <p style="color: rgba(255,255,255,0.7);">${item.description || 'Unable to load data'}</p>
            </div>
        `;
    }
    
    const sections = [];
    
    // Header
    sections.push(`
        <div class="detail-header" style="text-align: center; padding-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
            <div class="detail-icon" style="font-size: 48px; display: block; margin-bottom: 10px;">${category ? category.icon : '📿'}</div>
            <h2 class="detail-name" style="font-size: 24px; color: ${category ? category.color : '#fff'}; margin-bottom: 5px;">${item.name}</h2>
            ${item.deity ? `<p class="detail-deity" style="color: rgba(255,255,255,0.7); font-size: 16px;">✦ ${item.deity}</p>` : ''}
        </div>
    `);
    
    // Helper to add sections
    const addSection = (title, content) => {
        if (content) sections.push(`
            <div class="detail-section" style="margin-bottom: 16px; padding: 12px 16px; background: rgba(255,255,255,0.05); border-radius: 12px; border-left: 3px solid rgba(255,255,255,0.2);">
                <h4 style="font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.6); margin-bottom: 6px;">${title}</h4>
                <p style="color: rgba(255,255,255,0.9); line-height: 1.6; font-size: 15px;">${content}</p>
            </div>
        `);
    };
    
    const addList = (title, listItems) => {
        if (listItems && listItems.length) sections.push(`
            <div class="detail-section" style="margin-bottom: 16px; padding: 12px 16px; background: rgba(255,255,255,0.05); border-radius: 12px; border-left: 3px solid rgba(255,255,255,0.2);">
                <h4 style="font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.6); margin-bottom: 6px;">${title}</h4>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    ${listItems.map(i => `<li style="padding: 4px 0; color: rgba(255,255,255,0.9); display: flex; align-items: center; gap: 8px; font-size: 15px;"><span style="color: rgba(255,215,0,0.6);">✦</span> ${i}</li>`).join('')}
                </ul>
            </div>
        `);
    };
    
    // Display all item fields dynamically
    const displayOrder = [
        'description', 'since_when', 'why_reason', 'belief', 'where', 'how', 
        'text', 'meaning', 'origin', 'author', 'verses', 'language', 'best_time', 
        'duration', 'frequency', 'material', 'placement', 'activation', 'type'
    ];
    
    displayOrder.forEach(key => {
        if (item[key] && typeof item[key] === 'string' && item[key].trim().length > 0) {
            const label = key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
            addSection(label, item[key]);
        }
    });
    
    // Handle benefits as list
    if (item.benefits && item.benefits.length) {
        addList('Benefits', item.benefits);
    }
    
    return sections.join('');
}

// ===== CLOSE MODAL =====
function closeModal() {
    if (detailModal) detailModal.classList.remove('active');
    document.body.style.overflow = '';
}

// ===== GO BACK =====
function goBack() {
    if (itemsSection) itemsSection.classList.remove('active');
    const catSection = document.querySelector('.categories-section');
    const heroSection = document.querySelector('.hero-section');
    if (catSection) catSection.style.display = 'block';
    if (heroSection) heroSection.style.display = 'flex';
    if (searchInput) searchInput.value = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== SEARCH FUNCTIONALITY =====
function handleSearch(query) {
    const trimmedQuery = query.trim().toLowerCase();
    
    if (!trimmedQuery) {
        if (itemsSection && itemsSection.classList.contains('active')) {
            const categoryTitle = itemsTitle.textContent.replace(/[^a-zA-Z\s]/g, '').trim();
            const category = categories.find(c => c.name === categoryTitle);
            if (category) loadCategory(category.id);
        } else {
            document.querySelectorAll('.category-tile').forEach(tile => {
                tile.style.display = 'flex';
            });
        }
        return;
    }
    
    if (itemsSection && itemsSection.classList.contains('active')) {
        const cards = document.querySelectorAll('.item-card');
        let visibleCount = 0;
        cards.forEach(card => {
            const text = card.textContent.toLowerCase();
            const isVisible = text.includes(trimmedQuery);
            card.style.display = isVisible ? 'flex' : 'none';
            if (isVisible) visibleCount++;
        });
        if (itemsCount) itemsCount.textContent = visibleCount === 0 ? 'No matches found' : `${visibleCount} matching entries`;
    } else {
        document.querySelectorAll('.category-tile').forEach(tile => {
            const text = tile.textContent.toLowerCase();
            tile.style.display = text.includes(trimmedQuery) ? 'flex' : 'none';
        });
    }
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    if (backBtn) backBtn.addEventListener('click', goBack);
    if (modalClose) modalClose.addEventListener('click', closeModal);
    if (detailModal) {
        detailModal.addEventListener('click', (e) => {
            if (e.target === detailModal) closeModal();
        });
    }
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
    
    let searchTimeout;
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => handleSearch(e.target.value), 300);
        });
    }
    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = e.target.getAttribute('href');
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            e.target.classList.add('active');
            
            if (target === '#home' || target === '#categories') {
                goBack();
                const categoriesSec = document.getElementById('categories');
                if (categoriesSec) categoriesSec.scrollIntoView({ behavior: 'smooth' });
            } else if (target === '#about') {
                const aboutSec = document.getElementById('about');
                if (aboutSec) aboutSec.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// ===== SCROLL EFFECTS =====
function setupScrollEffects() {
    const header = document.querySelector('.glass-header');
    if (!header) return;
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.background = 'rgba(15, 10, 30, 0.95)';
            header.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.5)';
            header.style.backdropFilter = 'blur(20px)';
        } else {
            header.style.background = 'rgba(15, 10, 30, 0.7)';
            header.style.boxShadow = 'none';
            header.style.backdropFilter = 'blur(10px)';
        }
    });
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.category-tile, .item-card, .feature, .hero-content').forEach(el => {
        if (!el.classList.contains('active')) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        }
    });
}

// ===== EXPOSE FUNCTIONS =====
window.loadCategory = loadCategory;
window.showDetail = showDetail;
window.goBack = goBack;
window.closeModal = closeModal;

console.log('🙏 ShunyakiKhoj - Spiritual Wisdom Portal loaded successfully!');