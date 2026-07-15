const API="/UserLog/auth.php";

function getMockSession() {
    const user = localStorage.getItem('mock_user');
    if (user) {
        return { loggedIn: true, username: JSON.parse(user).username };
    }
    return { loggedIn: false };
}

function handleSessionResponse(data) {
    const btn=document.getElementById("profileBtn");
    if (!btn) return;
    if(data.loggedIn){
        btn.innerHTML=`
        <div class="profileMenu" style="position:relative; cursor:pointer;">
        ${data.username}
        <div class="profileDropdown" style="display:none; position:absolute; right:0; top:100%; background:var(--card-bg); border:var(--card-border); border-radius:6px; padding:8px; z-index:1000; min-width:120px;">
        <a href="#" style="display:block; color:var(--text-color); text-decoration:none; padding:4px 8px; font-size:0.85rem;">Settings</a>
        <a onclick="logout()" style="display:block; color:var(--accent-color); text-decoration:none; padding:4px 8px; font-size:0.85rem; font-weight:700;">Logout</a>
        </div>
        </div>
        `;
        // Setup dropdown toggle listener
        const menuEl = btn.querySelector('.profileMenu');
        const dropdownEl = btn.querySelector('.profileDropdown');
        if (menuEl && dropdownEl) {
            menuEl.addEventListener('click', (e) => {
                e.stopPropagation();
                dropdownEl.style.display = dropdownEl.style.display === 'none' ? 'block' : 'none';
            });
            document.addEventListener('click', () => {
                dropdownEl.style.display = 'none';
            });
        }
    } else {
        btn.onclick=openAuthModal;
    }
}

// Initial session check
fetch(API+"?action=session")
.then(res => {
    if (!res.ok) throw new Error("PHP offline");
    return res.text();
})
.then(text => {
    if (!text || text.trim().startsWith('<?php')) {
        throw new Error("PHP source code returned");
    }
    const data = JSON.parse(text);
    handleSessionResponse(data);
})
.catch(err => {
    const data = getMockSession();
    handleSessionResponse(data);
});

/* OPEN LOGIN MODAL */
function openAuthModal(){
    document.getElementById("authModal").style.display="flex";
}

/* LOGIN */
function login(){
    let email=document.getElementById("loginEmail").value;
    let password=document.getElementById("loginPassword").value;
    
    // Check local storage mock users
    const mockUsers = JSON.parse(localStorage.getItem('mock_users') || '[]');
    const user = mockUsers.find(u => u.email === email && u.password === password);
    
    if (user) {
        localStorage.setItem('mock_user', JSON.stringify(user));
        location.reload();
        return;
    }
    
    // Otherwise try PHP
    fetch(API,{
        method:"POST",
        headers:{
            "Content-Type":"application/x-www-form-urlencoded"
        },
        body:new URLSearchParams({
            action:"login",
            email:email,
            password:password
        })
    })
    .then(r=>r.text())
    .then(text=>{
        if (!text || text.trim().startsWith('<?php')) throw new Error("PHP offline");
        const data = JSON.parse(text);
        if(data.success){
            location.reload();
        }else{
            alert(data.error);
        }
    })
    .catch(err => {
        alert("Mock user not found. To create one, sign up first.");
    });
}

/* SIGNUP */
function signup(){
    let username=document.getElementById("signupUsername").value;
    let email=document.getElementById("signupEmail").value;
    let password=document.getElementById("signupPassword").value;
    let gender=document.getElementById("gender").value;
    let dob=document.getElementById("dob").value;
    let lang=document.getElementById("lang").value;
    
    const mockUsers = JSON.parse(localStorage.getItem('mock_users') || '[]');
    if (mockUsers.some(u => u.email === email)) {
        alert("Email already registered in mock database");
        return;
    }
    
    const newUser = { username, email, password, gender, dob, lang };
    mockUsers.push(newUser);
    localStorage.setItem('mock_users', JSON.stringify(mockUsers));
    localStorage.setItem('mock_user', JSON.stringify(newUser));
    alert("Signup successful (Mock Local Storage)");
    location.reload();
}

/* LOGOUT */
function logout(){
    localStorage.removeItem('mock_user');
    fetch(API,{
        method:"POST",
        headers:{
            "Content-Type":"application/x-www-form-urlencoded"
        },
        body:new URLSearchParams({
            action:"logout"
        })
    })
    .then(()=>location.reload())
    .catch(()=>location.reload());
}

function openAuth(){
    document.getElementById("authModal").style.display="flex"
}

function closeAuth(){
    document.getElementById("authModal").style.display="none"
}

function showSignup(){
    document.getElementById("authTitle").innerText="Sign Up"
}

function forgotPassword(){
    alert("Password recovery coming soon.")
}