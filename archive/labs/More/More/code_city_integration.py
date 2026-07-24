#!/data/data/com.termux/files/usr/bin/python3
"""
Code City - Rampage Refactor Integration
Turns vulnerability scanning into a gamified city-destruction experience

How it works:
- Each code file = a building in the city
- Vulnerabilities = structural weaknesses
- You're the monster that finds and smashes weak buildings
- Fix the vuln = rebuild the building stronger
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Import the scanners we built
sys.path.insert(0, str(Path(__file__).parent))

class Building:
    """A building in Code City (represents a code file)"""
    
    def __init__(self, filepath: Path, lines_of_code: int):
        self.filepath = filepath
        self.name = filepath.stem
        self.height = min(lines_of_code // 10, 50)  # Taller = more code
        self.health = 100
        self.vulnerabilities = []
        self.is_destroyed = False
        self.last_attacked = None
        
    def take_damage(self, vuln_severity: str) -> int:
        """Building takes damage from vulnerability"""
        damage_map = {
            "critical": 50,
            "high": 30,
            "medium": 15,
            "low": 5
        }
        damage = damage_map.get(vuln_severity, 10)
        self.health -= damage
        
        if self.health <= 0:
            self.health = 0
            self.is_destroyed = True
            
        return damage
        
    def repair(self, amount: int = 20):
        """Repair building (fix vulnerability)"""
        self.health = min(100, self.health + amount)
        if self.health > 0:
            self.is_destroyed = False
            
    def to_dict(self) -> Dict:
        """Convert to JSON for visualization"""
        return {
            "name": self.name,
            "filepath": str(self.filepath),
            "height": self.height,
            "health": self.health,
            "is_destroyed": self.is_destroyed,
            "vulnerability_count": len(self.vulnerabilities),
            "critical_vulns": len([v for v in self.vulnerabilities if v["severity"] == "critical"])
        }


class CodeCity:
    """The city - a visualization of your codebase"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.buildings: Dict[str, Building] = {}
        self.attack_log = []
        self.score = 0
        self.buildings_destroyed = 0
        
    def scan_project(self, extensions: List[str] = None):
        """Scan project and create buildings"""
        if extensions is None:
            extensions = ['.py', '.js', '.sh', '.html', '.css']
            
        print(f"🏗️  Building Code City from {self.project_root}...")
        
        for ext in extensions:
            for filepath in self.project_root.rglob(f'*{ext}'):
                if filepath.is_file():
                    try:
                        lines = len(filepath.read_text().splitlines())
                        building = Building(filepath, lines)
                        self.buildings[str(filepath)] = building
                        print(f"   Built: {building.name} ({building.height} floors)")
                    except Exception as e:
                        print(f"   Skipped {filepath}: {e}")
                        
        print(f"\n🏙️  Code City constructed: {len(self.buildings)} buildings")
        
    def rampage(self, scanner_results: List[Dict]):
        """RAMPAGE MODE - Attack buildings with vulnerabilities"""
        print("\n" + "=" * 70)
        print("🦖 RAMPAGE MODE ACTIVATED")
        print("=" * 70 + "\n")
        
        if not scanner_results:
            print("😴 No vulnerabilities found. City is safe... for now.")
            return
            
        # Group vulns by file
        vulns_by_file = {}
        for vuln in scanner_results:
            filepath = vuln["file"]
            if filepath not in vulns_by_file:
                vulns_by_file[filepath] = []
            vulns_by_file[filepath].append(vuln)
            
        # Attack each building
        for filepath, vulns in vulns_by_file.items():
            if filepath not in self.buildings:
                continue
                
            building = self.buildings[filepath]
            
            print(f"\n🎯 Targeting: {building.name}")
            print(f"   Height: {building.height} floors | Health: {building.health}%")
            print(f"   Vulnerabilities found: {len(vulns)}")
            
            # Store vulns in building
            building.vulnerabilities = vulns
            
            # Attack for each vulnerability
            total_damage = 0
            for vuln in vulns:
                damage = building.take_damage(vuln["severity"])
                total_damage += damage
                
                severity_emoji = {
                    "critical": "💥",
                    "high": "🔥", 
                    "medium": "⚡",
                    "low": "💨"
                }
                
                print(f"   {severity_emoji.get(vuln['severity'], '⚠️')} [{vuln['severity'].upper()}] {vuln['pattern']}")
                print(f"      Line {vuln['line']}: {vuln['description']}")
                print(f"      Damage: -{damage}% health")
                
                self.score += damage
                
            print(f"\n   💔 Total damage: {total_damage}%")
            print(f"   🏥 Remaining health: {building.health}%")
            
            if building.is_destroyed:
                print(f"   💀 BUILDING DESTROYED!")
                self.buildings_destroyed += 1
            else:
                print(f"   🏚️  Building damaged but standing")
                
            self.attack_log.append({
                "timestamp": datetime.now().isoformat(),
                "building": building.name,
                "damage": total_damage,
                "destroyed": building.is_destroyed,
                "vulns": len(vulns)
            })
            
    def generate_stats(self) -> Dict:
        """Generate game stats"""
        total_buildings = len(self.buildings)
        destroyed = sum(1 for b in self.buildings.values() if b.is_destroyed)
        damaged = sum(1 for b in self.buildings.values() if b.health < 100 and not b.is_destroyed)
        healthy = total_buildings - destroyed - damaged
        
        total_vulns = sum(len(b.vulnerabilities) for b in self.buildings.values())
        critical_vulns = sum(
            len([v for v in b.vulnerabilities if v["severity"] == "critical"])
            for b in self.buildings.values()
        )
        
        avg_health = sum(b.health for b in self.buildings.values()) / total_buildings if total_buildings > 0 else 0
        
        return {
            "total_buildings": total_buildings,
            "destroyed": destroyed,
            "damaged": damaged,
            "healthy": healthy,
            "total_vulnerabilities": total_vulns,
            "critical_vulnerabilities": critical_vulns,
            "rampage_score": self.score,
            "average_building_health": round(avg_health, 1),
            "destruction_rate": round((destroyed / total_buildings * 100), 1) if total_buildings > 0 else 0
        }
        
    def print_scoreboard(self):
        """Print game-style scoreboard"""
        stats = self.generate_stats()
        
        print("\n" + "=" * 70)
        print("📊 RAMPAGE SCOREBOARD")
        print("=" * 70)
        print(f"""
🏙️  Code City Status:
   Total Buildings:        {stats['total_buildings']}
   💚 Healthy:             {stats['healthy']}
   💛 Damaged:             {stats['damaged']}
   💀 Destroyed:           {stats['destroyed']}
   
🦖 Rampage Stats:
   Score:                  {stats['rampage_score']} points
   Destruction Rate:       {stats['destruction_rate']}%
   Average Building HP:    {stats['average_building_health']}%
   
⚠️  Vulnerabilities:
   Total Found:            {stats['total_vulnerabilities']}
   💥 Critical:            {stats['critical_vulnerabilities']}
""")
        
        # Rank
        if stats['destruction_rate'] > 50:
            rank = "🏆 MASTER DESTROYER"
        elif stats['destruction_rate'] > 25:
            rank = "💪 SKILLED MONSTER"
        elif stats['destruction_rate'] > 10:
            rank = "🔰 ROOKIE RAMPAGE"
        else:
            rank = "😇 CODE GUARDIAN"
            
        print(f"   Rank: {rank}")
        print("=" * 70)
        
    def save_city_state(self, output_path: Path):
        """Save city state as JSON for visualization"""
        city_data = {
            "project_root": str(self.project_root),
            "timestamp": datetime.now().isoformat(),
            "stats": self.generate_stats(),
            "buildings": [b.to_dict() for b in self.buildings.values()],
            "attack_log": self.attack_log
        }
        
        with open(output_path, 'w') as f:
            json.dump(city_data, f, indent=2)
            
        print(f"\n💾 City state saved to: {output_path}")
        print("   (Use this for 3D visualization, leaderboards, etc.)")
        
    def generate_html_visualization(self, output_path: Path):
        """Generate simple HTML visualization"""
        buildings_html = []
        
        for building in sorted(self.buildings.values(), key=lambda b: b.height, reverse=True):
            # Color based on health
            if building.is_destroyed:
                color = "#000000"
                status = "DESTROYED"
            elif building.health < 30:
                color = "#ff4444"
                status = "CRITICAL"
            elif building.health < 70:
                color = "#ffaa00"
                status = "DAMAGED"
            else:
                color = "#44ff44"
                status = "HEALTHY"
                
            buildings_html.append(f"""
            <div class="building" style="height: {building.height * 3}px; background: {color};" 
                 title="{building.name}: {building.health}% HP, {len(building.vulnerabilities)} vulns">
                <div class="building-label">{building.name[:15]}</div>
                <div class="health-bar" style="width: {building.health}%"></div>
            </div>
            """)
            
        stats = self.generate_stats()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Code City - Rampage Refactor</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: #1a1a2e;
            color: #eee;
            font-family: 'Courier New', monospace;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
            background: #16213e;
            padding: 20px;
            border-radius: 10px;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #ff6b6b;
        }}
        .city {{
            display: flex;
            align-items: flex-end;
            justify-content: center;
            gap: 5px;
            min-height: 400px;
            background: #0f3460;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
        }}
        .building {{
            width: 40px;
            position: relative;
            border: 2px solid #000;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        .building:hover {{
            transform: scale(1.1);
            z-index: 10;
        }}
        .building-label {{
            position: absolute;
            bottom: -20px;
            font-size: 8px;
            white-space: nowrap;
            transform: rotate(-45deg);
            transform-origin: top left;
        }}
        .health-bar {{
            position: absolute;
            bottom: 0;
            height: 3px;
            background: #00ff00;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦖 Code City - Rampage Refactor</h1>
        <p>Your codebase as a destructible city</p>
    </div>
    
    <div class="stats">
        <div class="stat">
            <div class="stat-value">{stats['total_buildings']}</div>
            <div>Buildings</div>
        </div>
        <div class="stat">
            <div class="stat-value" style="color: #ff4444">{stats['destroyed']}</div>
            <div>Destroyed</div>
        </div>
        <div class="stat">
            <div class="stat-value" style="color: #ffaa00">{stats['damaged']}</div>
            <div>Damaged</div>
        </div>
        <div class="stat">
            <div class="stat-value" style="color: #44ff44">{stats['healthy']}</div>
            <div>Healthy</div>
        </div>
        <div class="stat">
            <div class="stat-value">{stats['rampage_score']}</div>
            <div>Score</div>
        </div>
    </div>
    
    <div class="city">
        {''.join(buildings_html)}
    </div>
    
    <div style="text-align: center; margin-top: 30px; color: #888;">
        <p>Hover over buildings to see details</p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html)
            
        print(f"🌐 HTML visualization saved to: {output_path}")
        print(f"   Open in browser: file://{output_path.absolute()}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Code City - Rampage Refactor: Gamified vulnerability scanning"
    )
    parser.add_argument("project_path", help="Path to project to scan")
    parser.add_argument("--extensions", nargs="+", 
                       default=[".py", ".js", ".sh", ".html"],
                       help="File extensions to scan")
    parser.add_argument("--output", "-o", help="Save city state JSON")
    parser.add_argument("--html", help="Generate HTML visualization")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"Error: {project_path} not found")
        return
        
    # Build the city
    city = CodeCity(project_path)
    city.scan_project(args.extensions)
    
    # Import and run vulnerability scanner
    print("\n🔍 Scanning for vulnerabilities...")
    
    # Simple inline scanner (you can replace with adaptive_scanner.py)
    import re
    
    vuln_patterns = [
        ("command_injection", r'(system|exec|eval|subprocess\.call)\([^)]*\$', "critical"),
        ("hardcoded_creds", r'(password|secret|key)\s*=\s*["\'][^"\']+["\']', "high"),
        ("sql_injection", r'(SELECT|INSERT|UPDATE).*\$', "critical"),
        ("weak_crypto", r'(md5|sha1)\(', "medium"),
    ]
    
    all_vulns = []
    for filepath, building in city.buildings.items():
        try:
            content = Path(filepath).read_text()
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                for pattern_name, pattern, severity in vuln_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        all_vulns.append({
                            "file": filepath,
                            "line": i,
                            "pattern": pattern_name,
                            "severity": severity,
                            "description": f"Matched pattern: {pattern_name}",
                            "code": line.strip()
                        })
        except:
            pass
            
    # RAMPAGE!
    city.rampage(all_vulns)
    
    # Show results
    city.print_scoreboard()
    
    # Save outputs
    if args.output:
        city.save_city_state(Path(args.output))
        
    if args.html:
        city.generate_html_visualization(Path(args.html))
    else:
        # Generate default HTML
        default_html = project_path / "code_city_rampage.html"
        city.generate_html_visualization(default_html)


if __name__ == "__main__":
    main()
