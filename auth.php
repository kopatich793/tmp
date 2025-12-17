session_start();
$conn = mysqli_connect("localhost", "user", "pass", "db");

$username = $_GET['username'] ?? '';
$password = $_GET['password'] ?? '';
$login = $_GET['Login'] ?? '';

if (!isset($_SESSION['attempts'])) {
    $_SESSION['attempts'] = 0;
}

if ($_SESSION['attempts'] >= 5) {
    die("Слишком много попыток входа");
}

$stmt = mysqli_prepare($conn, "SELECT password FROM users WHERE user = ?");
mysqli_stmt_bind_param($stmt, "s", $username);
mysqli_stmt_execute($stmt);
$result = mysqli_stmt_get_result($stmt);

if ($row = mysqli_fetch_assoc($result)) {
    if (password_verify($password, $row['password'])) {
        $_SESSION['attempts'] = 0;
        echo "Успешная авторизация";
        exit;
    }
}

$_SESSION['attempts']++;
sleep(2);
echo "Неверный логин или пароль";



