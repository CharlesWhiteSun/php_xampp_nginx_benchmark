#!/bin/bash
# Test script to verify environment variables are being passed correctly

echo "=========================================="
echo "Environment Variables Test"
echo "=========================================="
echo ""
echo "Received DURATION: $DURATION"
echo "Received CONNECTIONS: $CONNECTIONS"
echo ""

if [ -z "$DURATION" ]; then
    echo "ERROR: DURATION not set!"
    exit 1
fi

if [ -z "$CONNECTIONS" ]; then
    echo "ERROR: CONNECTIONS not set!"
    exit 1
fi

# Verify they are numbers
if ! [[ "$DURATION" =~ ^[0-9]+$ ]]; then
    echo "ERROR: DURATION is not a number: $DURATION"
    exit 1
fi

if ! [[ "$CONNECTIONS" =~ ^[0-9]+$ ]]; then
    echo "ERROR: CONNECTIONS is not a number: $CONNECTIONS"
    exit 1
fi

echo "✓ DURATION is valid: $DURATION seconds"
echo "✓ CONNECTIONS is valid: $CONNECTIONS"
echo ""
echo "Test PASSED - Environment variables are correctly set!"
