#!/data/data/com.termux/files/usr/bin/bash
# Honest Code Tester - No hallucinated results, no emojis, just facts
# Tests code without the AI safety theater bullshit

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TEST_DIR="${1:-.}"
RESULTS_FILE="test_results_$(date +%Y%m%d_%H%M%S).log"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$RESULTS_FILE"
}

test_script_syntax() {
    local script="$1"
    log "Testing syntax: $script"
    
    if bash -n "$script" 2>&1 | tee -a "$RESULTS_FILE"; then
        log "PASS: Syntax valid"
        return 0
    else
        log "FAIL: Syntax errors detected"
        return 1
    fi
}

test_script_execution() {
    local script="$1"
    log "Testing execution: $script"
    
    # Run with timeout and capture all output
    if timeout 30s bash "$script" > /tmp/exec_out.log 2>&1; then
        log "PASS: Script executed without errors"
        cat /tmp/exec_out.log >> "$RESULTS_FILE"
        return 0
    else
        local exit_code=$?
        log "FAIL: Script failed with exit code $exit_code"
        cat /tmp/exec_out.log >> "$RESULTS_FILE"
        return 1
    fi
}

check_for_emoji_pollution() {
    local script="$1"
    log "Checking for emoji pollution: $script"
    
    # Detect non-ASCII characters that aren't part of legitimate code
    if grep -P '[^\x00-\x7F]' "$script" | grep -v '^#' > /tmp/emoji_check.log; then
        log "WARN: Non-ASCII characters detected (possible emoji pollution)"
        cat /tmp/emoji_check.log >> "$RESULTS_FILE"
        return 1
    else
        log "PASS: No emoji pollution detected"
        return 0
    fi
}

check_hardcoded_outputs() {
    local script="$1"
    log "Checking for hardcoded/fake outputs: $script"
    
    # Look for suspicious patterns that indicate scripted outputs
    local suspicious_patterns=(
        'echo.*PASS'
        'echo.*SUCCESS'
        'echo.*✓'
        'echo.*All tests passed'
        'cat.*<<.*PASS'
    )
    
    local found_suspicious=0
    for pattern in "${suspicious_patterns[@]}"; do
        if grep -E "$pattern" "$script" > /dev/null; then
            log "WARN: Suspicious hardcoded output pattern: $pattern"
            grep -n -E "$pattern" "$script" >> "$RESULTS_FILE"
            found_suspicious=1
        fi
    done
    
    if [[ $found_suspicious -eq 0 ]]; then
        log "PASS: No obvious fake outputs detected"
        return 0
    else
        return 1
    fi
}

analyze_test_coverage() {
    local script="$1"
    log "Analyzing test coverage: $script"
    
    # Count actual test assertions vs output statements
    local assertions=$(grep -c -E '(if.*then|test |\\[.*\\]|\$\\?)' "$script" || echo 0)
    local outputs=$(grep -c -E 'echo|printf' "$script" || echo 0)
    
    log "Assertions found: $assertions"
    log "Output statements: $outputs"
    
    if [[ $assertions -eq 0 ]] && [[ $outputs -gt 0 ]]; then
        log "FAIL: Script has outputs but no actual tests"
        return 1
    elif [[ $outputs -gt $((assertions * 3)) ]]; then
        log "WARN: Suspiciously high output-to-test ratio"
        return 1
    else
        log "PASS: Test coverage appears legitimate"
        return 0
    fi
}

run_full_audit() {
    local script="$1"
    
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}HONEST AUDIT: $script${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    local tests_passed=0
    local tests_failed=0
    
    # Run all checks
    test_script_syntax "$script" && ((tests_passed++)) || ((tests_failed++))
    check_for_emoji_pollution "$script" && ((tests_passed++)) || ((tests_failed++))
    check_hardcoded_outputs "$script" && ((tests_passed++)) || ((tests_failed++))
    analyze_test_coverage "$script" && ((tests_passed++)) || ((tests_failed++))
    
    # Only run execution if syntax is valid
    if bash -n "$script" 2>/dev/null; then
        test_script_execution "$script" && ((tests_passed++)) || ((tests_failed++))
    else
        ((tests_failed++))
    fi
    
    echo -e "${BLUE}========================================${NC}"
    echo -e "Results: ${GREEN}$tests_passed passed${NC} | ${RED}$tests_failed failed${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    log "SUMMARY: $tests_passed passed, $tests_failed failed"
    
    return $tests_failed
}

# Main execution
if [[ -f "$TEST_DIR" ]]; then
    # Single file
    run_full_audit "$TEST_DIR"
elif [[ -d "$TEST_DIR" ]]; then
    # Directory of scripts
    for script in "$TEST_DIR"/*.sh; do
        if [[ -f "$script" ]]; then
            run_full_audit "$script"
            echo
        fi
    done
else
    echo "Usage: $0 <script_or_directory>"
    exit 1
fi

echo
echo "Full results saved to: $RESULTS_FILE"
