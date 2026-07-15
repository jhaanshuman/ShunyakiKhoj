<?php

$host = "sql106.infinityfree.com";
$user = "if0_41366642";
$password = "ySp2t8afpDyv";
$db = "if0_41366642_sanskrit_dict_mw";

$conn = null;
$db_type = 'mysql';

// Turn off error throwing to prevent crash on connection failure
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
        // Ensure table exists
        $conn->exec("CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            Gen TEXT,
            DOB TEXT,
            DefLang TEXT,
            login_mode TEXT DEFAULT 'email',
            LastLog DATETIME DEFAULT CURRENT_TIMESTAMP
        )");
    } catch (Exception $e) {
        echo json_encode([
            "success" => false,
            "error" => "Database connection failed (MySQL failed, and SQLite failed: " . $e->getMessage() . ")"
        ]);
        exit;
    }
} else {
    mysqli_set_charset($conn, "utf8mb4");
}

function db_query($sql) {
    global $conn, $db_type;
    if ($db_type === 'sqlite') {
        try {
            return $conn->query($sql);
        } catch (Exception $e) {
            return false;
        }
    } else {
        return mysqli_query($conn, $sql);
    }
}

function db_fetch($result) {
    global $db_type;
    if (!$result) return null;
    if ($db_type === 'sqlite') {
        return $result->fetchArray(SQLITE3_ASSOC);
    } else {
        return mysqli_fetch_assoc($result);
    }
}

function db_escape($str) {
    global $conn, $db_type;
    if ($db_type === 'sqlite') {
        return SQLite3::escapeString($str);
    } else {
        return mysqli_real_escape_string($conn, $str);
    }
}
?>