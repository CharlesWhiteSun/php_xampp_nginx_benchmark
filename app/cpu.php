<?php
$start = hrtime(true);

$n = isset($_GET['n']) ? (int) $_GET['n'] : 10000;
if ($n < 1) {
    $n = 1;
}

$sum = 0.0;
for ($i = 1; $i <= $n; $i++) {
    $sum += sqrt($i);
}

$elapsedMs = (hrtime(true) - $start) / 1e6;

header('Content-Type: application/json');
echo json_encode([
    'workload' => 'cpu',
    'n' => $n,
    'sum' => $sum,
    'elapsed_ms' => $elapsedMs,
    'pid' => getmypid(),
]);
