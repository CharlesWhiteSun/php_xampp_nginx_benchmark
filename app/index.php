<?php
header('Content-Type: application/json');

echo json_encode([
    'message' => 'PHP benchmark endpoints',
    'endpoints' => [
        'cpu' => '/cpu.php?n=10000',
        'json' => '/json.php?n=2000',
        'io' => '/io.php?size=32768&iter=50',
    ],
]);
