/**
 * auth.js
 * Sanskrit AI Authentication & User Profile Management System
 * Integrates Google Identity Services, simulated/real Google Drive syncing,
 * auto-suggestions, and cross-page personalized hidden state passage.
 */

(function (global) {
    'use strict';

    // Injected elements
    let settingsModal = null;

    // Google API Configuration
    const metaClient = document.querySelector('meta[name="google-signin-client-id"]');
    const CLIENT_ID = metaClient ? metaClient.content : '134218957485-dummy.apps.googleusercontent.com';
    let tokenClient = null;

    // Retrieve active session profile from localStorage
    function getProfile() {
        const p = localStorage.getItem('shunya-profile');
        return p ? JSON.parse(p) : null;
    }

    function saveProfile(profile) {
        localStorage.setItem('shunya-profile', JSON.stringify(profile));
        // Fire custom event so other views know profile changed
        document.dispatchEvent(new CustomEvent('shunya-profile-changed', { detail: profile }));
        
        // Pass info in a hidden manner to form inputs on current page
        applyPersonalization(profile);
    }

    // Auto-populate form inputs across all features silently & cache Raw JSON Kundali
    function applyPersonalization(profile) {
        if (!profile) return;
        
        const nickname = profile.nickname || profile.name || 'Seeker';

        // Greeting personalization across header and cards
        const welcomeTitle = document.querySelector('.welcome-card h2');
        if (welcomeTitle) {
            welcomeTitle.innerHTML = `🕉️ Namaste, <span style="color:#fbbf24;">Hi, ${nickname}</span>! Welcome to ShunyakiKundali`;
        }

        const headerGreeting = document.getElementById('headerGreetingPill');
        if (headerGreeting) {
            headerGreeting.innerHTML = `🕉️ Hi, ${nickname}`;
        }

        // Auto-populate Panchang Place Input if blank or default
        const panchangPlace = document.getElementById('panchangPlaceInput');
        if (panchangPlace && (panchangPlace.value === 'New Delhi, India' || !panchangPlace.value)) {
            panchangPlace.value = profile.pob || 'New Delhi, India';
            if (profile.lat && profile.lon) {
                panchangPlace.dataset.lat = profile.lat;
                panchangPlace.dataset.lon = profile.lon;
            }
            panchangPlace.dispatchEvent(new Event('change', { bubbles: true }));
        }

        // Auto-populate Kundli/Astrology forms
        const mName = document.getElementById('mName');
        if (mName && !mName.value) mName.value = profile.name || nickname;

        const mGender = document.getElementById('mGender');
        if (mGender && profile.gender) mGender.value = profile.gender;

        const mDate = document.getElementById('mDate');
        if (mDate && profile.dob) mDate.value = profile.dob;

        const mTime = document.getElementById('mTime');
        if (mTime && profile.tob) mTime.value = profile.tob;

        const mPlace = document.getElementById('mPlace');
        if (mPlace && profile.pob) {
            mPlace.value = profile.pob;
            if (profile.lat && profile.lon) {
                mPlace.dataset.lat = profile.lat;
                mPlace.dataset.lon = profile.lon;
            }
        }

        // Check if raw Kundali JSON calculation is pending or cached
        if (profile.dob && profile.pob && (localStorage.getItem('shunya-pending-kundali-calc') === 'true' || !localStorage.getItem('shunya-cached-raw-json'))) {
            localStorage.removeItem('shunya-pending-kundali-calc');
            setTimeout(() => {
                const btnSubmit = document.getElementById('btnSubmitAstrology') || document.querySelector('#personalKundliSection button[type="submit"]');
                if (btnSubmit && typeof calculateAstrologyData === 'function') {
                    console.log("⚡ Auto-calculating & caching Raw JSON Kundali for:", nickname);
                    calculateAstrologyData();
                }
            }, 300);
        }
    }

    // Helper to redirect to homepage
    function loginWithGoogle() {
        window.location.href = '/index.html';
    }

    // Setup and render user header button & dropdown logic
    function updateProfileHeaderButton() {
        const btn = document.getElementById("profileBtn");
        
        const urlParams = new URLSearchParams(window.location.search);
        const urlUsername = urlParams.get('username');
        if (urlUsername) {
            localStorage.setItem('shunya-username', urlUsername);
        }

        const profile = getProfile();
        let username = urlUsername || localStorage.getItem('shunya-username') || (profile ? (profile.username || profile.nickname || profile.name) : null);
        if (username === 'Devotee' || username === 'Guest') {
            username = (profile && profile.username && profile.username !== 'Devotee') ? profile.username : null;
        }
        
        if (btn) {
            if (username) {
                btn.style.display = 'inline-flex';
                btn.style.alignItems = 'center';
                btn.style.gap = '6px';
                btn.style.cursor = 'pointer';
                btn.style.padding = '4px 14px';
                btn.style.borderRadius = '99px';
                btn.style.background = 'rgba(184, 50, 20, 0.12)';
                btn.style.border = '1.5px solid rgba(184, 50, 20, 0.35)';
                btn.style.transition = 'all 0.2s';
                
                btn.innerHTML = `
                    <span style="font-size:0.88rem; font-weight:800; color:var(--text-color, #92400e);">Namaste 🙏 ${username}</span>
                `;
                btn.onclick = (e) => {
                    e.stopPropagation();
                    toggleProfileDropdown(e);
                };
            } else {
                btn.style.display = 'inline-flex';
                btn.style.alignItems = 'center';
                btn.style.gap = '4px';
                btn.style.cursor = 'pointer';
                btn.style.padding = '4px 10px';
                btn.style.borderRadius = '99px';
                btn.style.background = 'transparent';
                btn.style.border = 'none';
                btn.innerHTML = '<span style="font-size:0.85rem; font-weight:700; color:var(--text-color, #92400e);">🔑 Login / Register</span>';
                btn.onclick = () => {
                    window.location.href = 'index.html';
                };
            }
        }
    }

    function toggleProfileDropdown(e) {
        let dd = document.getElementById('profileDropdownEl');
        if (dd) {
            dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
            if (dd.style.display === 'block') {
                positionDropdown(e, dd);
            }
            return;
        }

        dd = document.createElement('div');
        dd.id = 'profileDropdownEl';
        dd.style.cssText = `
            position: fixed;
            width: 240px;
            background: #ffffff;
            border: 2px solid #b83214;
            border-radius: 12px;
            padding: 16px;
            z-index: 100000;
            box-shadow: 0 15px 35px rgba(0,0,0,0.25);
            color: #1e293b;
            font-family: 'Inter', sans-serif;
        `;
        
        const profile = getProfile();
        const name = profile ? (profile.name || profile.nickname || profile.username || 'Devotee') : 'Login / Register';
        const contact = profile ? (profile.email || profile.mobile || 'Logged in') : 'Sign in to continue';

        dd.innerHTML = `
            <div style="font-weight:800; border-bottom:1px solid #e2e8f0; padding-bottom:8px; margin-bottom:6px; font-size:0.95rem; color:#b83214; display:flex; align-items:center; gap:6px;">
                <span>👤</span> ${name}
            </div>
            <div style="font-size:0.78rem; color:#64748b; margin-bottom:14px; word-break:break-all; font-weight:600;">
                ${contact}
            </div>
            <button id="btnOpenSettings" style="width:100%; text-align:left; background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:8px; color:#1e293b; font-weight:700; padding:10px 12px; cursor:pointer; font-size:0.85rem; margin-bottom:8px; display:flex; align-items:center; gap:8px; transition:background 0.2s;">
                ⚙️ Profile Settings
            </button>
            <button id="btnLogout" style="width:100%; text-align:left; background:#fef2f2; border:1.5px solid #fecaca; border-radius:8px; color:#dc2626; font-weight:700; padding:10px 12px; cursor:pointer; font-size:0.85rem; display:flex; align-items:center; gap:8px; transition:background 0.2s;">
                🚪 Log Out
            </button>
        `;
        
        document.body.appendChild(dd);

        dd.addEventListener('click', (ev) => ev.stopPropagation());

        dd.querySelector('#btnOpenSettings').onclick = () => {
            dd.style.display = 'none';
            openSettingsModal();
        };

        dd.querySelector('#btnLogout').onclick = () => {
            dd.style.display = 'none';
            logout();
        };

        positionDropdown(e, dd);
    }

    function positionDropdown(e, dd) {
        const btn = document.getElementById("profileBtn") || e.currentTarget;
        const rect = btn.getBoundingClientRect();
        dd.style.top = `${rect.bottom + 8}px`;
        dd.style.right = `${Math.max(10, window.innerWidth - rect.right)}px`;
        dd.style.left = 'auto';
    }

    // Settings Modal
    function injectSettingsModal() {
        if (document.getElementById('profileSettingsModal')) return;
        
        const modal = document.createElement('div');
        modal.id = 'profileSettingsModal';
        modal.style.cssText = `
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(4px);
            align-items: center; justify-content: center;
            z-index: 10005;
        `;
        
        modal.innerHTML = `
            <div class="glass-card" style="width: 90%; max-width: 460px; background: rgba(15,23,42,0.95); border: 2.5px solid #a23922; border-radius: 12px; padding: 25px; color:#fff;">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:12px; margin-bottom:20px;">
                    <h3 style="margin:0; color:#fbbf24; font-weight:800;">⚙️ Vedic Profile Settings</h3>
                    <button id="btnCloseSettings" style="background:none; border:none; color:#fff; font-size:1.2rem; cursor:pointer;">✕</button>
                </div>
                
                <div style="display:flex; flex-direction:column; gap:12px;">
                    <div>
                        <label style="display:block; font-size:0.75rem; font-weight:700; margin-bottom:4px; color:#94a3b8;">Full Name</label>
                        <input type="text" id="setpName" style="width:100%; padding:8px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:6px; color:#fff;">
                    </div>
                    <div>
                        <label style="display:block; font-size:0.75rem; font-weight:700; margin-bottom:4px; color:#94a3b8;">Nickname (appears in greetings)</label>
                        <input type="text" id="setpNickname" style="width:100%; padding:8px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:6px; color:#fff;">
                    </div>
                    <div style="display:flex; gap:10px;">
                        <div style="flex:1;">
                            <label style="display:block; font-size:0.75rem; font-weight:700; margin-bottom:4px; color:#94a3b8;">Date of Birth</label>
                            <input type="date" id="setpDob" style="width:100%; padding:8px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:6px; color:#fff;">
                        </div>
                        <div style="flex:1;">
                            <label style="display:block; font-size:0.75rem; font-weight:700; margin-bottom:4px; color:#94a3b8;">Time of Birth</label>
                            <input type="time" id="setpTob" style="width:100%; padding:8px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:6px; color:#fff;">
                        </div>
                    </div>
                    <div>
                        <label style="display:block; font-size:0.75rem; font-weight:700; margin-bottom:4px; color:#94a3b8;">Place of Birth (POB)</label>
                        <input type="text" id="setpPob" style="width:100%; padding:8px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:6px; color:#fff;" placeholder="Search city...">
                    </div>
                </div>
                
                <button id="btnSaveProfileSettings" style="width:100%; margin-top:20px; background:#a23922; border:none; padding:10px; color:#fff; font-weight:700; border-radius:6px; cursor:pointer;">Save & Synchronize</button>
            </div>
        `;
        document.body.appendChild(modal);

        modal.querySelector('#btnCloseSettings').onclick = () => {
            modal.style.display = 'none';
        };

        modal.querySelector('#btnSaveProfileSettings').onclick = () => {
            const pobInput = document.getElementById('setpPob');
            const profile = getProfile() || {};
            profile.name = document.getElementById('setpName').value;
            profile.nickname = document.getElementById('setpNickname').value;
            profile.dob = document.getElementById('setpDob').value;
            profile.tob = document.getElementById('setpTob').value;
            profile.pob = pobInput.value;
            profile.lat = pobInput.dataset.lat ? parseFloat(pobInput.dataset.lat) : profile.lat;
            profile.lon = pobInput.dataset.lon ? parseFloat(pobInput.dataset.lon) : profile.lon;

            saveProfile(profile);
            modal.style.display = 'none';
            updateProfileHeaderButton();
            saveProfileToDrive();
        };

        // Initialize Geocomplete for birth place inside settings modal
        if (typeof initGeoComplete === 'function') {
            initGeoComplete('setpPob', { defaultPlace: 'New Delhi, India' });
        }
    }

    function openSettingsModal() {
        injectSettingsModal();
        const profile = getProfile();
        if (profile) {
            document.getElementById('setpName').value = profile.name || '';
            document.getElementById('setpNickname').value = profile.nickname || '';
            document.getElementById('setpDob').value = profile.dob || '';
            document.getElementById('setpTob').value = profile.tob || '';
            document.getElementById('setpPob').value = profile.pob || '';
            
            // Set coords dataset
            const pobInput = document.getElementById('setpPob');
            if (pobInput) {
                pobInput.dataset.lat = profile.lat || '';
                pobInput.dataset.lon = profile.lon || '';
            }
        }
        document.getElementById('profileSettingsModal').style.display = 'flex';
    }

    function promptSettingsIfIncomplete() {
        const profile = getProfile();
        if (profile && (!profile.dob || !profile.pob)) {
            setTimeout(() => {
                const confirm = window.confirm("Welcome to Sanskrit AI! Would you like to enter your birth details (DOB, TOB, Place) now for customized astrological calculations?");
                if (confirm) {
                    openSettingsModal();
                }
            }, 1000);
        }
    }

    // Sign up mock users
    function signup() {
        const email = document.getElementById('signupEmail').value;
        const username = document.getElementById('signupUsername').value;
        const password = document.getElementById('signupPassword').value;

        if (!email || !username || !password) {
            alert("All fields are required.");
            return;
        }

        const newUser = {
            email,
            name: username,
            nickname: username.toUpperCase(),
            dob: '', tob: '', pob: ''
        };

        saveProfile(newUser);
        alert("Account signed up successfully!");
        closeAuth();
        updateProfileHeaderButton();
        promptSettingsIfIncomplete();
    }

    // Classic Email Sign in mock
    function login() {
        const email = document.getElementById('loginEmail').value;
        if (!email) {
            alert("Email is required.");
            return;
        }
        const profile = {
            email,
            name: email.split('@')[0],
            nickname: email.split('@')[0].toUpperCase(),
            dob: '1995-07-20',
            tob: '12:00',
            pob: 'New Delhi, India',
            lat: 28.6139,
            lon: 77.2090
        };
        saveProfile(profile);
        closeAuth();
        updateProfileHeaderButton();
        promptSettingsIfIncomplete();
    }

    function logout() {
        localStorage.removeItem('shunya-profile');
        localStorage.removeItem('shunya-cached-raw-json');
        sessionStorage.removeItem('google-access-token');
        sessionStorage.removeItem('google-drive-file-id');
        window.location.href = '/index.html';
    }

    function openAuth() {
        document.getElementById("authModal").style.display = "flex";
    }

    function closeAuth() {
        document.getElementById("authModal").style.display = "none";
    }

    function showSignup() {
        document.getElementById("authTitle").innerText = "Sign Up";
        const form = document.querySelector('.auth-card');
        if (form) {
            form.innerHTML = `
                <button class="auth-close" onclick="closeAuth()">✕</button>
                <h2 id="authTitle">Sign Up</h2>
                <input id="signupUsername" placeholder="User Name" style="width:100%; margin-bottom:10px; padding:10px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:6px; color:#fff;">
                <input id="signupEmail" placeholder="example@ex.ex" style="width:100%; margin-bottom:10px; padding:10px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:6px; color:#fff;">
                <input id="signupPassword" type="password" placeholder="Password" style="width:100%; margin-bottom:15px; padding:10px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:6px; color:#fff;">
                <button class="primary-btn" onclick="signup()" style="width:100%; background:#a23922; border:none; padding:10px; font-weight:700; color:#fff; border-radius:6px; cursor:pointer;">Register Account</button>
            `;
        }
    }

    // Set globals
    global.openAuth = openAuth;
    global.closeAuth = closeAuth;
    global.showSignup = showSignup;
    global.login = login;
    global.signup = signup;
    global.logout = logout;
    global.loginWithGoogle = loginWithGoogle;
    global.openSettingsModal = openSettingsModal;
    global.getProfile = getProfile;
    global.updateProfileHeaderButton = updateProfileHeaderButton;

    // Immediate execution on script load
    try {
        updateProfileHeaderButton();
    } catch(e) {}

    // Load libraries on content load
    document.addEventListener('DOMContentLoaded', () => {
        updateProfileHeaderButton();
        
        // Hide profileDropdown when clicking outside
        document.addEventListener('click', () => {
            const dd = document.getElementById('profileDropdownEl');
            if (dd) dd.style.display = 'none';
        });

        // Trigger auto-population for initial load
        const profile = getProfile();
        if (profile) {
            applyPersonalization(profile);
        }
    });

    // Re-run personalization when SPA transitions views
    document.addEventListener('shunya-profile-changed', (e) => {
        updateProfileHeaderButton();
        applyPersonalization(e.detail);
    });

})(window);