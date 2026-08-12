<?php
/**
 * auth.php - Authentication & Birth Details Service for ShunyakiKhoj
 */
error_reporting(0);
ini_set('display_errors', '0');

header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With, *");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}

session_start();
require_once "db.php";

$raw_input = file_get_contents('php://input');
$json_data = json_decode($raw_input, true) ?? [];

$action = $_POST['action'] ?? $_GET['action'] ?? $json_data['action'] ?? '';

/* 1. SESSION CHECK */
if ($action === "session") {
    if (isset($_SESSION['user_id']) || isset($_SESSION['guest_mode'])) {
        echo json_encode([
            "loggedIn" => true,
            "username" => $_SESSION['username'] ?? $_SESSION['name'] ?? 'Seeker',
            "isGuest" => isset($_SESSION['guest_mode']),
            "profile" => $_SESSION['profile'] ?? null
        ]);
    } else {
        echo json_encode([
            "loggedIn" => false
        ]);
    }
    exit;
}

/* 2. SIGNUP */
if ($action === "signup") {
    // Clean inputs
    $username = db_escape(trim($_POST['username'] ?? ''));
    $email = db_escape(trim($_POST['email'] ?? ''));
    $mobile = db_escape(trim($_POST['mobile'] ?? ''));
    $password = $_POST['password'] ?? '';
    $gender = db_escape($_POST['gender'] ?? 'Male');
    $dob = db_escape($_POST['dob'] ?? '');
    $tob = db_escape($_POST['tob'] ?? '');
    $pob = db_escape($_POST['pob'] ?? '');
    $lat = floatval($_POST['lat'] ?? 28.6139);
    $lon = floatval($_POST['lon'] ?? 77.2090);

    if (empty($username) || empty($password) || (empty($email) && empty($mobile))) {
        echo json_encode(["success" => false, "error" => "Username, Email/Mobile, and Password are required."]);
        exit;
    }

    // Check if username, email, or mobile already exists
    $check_conds = [];
    if (!empty($username)) $check_conds[] = "username='$username'";
    if (!empty($email)) $check_conds[] = "email='$email'";
    if (!empty($mobile)) $check_conds[] = "mobile='$mobile'";

    if (!empty($check_conds)) {
        $check_sql = "SELECT id FROM users WHERE " . implode(" OR ", $check_conds);
        $check_res = db_query($check_sql);
        if ($check_res && db_fetch($check_res)) {
            echo json_encode(["success" => false, "error" => "User with this Username, Email, or Mobile already exists. Please Login."]);
            exit;
        }
    }

    $hash = password_hash($password, PASSWORD_DEFAULT);
    
    // Convert empty email/mobile strings to NULL to avoid MySQL UNIQUE constraint failure (Error #1062)
    $email_val = !empty($email) ? "'$email'" : "NULL";
    $mobile_val = !empty($mobile) ? "'$mobile'" : "NULL";

    $sql = "INSERT INTO users (username, email, mobile, password_hash, gender, dob, tob, pob, lat, lon, login_mode)
            VALUES ('$username', $email_val, $mobile_val, '$hash', '$gender', '$dob', '$tob', '$pob', $lat, $lon, 'email')";

    if (db_query($sql)) {
        $_SESSION['user_id'] = $username;
        $_SESSION['username'] = $username;
        $_SESSION['profile'] = [
            "name" => $username,
            "username" => $username,
            "email" => $email,
            "mobile" => $mobile,
            "gender" => $gender,
            "dob" => $dob,
            "tob" => $tob,
            "pob" => $pob,
            "lat" => $lat,
            "lon" => $lon
        ];

        echo json_encode([
            "success" => true,
            "username" => $username,
            "profile" => $_SESSION['profile']
        ]);
    } else {
        global $conn;
        $err_msg = ($conn && is_object($conn) && mysqli_error($conn)) ? mysqli_error($conn) : "Database insertion error. Could not register user into MySQL.";
        echo json_encode(["success" => false, "error" => $err_msg]);
    }
    exit;
}

