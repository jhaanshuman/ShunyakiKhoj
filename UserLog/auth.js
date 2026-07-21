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

    // Auto-populate form inputs across all features silently
    function applyPersonalization(profile) {
        if (!profile) return;
        
        // Greeting personalization
        const welcomeTitle = document.querySelector('.welcome-card h2');
        if (welcomeTitle) {
            const nickname = profile.nickname || profile.name || 'Seeker';
            welcomeTitle.innerHTML = `🕉️ Namaste, <span style="color:#fbbf24;">${nickname}</span>! Welcome to Sanskrit AI`;
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
        const mDate = document.getElementById('mDate');
        if (mDate && !mDate.value) mDate.value = profile.dob || '';

        const mTime = document.getElementById('mTime');
        if (mTime && !mTime.value) mTime.value = profile.tob || '';

        const mPlace = document.getElementById('mPlace');
        if (mPlace && (!mPlace.value || mPlace.value === 'Patna, Bihar, India')) {
            mPlace.value = profile.pob || '';
            mPlace.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }

    // Load GIS SDK dynamically
    function loadGoogleGSI() {
        if (window.google && window.google.accounts) return;
        const script = document.createElement('script');
        script.src = 'https://accounts.google.com/gsi/client';
        script.async = true;
        script.defer = true;
        script.onload = () => {
            try {
                tokenClient = google.accounts.oauth2.initTokenClient({
                    client_id: CLIENT_ID,
                    scope: 'https://www.googleapis.com/auth/drive.file',
                    callback: handleGoogleAuthResponse
                });
            } catch(e) {
                console.warn("GSI Token init failed (likely local development). Mock flow will be used.", e);
            }
        };
        document.head.appendChild(script);
    }

    // Trigger Google Sign-In GSI popup
    function loginWithGoogle() {
        if (tokenClient && !CLIENT_ID.includes('dummy')) {
            tokenClient.requestAccessToken();
        } else {
            // Simulated login flow if GSI block/offline
            const email = prompt("Enter your Google Account email to sign in:", "anshuman.jha@gmail.com");
            if (email) {
                const mockProfile = {
                    email: email,
                    name: email.split('@')[0],
                    nickname: email.split('@')[0].toUpperCase(),
                    dob: '1995-07-20',
                    tob: '12:00',
                    pob: 'New Delhi, India',
                    lat: 28.6139,
                    lon: 77.2090
                };
                saveProfile(mockProfile);
                alert("Simulated Google Login Successful for: " + email);
                closeAuth();
                updateProfileHeaderButton();
                promptSettingsIfIncomplete();
            }
        }
    }

    // Handle real Google Drive token
    async function handleGoogleAuthResponse(response) {
        if (response.error) {
            console.error("Google Auth error:", response);
            return;
        }
        const accessToken = response.access_token;
        sessionStorage.setItem('google-access-token', accessToken);

        // Fetch User Info using token
        try {
            const userRes = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
                headers: { Authorization: `Bearer ${accessToken}` }
            });
            const userData = await userRes.json();
            
            // Try to fetch profile from user's Google Drive
            const driveProfile = await fetchProfileFromDrive(accessToken);
            if (driveProfile) {
                saveProfile(driveProfile);
                alert("Profile synchronized from Google Drive!");
            } else {
                // Initialize default profile using google details
                const defaultProf = {
                    email: userData.email,
                    name: userData.name,
                    nickname: userData.given_name || userData.name,
                    dob: '', tob: '', pob: ''
                };
                saveProfile(defaultProf);
            }
            
            closeAuth();
            updateProfileHeaderButton();
            promptSettingsIfIncomplete();
        } catch(err) {
            console.error("Failed to fetch profile details", err);
        }
    }

    // Google Drive REST API integration to search and fetch file
    async function fetchProfileFromDrive(token) {
        try {
            const searchUrl = `https://www.googleapis.com/drive/v3/files?q=name='shunyaki_profile.json'+and+trashed=false&fields=files(id,name)`;
            const res = await fetch(searchUrl, {
                headers: { Authorization: `Bearer ${token}` }
            });
            const searchData = await res.json();
            if (searchData.files && searchData.files.length > 0) {
                const fileId = searchData.files[0].id;
                sessionStorage.setItem('google-drive-file-id', fileId);
                const fileRes = await fetch(`https://www.googleapis.com/drive/v3/files/${fileId}?alt=media`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                return await fileRes.json();
            }
        } catch(e) {
            console.warn("Drive fetch error:", e);
        }
        return null;
    }

    // Save profile configurations back to Google Drive
    async function saveProfileToDrive() {
        const token = sessionStorage.getItem('google-access-token');
        const profile = getProfile();
        if (!token || !profile) {
            // Fallback: Local save visual alert
            alert("Settings saved locally! To sync with Google Drive, sign in via Google.");
            return;
        }

        const fileId = sessionStorage.getItem('google-drive-file-id');
        const boundary = 'foo_bar_boundary';
        
        const metadata = {
            name: 'shunyaki_profile.json',
            mimeType: 'application/json'
        };

        const multipartBody = 
            `\r\n--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n` +
            JSON.stringify(metadata) +
            `\r\n--${boundary}\r\nContent-Type: application/json\r\n\r\n` +
            JSON.stringify(profile) +
            `\r\n--${boundary}--`;

        let url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart';
        let method = 'POST';

        if (fileId) {
            url = `https://www.googleapis.com/upload/drive/v3/files/${fileId}?uploadType=multipart`;
            method = 'PATCH';
        }

        try {
            const res = await fetch(url, {
                method: method,
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': `multipart/related; boundary=${boundary}`
                },
                body: multipartBody
            });
            const data = await res.json();
            if (data.id) {
                sessionStorage.setItem('google-drive-file-id', data.id);
                alert("Profile configuration synchronized with Google Drive successfully!");
            }
        } catch(err) {
            console.error("Save to Drive failed:", err);
            alert("Failed to synchronize with Google Drive. Local copy was saved.");
        }
    }

    // Setup and render custom dropdown/form logic
    function updateProfileHeaderButton() {
        const btn = document.getElementById("profileBtn");
        if (!btn) return;
        
        const profile = getProfile();
        if (profile) {
            btn.innerHTML = `
                <div class="profile-menu-container" style="position:relative; display:inline-block;">
                    <span style="font-size:0.8rem; font-weight:700; color:#fbbf24; margin-right:4px;">${profile.nickname || profile.name}</span>
                    <span class="active-dot" style="position:absolute; bottom:2px; right:2px; width:8px; height:8px; background:#10b981; border-radius:50%; border:1px solid #000;"></span>
                    👤
                </div>
            `;
            btn.onclick = (e) => {
                e.stopPropagation();
                toggleProfileDropdown(e);
            };
        } else {
            btn.innerHTML = '👤';
            btn.onclick = openAuth;
        }
    }

    function toggleProfileDropdown(e) {
        let dd = document.getElementById('profileDropdownEl');
        if (dd) {
            dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
            return;
        }

        dd = document.createElement('div');
        dd.id = 'profileDropdownEl';
        dd.className = 'glass-card';
        dd.style.cssText = `
            position: absolute;
            top: 50px;
            right: 20px;
            width: 240px;
            background: rgba(15, 23, 42, 0.95);
            border: 1.5px solid var(--glass-border);
            border-radius: 8px;
            padding: 12px 15px;
            z-index: 10000;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            color: #fff;
        `;
        
        const profile = getProfile();
        dd.innerHTML = `
            <div style="font-weight:800; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px; margin-bottom:8px; font-size:0.9rem; color:#fbbf24;">
                ${profile ? profile.name : 'Vedic Profile'}
            </div>
            <div style="font-size:0.75rem; color:#94a3b8; margin-bottom:12px; word-break:break-all;">
                ${profile ? profile.email || 'offline-mode' : ''}
            </div>
            <button id="btnOpenSettings" style="width:100%; text-align:left; background:none; border:none; color:#fff; font-weight:700; padding:8px 0; cursor:pointer; font-size:0.85rem;">⚙️ Profile Settings</button>
            <button id="btnSyncDrive" style="width:100%; text-align:left; background:none; border:none; color:#fbbf24; font-weight:700; padding:8px 0; cursor:pointer; font-size:0.85rem;">💾 Sync to Google Drive</button>
            <button id="btnLogout" style="width:100%; text-align:left; background:none; border:none; color:#f87171; font-weight:700; padding:8px 0; cursor:pointer; font-size:0.85rem; border-top:1px solid rgba(255,255,255,0.08); margin-top:8px; padding-top:10px;">🚪 Log Out</button>
        `;
        
        document.body.appendChild(dd);

        // Bind clicks inside dropdown
        dd.querySelector('#btnOpenSettings').onclick = () => {
            dd.style.display = 'none';
            openSettingsModal();
        };
        dd.querySelector('#btnSyncDrive').onclick = () => {
            dd.style.display = 'none';
            saveProfileToDrive();
        };
        dd.querySelector('#btnLogout').onclick = () => {
            dd.style.display = 'none';
            logout();
        };

        // Align coordinates dynamically below user button
        const rect = e.currentTarget.getBoundingClientRect();
        dd.style.top = `${rect.bottom + window.scrollY + 8}px`;
        dd.style.left = `${rect.right - 240 + window.scrollX}px`;

        e.stopPropagation();
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
        sessionStorage.removeItem('google-access-token');
        sessionStorage.removeItem('google-drive-file-id');
        alert("Logged out successfully.");
        location.reload();
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
                <input id="signupEmail" placeholder="Email" style="width:100%; margin-bottom:10px; padding:10px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:6px; color:#fff;">
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

    // Load libraries on content load
    document.addEventListener('DOMContentLoaded', () => {
        loadGoogleGSI();
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
        applyPersonalization(e.detail);
    });

})(window);