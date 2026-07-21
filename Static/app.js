// ===== DATA STORE =====
const categories = [
    { id: 'puja-vidhi', name: 'Puja Vidhi', icon: '🙏', color: '#FF6B35', glow: 'rgba(255, 107, 53, 0.2)', description: 'Sacred worship rituals and procedures for various deities and occasions' },
    { id: 'vrat', name: 'Vrat', icon: '🪔', color: '#FF9500', glow: 'rgba(255, 149, 0, 0.2)', description: 'Fasting rituals observed for spiritual purification and divine blessings' },
    { id: 'upavas', name: 'Upavas', icon: '🌿', color: '#34C759', glow: 'rgba(52, 199, 89, 0.2)', description: 'Complete or partial fasting practices for spiritual discipline' },
    { id: 'mantra', name: 'Mantra', icon: '📿', color: '#5856D6', glow: 'rgba(88, 86, 214, 0.2)', description: 'Sacred Sanskrit chants and hymns for meditation and spiritual power' },
    { id: 'stotra', name: 'Stotra', icon: '🕉️', color: '#AF52DE', glow: 'rgba(175, 82, 222, 0.2)', description: 'Devotional hymns and praises composed for various deities' },
    { id: 'ashtakam', name: 'Ashtakam', icon: '✨', color: '#5AC8FA', glow: 'rgba(90, 200, 250, 0.2)', description: 'Eight-verse devotional hymns dedicated to divine beings' },
    { id: 'yantra', name: 'Yantra', icon: '🔯', color: '#FF2D55', glow: 'rgba(255, 45, 85, 0.2)', description: 'Sacred geometric diagrams used for meditation and spiritual practices' },
    { id: 'paath', name: 'Paath', icon: '📖', color: '#FFD700', glow: 'rgba(255, 215, 0, 0.2)', description: 'Sacred recitations and readings of holy scriptures and texts' }
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
};

