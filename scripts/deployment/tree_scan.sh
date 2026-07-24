#!/bin/bash
# SYNTAX TREE SCANNER
# BleakNarratives / RootBase
# Pulls clean tree from your three main storage roots
# Excludes: node_modules, pip cache, .git internals, __pycache__, build artifacts
# Output: /storage/emulated/0/RootBase/TREE_SNAPSHOT.txt

OUT="/storage/emulated/0/RootBase/TREE_SNAPSHOT.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

PRUNE_DIRS=(
    "node_modules"
    ".git"
    "__pycache__"
    ".pnpm"
    "pip-build-env*"
    "pip-unpack*"
    "pip-install*"
    "pip-metadata*"
    "pip-ephem*"
    "pip-modern*"
    "pip-build-tracker*"
    "go-build"
    "blobs"
    "*.egg-info"
    ".cache"
    ".npm"
    "venv"
    ".venv"
    "dist"
    "build"
    ".pytest_cache"
)

# Build find prune expression
PRUNE_EXPR=""
for dir in "${PRUNE_DIRS[@]}"; do
    PRUNE_EXPR="$PRUNE_EXPR -o -name '$dir' -prune"
done

echo "ROOTBASE TREE SNAPSHOT" > "$OUT"
echo "Generated: $TIMESTAMP" >> "$OUT"
echo "Scanner: BleakNarratives/Syntax" >> "$OUT"
echo "========================================" >> "$OUT"

scan_dir() {
    local ROOT="$1"
    local LABEL="$2"
    
    echo "" >> "$OUT"
    echo "════════════════════════════════════════" >> "$OUT"
    echo "  $LABEL" >> "$OUT"
    echo "  $ROOT" >> "$OUT"
    echo "════════════════════════════════════════" >> "$OUT"

    if [ ! -d "$ROOT" ]; then
        echo "  [NOT FOUND]" >> "$OUT"
        return
    fi

    find "$ROOT" \
        -maxdepth 6 \
        \( \
            -name "node_modules" \
            -o -name ".git" \
            -o -name "__pycache__" \
            -o -name ".pnpm" \
            -o -name "*.egg-info" \
            -o -name ".cache" \
            -o -name ".npm" \
            -o -name "venv" \
            -o -name ".venv" \
            -o -name "dist" \
            -o -name "build" \
            -o -name ".pytest_cache" \
            -o -name "go-build" \
            -o -name "blobs" \
            -o -name "pip-*" \
            -o -name "tmp" \
        \) -prune \
        -o -print 2>/dev/null \
    | sed "s|$ROOT||" \
    | sort \
    >> "$OUT"
    
    # Quick stats
    FILE_COUNT=$(find "$ROOT" \
        \( -name "node_modules" -o -name ".git" -o -name "__pycache__" \
           -o -name "*.egg-info" -o -name ".cache" -o -name "tmp" \
           -o -name "blobs" -o -name "pip-*" \) -prune \
        -o -type f -print 2>/dev/null | wc -l)
    
    DIR_COUNT=$(find "$ROOT" \
        \( -name "node_modules" -o -name ".git" -o -name "__pycache__" \
           -o -name "*.egg-info" -o -name ".cache" -o -name "tmp" \
           -o -name "blobs" -o -name "pip-*" \) -prune \
        -o -type d -print 2>/dev/null | wc -l)

    echo "" >> "$OUT"
    echo "  [$FILE_COUNT files | $DIR_COUNT dirs]" >> "$OUT"
}

# ── Scan the three roots ──────────────────────────────────────────────────────
scan_dir "/storage/emulated/0/RootBase" "ROOTBASE"
scan_dir "/storage/emulated/0/GRAB"     "GRAB"
scan_dir "/storage/emulated/0/Zip"      "ZIP"

# ── Disk usage summary ────────────────────────────────────────────────────────
echo "" >> "$OUT"
echo "════════════════════════════════════════" >> "$OUT"
echo "  DISK USAGE SUMMARY" >> "$OUT"
echo "════════════════════════════════════════" >> "$OUT"

for ROOT in "/storage/emulated/0/RootBase" "/storage/emulated/0/GRAB" "/storage/emulated/0/Zip"; do
    if [ -d "$ROOT" ]; then
        SIZE=$(du -sh "$ROOT" 2>/dev/null | cut -f1)
        echo "  $SIZE  $ROOT" >> "$OUT"
    fi
done

echo "" >> "$OUT"
echo "════════════════════════════════════════" >> "$OUT"
echo "  END OF SNAPSHOT" >> "$OUT"
echo "════════════════════════════════════════" >> "$OUT"

echo "[SYNTAX] Tree snapshot written to: $OUT"
echo "[SYNTAX] Open with: cat $OUT | less"
