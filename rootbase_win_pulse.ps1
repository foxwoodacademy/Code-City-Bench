# RootBase Windows Pulse Launcher - v1.0
# This script initializes the Sovereign Stack on Windows.

$ErrorActionPreference = "Stop"
Write-Host "🚀 Initializing RootBase Windows Pulse..." -ForegroundColor Cyan

# 1. Python Check
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[-] Error: Python not found. Please install Python 3.10+ from python.org" -ForegroundColor Red
    exit
}

# 2. Virtual Environment Setup
if (!(Test-Path "venv")) {
    Write-Host "[+] Creating Virtual Environment..." -ForegroundColor Gray
    python -m venv venv
}

# Activate Environment
Write-Host "[+] Activating Sovereign Environment..." -ForegroundColor Gray
.\venv\Scripts\Activate.ps1

# 3. Dependency Sync
Write-Host "[+] Syncing Dependencies..." -ForegroundColor Gray
pip install -r requirements.txt --quiet

# 4. Service Selection
Write-Host "`n--- RootBase Service Menu ---" -ForegroundColor Yellow
Write-Host "1. Start Mel-Bridge (Visual Dashboard)"
Write-Host "2. Run Oneshot Pipeline (Revenue Generation)"
Write-Host "3. Launch DNA Sequencer (Strategy Simulation)"
Write-Host "4. Run MRD Auto-Generator (Documentation)"
Write-Host "Q. Quit"

$choice = Read-Host "`nSelect a service to launch"

switch ($choice) {
    "1" { python src/swarm/molt/mel_bridge.py }
    "2" { python rootbase_oneshot.py } # Assuming .sh was converted to .py
    "3" { python src/swarm/molt/dna_sequencer.py }
    "4" { python rootbase_mrd_generator.py }
    "Q" { exit }
    Default { Write-Host "Invalid selection." -ForegroundColor Red }
}

Write-Host "`n[!] Pulse Session Ended." -ForegroundColor Cyan
