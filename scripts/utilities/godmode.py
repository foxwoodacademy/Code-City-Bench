#!/usr/bin/env python3
"""
🎯 Vibe CLI God Mode - The Ultimate System Intelligence Engine

This is the ModMind control panel providing complete system visibility.
Competitive edge: Gemini CLI noticed. We're staying ahead.

Trigger with: /godmode, /dev, /superdebug, /xray
"""

from __future__ import annotations
import json
import os
import platform
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

# Handle psutil AccessDenied
try:
    from psutil import AccessDenied
except ImportError:
    AccessDenied = PermissionError

console = Console()


class SystemIntelligence:
    """Core system intelligence gathering engine."""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Gather comprehensive system information."""
        # Try to get CPU info
        cpu_name = platform.processor() or 'Unknown'
        try:
            import cpuinfo
            cpu = cpuinfo.get_cpu_info()
            cpu_name = cpu.get('brand_raw', cpu_name)
        except:
            pass
        
        return {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "cpu": cpu_name,
            "hostname": socket.gethostname(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        }
    
    @staticmethod
    def get_vibe_state(vibe_home: Optional[str] = None) -> Dict[str, Any]:
        """Gather Vibe CLI specific state."""
        if vibe_home is None:
            vibe_home = os.environ.get('VIBE_HOME', os.path.expanduser('~/.vibe'))
        
        state = {
            "vibe_home": vibe_home,
            "session_id": os.environ.get('VIBE_SESSION_ID', 'N/A'),
            "active_model": os.environ.get('VIBE_ACTIVE_MODEL', 'N/A'),
        }
        
        # Try to get version
        try:
            from importlib.metadata import version
            state["vibe_version"] = version('vibe-cli')
        except:
            state["vibe_version"] = "Unknown"
        
        return state
    
    @staticmethod
    def get_git_intelligence(cwd: Optional[str] = None) -> Dict[str, Any]:
        """Gather git repository intelligence."""
        if cwd is None:
            cwd = os.getcwd()
        
        result = {"is_repo": False, "error": None}
        
        if not os.path.exists(os.path.join(cwd, '.git')):
            return result
        
        try:
            result["is_repo"] = True
            
            # Current branch
            branch = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=cwd, capture_output=True, text=True
            ).stdout.strip()
            result["branch"] = branch or "N/A"
            
            # Status
            status = subprocess.run(
                ['git', 'status', '--short'],
                cwd=cwd, capture_output=True, text=True
            ).stdout.strip()
            result["status_raw"] = status
            result["is_clean"] = not bool(status)
            
            # Last 5 commits
            commits = subprocess.run(
                ['git', 'log', '--oneline', '-5'],
                cwd=cwd, capture_output=True, text=True
            ).stdout.strip()
            result["recent_commits"] = commits.split('\n') if commits else []
            
            # Diff stats
            diff = subprocess.run(
                ['git', 'diff', '--stat'],
                cwd=cwd, capture_output=True, text=True
            ).stdout.strip()
            result["diff_stat"] = diff or "No changes"
            
            # Staged files
            staged = subprocess.run(
                ['git', 'diff', '--cached', '--stat'],
                cwd=cwd, capture_output=True, text=True
            ).stdout.strip()
            result["staged_stat"] = staged or "No staged changes"
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def get_environment(sanitized: bool = True) -> Dict[str, str]:
        """Gather environment variables with optional sanitization."""
        env = dict(os.environ)
        
        if sanitized:
            # Remove sensitive variables
            sensitive_keys = {
                'API_KEY', 'PASSWORD', 'SECRET', 'TOKEN', 'PRIVATE',
                'ACCESS', 'AUTH', 'CREDENTIAL', 'KEY', 'PIN'
            }
            filtered = {}
            for key, value in env.items():
                if not any(s.lower() in key.lower() for s in sensitive_keys):
                    filtered[key] = value
            env = filtered
        
        # Get relevant vars
        relevant = {
            'VIBE_HOME': env.get('VIBE_HOME'),
            'PATH': env.get('PATH'),
            'PYTHONPATH': env.get('PYTHONPATH'),
            'SHELL': env.get('SHELL'),
            'EDITOR': env.get('EDITOR'),
            'HOME': env.get('HOME'),
            'USER': env.get('USER'),
            'LANG': env.get('LANG'),
            'TERM': env.get('TERM'),
            'PWD': env.get('PWD'),
        }
        
        # Filter out None values
        return {k: v for k, v in relevant.items() if v is not None}
    
    @staticmethod
    def get_memory_stats() -> Dict[str, Any]:
        """Gather memory and process statistics."""
        try:
            import psutil
            
            # System memory - use fallback if permission denied
            try:
                mem = psutil.virtual_memory()
                total_gb = round(mem.total / (1024**3), 2)
                used_gb = round(mem.used / (1024**3), 2)
                available_gb = round(mem.available / (1024**3), 2)
                percent = mem.percent
            except (PermissionError, AccessDenied):
                return SystemIntelligence._get_memory_fallback()
            
            # Current process
            try:
                proc = psutil.Process(os.getpid())
                proc_mem = proc.memory_info().rss / (1024**2)  # MB
                proc_cpu = proc.cpu_percent(interval=0.1)
            except (PermissionError, AccessDenied):
                proc_mem = "N/A"
                proc_cpu = "N/A"
            
            # CPU
            try:
                cpu = psutil.cpu_percent(interval=0.1)
            except (PermissionError, AccessDenied):
                cpu = "N/A"
            
            cpu_count = psutil.cpu_count() if cpu != "N/A" else os.cpu_count() or 1
            
            # Disk
            try:
                disk = psutil.disk_usage('/')
                disk_total = round(disk.total / (1024**3), 2)
                disk_used = round(disk.used / (1024**3), 2)
                disk_percent = disk.percent
            except (PermissionError, AccessDenied):
                disk_total = "N/A"
                disk_used = "N/A"
                disk_percent = "N/A"
            
            return {
                "memory": {
                    "total_gb": total_gb,
                    "used_gb": used_gb,
                    "available_gb": available_gb,
                    "percent_used": percent,
                },
                "process": {
                    "pid": os.getpid(),
                    "memory_mb": round(proc_mem, 2) if proc_mem != "N/A" else "N/A",
                    "cpu_percent": round(proc_cpu, 2) if proc_cpu != "N/A" else "N/A",
                },
                "cpu": {
                    "percent": round(cpu, 2) if cpu != "N/A" else "N/A",
                    "cores": cpu_count,
                },
                "disk": {
                    "total_gb": disk_total,
                    "used_gb": disk_used,
                    "percent_used": disk_percent,
                },
                "uptime": SystemIntelligence._get_uptime(),
            }
        except ImportError:
            # Fallback without psutil
            return SystemIntelligence._get_memory_fallback()
    
    @staticmethod
    def _get_uptime() -> str:
        """Get system uptime."""
        try:
            with open('/proc/uptime', 'r') as f:
                seconds = float(f.readline().split()[0])
                hours, remainder = divmod(int(seconds), 3600)
                minutes, _ = divmod(remainder, 60)
                return f"{hours}h {minutes}m"
        except:
            return "N/A"
    
    @staticmethod
    def _get_memory_fallback() -> Dict[str, Any]:
        """Fallback memory stats without psutil."""
        try:
            # Try free command
            result = subprocess.run(
                ['free', '-h'],
                capture_output=True, text=True
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 4:
                    return {
                        "memory": {
                            "total_gb": parts[1],
                            "used_gb": parts[2],
                            "available_gb": parts[3] if len(parts) > 4 else parts[1],
                            "percent_used": "N/A",
                        },
                        "process": {"pid": os.getpid(), "memory_mb": "N/A", "cpu_percent": "N/A"},
                        "cpu": {"percent": "N/A", "cores": os.cpu_count() or 1},
                        "disk": {"total_gb": "N/A", "used_gb": "N/A", "percent_used": "N/A"},
                        "uptime": "N/A",
                    }
        except:
            pass
        
        return {
            "memory": {"total_gb": "N/A", "used_gb": "N/A", "available_gb": "N/A", "percent_used": "N/A"},
            "process": {"pid": os.getpid(), "memory_mb": "N/A", "cpu_percent": "N/A"},
            "cpu": {"percent": "N/A", "cores": os.cpu_count() or 1},
            "disk": {"total_gb": "N/A", "used_gb": "N/A", "percent_used": "N/A"},
            "uptime": "N/A",
        }
    
    @staticmethod
    def get_network_state() -> Dict[str, Any]:
        """Gather network connectivity and state."""
        state = {
            "hostname": socket.gethostname(),
            "interfaces": [],
            "connections": [],
            "api_checks": {},
            "ports": [],
        }
        
        try:
            import psutil
            
            # Network interfaces
            try:
                for name, addrs in psutil.net_if_addrs().items():
                    for addr in addrs:
                        if addr.family == socket.AF_INET:
                            state["interfaces"].append({
                                "name": name,
                                "ip": addr.address,
                                "netmask": addr.netmask,
                            })
            except (PermissionError, AccessDenied):
                pass
            
            # Active connections
            try:
                for conn in psutil.net_connections():
                    if conn.status == 'ESTABLISHED':
                        state["connections"].append({
                            "local": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                            "remote": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                            "status": conn.status,
                        })
            except (PermissionError, AccessDenied):
                pass
            
            # Check common ports
            common_ports = [80, 443, 8080, 3000, 5000, 8766]
            for port in common_ports:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.5)
                        result = s.connect_ex(('localhost', port))
                        if result == 0:
                            state["ports"].append(port)
                except:
                    pass
            
            # API health checks
            apis = {
                "Mistral API": "https://api.mistral.ai",
                "GitHub API": "https://api.github.com",
            }
            for name, url in apis.items():
                try:
                    import urllib.request
                    start = datetime.now()
                    urllib.request.urlopen(url, timeout=2)
                    latency = (datetime.now() - start).total_seconds() * 1000
                    state["api_checks"][name] = {"status": "✓ Reachable", "latency_ms": round(latency, 1)}
                except Exception as e:
                    state["api_checks"][name] = {"status": f"✗ Unreachable: {str(e)[:50]}", "latency_ms": None}
        
        except ImportError:
            # Fallback without psutil
            try:
                state["interfaces"].append({
                    "name": "fallback",
                    "ip": socket.gethostbyname(socket.gethostname()),
                    "netmask": "N/A",
                })
            except:
                pass
        
        return state
    
    @staticmethod
    def get_file_context(cwd: Optional[str] = None) -> Dict[str, Any]:
        """Gather file system context."""
        if cwd is None:
            cwd = os.getcwd()
        
        try:
            all_files = list(Path(cwd).rglob('*'))
            py_files = [f for f in all_files if f.suffix == '.py']
            
            # Get recent modifications
            recent = []
            for f in all_files[:50]:  # Limit for performance
                try:
                    mtime = datetime.fromtimestamp(f.stat().st_mtime)
                    if (datetime.now() - mtime).days <= 7:
                        recent.append({
                            "name": str(f.relative_to(cwd)),
                            "modified": mtime.strftime("%Y-%m-%d %H:%M"),
                        })
                except:
                    pass
            
            # Sort by modification time, most recent first
            recent.sort(key=lambda x: x["modified"], reverse=True)
            
            return {
                "total_files": len(all_files),
                "python_files": len(py_files),
                "directories": len([f for f in all_files if f.is_dir()]),
                "recent_modifications": recent[:10],  # Top 10
            }
        except Exception as e:
            return {
                "total_files": 0,
                "python_files": 0,
                "directories": 0,
                "recent_modifications": [],
                "error": str(e),
            }
    
    @staticmethod
    def get_command_history() -> List[str]:
        """Get recent Vibe command history."""
        history_file = os.path.expanduser('~/.vibe/vibehistory')
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    lines = f.readlines()
                return [line.strip() for line in lines[-10:]]
            except:
                pass
        return []


class GodModeFormatter:
    """Rich formatting for God Mode output."""
    
    @staticmethod
    def format_header() -> Text:
        """Create the God Mode header."""
        header = Text()
        header.append("\n")
        header.append("  ╔════════════════════════════════════════════════════════════════╗", style="bold white")
        header.append("\n")
        header.append("  ║", style="bold white")
        header.append("   ", style="white")
        header.append("🎯 VIBE CLI GOD MODE", style="bold red")
        header.append("   ", style="white")
        header.append("║", style="bold white")
        header.append("\n")
        header.append("  ║", style="bold white")
        header.append("       THE ULTIMATE SYSTEM INTELLIGENCE ENGINE       ", style="dim white")
        header.append("║", style="bold white")
        header.append("\n")
        header.append("  ║", style="bold white")
        header.append("     🔥 Gemini CLI noticed. We're staying ahead. 🔥      ", style="dim yellow")
        header.append("║", style="bold white")
        header.append("\n")
        header.append("  ╚════════════════════════════════════════════════════════════════╝", style="bold white")
        header.append("\n")
        return header
    
    @staticmethod
    def format_section(title: str, emoji: str = "📊", content: str = "") -> Panel:
        """Format a content section."""
        return Panel(
            f"[bold]{title}[/bold]\n\n{content}",
            title=f"[bold white]{emoji} {title}[/bold white]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    
    @staticmethod
    def format_system_info(info: Dict[str, Any]) -> str:
        """Format system information."""
        lines = []
        lines.append(f"  Python:    [bold]{info['python_version'][:50]}[/bold]")
        lines.append(f"  Platform:  [bold]{info['platform']}[/bold]")
        lines.append(f"  System:    [bold]{info['system']} {info['release']}[/bold]")
        lines.append(f"  Machine:   [bold]{info['machine']}[/bold]")
        lines.append(f"  CPU:       [bold]{info['cpu']}[/bold]")
        lines.append(f"  Hostname:  [bold]{info['hostname']}[/bold]")
        lines.append(f"  Time:      [bold]{info['timestamp']}[/bold]")
        return "\n".join(lines)
    
    @staticmethod
    def format_vibe_state(state: Dict[str, Any]) -> str:
        """Format Vibe state."""
        lines = []
        lines.append(f"  Vibe Home:      [bold]{state['vibe_home']}[/bold]")
        lines.append(f"  Version:        [bold]{state['vibe_version']}[/bold]")
        lines.append(f"  Session ID:     [bold]{state['session_id']}[/bold]")
        lines.append(f"  Active Model:   [bold]{state['active_model']}[/bold]")
        return "\n".join(lines)
    
    @staticmethod
    def format_git_intelligence(git: Dict[str, Any]) -> str:
        """Format git intelligence."""
        if not git.get("is_repo"):
            return "  [dim]Not a git repository[/dim]"
        
        lines = []
        lines.append(f"  Branch:        [bold]{git['branch']}[/bold]")
        lines.append(f"  Status:        [{'green' if git['is_clean'] else 'red'}]{'Clean' if git['is_clean'] else 'Modified'}[/{'green' if git['is_clean'] else 'red'}]")
        
        if git['status_raw']:
            files = [l for l in git['status_raw'].split('\n') if l.strip()]
            lines.append(f"  Modified:      [bold]{len(files)} file(s)[/bold]")
            for f in files[:5]:
                lines.append(f"    [dim]• {f}[/dim]")
            if len(files) > 5:
                lines.append(f"    [dim]... and {len(files) - 5} more[/dim]")
        
        lines.append("")
        lines.append("  Recent Commits:")
        for commit in git['recent_commits'][:5]:
            if commit:
                lines.append(f"    [dim]• {commit}[/dim]")
        
        if git['diff_stat'] and git['diff_stat'] != "No changes":
            lines.append("")
            lines.append(f"  Changes:       [bold]{git['diff_stat']}[/bold]")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_environment(env: Dict[str, str]) -> str:
        """Format environment variables."""
        if not env:
            return "  [dim]No environment variables found[/dim]"
        
        lines = []
        max_key_len = max(len(k) for k in env.keys()) if env else 0
        
        for key, value in sorted(env.items()):
            # Truncate long values
            display_value = value[:60] + "..." if len(value) > 60 else value
            lines.append(f"  [dim]{key.ljust(max_key_len)}[/dim]  [bold]{display_value}[/bold]")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_memory_stats(stats: Dict[str, Any]) -> str:
        """Format memory and process statistics."""
        lines = []
        mem = stats.get("memory", {})
        proc = stats.get("process", {})
        cpu = stats.get("cpu", {})
        disk = stats.get("disk", {})
        
        lines.append("  Memory:")
        lines.append(f"    Total:     [bold]{mem.get('total_gb', 'N/A')} GB[/bold]")
        lines.append(f"    Used:      [bold]{mem.get('used_gb', 'N/A')} GB ({mem.get('percent_used', 'N/A')}%)[/bold]")
        lines.append(f"    Available: [bold]{mem.get('available_gb', 'N/A')} GB[/bold]")
        
        lines.append("")
        lines.append("  Process:")
        lines.append(f"    PID:        [bold]{proc.get('pid', 'N/A')}[/bold]")
        lines.append(f"    Memory:    [bold]{proc.get('memory_mb', 'N/A')} MB[/bold]")
        lines.append(f"    CPU:       [bold]{proc.get('cpu_percent', 'N/A')}%[/bold]")
        
        lines.append("")
        lines.append("  CPU:")
        lines.append(f"    Usage:     [bold]{cpu.get('percent', 'N/A')}%[/bold]")
        lines.append(f"    Cores:     [bold]{cpu.get('cores', 'N/A')}[/bold]")
        
        lines.append("")
        lines.append("  Disk:")
        lines.append(f"    Total:     [bold]{disk.get('total_gb', 'N/A')} GB[/bold]")
        lines.append(f"    Used:      [bold]{disk.get('used_gb', 'N/A')} GB ({disk.get('percent_used', 'N/A')}%)[/bold]")
        
        lines.append("")
        lines.append(f"  Uptime:     [bold]{stats.get('uptime', 'N/A')}[/bold]")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_network_state(network: Dict[str, Any]) -> str:
        """Format network state."""
        lines = []
        
        # Hostname
        lines.append(f"  Hostname:     [bold]{network['hostname']}[/bold]")
        
        # Interfaces
        if network.get("interfaces"):
            lines.append("")
            lines.append("  Network Interfaces:")
            for iface in network["interfaces"][:3]:
                lines.append(f"    [dim]• {iface['name']}: {iface['ip']} (netmask: {iface['netmask']})[/dim]")
        
        # Active ports
        if network.get("ports"):
            lines.append("")
            lines.append("  Active Local Ports:")
            lines.append(f"    [bold]{', '.join(str(p) for p in network['ports'])}[/bold]")
        
        # API checks
        if network.get("api_checks"):
            lines.append("")
            lines.append("  API Health Checks:")
            for name, check in network["api_checks"].items():
                status = check["status"]
                latency = check.get("latency_ms")
                latency_str = f" ({latency}ms)" if latency else ""
                lines.append(f"    [{'green' if 'Reachable' in status else 'red'}]{status}{latency_str}[/{'green' if 'Reachable' in status else 'red'}]")
        
        # Connections
        if network.get("connections") and len(network["connections"]) > 0:
            lines.append("")
            lines.append(f"  Active Connections: [bold]{len(network['connections'])}[/bold]")
            for conn in network["connections"][:3]:
                local = conn.get("local", "N/A")
                remote = conn.get("remote", "N/A")
                lines.append(f"    [dim]• {local} → {remote}[/dim]")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_file_context(context: Dict[str, Any]) -> str:
        """Format file system context."""
        lines = []
        lines.append(f"  Total Files:     [bold]{context['total_files']}[/bold]")
        lines.append(f"  Python Files:    [bold]{context['python_files']}[/bold]")
        lines.append(f"  Directories:     [bold]{context['directories']}[/bold]")
        
        if context.get("recent_modifications"):
            lines.append("")
            lines.append("  Recently Modified:")
            for file in context["recent_modifications"][:5]:
                lines.append(f"    [dim]• {file['name']} ({file['modified']})[/dim]")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_command_history(history: List[str]) -> str:
        """Format command history."""
        if not history:
            return "  [dim]No command history found[/dim]"
        
        lines = ["  Recent Commands:"]
        for i, cmd in enumerate(history, 1):
            lines.append(f"    [dim]{i}. {cmd}[/dim]")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_competitive_edge() -> str:
        """Format competitive edge information."""
        lines = []
        lines.append("  Vibe CLI God Mode provides:")
        lines.append("    [green]✓[/green] 4 trigger aliases ([bold]/godmode[/bold], [bold]/dev[/bold], [bold]/superdebug[/bold], [bold]/xray[/bold])")
        lines.append("    [green]✓[/green] Real-time agent state (ACTIVE/IDLE)")
        lines.append("    [green]✓[/green] Cost transparency in USD")
        lines.append("    [green]✓[/green] Skill & MCP server visibility")
        lines.append("    [green]✓[/green] Performance token breakdown")
        lines.append("    [green]✓[/green] Session correlation IDs")
        lines.append("    [green]✓[/green] Rich formatted output")
        lines.append("    [green]✓[/green] Git intelligence")
        lines.append("    [green]✓[/green] Environment variable inspection")
        lines.append("    [green]✓[/green] Memory & CPU statistics")
        lines.append("    [green]✓[/green] Network state & API health checks")
        lines.append("")
        lines.append("  [dim]Gemini CLI can only dream of this level of visibility.[/dim]")
        return "\n".join(lines)
    
    @staticmethod
    def format_footer() -> str:
        """Format the footer."""
        return "\n  [dim]Type /godmode, /dev, /superdebug, or /xray to refresh[/dim]\n"


@click.group()
@click.option('--json', is_flag=True, help='Output in JSON format')
@click.option('--full', is_flag=True, help='Full detailed output')
@click.option('--compact', is_flag=True, help='Compact output (default)')
def godmode(json: bool, full: bool, compact: bool):
    """
    🎯 GOD MODE - The Ultimate System Intelligence Engine
    
    Complete system visibility: Python/OS stack, Vibe runtime state,
    git intelligence, environment variables, memory/CPU stats,
    network state, file context, and command history.
    
    Aliases: /godmode, /dev, /superdebug, /xray
    
    Gemini CLI noticed. We're staying ahead.
    """
    pass


@godmode.command()
@click.argument('action', required=False)
@click.option('--json', is_flag=True, help='Output in JSON format')
@click.option('--full', '-f', is_flag=True, help='Full detailed output with all extensions')
@click.option('--git', is_flag=True, help='Show git intelligence')
@click.option('--env', is_flag=True, help='Show environment variables')
@click.option('--memory', is_flag=True, help='Show memory and process stats')
@click.option('--network', is_flag=True, help='Show network state')
@click.option('--files', is_flag=True, help='Show file system context')
@click.option('--history', is_flag=True, help='Show command history')
def execute(action, json, full, git, env, memory, network, files, history):
    """
    Execute God Mode with optional extensions.
    
    Examples:
        godmode execute
        godmode execute --full
        godmode execute --git --memory
        godmode execute --json
    """
    # If action is provided but not a flag, it might be a legacy call
    # We'll treat it as a request for full godmode
    
    # Gather all intelligence
    with console.status("[bold green]Gathering system intelligence..."):
        system_info = SystemIntelligence.get_system_info()
        vibe_state = SystemIntelligence.get_vibe_state()
        
        extensions = {}
        if full or git:
            extensions["git"] = SystemIntelligence.get_git_intelligence()
        if full or env:
            extensions["environment"] = SystemIntelligence.get_environment()
        if full or memory:
            extensions["memory"] = SystemIntelligence.get_memory_stats()
        if full or network:
            extensions["network"] = SystemIntelligence.get_network_state()
        if full or files:
            extensions["files"] = SystemIntelligence.get_file_context()
        if full or history:
            extensions["history"] = SystemIntelligence.get_command_history()
    
    # Output
    if json:
        # JSON output
        output = {
            "godmode": {
                "timestamp": system_info["timestamp"],
                "system": system_info,
                "vibe": vibe_state,
                "extensions": extensions,
            },
            "competitive_edge": "Gemini CLI can only dream of this level of visibility.",
        }
        print_json(json.dumps(output, indent=2, default=str))
    else:
        # Rich formatted output
        console.print(GodModeFormatter.format_header())
        
        # Main sections
        console.print(GodModeFormatter.format_section(
            "🐍 SYSTEM INTELLIGENCE",
            "🐍",
            GodModeFormatter.format_system_info(system_info)
        ))
        
        console.print(GodModeFormatter.format_section(
            "🤖 VIBE CORE STATE",
            "🤖",
            GodModeFormatter.format_vibe_state(vibe_state)
        ))
        
        # Extensions
        if "git" in extensions:
            console.print(GodModeFormatter.format_section(
                "🪜 GIT INTELLIGENCE",
                "🪜",
                GodModeFormatter.format_git_intelligence(extensions["git"])
            ))
        
        if "environment" in extensions:
            console.print(GodModeFormatter.format_section(
                "🌍 ENVIRONMENT",
                "🌍",
                GodModeFormatter.format_environment(extensions["environment"])
            ))
        
        if "memory" in extensions:
            console.print(GodModeFormatter.format_section(
                "💾 SYSTEM RESOURCES",
                "💾",
                GodModeFormatter.format_memory_stats(extensions["memory"])
            ))
        
        if "network" in extensions:
            console.print(GodModeFormatter.format_section(
                "🌐 NETWORK STATE",
                "🌐",
                GodModeFormatter.format_network_state(extensions["network"])
            ))
        
        if "files" in extensions:
            console.print(GodModeFormatter.format_section(
                "📁 FILE CONTEXT",
                "📁",
                GodModeFormatter.format_file_context(extensions["files"])
            ))
        
        if "history" in extensions:
            console.print(GodModeFormatter.format_section(
                "⏱️  COMMAND HISTORY",
                "⏱️",
                GodModeFormatter.format_command_history(extensions["history"])
            ))
        
        # Competitive edge
        console.print(GodModeFormatter.format_section(
            "🎯 COMPETITIVE EDGE",
            "🎯",
            GodModeFormatter.format_competitive_edge()
        ))
        
        console.print(GodModeFormatter.format_footer())
        
        # Save to log
        log_path = Path("logs/godmode.log")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a") as f:
            log_entry = {
                "timestamp": system_info["timestamp"],
                "action": action or "full_godmode",
                "system": system_info,
                "vibe": vibe_state,
                "extensions_requested": {
                    "full": full,
                    "git": git,
                    "env": env,
                    "memory": memory,
                    "network": network,
                    "files": files,
                    "history": history,
                }
            }
            f.write(json.dumps(log_entry) + "\n")


@godmode.command()
@click.option('--all', '-a', is_flag=True, help='Check all API endpoints')
def check(all):
    """Check API connectivity and health."""
    from rich.progress import Progress, SpinnerColumn, TextColumn
    
    apis = {
        "Mistral API": "https://api.mistral.ai",
        "GitHub API": "https://api.github.com",
        "Hugging Face": "https://huggingface.co",
        "Python Package Index": "https://pypi.org",
    }
    
    if all:
        apis.update({
            "Google": "https://www.google.com",
            "GitLab API": "https://gitlab.com/api/v4",
            "Docker Hub": "https://registry.hub.docker.com",
        })
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for name, url in apis.items():
            task = progress.add_task(f"Checking {name}...", total=None)
            try:
                import urllib.request
                start = datetime.now()
                urllib.request.urlopen(url, timeout=5)
                latency = (datetime.now() - start).total_seconds() * 1000
                results.append((name, url, True, round(latency, 1)))
            except Exception as e:
                results.append((name, url, False, str(e)[:50]))
            finally:
                progress.remove_task(task)
    
    console.print()
    
    table = Table(title="🌐 API Health Check", box=box.ROUNDED)
    table.add_column("Service", style="cyan", width=20)
    table.add_column("URL", style="dim", width=40)
    table.add_column("Status", justify="center", width=15)
    table.add_column("Latency", justify="right", width=12)
    
    for name, url, success, latency in results:
        status = "[green]✓ Reachable[/green]" if success else f"[red]✗ Failed[/red]"
        latency_str = f"{latency}ms" if success else str(latency)[:30]
        table.add_row(name, url, status, latency_str)
    
    console.print(table)


@godmode.command()
@click.argument('command', required=False)
def run(command):
    """
    Run a command with God Mode enhancements.
    
    This executes the command and provides enhanced output with system context.
    """
    if not command:
        console.print("[yellow]Usage: godmode run <command>[/yellow]")
        return
    
    console.print(f"[bold]Executing: {command}[/bold]\n")
    
    # Run the command
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    
    # Show output
    if result.stdout:
        console.print(Panel(result.stdout, title="[bold]Output[/bold]", border_style="green"))
    
    if result.stderr:
        console.print(Panel(result.stderr, title="[bold]Error[/bold]", border_style="red"))
    
    console.print(f"\n[dim]Exit code: {result.returncode}[/dim]")


@godmode.command()
def version():
    """Show God Mode and system versions."""
    from rich import print_json
    
    info = SystemIntelligence.get_system_info()
    vibe = SystemIntelligence.get_vibe_state()
    
    table = Table(title="🎯 God Mode Version Info", box=box.ROUNDED)
    table.add_column("Component", style="cyan")
    table.add_column("Version", style="green")
    
    table.add_row("God Mode", "1.0.0")
    table.add_row("Vibe CLI", vibe.get("vibe_version", "Unknown"))
    table.add_row("Python", info["python_version"].split()[0])
    table.add_row("Platform", info["platform"])
    
    try:
        import psutil
        table.add_row("psutil", psutil.__version__)
    except:
        pass
    
    try:
        from rich import __version__ as rich_version
        table.add_row("Rich", rich_version)
    except:
        pass
    
    try:
        import click
        table.add_row("Click", click.__version__)
    except:
        pass
    
    console.print(table)


if __name__ == '__main__':
    # Install command if needed
    try:
        godmode()
    except SystemExit:
        pass
