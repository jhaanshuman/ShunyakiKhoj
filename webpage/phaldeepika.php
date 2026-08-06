<?php
/**
 * phaldeepika.php - ASTRO-OS PhalDeepika Interactive Intelligence Assistant
 * Mobile-Responsive & Protected by PHP Session Authentication.
 * 10,000+ Scenarios & 50 Life Domains Active.
 */
session_start();

if (!isset($_SESSION['user_id']) && !isset($_SESSION['username']) && !isset($_SESSION['user']) && !isset($_SESSION['guest_mode'])) {
    header("Location: /index.html?reason=login_required");
    exit();
}

$username = $_SESSION['username'] ?? $_SESSION['name'] ?? $_SESSION['user'] ?? 'Vedic Seeker';
$profile = $_SESSION['profile'] ?? [];
$dob = $profile['dob'] ?? $_SESSION['dob'] ?? 'N/A';
$tob = $profile['tob'] ?? $_SESSION['tob'] ?? 'N/A';
$pob = $profile['pob'] ?? $_SESSION['pob'] ?? 'N/A';

$userMeta = "Authenticated User (DOB: " . htmlspecialchars($dob) . ", TOB: " . htmlspecialchars($tob) . ", POB: " . htmlspecialchars($pob) . ")";
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>PhalDeepika | 10,000+ Life Scenarios & 50 Domains</title>
  <link rel="stylesheet" href="style.css">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
  <!-- MOBILE VIEW SWITCHER TAB BAR (Hidden on Desktop) -->
  <div class="mobile-tab-bar">
    <button class="mobile-tab-btn active" id="tabBtnScenarios" onclick="switchMobileView('scenarios')">📌 10,000+ Scenarios</button>
    <button class="mobile-tab-btn" id="tabBtnChat" onclick="switchMobileView('chat')">💬 Chat Assistant</button>
  </div>

  <div class="whatsapp-container" id="whatsappContainer">
    
    <!-- LEFT SIDEBAR: 10,000+ FEATURES NAVIGATOR ACROSS 50 DOMAINS -->
    <aside class="sidebar">
      <header class="sidebar-header">
        <div class="user-avatar">
          <img src="https://ui-avatars.com/api/?name=<?php echo urlencode($username); ?>&background=00a884&color=fff" alt="Avatar">
          <div class="user-info">
            <span class="user-name" id="displayUsername"><?php echo htmlspecialchars($username); ?></span>
            <span class="user-status" id="displayUserMeta"><?php echo htmlspecialchars($userMeta); ?></span>
          </div>
        </div>
      </header>

      <!-- SEARCH BAR -->
      <div class="search-box">
        <div class="search-wrapper">
          <span class="search-icon">🔍</span>
          <input type="text" id="featureSearchInput" placeholder="Search 10,000+ Life Scenarios across 50 Domains..." onkeyup="filterFeatures()">
        </div>
      </div>

      <!-- DOMAIN CATEGORIES & FEATURES LIST -->
      <div class="features-list" id="featuresList">
        <!-- Populated dynamically via app.js -->
      </div>
    </aside>

    <!-- RIGHT CHAT AREA -->
    <main class="chat-area">
      <!-- CHAT HEADER -->
      <header class="chat-header">
        <div class="assistant-avatar">🔮</div>
        <div class="assistant-info">
          <h2>PhalDeepika AI Reasoning Assistant</h2>
          <span class="online-indicator">🟢 10,000+ Scenarios & 50 Life Domains Active</span>
        </div>
      </header>

      <!-- MESSAGES STREAM CONTAINER -->
      <div class="messages-container" id="messagesContainer">
        <!-- System Welcome Message -->
        <div class="message system-msg">
          <div class="bubble">
            <div class="system-title">✨ Welcome to PhalDeepika Astrological Operating System</div>
            <p>Welcome, <strong id="welcomeUsername"><?php echo htmlspecialchars($username); ?></strong>. Search or select any of the <strong>10,000+ life scenarios</strong> across <strong>50 life domains</strong> from the sidebar or type your life question below.</p>
            <p>Every answer executes the <strong>Astrological Decision Graph</strong>, validating graph topology, evidence weights, classical citations, and self-audited probability curves with zero hardcoded fallbacks.</p>
          </div>
        </div>
      </div>

      <!-- CHAT INPUT FOOTER -->
      <footer class="chat-footer">
        <form id="chatForm" onsubmit="handleQuerySubmit(event)">
          <input type="text" id="chatInput" placeholder="Type your life question (e.g. Will I get a baby this year?)..." required autocomplete="off">
          <button type="submit" id="sendBtn">
            <span>Send</span>
          </button>
        </form>
      </footer>
    </main>

  </div>

  <script src="app.js"></script>
</body>
</html>
