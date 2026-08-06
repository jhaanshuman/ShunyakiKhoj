/**
 * Dynamic View Builder for Spiritual Wisdom Library
 */
function renderWisdomView() {
    return `
    <div id="wisdomViewContainer">
        
    <!-- Animated Background -->
    <div class="bg-container">
        <div class="bg-gradient"></div>
        <div class="floating-om">ॐ</div>
        <div class="floating-lotus">🪷</div>
        <div class="floating-diya">🪔</div>
        <div class="particles" id="particles"></div>
        <div class="mandala-bg"></div>
    </div>

    <!-- Header -->
    <header class="glass-header">
        <div class="header-content">
            <div class="logo">
                <span class="om-symbol">ॐ</span>
                <div class="logo-text">
                    <h1>ShunyakiKhoj</h1>
                    <span class="tagline">Spiritual Wisdom Portal</span>
                </div>
            </div>
            <nav class="main-nav">
                <a href="javascript:void(0)" onclick="if(typeof switchPortalTab==='function'){switchPortalTab('panchang');}else{window.location.href='/landing.html';}" class="nav-link">← Sanskrit AI</a>
                <a href="javascript:void(0)" onclick="document.getElementById('home').scrollIntoView({behavior:'smooth'});" class="nav-link active">Home</a>
                <a href="javascript:void(0)" onclick="document.getElementById('categories').scrollIntoView({behavior:'smooth'});" class="nav-link">Categories</a>
                <a href="javascript:void(0)" onclick="document.getElementById('about').scrollIntoView({behavior:'smooth'});" class="nav-link">About</a>
            </nav>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search spiritual content...">
                <button class="search-btn">🔍</button>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero-section" id="home">
        <div class="hero-content glass-card" style="padding: 5px !important;">
            <div class="hero-om">ॐ</div>
            <h2 class="hero-title">Discover Ancient Spiritual Wisdom</h2>
            <p class="hero-subtitle">Explore 11,000+ sacred texts, Upanishads, Vedic hymns, mantras, and shlokas from Sanatana Dharma</p>
            <div class="hero-stats">
                <div class="stat-item">
                    <span class="stat-number" id="totalItems">11,100+</span>
                    <span class="stat-label">Sacred Entries</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">12</span>
                    <span class="stat-label">Categories</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">∞</span>
                    <span class="stat-label">Divine Blessings</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Category Tiles Section -->
    <section class="categories-section" id="categories">
        <div class="section-header">
            <h2 class="section-title">Sacred Categories</h2>
            <p class="section-subtitle">Click on any category to explore divine knowledge</p>
        </div>
        
        <div class="category-grid" id="categoryGrid">
            <!-- Categories will be loaded dynamically -->
        </div>
    </section>

    <!-- Items Grid Section with Category Searchbar -->
    <section class="items-section" id="itemsSection">
        <div class="items-header glass-card" style="padding: 5px !important; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px;">
            <button class="back-btn" id="backBtn">
                <span>←</span> Back to Categories
            </button>
            <h2 class="items-title" id="itemsTitle" style="margin:0;">Category Name</h2>
            <div class="category-search-box" style="display: flex; gap: 6px; align-items: center;">
                <input type="text" id="categorySearchInput" placeholder="Search in this category..." style="padding: 5px 10px; border-radius: 6px; border: 1px solid var(--border-color); background: rgba(0,0,0,0.3); color: #fff; font-size: 0.85rem; width: 200px;">
                <span style="font-size: 0.85rem; color: var(--text-muted);" id="itemsCount">0 items</span>
            </div>
        </div>
        <div class="items-grid" id="itemsGrid">
            <!-- Items will be loaded dynamically -->
        </div>
    </section>

    <!-- Detail Modal -->
    <div class="modal-overlay" id="detailModal">
        <div class="modal-content glass-modal">
            <button class="modal-close" id="modalClose">&times;</button>
            <div class="modal-body" id="modalBody">
                <!-- Detail content will be loaded dynamically -->
            </div>
        </div>
    </div>

    <!-- About Section -->
    <section class="about-section" id="about">
        <div class="about-content glass-card">
            <h2>About ShunyakiKhoj</h2>
            <p>ShunyakiKhoj is a comprehensive spiritual portal dedicated to preserving and sharing the ancient wisdom of Sanatana Dharma. Our mission is to make sacred knowledge accessible to seekers worldwide.</p>
            <div class="about-features">
                <div class="feature">
                    <span class="feature-icon">📿</span>
                    <h3>Authentic Content</h3>
                    <p>Carefully curated from ancient scriptures and traditions</p>
                </div>
                <div class="feature">
                    <span class="feature-icon">🪷</span>
                    <h3>Comprehensive Library</h3>
                    <p>700+ entries across 7 spiritual categories</p>
                </div>
                <div class="feature">
                    <span class="feature-icon">✨</span>
                    <h3>Divine Experience</h3>
                    <p>Immersive design inspired by sacred aesthetics</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="glass-footer">
        <div class="footer-content">
            <div class="footer-logo">
                <span class="om-symbol">ॐ</span>
                <span>ShunyakiKhoj</span>
            </div>
            <p class="footer-text">Connecting seekers with divine wisdom since time immemorial</p>
            <div class="footer-links">
                <a href="https://shunyakikhoj.co.in" target="_blank">Main Website</a>
                <a href="https://sanskritai.vercel.app/" target="_blank">Sanskrit AI</a>
            </div>
            <p class="copyright">© 2026 ShunyakiKhoj. All Rights Reserved. 🙏</p>
        </div>
    </footer>

    
    </div>
    `;
}
