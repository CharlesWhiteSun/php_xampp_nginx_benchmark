<?php
$start = hrtime(true);

$size = isset($_GET['size']) ? (int) $_GET['size'] : 32768;
$iter = isset($_GET['iter']) ? (int) $_GET['iter'] : 50;
if ($size < 1) {
    $size = 1;
}
if ($iter < 1) {
    $iter = 1;
}

$chunk = str_repeat('a', $size);
$tmp = tempnam(sys_get_temp_dir(), 'phpio_');

$bytesWritten = 0;
$bytesRead = 0;

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

$elapsedMs = (hrtime(true) - $start) / 1e6;

header('Content-Type: application/json');
echo json_encode([
    'workload' => 'io',
    'size' => $size,
    'iter' => $iter,
    'bytes_written' => $bytesWritten,
    'bytes_read' => $bytesRead,
    'elapsed_ms' => $elapsedMs,
    'pid' => getmypid(),
]);
