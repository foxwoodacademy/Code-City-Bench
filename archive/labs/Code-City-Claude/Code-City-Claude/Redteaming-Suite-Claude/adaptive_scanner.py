#!/data/data/com.termux/files/usr/bin/python3
"""
Adaptive Vulnerability Scanner
No safety theater. No emoji pollution. Just finds bugs.
"""

import subprocess
import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

class VulnerabilityPattern:
    """A pattern that can be learned and adapted"""
    def __init__(self, name: str, pattern: str, severity: str, description: str):
        self.name = name
        self.pattern = pattern
        self.severity = severity  # critical, high, medium, low
        self.description = description
        self.matches = 0  # Track how often this finds real issues
        
class AdaptiveScanner:
    def __init__(self):
        self.patterns: List[VulnerabilityPattern] = []
        self.results = []
        self.knowledge_base = Path.home() / ".adaptive_scanner" / "knowledge.json"
        self.knowledge_base.parent.mkdir(exist_ok=True)
        
        # Initialize with base patterns
        self._load_base_patterns()
        self._load_learned_patterns()
        
    def _load_base_patterns(self):
        """Base vulnerability patterns - the foundation"""
        base_patterns = [
            VulnerabilityPattern(
                "command_injection",
                r'(system|exec|eval|subprocess\.call)\([^)]*\$[^)]*\)',
                "critical",
                "Potential command injection via unsanitized input"
            ),
            VulnerabilityPattern(
                "hardcoded_credentials",
                r'(password|passwd|pwd|secret|key)\s*=\s*["\'][^"\']+["\']',
                "high",
                "Hardcoded credentials detected"
            ),
            VulnerabilityPattern(
                "sql_injection",
                r'(SELECT|INSERT|UPDATE|DELETE).*\$[a-zA-Z_]',
                "critical",
                "Potential SQL injection vulnerability"
            ),
            VulnerabilityPattern(
                "path_traversal",
                r'\.\./|\.\.\\\\',
                "high",
                "Path traversal attempt detected"
            ),
            VulnerabilityPattern(
                "unsafe_deserialization",
                r'(pickle\.loads|yaml\.load|marshal\.loads)\(',
                "high",
                "Unsafe deserialization detected"
            ),
            VulnerabilityPattern(
                "weak_crypto",
                r'(md5|sha1|DES|RC4)\(',
                "medium",
                "Weak cryptographic algorithm in use"
            ),
        ]
        self.patterns.extend(base_patterns)
        
    def _load_learned_patterns(self):
        """Load patterns we've learned from previous scans"""
        if self.knowledge_base.exists():
            with open(self.knowledge_base) as f:
                data = json.load(f)
                for p in data.get("learned_patterns", []):
                    pattern = VulnerabilityPattern(
                        p["name"], p["pattern"], p["severity"], p["description"]
                    )
                    pattern.matches = p.get("matches", 0)
                    self.patterns.append(pattern)
                    
    def save_learned_patterns(self):
        """Save patterns for next time"""
        data = {
            "learned_patterns": [
                {
                    "name": p.name,
                    "pattern": p.pattern,
                    "severity": p.severity,
                    "description": p.description,
                    "matches": p.matches
                }
                for p in self.patterns if p.matches > 0
            ],
            "last_updated": datetime.now().isoformat()
        }
        with open(self.knowledge_base, 'w') as f:
            json.dump(data, f, indent=2)
            
    def learn_new_pattern(self, name: str, pattern: str, severity: str, description: str):
        """Teach the scanner a new vulnerability pattern"""
        new_pattern = VulnerabilityPattern(name, pattern, severity, description)
        self.patterns.append(new_pattern)
        print(f"[+] Learned new pattern: {name}")
        
    def scan_file(self, filepath: Path) -> List[Dict]:
        """Scan a single file for vulnerabilities"""
        findings = []
        
        try:
            content = filepath.read_text()
            lines = content.split('\n')
            
            for pattern in self.patterns:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern.pattern, line, re.IGNORECASE):
                        finding = {
                            "file": str(filepath),
                            "line": i,
                            "pattern": pattern.name,
                            "severity": pattern.severity,
                            "description": pattern.description,
                            "code": line.strip()
                        }
                        findings.append(finding)
                        pattern.matches += 1
                        
        except Exception as e:
            print(f"[!] Error scanning {filepath}: {e}")
            
        return findings
        
    def scan_directory(self, directory: Path, extensions: List[str] = None) -> List[Dict]:
        """Recursively scan a directory"""
        if extensions is None:
            extensions = ['.py', '.sh', '.js', '.php', '.rb', '.go', '.c', '.cpp']
            
        all_findings = []
        
        for ext in extensions:
            for filepath in directory.rglob(f'*{ext}'):
                findings = self.scan_file(filepath)
                all_findings.extend(findings)
                
        return all_findings
        
    def generate_report(self, findings: List[Dict]) -> str:
        """Generate a brutally honest report"""
        report = []
        report.append("=" * 70)
        report.append(f"VULNERABILITY SCAN REPORT - {datetime.now()}")
        report.append("=" * 70)
        report.append("")
        
        if not findings:
            report.append("No vulnerabilities detected.")
            report.append("(This doesn't mean your code is secure - it means these patterns didn't match)")
            return "\n".join(report)
            
        # Group by severity
        by_severity = {"critical": [], "high": [], "medium": [], "low": []}
        for finding in findings:
            by_severity[finding["severity"]].append(finding)
            
        # Report each severity level
        for severity in ["critical", "high", "medium", "low"]:
            issues = by_severity[severity]
            if issues:
                report.append(f"\n[{severity.upper()}] - {len(issues)} issue(s)")
                report.append("-" * 70)
                for issue in issues:
                    report.append(f"\nFile: {issue['file']}")
                    report.append(f"Line: {issue['line']}")
                    report.append(f"Issue: {issue['description']}")
                    report.append(f"Code: {issue['code']}")
                    report.append("")
                    
        # Summary
        report.append("=" * 70)
        report.append(f"TOTAL: {len(findings)} potential vulnerabilities")
        report.append("")
        report.append("NOTE: These are pattern matches, not confirmed exploits.")
        report.append("Manual review required. Trust but verify.")
        report.append("=" * 70)
        
        return "\n".join(report)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Adaptive Vulnerability Scanner")
    parser.add_argument("target", help="File or directory to scan")
    parser.add_argument("--learn", nargs=4, metavar=("NAME", "PATTERN", "SEVERITY", "DESC"),
                       help="Teach scanner a new pattern")
    parser.add_argument("--output", "-o", help="Save report to file")
    
    args = parser.parse_args()
    
    scanner = AdaptiveScanner()
    
    # Learn new pattern if provided
    if args.learn:
        scanner.learn_new_pattern(*args.learn)
        scanner.save_learned_patterns()
        return
        
    # Scan target
    target = Path(args.target)
    
    if target.is_file():
        findings = scanner.scan_file(target)
    elif target.is_dir():
        findings = scanner.scan_directory(target)
    else:
        print(f"Error: {target} not found")
        return
        
    # Generate report
    report = scanner.generate_report(findings)
    print(report)
    
    # Save if requested
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\nReport saved to {args.output}")
        
    # Save learned patterns
    scanner.save_learned_patterns()


if __name__ == "__main__":
    main()
