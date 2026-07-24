from __future__ import annotations
import click
from rich import print_json
import json
from datetime import datetime

@click.group()
def dev():
    """Developer visibility mode."""
    pass

@dev.command()
def status():
    """Show internal developer state."""
    data = {"status": "operational", "internal_visibility": "enabled", "mode": "dev"}
    print_json(json.dumps(data, indent=2, default=str))

@click.group()
def superdebug():
    """System-wide debug visibility."""
    pass

@superdebug.command()
def dump():
    """Dump system internal state."""
    data = {"timestamp": datetime.now().isoformat(), "state": "DEBUG_ENABLED", "swarm_intelligence": "active"}
    print_json(json.dumps(data, indent=2, default=str))
