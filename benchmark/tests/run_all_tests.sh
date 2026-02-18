#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

sh "$SCRIPT_DIR/test_ab_parse.sh"
sh "$SCRIPT_DIR/test_ab_command_flags.sh"
sh "$SCRIPT_DIR/test_high_concurrency_tuning.sh"
sh "$SCRIPT_DIR/test_integration_no_empty_nginx.sh"

echo "[PASS] all benchmark tests"
