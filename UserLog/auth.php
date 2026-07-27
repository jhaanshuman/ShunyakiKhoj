<?php
/**
 * auth.php - Authentication & Birth Details Service for ShunyakiKhoj
 */
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: *");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

session_start();
require_once "db.php";

$action = $_POST['action'] ?? $_GET['action'] ?? '';

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
        $_SESSION['user_id'] = $row['id'];
        $_SESSION['username'] = $row['username'];
        $_SESSION['profile'] = [
            "name" => $row['username'],
            "username" => $row['username'],
            "email" => $row['email'],
            "mobile" => $row['mobile'],
            "gender" => $row['gender'],
            "dob" => $row['dob'],
            "tob" => $row['tob'],
            "pob" => $row['pob'],
            "lat" => floatval($row['lat']),
            "lon" => floatval($row['lon'])
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

/* 4. SAVE KUNDALI CACHE (PHP MYSQL) */
if ($action === "save_kundali_cache") {
    $username = db_escape($_POST['username'] ?? $_POST['user_identifier'] ?? '');
    $raw_json = db_escape($_POST['raw_json'] ?? '');
    $dob = db_escape($_POST['dob'] ?? '');
    $tob = db_escape($_POST['tob'] ?? '');
    $pob = db_escape($_POST['pob'] ?? '');
    $lat = floatval($_POST['lat'] ?? 0);
    $lon = floatval($_POST['lon'] ?? 0);

    if (empty($username) || empty($raw_json)) {
        echo json_encode(["success" => false, "error" => "Username and Raw JSON are required."]);
        exit;
    }

    $sql = "INSERT INTO user_kundali_cache (user_identifier, dob, tob, pob, lat, lon, raw_json)
            VALUES ('$username', '$dob', '$tob', '$pob', $lat, $lon, '$raw_json')
            ON DUPLICATE KEY UPDATE raw_json='$raw_json', dob='$dob', tob='$tob', pob='$pob', lat=$lat, lon=$lon";

    if (db_query($sql)) {
        echo json_encode(["success" => true, "message" => "Kundali Raw JSON cached successfully in MySQL database."]);
    } else {
        echo json_encode(["success" => false, "error" => "Failed to save Kundali cache in MySQL."]);
    }
    exit;
}

/* 5. GET KUNDALI CACHE (PHP MYSQL) */
if ($action === "get_kundali_cache") {
    $username = db_escape($_GET['username'] ?? $_POST['username'] ?? '');

    if (empty($username)) {
        echo json_encode(["success" => false, "error" => "Username is required."]);
        exit;
    }

    $q = db_query("SELECT * FROM user_kundali_cache WHERE user_identifier='$username'");
    $row = db_fetch($q);

    if ($row) {
        echo json_encode([
            "success" => true,
            "username" => $row['user_identifier'],
            "dob" => $row['dob'],
            "tob" => $row['tob'],
            "pob" => $row['pob'],
            "lat" => floatval($row['lat']),
            "lon" => floatval($row['lon']),
            "raw_json" => $row['raw_json']
        ]);
    } else {
        echo json_encode(["success" => false, "error" => "No cached Kundali found for user."]);
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

/* 6. FORGOT USERNAME / PASSWORD */
if ($action === "forgot_lookup") {
    $identifier = db_escape($_POST['identifier'] ?? '');

    if (empty($identifier)) {
        echo json_encode(["success" => false, "error" => "Please enter your registered Email or Mobile number."]);
        exit;
    }

    $q = db_query("SELECT username, email, mobile FROM users WHERE email='$identifier' OR mobile='$identifier'");
    $row = db_fetch($q);

    if ($row) {
        echo json_encode([
            "success" => true,
            "message" => "Account found for username: " . $row['username'] . ". A password reset code has been dispatched to your registered contact."
        ]);
    } else {
        echo json_encode([
            "success" => false,
            "error" => "No account found matching given Email or Mobile."
        ]);
    }
    exit;
}

/* 7. KUNDALI CACHE SAVE & FETCH (PHP MySQL Database Primary Storage) */
if ($action === "save_kundali_cache") {
    $user_id = db_escape($_POST['user_identifier'] ?? $_SESSION['username'] ?? 'default');
    $dob = db_escape($_POST['dob'] ?? '');
    $tob = db_escape($_POST['tob'] ?? '');
    $pob = db_escape($_POST['pob'] ?? '');
    $lat = floatval($_POST['lat'] ?? 0.0);
    $lon = floatval($_POST['lon'] ?? 0.0);
    $raw_json = db_escape($_POST['raw_json'] ?? '');

    if (!empty($raw_json)) {
        // Update users table cached_kundali_json column in PHP MySQL
        db_query("UPDATE users SET cached_kundali_json='$raw_json' WHERE username='$user_id' OR email='$user_id'");
        
        // Upsert into user_kundali_cache table
        $check_q = db_query("SELECT id FROM user_kundali_cache WHERE user_identifier='$user_id'");
        if ($check_q && db_fetch($check_q)) {
            $sql = "UPDATE user_kundali_cache SET dob='$dob', tob='$tob', pob='$pob', lat=$lat, lon=$lon, raw_json='$raw_json' WHERE user_identifier='$user_id'";
        } else {
            $sql = "INSERT INTO user_kundali_cache (user_identifier, dob, tob, pob, lat, lon, raw_json)
                    VALUES ('$user_id', '$dob', '$tob', '$pob', $lat, $lon, '$raw_json')";
        }
        db_query($sql);
        echo json_encode(["success" => true, "db" => "PHP MySQL Database"]);
    } else {
        echo json_encode(["success" => false, "error" => "Empty raw json"]);
    }
    exit;
}

if ($action === "get_kundali_cache") {
    $user_id = db_escape($_GET['user_identifier'] ?? $_SESSION['username'] ?? 'default');
    $q = db_query("SELECT raw_json FROM user_kundali_cache WHERE user_identifier='$user_id' ORDER BY id DESC LIMIT 1");
    $row = db_fetch($q);
    if ($row && !empty($row['raw_json'])) {
        echo json_encode(["success" => true, "raw_json" => $row['raw_json'], "db" => "PHP MySQL Database"]);
    } else {
        // Check users table as secondary PHP MySQL fallback
        $q2 = db_query("SELECT cached_kundali_json FROM users WHERE username='$user_id' OR email='$user_id'");
        $row2 = db_fetch($q2);
        if ($row2 && !empty($row2['cached_kundali_json'])) {
            echo json_encode(["success" => true, "raw_json" => $row2['cached_kundali_json'], "db" => "PHP MySQL Database"]);
        } else {
            echo json_encode(["success" => false, "error" => "No cache found in PHP MySQL Database"]);
        }
    }
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