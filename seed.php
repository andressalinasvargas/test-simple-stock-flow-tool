<?php

declare(strict_types=1);

/**
 * Simple Stock Flow CLI Seeder (HTTP API).
 * Runs against the running API container or localhost.
 */

$baseUrl = getenv('API_BASE_URL') ?: 'http://127.0.0.1:8000';
$adminEmail = getenv('ADMIN_EMAIL') ?: 'admin@stockflow.local';
$adminPassword = getenv('ADMIN_PASSWORD') ?: 'Admin123*!';

function request(string $method, string $url, ?array $data = null, ?string $token = null): array
{
    $headers = [
        'Accept: application/json',
        'Content-Type: application/json',
    ];
    if ($token !== null) {
        $headers[] = "Authorization: Bearer {$token}";
    }

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    if ($data !== null) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    }

    $resp = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($status === 204) {
        return [];
    }

    $json = json_decode((string) $resp, true);
    if (!is_array($json)) {
        throw new RuntimeException("HTTP {$status}: {$resp}");
    }

    return $json;
}

echo "[*] Conectando a Simple Stock Flow API en {$baseUrl}...\n";

// 1. Login admin
echo "[*] Autenticando administrador ({$adminEmail})...\n";
$login = request('POST', "{$baseUrl}/api/auth/login", [
    'username' => $adminEmail,
    'password' => $adminPassword,
]);
$adminToken = $login['accessToken'];
echo "    [+] Token obtenido con éxito.\n";

// 2. Categorías
echo "[*] Consultando categorías...\n";
$categories = request('GET', "{$baseUrl}/api/categories", null, $adminToken);
$catMap = [];
foreach ($categories as $cat) {
    $catMap[strtolower($cat['name'])] = $cat['id'];
}
echo "    [+] " . count($categories) . " categorías encontradas.\n";

// 3. Productos existentes (idempotencia)
$existing = request('GET', "{$baseUrl}/api/products?page=1&size=100", null, $adminToken);
$existingNames = [];
foreach ($existing['items'] ?? [] as $item) {
    $existingNames[strtolower($item['name'])] = true;
}

$demoProducts = [
    ['name' => 'Martillo Galponero 20oz', 'price' => 38000.00, 'stock' => 25, 'category' => 'Herramientas'],
    ['name' => 'Juego Destornilladores 6 Piezas', 'price' => 42000.00, 'stock' => 18, 'category' => 'Herramientas'],
    ['name' => 'Cinta Aislante 20m Negra', 'price' => 4500.00, 'stock' => 100, 'category' => 'Electricidad'],
    ['name' => 'Breaker Monopolar 20A', 'price' => 18500.00, 'stock' => 40, 'category' => 'Electricidad'],
    ['name' => 'Tubo PVC Presión 1/2 pulgada 6m', 'price' => 16000.00, 'stock' => 30, 'category' => 'Fontanería'],
    ['name' => 'Pintura Vinilo Blanco Tipo 1 Galón', 'price' => 68000.00, 'stock' => 15, 'category' => 'Pinturas'],
];

foreach ($demoProducts as $p) {
    if (isset($existingNames[strtolower($p['name'])])) {
        echo "    [-] Omitiendo '{$p['name']}': ya existe.\n";
        continue;
    }

    $catId = $catMap[strtolower($p['category'])] ?? reset($catMap);
    $created = request('POST', "{$baseUrl}/api/products", [
        'name' => $p['name'],
        'price' => $p['price'],
        'stock' => $p['stock'],
        'categoryId' => $catId,
    ], $adminToken);

    echo "    [+] Producto creado: '{$p['name']}' (ID: {$created['id']})\n";
}

// 4. Registro y login de vendedor
echo "[*] Verificando vendedor de demostración...\n";
try {
    request('POST', "{$baseUrl}/api/auth/register", [
        'username' => 'vendedor.demo',
        'password' => 'Password123*!',
        'role' => 'seller',
    ], $adminToken);
    echo "    [+] Vendedor registrado.\n";
} catch (\Throwable $e) {
    echo "    [-] Vendedor ya disponible.\n";
}

$sellerLogin = request('POST', "{$baseUrl}/api/auth/login", [
    'username' => 'vendedor.demo',
    'password' => 'Password123*!',
]);
$sellerToken = $sellerLogin['accessToken'];

// 5. Registrar venta de prueba
$catalog = request('GET', "{$baseUrl}/api/products?page=1&size=5", null, $sellerToken);
if (!empty($catalog['items'])) {
    $item = $catalog['items'][0];
    echo "[*] Registrando venta de prueba para '{$item['name']}'...\n";
    $sale = request('POST', "{$baseUrl}/api/sales", [
        'lines' => [
            ['productId' => $item['id'], 'quantity' => 1],
        ],
    ], $sellerToken);
    echo "    [+] Venta registrada (ID: {$sale['id']})\n";
}

echo "[*] Siembra completada con éxito.\n";