// ===== PARTICLES =====
function createParticles() {
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

// ===== RENDER CATEGORIES =====
function renderCategories() {
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
    
    // Load counts for each category
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

const OFFLINE_WISDOM_DATA = {
    "puja-vidhi": {
        items: [
            { id: "pv001", name: "Ganesha Puja Vidhi", deity: "Lord Ganesha", description: "Complete step-by-step rituals to worship Lord Ganesha for removing obstacles.", benefits: ["Removes obstacles", "Brings prosperity", "Success in new ventures"] },
            { id: "pv002", name: "Shiva Puja Vidhi", deity: "Lord Shiva", description: "Sanskrit mantras and water/bilva offering procedures for Shiva worship.", benefits: ["Inner peace", "Spiritual growth", "Destruction of negativity"] }
        ]
    },
    "vrat": {
        items: [
            { id: "vr001", name: "Satyanarayana Vrat", deity: "Lord Vishnu", description: "Fast and narration ceremony of Satyanarayana stories for truth and devotion.", benefits: ["Family harmony", "Wealth and health", "Cleanses karma"] },
            { id: "vr002", name: "Ekadashi Vrat", deity: "Lord Vishnu", description: "Bi-monthly fasting ritual observed on the 11th lunar day of Moon cycles.", benefits: ["Detoxification", "Mental clarity", "Spiritual purification"] }
        ]
    },
    "upavas": {
        items: [
            { id: "up001", name: "Pradosha Upavas", deity: "Lord Shiva", description: "Fasting during twilight period on the 13th day of lunar fortnight.", benefits: ["Removes sins", "Fulfills desires", "Liberates from fears"] }
        ]
    },
    "mantra": {
        items: [
            { id: "mn001", name: "Gayatri Mantra", deity: "Savitar (Sun)", text: "ॐ भूर्भुवः स्वः तत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि धियो यो नः प्रचोदयात्", meaning: "We meditate on the divine light of the Sun. May it illuminate our intellect.", benefits: ["Mental focus", "Vibrant health", "Spiritual awakening"] },
            { id: "mn002", name: "Mahamrityunjaya Mantra", deity: "Lord Shiva", text: "ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम् उर्वारुकमिव बन्धनान्मृत्योर्मुक्षीय मामृतात्", meaning: "We worship the three-eyed Lord Shiva who nourishes all. Deliver us from death.", benefits: ["Longevity", "Healing", "Overcomes fear of death"] }
        ]
    },
    "stotra": {
        items: [
            { id: "st001", name: "Shiva Tandava Stotra", deity: "Lord Shiva", description: "Powerful hymn composed by Ravana describing Shiva's cosmic dance.", benefits: ["Strength", "Creativity", "Removes depression"] }
        ]
    },
    "ashtakam": {
        items: [
            { id: "as001", name: "Madhurashtakam", deity: "Lord Krishna", description: "Devotional eight-stanza hymn praising the sweetness of Lord Krishna.", benefits: ["Pure love", "Happiness", "Inner joy"] }
        ]
    },
    "yantra": {
        items: [
            { id: "yn001", name: "Sri Yantra", deity: "Goddess Lalita Tripurasundari", description: "Sacred geometry diagram representing the cosmic union of Shiva and Shakti.", benefits: ["Abundance", "Cosmic alignment", "Material success"] }
        ]
    },
    "paath": {
        items: [
            { id: "pt001", name: "Sundarkand Paath", deity: "Lord Hanuman", description: "Detailed narration of Hanuman's search for Sita and his devotion.", benefits: ["Protection", "Courage", "Confidence in adversity"] }
        ]
    }
};

// ===== LOAD CATEGORY DATA =====
async function loadCategoryData(categoryId) {
    // Return from cache if available
    if (dataStore[categoryId]) {
        return dataStore[categoryId];
    }
    
    const fileMap = {
        'puja-vidhi': './data/puja-vidhi.json',
        'vrat': './data/vrat.json',
        'upavas': './data/upavas.json',
        'mantra': './data/mantra.json',
        'stotra': './data/stotra.json',
        'ashtakam': './data/ashtakam.json',
        'yantra': './data/yantra.json',
        'paath': './data/paath.json'
    };
    
    try {
        const isRoot = !window.location.pathname.includes('/Static/') && !window.location.pathname.includes('/Features/');
        const fetchPath = isRoot ? `./Static/data/${categoryId}.json` : `./data/${categoryId}.json`;
        const response = await fetch(fetchPath);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: Failed to load ${categoryId}`);
        }
        const data = await response.json();
        
        // Validate data structure
        if (!data || !data.items || !Array.isArray(data.items) || data.items.length === 0) {
            throw new Error('Invalid or empty data structure');
        }
        
        dataStore[categoryId] = data;
        return data;
        
    } catch (error) {
        console.warn(`⚠️ Error loading ${categoryId} from JSON, using offline local copy:`, error.message);
        
        const category = categories.find(c => c.id === categoryId);
        const offlineData = OFFLINE_WISDOM_DATA[categoryId] || { items: [] };
        
        const fallbackData = {
            category: category ? category.name : categoryId,
            icon: category ? category.icon : '📿',
            color: category ? category.color : '#5856D6',
            items: offlineData.items.map(item => ({
                ...item,
                benefits: item.benefits || [],
                description: item.description || ''
            }))
        };
        
        if (fallbackData.items.length === 0) {
            fallbackData.items.push({
                id: `${categoryId.substring(0, 2)}001`,
                name: `⚠️ Unable to Load Data`,
                deity: 'Please check file path',
                description: `The data file for "${categoryId}" could not be loaded. Make sure the JSON file exists at: data/${categoryId}.json`,
                benefits: ['Check console for details', 'Verify file exists', 'Check JSON syntax'],
                error: true
            });
        }
        
        dataStore[categoryId] = fallbackData;
        return fallbackData;
    }
}

// ===== LOAD CATEGORY =====
async function loadCategory(categoryId) {
    const category = categories.find(c => c.id === categoryId);
    if (!category) return;
    
    // Show loading state
    itemsGrid.innerHTML = `
        <div class="loading-shimmer" style="height: 200px; border-radius: 20px;"></div>
    `.repeat(6);
    
    // Hide categories, show items
    document.querySelector('.categories-section').style.display = 'none';
    document.querySelector('.hero-section').style.display = 'none';
    itemsSection.classList.add('active');
    
    // Update header
    itemsTitle.textContent = `${category.icon} ${category.name}`;
    itemsTitle.style.color = category.color;
    
    try {
        const data = await loadCategoryData(categoryId);
        
        if (data && data.items && data.items.length > 0) {
            // Check if it's an error fallback
            if (data.items[0] && data.items[0].error) {
                itemsCount.textContent = '⚠️ Data Load Error';
                renderItems(data.items, category);
            } else {
                itemsCount.textContent = `${data.items.length} Sacred Entries`;
                renderItems(data.items, category);
            }
        } else {
            itemsGrid.innerHTML = `
                <div class="empty-state" style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: rgba(255,255,255,0.6);">
                    <div style="font-size: 48px; margin-bottom: 20px;">📂</div>
                    <h3 style="color: white; margin-bottom: 10px;">No entries found</h3>
                    <p>The data file loaded but contained no items.</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading category:', error);
        itemsGrid.innerHTML = `
            <div class="error-state" style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: rgba(255,255,255,0.6);">
                <div style="font-size: 48px; margin-bottom: 20px;">⚠️</div>
                <h3 style="color: white; margin-bottom: 10px;">Unable to load content</h3>
                <p>Error: ${error.message}</p>
                <p style="margin-top: 10px; font-size: 12px; color: rgba(255,255,255,0.4);">Please check the console for details.</p>
            </div>
        `;
    }
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== RENDER ITEMS =====
function renderItems(items, category) {
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
    
    switch(categoryId) {
        case 'puja-vidhi': 
            return item.purpose || item.description || 'Sacred worship ritual';
        case 'vrat': 
            return item.story ? item.story.substring(0, 80) + '...' : (item.purpose || 'Divine fasting ritual');
        case 'upavas': 
            return item.purpose || 'Spiritual fasting practice';
        case 'mantra': 
            return item.meaning ? item.meaning.substring(0, 100) + '...' : 'Sacred Sanskrit chant';
        case 'stotra': 
            return item.description ? item.description.substring(0, 100) + '...' : 'Devotional hymn';
        case 'ashtakam': 
            return item.description ? item.description.substring(0, 100) + '...' : 'Eight-verse hymn';
        case 'yantra': 
            return item.description ? item.description.substring(0, 100) + '...' : 'Sacred geometric diagram';
        case 'paath': 
            return item.description ? item.description.substring(0, 100) + '...' : 'Sacred recitation';
        default: 
            return 'Sacred spiritual content';
    }
}

// ===== GET ITEM TAGS =====
function getItemTags(item, categoryId) {
    if (item.error) return `<span class="item-tag">⚠️ Error</span>`;
    
    const tags = [];
    
    switch(categoryId) {
        case 'puja-vidhi':
            if (item.duration) tags.push(`⏱ ${item.duration}`);
            if (item.best_time) tags.push(`🌅 ${item.best_time.split(',')[0]}`);
            if (item.steps) tags.push(`📋 ${item.steps} Steps`);
            break;
        case 'vrat':
            if (item.type) tags.push(`📅 ${item.type}`);
            if (item.duration) tags.push(`⏱ ${item.duration}`);
            if (item.best_day) tags.push(`📆 ${item.best_day.substring(0, 15)}...`);
            break;
        case 'upavas':
            if (item.type) tags.push(`🌿 ${item.type}`);
            if (item.duration) tags.push(`⏱ ${item.duration}`);
            if (item.water_allowed !== undefined) tags.push(item.water_allowed ? '💧 Water OK' : '💧 No Water');
            break;
        case 'mantra':
            if (item.chant_count) tags.push(`📿 ${item.chant_count}x`);
            if (item.origin) tags.push(`📜 ${item.origin.split(' ')[0]}`);
            if (item.rishi) tags.push(`🧘 ${item.rishi}`);
            break;
        case 'stotra':
            if (item.verses) tags.push(`📖 ${item.verses} V`);
            if (item.author) tags.push(`✍️ ${item.author}`);
            if (item.language) tags.push(`🗣️ ${item.language}`);
            break;
        case 'ashtakam':
            if (item.verses) tags.push(`📖 ${item.verses} V`);
            if (item.author) tags.push(`✍️ ${item.author}`);
            if (item.best_time) tags.push(`🌅 ${item.best_time.split(',')[0]}`);
            break;
        case 'yantra':
            if (item.type) tags.push(`🔯 ${item.type}`);
            if (item.material) tags.push(`🪵 ${item.material.split(',')[0]}`);
            if (item.placement) tags.push(`📍 ${item.placement}`);
            break;
        case 'paath':
            if (item.duration) tags.push(`⏱ ${item.duration}`);
            if (item.frequency) tags.push(`📅 ${item.frequency}`);
            break;
    }
    
    return tags.slice(0, 4).map(tag => `<span class="item-tag">${tag}</span>`).join('');
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
        modalBody.innerHTML = generateDetailHTML(item, category);
        detailModal.classList.add('active');
        document.body.style.overflow = 'hidden';
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
                <p style="color: rgba(255,255,255,0.4); font-size: 12px; margin-top: 20px;">Please check the console for details.</p>
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
    
    const addList = (title, items) => {
        if (items && items.length) sections.push(`
            <div class="detail-section" style="margin-bottom: 16px; padding: 12px 16px; background: rgba(255,255,255,0.05); border-radius: 12px; border-left: 3px solid rgba(255,255,255,0.2);">
                <h4 style="font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.6); margin-bottom: 6px;">${title}</h4>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    ${items.map(i => `<li style="padding: 4px 0; color: rgba(255,255,255,0.9); display: flex; align-items: center; gap: 8px; font-size: 15px;"><span style="color: rgba(255,215,0,0.6);">✦</span> ${i}</li>`).join('')}
                </ul>
            </div>
        `);
    };
    
    // Display all item fields dynamically
    const displayOrder = ['description', 'purpose', 'meaning', 'text', 'origin', 'author', 'verses', 'language', 'best_time', 'duration', 'frequency', 'method', 'steps', 'material', 'placement', 'activation', 'type', 'food_rule', 'best_day', 'story', 'procedure', 'chant_count', 'rishi', 'ideal_for'];
    
    displayOrder.forEach(key => {
        if (item[key] && typeof item[key] === 'string' && item[key].length > 0) {
            const label = key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
            addSection(label, item[key]);
        }
    });
    
    // Handle benefits as list
    if (item.benefits && item.benefits.length) {
        addList('Benefits', item.benefits);
    }
    
    // Handle items as list (for puja vidhi)
    if (item.items && item.items.length && typeof item.items[0] === 'string') {
        addList('Required Items', item.items);
    }
    
    // Handle allowed food as list
    if (item.allowed_food && item.allowed_food.length) {
        addList('Allowed Food', item.allowed_food);
    }
    
    // Handle mantra text specially
    if (item.text && item.text.length > 0) {
        sections.push(`
            <div class="detail-section" style="margin-bottom: 16px; padding: 16px; background: rgba(255,215,0,0.08); border-radius: 12px; border-left: 3px solid #FFD700;">
                <h4 style="font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: #FFD700; margin-bottom: 6px;">Sacred Mantra</h4>
                <p style="font-size: 18px; color: #FFD700; font-weight: 600; line-height: 1.6; margin-bottom: 8px;">${item.text}</p>
                ${item.meaning ? `<p style="color: rgba(255,255,255,0.8); font-size: 14px; line-height: 1.6;">📖 ${item.meaning}</p>` : ''}
            </div>
        `);
    }
    
    return sections.join('');
}

// ===== CLOSE MODAL =====
function closeModal() {
    detailModal.classList.remove('active');
    document.body.style.overflow = '';
}

// ===== GO BACK =====
function goBack() {
    itemsSection.classList.remove('active');
    document.querySelector('.categories-section').style.display = 'block';
    document.querySelector('.hero-section').style.display = 'flex';
    searchInput.value = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== SEARCH FUNCTIONALITY =====
function handleSearch(query) {
    const trimmedQuery = query.trim().toLowerCase();
    
    if (!trimmedQuery) {
        // Reset view
        if (itemsSection.classList.contains('active')) {
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
    
    if (itemsSection.classList.contains('active')) {
        const cards = document.querySelectorAll('.item-card');
        let visibleCount = 0;
        cards.forEach(card => {
            const text = card.textContent.toLowerCase();
            const isVisible = text.includes(trimmedQuery);
            card.style.display = isVisible ? 'flex' : 'none';
            if (isVisible) visibleCount++;
        });
        itemsCount.textContent = visibleCount === 0 ? 'No matches found' : `${visibleCount} matching entries`;
    } else {
        document.querySelectorAll('.category-tile').forEach(tile => {
            const text = tile.textContent.toLowerCase();
            tile.style.display = text.includes(trimmedQuery) ? 'flex' : 'none';
        });
    }
}

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    backBtn.addEventListener('click', goBack);
    modalClose.addEventListener('click', closeModal);
    detailModal.addEventListener('click', (e) => {
        if (e.target === detailModal) closeModal();
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
    
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => handleSearch(e.target.value), 300);
    });
    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = e.target.getAttribute('href');
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            e.target.classList.add('active');
            
            if (target === '#home' || target === '#categories') {
                goBack();
                document.getElementById('categories').scrollIntoView({ behavior: 'smooth' });
            } else if (target === '#about') {
                document.getElementById('about').scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// ===== SCROLL EFFECTS =====
function setupScrollEffects() {
    const header = document.querySelector('.glass-header');
    
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