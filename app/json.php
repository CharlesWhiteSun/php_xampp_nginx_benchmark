<?php
$start = hrtime(true);

$n = isset($_GET['n']) ? (int) $_GET['n'] : 2000;
if ($n < 1) {
    $n = 1;
}

$items = [];
for ($i = 0; $i < $n; $i++) {
    $items[] = [
        'id' => $i,
        'name' => 'item_' . $i,
        'value' => $i * 3,
        'flag' => ($i % 2) === 0,
    ];
}

$json = json_encode([
    'workload' => 'json',
    'count' => $n,
    'items' => $items,
]);

$elapsedMs = (hrtime(true) - $start) / 1e6;

header('Content-Type: application/json');
echo json_encode([
    'workload' => 'json',
    'count' => $n,
    'json_bytes' => strlen($json),
    'elapsed_ms' => $elapsedMs,
    'pid' => getmypid(),
]);
