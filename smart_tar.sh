#!/bin/bash

# smart_tar.sh — auto-name tarballs after directories, exclude cruft

SOURCE_DIR="${1:-.}"
OUTPUT_DIR="${2:-.}"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: $SOURCE_DIR does not exist"
    exit 1
fi

DIRNAME=$(basename "$SOURCE_DIR")
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TARBALL="$OUTPUT_DIR/${DIRNAME}_${TIMESTAMP}.tar.gz"

echo "[smart_tar] Packing: $SOURCE_DIR"
echo "[smart_tar] Output: $TARBALL"

tar --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.pytest_cache' \
    --exclude='node_modules' \
    --exclude='.venv' \
    --exclude='venv' \
    --exclude='.env' \
    --exclude='.cache' \
    --exclude='.local' \
    --exclude='*.egg-info' \
    --exclude='dist' \
    --exclude='build' \
    -czf "$TARBALL" -C "$(dirname "$SOURCE_DIR")" "$DIRNAME"

SIZE=$(du -h "$TARBALL" | cut -f1)
echo "[smart_tar] Complete: $SIZE"
ls -lh "$TARBALL"
