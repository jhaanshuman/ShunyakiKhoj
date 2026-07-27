<?php
header("Content-Type: text/plain");
echo "PHP Version: " . phpversion() . "\n";
echo "mysqli: " . (function_exists("mysqli_connect") ? "YES" : "NO") . "\n\n";
$host = "sql106.infinityfree.com";
$user = "if0_41366642";
$password = "ySp2t8afpDyv";
$db = "if0_41366642_sanskrit_dict_mw";
mysqli_report(MYSQLI_REPORT_OFF);
$conn = @mysqli_connect($host, $user, $password, $db);
if (!$conn) {
    echo "MySQL: FAILED\n";
    echo "Error: " . mysqli_connect_error() . "\n";
    echo "Code: " . mysqli_connect_errno() . "\n";
} else {
    echo "MySQL: SUCCESS\n";
    echo "Server: " . mysqli_get_server_info($conn) . "\n\n";
    $res = mysqli_query($conn, "SHOW TABLES");
    echo "Tables:\n";
    while ($row = mysqli_fetch_row($res)) { echo "  - " . $row[0] . "\n"; }
    $res2 = mysqli_query($conn, "DESCRIBE users");
    if ($res2) {
        echo "\nusers columns:\n";
        while ($row = mysqli_fetch_assoc($res2)) {
            echo "  " . $row["Field"] . " => " . $row["Type"] . "\n";
        }
    } else { echo "\nusers table: not found\n"; }
    mysqli_close($conn);
}
?>
