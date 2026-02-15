<?php
$start = hrtime(true);

$size = isset($_GET['size']) ? (int) $_GET['size'] : 32768;
$iter = isset($_GET['iter']) ? (int) $_GET['iter'] : 50;

// 選擇 IO 模式：memory（推薦）或 disk
$mode = isset($_GET['mode']) ? $_GET['mode'] : 'memory';

if ($size < 1) {
    $size = 1;
}
if ($iter < 1) {
    $iter = 1;
}

$chunk = str_repeat('a', $size);
$bytesWritten = 0;
$bytesRead = 0;

if ($mode === 'memory') {
    // ============================================================
    // 方案 A：使用 PHP 內存流（推薦 - 避免磁盤 IO 開銷）
    // ============================================================
    $fh = fopen('php://memory', 'r+');
    
    // 寫入操作
    for ($i = 0; $i < $iter; $i++) {
        $bytesWritten += fwrite($fh, $chunk);
    }
    
    // 重置文件指針
    rewind($fh);
    
    // 讀取操作
    while (!feof($fh)) {
        $data = fread($fh, $size);
        if ($data === false) {
            break;
        }
        $bytesRead += strlen($data);
    }
    
    fclose($fh);
    
} else {
    // ============================================================
    // 原始方案：物理臨時文件（保留以進行比較）
    // ============================================================
    $tmp = tempnam(sys_get_temp_dir(), 'phpio_');
    
    $fh = fopen($tmp, 'wb');
    for ($i = 0; $i < $iter; $i++) {
        $bytesWritten += fwrite($fh, $chunk);
    }
    fclose($fh);
    
    $fh = fopen($tmp, 'rb');
    while (!feof($fh)) {
        $data = fread($fh, $size);
        if ($data === false) {
            break;
        }
        $bytesRead += strlen($data);
    }
    fclose($fh);
    
    unlink($tmp);
}

$elapsedMs = (hrtime(true) - $start) / 1e6;

header('Content-Type: application/json');
echo json_encode([
    'workload' => 'io',
    'mode' => $mode,
    'size' => $size,
    'iter' => $iter,
    'bytes_written' => $bytesWritten,
    'bytes_read' => $bytesRead,
    'elapsed_ms' => $elapsedMs,
    'pid' => getmypid(),
]);
