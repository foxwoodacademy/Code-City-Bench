# Whorl PowerShell Runtime
# Standardized entry point for RootBase agentic operations.

param (
    [string]$cmd
)

function Whorl-Exec {
    param([string]$Action)
    
    # Unified JSON communication protocol
    $Response = [PSCustomObject]@{
        status = "executing"
        cmd = $Action
    }
    $Response | ConvertTo-Json
}

if ($cmd) {
    Whorl-Exec -Action $cmd
}