/* 3. LOGIN */
if ($action === "login") {
    $login_id = db_escape($_POST['login_id'] ?? $_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';

    if (empty($login_id) || empty($password)) {
        echo json_encode(["success" => false, "error" => "Username/Email/Mobile and Password are required."]);
        exit;
    }

    $q = db_query("SELECT * FROM users WHERE email='$login_id' OR username='$login_id' OR mobile='$login_id'");
    $row = db_fetch($q);

    if (!$row) {
        echo json_encode(["success" => false, "error" => "Invalid Credentials. Username/Email/Mobile not registered."]);
        exit;
    }

    // Verify Password against hash or plain
    $pwd_matched = password_verify($password, $row['password_hash']) || 
                  ($row['password_hash'] === hash('sha256', $password)) ||
                  ($row['password_hash'] === $password);

    if ($pwd_matched) {
        // Update last_login timestamp in MySQL database
        db_query("UPDATE users SET last_login = NOW() WHERE id = " . intval($row['id']));

        $_SESSION['user_id'] = $row['id'];
        $_SESSION['username'] = $row['username'];
        $_SESSION['profile'] = [
            "name"                => $row['username'],
            "username"            => $row['username'],
            "email"               => $row['email'],
            "mobile"              => $row['mobile'],
            "gender"              => $row['gender'],
            "dob"                 => $row['dob'],
            "tob"                 => $row['tob'],
            "pob"                 => $row['pob'],
            "lat"                 => floatval($row['lat']),
            "lon"                 => floatval($row['lon']),
            "cached_kundali_json" => $row['cached_kundali_json'],
            "kundali_analytics"   => $row['kundali_analytics']
        ];

        echo json_encode([
            "success" => true,
            "username" => $row['username'],
            "profile" => $_SESSION['profile']
        ]);
    } else {
        echo json_encode(["success" => false, "error" => "Invalid Credentials. Incorrect Password."]);
    }
    exit;
}

/* 3.b GET ALL USERS (FOR ADMIN USERDATA TAB) */
if ($action === "get_all_users") {
    $q = db_query("SELECT * FROM users ORDER BY id DESC LIMIT 500");
    $users = [];
    if ($q) {
        while ($r = db_fetch($q)) {
            $last_login_time = !empty($r['last_login']) ? $r['last_login'] : (!empty($r['last_log']) ? $r['last_log'] : 'Never');
            $created_time = !empty($r['created_at']) ? $r['created_at'] : 'N/A';

            $users[] = [
                "id"         => $r['id'],
                "username"   => $r['username'],
                "email"      => $r['email'] ?? 'N/A',
                "mobile"     => $r['mobile'] ?? 'N/A',
                "gender"     => $r['gender'] ?? 'N/A',
                "created_at" => $created_time,
                "last_login" => $last_login_time
            ];
        }
    }
    echo json_encode(["success" => true, "users" => $users, "count" => count($users)]);
    exit;
}

/* 3b. GET USER PROFILE (birth details + cached kundali + analytics from users table) */
if ($action === "get_user_profile") {
    $username = db_escape($_GET['username'] ?? $_POST['username'] ?? $json_data['username'] ?? '');
    if (empty($username)) {
        echo json_encode(["success" => false, "error" => "Username required"]);
        exit;
    }
    $q = db_query("SELECT username, email, mobile, gender, dob, tob, pob, lat, lon, cached_kundali_json, kundali_analytics FROM users WHERE username='$username' OR email='$username' LIMIT 1");
    $row = db_fetch($q);
    if ($row) {
        echo json_encode(["success" => true, "profile" => [
            "username"           => $row['username'],
            "email"              => $row['email'],
            "mobile"             => $row['mobile'],
            "gender"             => $row['gender'],
            "dob"                => $row['dob'],
            "tob"                => $row['tob'],
            "pob"                => $row['pob'],
            "lat"                => floatval($row['lat']),
            "lon"                => floatval($row['lon']),
            "cached_kundali_json" => $row['cached_kundali_json'],
            "kundali_analytics"   => $row['kundali_analytics']
        ]]);
    } else {
        echo json_encode(["success" => false, "error" => "User not found"]);
    }
    exit;
}

/* 4. SAVE KUNDALI CACHE — writes directly to users.cached_kundali_json */
if ($action === "save_kundali_cache") {
    $username = db_escape($_POST['username'] ?? $_POST['user_identifier'] ?? '');
    $raw_json = db_escape($_POST['raw_json'] ?? '');

    if (empty($username) || empty($raw_json)) {
        echo json_encode(["success" => false, "error" => "Username and Raw JSON are required."]);
        exit;
    }

    $sql = "UPDATE users SET cached_kundali_json='$raw_json' WHERE username='$username' OR email='$username'";

    if (db_query($sql)) {
        echo json_encode(["success" => true, "message" => "Kundali JSON saved to users table."]);
    } else {
        echo json_encode(["success" => false, "error" => "Failed to update cached_kundali_json in users table."]);
    }
    exit;
}

/* 4b. SAVE KUNDALI ANALYTICS — writes directly to users.kundali_analytics */
if ($action === "save_kundali_analytics") {
    $username = db_escape($_POST['username'] ?? $_POST['user_identifier'] ?? '');
    $analytics = db_escape($_POST['kundali_analytics'] ?? $_POST['analytics'] ?? '');

    if (empty($username) || empty($analytics)) {
        echo json_encode(["success" => false, "error" => "Username and Kundali Analytics are required."]);
        exit;
    }

    $sql = "UPDATE users SET kundali_analytics='$analytics' WHERE username='$username' OR email='$username'";

    if (db_query($sql)) {
        echo json_encode(["success" => true, "message" => "Kundali Analytics saved to users table."]);
    } else {
        echo json_encode(["success" => false, "error" => "Failed to update kundali_analytics in users table."]);
    }
    exit;
}

/* 4c. VERIFY SESSION — checks if user account exists in MySQL database */
if ($action === "verify_session" || $action === "check_user") {
    $username = db_escape($_GET['username'] ?? $_POST['username'] ?? '');

    if (empty($username)) {
        echo json_encode(["success" => false, "exists" => false, "error" => "Username parameter is required."]);
        exit;
    }

    $q = db_query("SELECT id, username, email, gender, dob, tob, pob, lat, lon FROM users WHERE username='$username' OR email='$username' LIMIT 1");
    $row = db_fetch($q);

    if ($row) {
        echo json_encode([
            "success"  => true,
            "exists"   => true,
            "user"     => [
                "id"       => $row['id'],
                "username" => $row['username'],
                "email"    => $row['email'],
                "gender"   => $row['gender'],
                "dob"      => $row['dob'],
                "tob"      => $row['tob'],
                "pob"      => $row['pob'],
                "lat"      => floatval($row['lat']),
                "lon"      => floatval($row['lon'])
            ]
        ]);
    } else {
        echo json_encode([
            "success" => false,
            "exists"  => false,
            "error"   => "User account does not exist or has been deleted from database."
        ]);
    }
    exit;
}

/* 5. GET KUNDALI CACHE — reads from users.cached_kundali_json & kundali_analytics directly */
if ($action === "get_kundali_cache" || $action === "get_kundali_analytics") {
    $username = db_escape($_GET['username'] ?? $_POST['username'] ?? '');

    if (empty($username)) {
        echo json_encode(["success" => false, "error" => "Username is required."]);
        exit;
    }

    $q = db_query("SELECT username, dob, tob, pob, lat, lon, cached_kundali_json, kundali_analytics FROM users WHERE username='$username' OR email='$username' LIMIT 1");
    $row = db_fetch($q);

    if ($row) {
        echo json_encode([
            "success"           => true,
            "username"          => $row['username'],
            "dob"               => $row['dob'],
            "tob"               => $row['tob'],
            "pob"               => $row['pob'],
            "lat"               => floatval($row['lat']),
            "lon"               => floatval($row['lon']),
            "raw_json"          => $row['cached_kundali_json'],
            "kundali_analytics" => $row['kundali_analytics']
        ]);
    } else {
        echo json_encode(["success" => false, "error" => "No record found for user."]);
    }
    exit;
}

/* 4. GUEST MODE */
if ($action === "guest") {
    $name = db_escape($_POST['name'] ?? 'Guest');
    $gender = db_escape($_POST['gender'] ?? 'Male');
    $dob = db_escape($_POST['dob'] ?? date('Y-m-d'));
    $tob = db_escape($_POST['tob'] ?? '12:00');
    $pob = db_escape($_POST['pob'] ?? 'New Delhi, India');
    $lat = floatval($_POST['lat'] ?? 28.6139);
    $lon = floatval($_POST['lon'] ?? 77.2090);

    $_SESSION['guest_mode'] = true;
    $_SESSION['username'] = $name;
    $_SESSION['profile'] = [
        "name" => $name,
        "username" => $name,
        "isGuest" => true,
        "gender" => $gender,
        "dob" => $dob,
        "tob" => $tob,
        "pob" => $pob,
        "lat" => $lat,
        "lon" => $lon
    ];

    echo json_encode([
        "success" => true,
        "username" => $name,
        "profile" => $_SESSION['profile']
    ]);
    exit;
}

/* 5.1 GOOGLE ID TOKEN VERIFICATION (Server-Side) */
if ($action === "verify_google_token") {
    $id_token = $_POST['id_token'] ?? '';
    
    if (empty($id_token)) {
        echo json_encode(["success" => false, "error" => "No ID token provided."]);
        exit;
    }

    // Call Google's tokeninfo verification API to verify token signature and claims
    $verify_url = "https://oauth2.googleapis.com/tokeninfo?id_token=" . urlencode($id_token);
    $response = @file_get_contents($verify_url);
    
    if ($response !== false) {
        $token_data = json_decode($response, true);
        if (isset($token_data['email']) && isset($token_data['sub'])) {
            $email = db_escape($token_data['email']);
            $name = db_escape($token_data['name'] ?? $token_data['given_name'] ?? 'Google User');
            $picture = db_escape($token_data['picture'] ?? '');
            
            // Check if user exists in database
            $q = db_query("SELECT * FROM users WHERE email='$email'");
            $user = db_fetch($q);
            
            if (!$user) {
                // Insert new Google OAuth user into MySQL
                $sql = "INSERT INTO users (username, email, social_provider, password_hash, dob, tob, pob, lat, lon)
                        VALUES ('$name', '$email', 'google', 'OAUTH_GOOGLE', '1995-07-20', '12:00', 'New Delhi, India', 28.6139, 77.2090)";
                db_query($sql);
            }
            
            $_SESSION['user_id'] = $email;
            $_SESSION['username'] = $name;
            
            echo json_encode([
                "success" => true,
                "verified_by_google" => true,
                "email" => $token_data['email'],
                "name" => $token_data['name'] ?? $token_data['given_name'] ?? 'Google User',
                "picture" => $token_data['picture'] ?? '',
                "sub" => $token_data['sub']
            ]);
            exit;
        }
    }

    echo json_encode(["success" => false, "error" => "Invalid Google ID Token."]);
    exit;
}

/* 5. SOCIAL AUTH */
if ($action === "social_auth") {
    $provider = db_escape($_POST['provider'] ?? 'google');
    $name = db_escape($_POST['name'] ?? 'Devotee');
    $email = db_escape($_POST['email'] ?? '');
    $gender = db_escape($_POST['gender'] ?? 'Male');
    $dob = db_escape($_POST['dob'] ?? '');
    $tob = db_escape($_POST['tob'] ?? '');
    $pob = db_escape($_POST['pob'] ?? '');
    $lat = floatval($_POST['lat'] ?? 28.6139);
    $lon = floatval($_POST['lon'] ?? 77.2090);

    $_SESSION['user_id'] = $name;
    $_SESSION['username'] = $name;
    $_SESSION['profile'] = [
        "name" => $name,
        "username" => $name,
        "email" => $email,
        "provider" => $provider,
        "gender" => $gender,
        "dob" => $dob,
        "tob" => $tob,
        "pob" => $pob,
        "lat" => $lat,
        "lon" => $lon
    ];

    echo json_encode([
        "success" => true,
        "username" => $name,
        "profile" => $_SESSION['profile']
    ]);
    exit;
}

/* 6. RESET USERNAME & PASSWORD BY MOBILE */
if ($action === "forgot_lookup" || $action === "reset_credentials") {
    $mobile = db_escape($_POST['mobile'] ?? $_POST['identifier'] ?? $json_data['mobile'] ?? $json_data['identifier'] ?? '');
    $new_username = db_escape($_POST['new_username'] ?? $_POST['username'] ?? $json_data['new_username'] ?? $json_data['username'] ?? '');
    $new_password = $_POST['new_password'] ?? $_POST['password'] ?? $json_data['new_password'] ?? $json_data['password'] ?? '';

    if (empty($mobile)) {
        echo json_encode(["success" => false, "error" => "Registered Mobile Number is required."]);
        exit;
    }

    if (empty($new_username) || empty($new_password)) {
        echo json_encode(["success" => false, "error" => "New Username and New Password are required."]);
        exit;
    }

    // Verify mobile number exists in database
    $q = db_query("SELECT id, username FROM users WHERE mobile='$mobile'");
    $row = db_fetch($q);

    if (!$row) {
        echo json_encode([
            "success" => false,
            "error" => "No account found registered with Mobile Number: " . $mobile
        ]);
        exit;
    }

    // Check if new username is already taken by another user
    $chk_user = db_query("SELECT id FROM users WHERE username='$new_username' AND mobile != '$mobile'");
    if ($chk_user && db_fetch($chk_user)) {
        echo json_encode([
            "success" => false,
            "error" => "Username '$new_username' is already taken by another user. Please choose a different username."
        ]);
        exit;
    }

    $pwd_hash = password_hash($new_password, PASSWORD_DEFAULT);
    $upd = db_query("UPDATE users SET username='$new_username', password_hash='$pwd_hash' WHERE mobile='$mobile'");

    if ($upd) {
        echo json_encode([
            "success" => true,
            "message" => "Credentials updated successfully! Reloading page..."
        ]);
    } else {
        echo json_encode([
            "success" => false,
            "error" => "Failed to update database record. Please try again."
        ]);
    }
    exit;
}

/* VISITOR COUNT */
if ($action === "visitor_count") {
    @db_query("CREATE TABLE IF NOT EXISTS site_analytics (id INT PRIMARY KEY AUTO_INCREMENT, total_visits INT DEFAULT 1250, unique_visitors INT DEFAULT 480, last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)");
    $res = db_query("SELECT total_visits, unique_visitors FROM site_analytics WHERE id = 1");
    $row = $res ? db_fetch($res) : null;
    
    if (!$row) {
        @db_query("INSERT INTO site_analytics (id, total_visits, unique_visitors) VALUES (1, 1251, 481)");
        $total = 1251;
        $unique = 481;
    } else {
        $total = intval($row['total_visits']) + 1;
        $unique = intval($row['unique_visitors']);
        $ip = $_SERVER['REMOTE_ADDR'] ?? '';
        $visitor_key = 'sk_vis_' . md5($ip . date('Y-m-d'));
        if (!isset($_COOKIE[$visitor_key])) {
            setcookie($visitor_key, '1', time() + 86400, '/');
            $unique += 1;
        }
        @db_query("UPDATE site_analytics SET total_visits = $total, unique_visitors = $unique WHERE id = 1");
    }
    
    echo json_encode([
        "status" => "success",
        "total_visits" => $total,
        "unique_visitors" => $unique
    ]);
    exit;
}

/* LOGOUT */
if ($action === "logout") {
    session_destroy();
    echo json_encode(["success" => true]);
    exit;
}

echo json_encode(["success" => false, "error" => "Invalid action"]);
?>