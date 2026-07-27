<?php
/**
 * db.php - Database Configuration & Wrapper for ShunyakiKhoj
 * Supports MySQL (sql106.infinityfree.com) with automatic SQLite fallback for local dev.
 */

$host = "sql106.infinityfree.com";
$user = "if0_41366642";
$password = "ySp2t8afpDyv";
$db = "if0_41366642_sanskrit_dict_mw";

$conn = null;
$db_type = 'mysql';

// Disable default warning reporting
mysqli_report(MYSQLI_REPORT_OFF);

try {
    $conn = @mysqli_connect($host, $user, $password, $db);
} catch (Exception $e) {
    $conn = null;
}

if (!$conn) {
    $db_type = 'sqlite';
    try {
        $conn = new SQLite3(__DIR__ . '/sanskrit_ai.db');
        
        // Ensure users table exists with birth details & mobile fields
        $conn->exec("CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            mobile TEXT UNIQUE,
            password_hash TEXT,
            gender TEXT,
            dob TEXT,
            tob TEXT,
            pob TEXT,
            lat REAL,
            lon REAL,
            def_lang TEXT DEFAULT 'en',
            login_mode TEXT DEFAULT 'email',
            social_provider TEXT,
            cached_kundali_json TEXT,
            last_log DATETIME DEFAULT CURRENT_TIMESTAMP
        )");

        // Table for cached Kundali Raw JSON
        $conn->exec("CREATE TABLE IF NOT EXISTS user_kundali_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_identifier TEXT UNIQUE,
            dob TEXT,
            tob TEXT,
            pob TEXT,
            lat REAL,
            lon REAL,
            raw_json TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )");
    } catch (Exception $e) {
        // Fallback: Continue operating with session/localStorage support
        $db_type = 'offline';
    }
} else {
    mysqli_set_charset($conn, "utf8mb4");
    
    // Auto-create MySQL tables if missing
    $mysql_users_table = "CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        email VARCHAR(150) UNIQUE,
        mobile VARCHAR(30) UNIQUE,
        password_hash VARCHAR(255),
        gender VARCHAR(20),
        dob VARCHAR(20),
        tob VARCHAR(20),
        pob VARCHAR(255),
        lat DOUBLE,
        lon DOUBLE,
        def_lang VARCHAR(10) DEFAULT 'en',
        login_mode VARCHAR(30) DEFAULT 'email',
        social_provider VARCHAR(50),
        cached_kundali_json LONGTEXT,
        last_log DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;";
    
    $mysql_cache_table = "CREATE TABLE IF NOT EXISTS user_kundali_cache (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_identifier VARCHAR(150) UNIQUE NOT NULL,
        dob VARCHAR(20),
        tob VARCHAR(20),
        pob VARCHAR(255),
        lat DOUBLE,
        lon DOUBLE,
        raw_json LONGTEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;";
    
    @mysqli_query($conn, $mysql_users_table);
    @mysqli_query($conn, $mysql_cache_table);
}

function db_query($sql) {
    global $conn, $db_type;
    if ($db_type === 'sqlite') {
        try {
            return $conn->query($sql);
        } catch (Exception $e) {
            return false;
        }
    } else if ($db_type === 'mysql') {
        return mysqli_query($conn, $sql);
    }
    return false;
}

function db_fetch($result) {
    global $db_type;
    if (!$result) return null;
    if ($db_type === 'sqlite') {
        return $result->fetchArray(SQLITE3_ASSOC);
    } else if ($db_type === 'mysql') {
        return mysqli_fetch_assoc($result);
    }
    return null;
}

function db_escape($str) {
    global $conn, $db_type;
    if (!$str) return '';
    if ($db_type === 'sqlite') {
        return SQLite3::escapeString($str);
    } else if ($db_type === 'mysql') {
        return mysqli_real_escape_string($conn, $str);
    }
    return addslashes($str);
}
?>