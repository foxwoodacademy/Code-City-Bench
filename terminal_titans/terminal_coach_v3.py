#!/usr/bin/env python3
"""
Terminal Coach v2 - Padded Room Edition
Natural Language Bash Helper with MUCH better hand-holding

Built by: Mike + Claude (Thread 5, Nov 22 2025, 6am)
Purpose: Teach bash to people who don't know shit about bash
"""

import os
import sys
import subprocess
import difflib
from pathlib import Path

class TerminalCoachV2:
    """
    Your patient bash teacher. Handles stupid questions gracefully.
    Teaches you bash without making you feel dumb.
    """
    
    def __init__(self):
        self.command_map = self._build_command_map()
        self.flag_explanations = self._build_flag_explanations()
        self.tutorials = self._build_tutorials()
        self.last_command = None
        self.session_history = []
        
    def _build_command_map(self):
        """Comprehensive command map with better coverage"""
        return {
            # File finding (enhanced with extensions)
            'find python files': 'find . -name "*.py" -type f',
            'find mp3 files': 'find . -name "*.mp3" -type f',
            'find mp4 files': 'find . -name "*.mp4" -type f',
            'find pdf files': 'find . -name "*.pdf" -type f',
            'find jpg files': 'find . -name "*.jpg" -type f',
            'find png files': 'find . -name "*.png" -type f',
            'find txt files': 'find . -name "*.txt" -type f',
            'find json files': 'find . -name "*.json" -type f',
            'find all audio files': 'find . -type f \( -name "*.mp3" -o -name "*.wav" -o -name "*.m4a" \)',
            'find all video files': 'find . -type f \( -name "*.mp4" -o -name "*.mkv" -o -name "*.avi" \)',
            'find all image files': 'find . -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.gif" \)',
            
            # File finding (time-based)
            'find files modified today': 'find . -type f -mtime 0',
            'find files modified yesterday': 'find . -type f -mtime 1',
            'find files modified this week': 'find . -type f -mtime -7',
            'find files modified this month': 'find . -type f -mtime -30',
            'find old files': 'find . -type f -mtime +365',
            
            # File finding (size-based)
            'find large files': 'find . -type f -size +10M',
            'find huge files': 'find . -type f -size +100M',
            'find small files': 'find . -type f -size -1M',
            'find empty files': 'find . -type f -empty',
            
            # File finding (structure)
            'find directories': 'find . -type d',
            'find hidden files': 'find . -name ".*"',
            
            # File operations
            'list files': 'ls -lh',
            'list all files': 'ls -lha',
            'list files by date': 'ls -lht',
            'list files by size': 'ls -lhS',
            'show file tree': 'tree -L 2',
            'count files': 'ls -1 | wc -l',
            'count files in directory': 'find . -type f | wc -l',
            'disk usage': 'du -sh *',
            'show disk space': 'df -h',
            'show folder sizes': 'du -h --max-depth=1',
            
            # Text operations
            'search in files': 'grep -r "PATTERN" .',
            'search python files': 'grep -r "PATTERN" --include="*.py" .',
            'search case insensitive': 'grep -ri "PATTERN" .',
            'count lines': 'wc -l FILE',
            'count words': 'wc -w FILE',
            'show first lines': 'head -n 10 FILE',
            'show last lines': 'tail -n 10 FILE',
            'follow log file': 'tail -f FILE',
            'show file contents': 'cat FILE',
            'page through file': 'less FILE',
            
            # Process management
            'show running processes': 'ps aux',
            'find process': 'ps aux | grep PATTERN',
            'kill process': 'kill -9 PID',
            'show system resources': 'top -n 1',
            'show memory usage': 'free -h',
            'show cpu info': 'lscpu',
            
            # Network
            'show network connections': 'netstat -tuln',
            'check internet': 'ping -c 4 google.com',
            'download file': 'curl -O URL',
            'show my ip': 'curl ifconfig.me',
            'test connection': 'ping -c 4 HOST',
            
            # Archive operations
            'compress folder': 'tar -czf archive.tar.gz FOLDER',
            'extract archive': 'tar -xzf archive.tar.gz',
            'zip folder': 'zip -r archive.zip FOLDER',
            'unzip file': 'unzip archive.zip',
            'list archive contents': 'tar -tzf archive.tar.gz',
            
            # Git operations
            'git status': 'git status',
            'git commit': 'git commit -m "MESSAGE"',
            'git push': 'git push origin main',
            'git pull': 'git pull origin main',
            'show git log': 'git log --oneline -10',
            'undo last commit': 'git reset --soft HEAD~1',
            
            # System info
            'show system info': 'uname -a',
            'show storage': 'df -h',
            'show memory': 'free -h',
            'current directory': 'pwd',
            'home directory': 'cd ~',
            'where am i': 'pwd',
            
            # Permissions
            'make executable': 'chmod +x FILE',
            'change permissions': 'chmod 755 FILE',
            'change owner': 'chown user:group FILE',
            'show permissions': 'ls -l',
            
            # Package management (Termux)
            'install package': 'pkg install PACKAGE',
            'update packages': 'pkg update && pkg upgrade',
            'search package': 'pkg search PATTERN',
            'list installed packages': 'pkg list-installed',
            'remove package': 'pkg uninstall PACKAGE',
            
            # Useful shortcuts
            'clear screen': 'clear',
            'command history': 'history',
            'previous directory': 'cd -',
            'parent directory': 'cd ..',
            'create directory': 'mkdir -p DIR',
            'remove directory': 'rm -rf DIR',
            'remove file': 'rm FILE',
            'copy file': 'cp SOURCE DEST',
            'copy directory': 'cp -r SOURCE DEST',
            'move file': 'mv SOURCE DEST',
            'rename file': 'mv OLD NEW',
            'create empty file': 'touch FILE',
            
            # Mike's specific needs
            'find context files': 'find /storage/emulated/0/context_system -type f',
            'show recent snapshots': 'ls -lht /storage/emulated/0/context_system/context_history/',
            'backup everything': 'tar -czf backup_$(date +%Y%m%d).tar.gz /storage/emulated/0/context_system',
            'find my python code': 'find /storage/emulated/0/root_2025 -name "*.py" -type f',
            'find my recent work': 'find /storage/emulated/0/root_2025 -type f -mtime -7',
        }
    
    def _build_flag_explanations(self):
        """Comprehensive flag explanations"""
        return {
            '-r': 'Recursive - includes subdirectories',
            '-f': 'Force (no confirmation) OR Follow (for tail/logs)',
            '-l': 'Long format - shows detailed file information',
            '-h': 'Human readable - shows sizes as KB/MB/GB instead of bytes',
            '-a': 'All - includes hidden files (starting with .)',
            '-n': 'Number - specify a count',
            '-t': 'Sort by Time - newest first',
            '-v': 'Verbose - shows detailed progress/output',
            '-i': 'Interactive OR Case-insensitive (depends on command)',
            '-p': 'Parents - creates parent directories if needed',
            '-z': 'Compress with gzip',
            '-x': 'Extract archive',
            '-c': 'Create archive OR Count (depends on command)',
            '-s': 'Silent/Quiet OR Size (depends on command)',
            '-d': 'Directory OR Debug (depends on command)',
            '-u': 'Update OR User (depends on command)',
            '-g': 'Group',
            '-o': 'Output file OR Owner (depends on command)',
            '-name': 'Search by filename pattern',
            '-type': 'Search by type (f=file, d=directory, l=link)',
            '-mtime': 'Modified time in days (0=today, -7=last 7 days, +30=older than 30 days)',
            '-size': 'File size (+10M=larger than 10MB, -1M=smaller than 1MB)',
            '-empty': 'Find empty files or directories',
            '--help': 'Show help information for a command',
            '--version': 'Show version information',
        }
    
    def _build_tutorials(self):
        """Mini tutorials for common commands"""
        return {
            'grep': {
                'description': 'Searches for text patterns in files',
                'basic_usage': 'grep "search term" filename',
                'common_flags': {
                    '-r': 'Search recursively in directories',
                    '-i': 'Case-insensitive search',
                    '-n': 'Show line numbers',
                    '-v': 'Invert match (show lines that DON\'T match)'
                },
                'examples': [
                    'grep "error" logfile.txt  # Find "error" in logfile',
                    'grep -r "TODO" .  # Find all TODOs in current directory',
                    'grep -i "password" *.txt  # Case-insensitive search in all txt files'
                ]
            },
            'find': {
                'description': 'Searches for files and directories',
                'basic_usage': 'find [where] [what]',
                'common_flags': {
                    '-name': 'Search by filename',
                    '-type f': 'Find only files',
                    '-type d': 'Find only directories',
                    '-mtime': 'Find by modification time'
                },
                'examples': [
                    'find . -name "*.py"  # Find all Python files',
                    'find /home -type d  # Find all directories in /home',
                    'find . -mtime -7  # Files modified in last 7 days'
                ]
            },
            'ls': {
                'description': 'Lists directory contents',
                'basic_usage': 'ls [options] [directory]',
                'common_flags': {
                    '-l': 'Long format (detailed)',
                    '-a': 'Show hidden files',
                    '-h': 'Human-readable sizes',
                    '-t': 'Sort by time'
                },
                'examples': [
                    'ls -lh  # Detailed list with readable sizes',
                    'ls -lha  # Show everything including hidden',
                    'ls -lht  # List by time, newest first'
                ]
            },
            'cd': {
                'description': 'Changes current directory',
                'basic_usage': 'cd [directory]',
                'common_patterns': {
                    'cd ~': 'Go to home directory',
                    'cd ..': 'Go to parent directory',
                    'cd -': 'Go to previous directory',
                    'cd /': 'Go to root directory'
                },
                'examples': [
                    'cd Documents  # Go to Documents folder',
                    'cd /storage/emulated/0  # Go to Android storage root',
                    'cd ..  # Go up one level'
                ]
            }
        }
    
    def smart_match(self, query):
        """Smarter matching that understands intent"""
        query_lower = query.lower().strip()
        
        # Check for file extension queries
        if 'find' in query_lower and ('file' in query_lower or 'files' in query_lower):
            # Extract potential file extension
            words = query_lower.split()
            for word in words:
                if word.endswith('files') or word.endswith('file'):
                    continue
                # Check if it's a common extension
                ext = word.replace('files', '').replace('file', '').strip()
                if ext and not ext.startswith('-'):
                    # Try to find it in command map
                    search_key = f'find {ext} files'
                    if search_key in self.command_map:
                        return ('exact', search_key, self.command_map[search_key])
                    else:
                        # Generate command dynamically
                        cmd = f'find . -name "*.{ext}" -type f'
                        return ('generated', f'find {ext} files', cmd)
        
        # Exact match
        if query_lower in self.command_map:
            return ('exact', query_lower, self.command_map[query_lower])
        
        # Fuzzy match
        close_matches = difflib.get_close_matches(query_lower, self.command_map.keys(), n=3, cutoff=0.6)
        if close_matches:
            matches = [(key, self.command_map[key]) for key in close_matches]
            return ('fuzzy', close_matches[0], matches)
        
        # Partial match (word-based)
        query_words = set(query_lower.split())
        matches = []
        for key in self.command_map:
            key_words = set(key.split())
            if query_words & key_words:  # If any words match
                matches.append((key, self.command_map[key]))
        
        if matches:
            # Sort by number of matching words
            matches.sort(key=lambda x: len(set(x[0].split()) & query_words), reverse=True)
            return ('partial', query_lower, matches[:10])
        
        return ('none', query_lower, [])
    
    def explain_flag(self, flag):
        """Explain what a flag means"""
        flag = flag.strip()
        
        if flag in self.flag_explanations:
            return self.flag_explanations[flag]
        
        # Try without leading dash
        if flag.startswith('-'):
            clean_flag = flag.lstrip('-')
            if clean_flag in self.flag_explanations:
                return self.flag_explanations[clean_flag]
        
        return None
    
    def show_tutorial(self, command):
        """Show tutorial for a command"""
        command = command.lower().strip()
        
        if command in self.tutorials:
            tut = self.tutorials[command]
            print(f"\n📚 TUTORIAL: {command.upper()}")
            print("=" * 60)
            print(f"\n{tut['description']}\n")
            
            print(f"📝 Basic Usage:")
            print(f"  {tut['basic_usage']}\n")
            
            if 'common_flags' in tut:
                print(f"🚩 Common Flags:")
                for flag, desc in tut['common_flags'].items():
                    print(f"  {flag}: {desc}")
                print()
            
            if 'common_patterns' in tut:
                print(f"🔄 Common Patterns:")
                for pattern, desc in tut['common_patterns'].items():
                    print(f"  {pattern}: {desc}")
                print()
            
            print(f"💡 Examples:")
            for example in tut['examples']:
                print(f"  {example}")
            
            return True
        
        return False
    
    def suggest_learning_path(self, query):
        """Suggest what the user might want to learn"""
        query_lower = query.lower()
        
        suggestions = []
        
        # Detect learning intent
        if any(word in query_lower for word in ['teach', 'learn', 'how to', 'tutorial', 'explain']):
            # Extract potential command
            for cmd in ['grep', 'find', 'ls', 'cd', 'cp', 'mv', 'rm']:
                if cmd in query_lower:
                    suggestions.append(f"Type 'tutorial {cmd}' to learn about {cmd}")
        
        # Detect confusion about syntax
        if any(word in query_lower for word in ['help', 'stuck', 'confused', 'don\'t understand']):
            suggestions.append("Type 'examples' to see what I can help with")
            suggestions.append("Type 'tutorial [command]' to learn a specific command")
            suggestions.append("Type 'cheatsheet' for quick reference")
        
        # Detect flag confusion
        if query_lower.startswith('-') or 'flag' in query_lower or 'option' in query_lower:
            suggestions.append("Type 'explain -FLAG' to learn what a flag does")
            suggestions.append("Example: 'explain -r' or 'explain -lha'")
        
        return suggestions
    
    def handle_special_commands(self, query):
        """Handle built-in special commands"""
        query_lower = query.lower().strip()
        
        # Help
        if query_lower in ['help', '?', 'h']:
            self.show_help()
            return True
        
        # Cheat sheet
        if 'cheatsheet' in query_lower or 'cheat sheet' in query_lower:
            self.show_cheatsheet()
            return True
        
        # Tutorial
        if query_lower.startswith('tutorial '):
            cmd = query_lower[9:].strip()
            if self.show_tutorial(cmd):
                return True
            else:
                print(f"\n❌ No tutorial for '{cmd}'")
                print(f"💡 Available tutorials: {', '.join(self.tutorials.keys())}")
                return True
        
        # Explain flag
        if query_lower.startswith('explain -'):
            flag = query_lower[8:].strip()
            explanation = self.explain_flag(flag)
            if explanation:
                print(f"\n📖 FLAG: {flag}")
                print(f"  → {explanation}")
                return True
            else:
                print(f"\n❌ No explanation for flag '{flag}'")
                print("💡 Try 'explain --help' or check 'cheatsheet'")
                return True
        
        return False
    
    def show_help(self):
        """Show comprehensive help"""
        print("\n" + "=" * 60)
        print("🎓 TERMINAL COACH - HELP")
        print("=" * 60)
        
        print("\n📝 HOW TO USE:")
        print("  • Just tell me what you want to do in plain English")
        print("  • I'll show you the command and explain it")
        print("  • You decide if you want to run it\n")
        
        print("🔧 SPECIAL COMMANDS:")
        print("  help           - Show this help message")
        print("  examples       - Show example queries")
        print("  cheatsheet     - Quick reference guide")
        print("  tutorial CMD   - Learn about a specific command")
        print("  explain -FLAG  - Learn what a flag does")
        print("  explain CMD    - Break down a command")
        print("  run CMD        - Run any bash command")
        print("  again          - Repeat last command")
        print("  quit/exit      - Exit Terminal Coach\n")
        
        print("💡 LEARNING PATH:")
        print("  1. Start with 'examples' to see what's possible")
        print("  2. Try simple queries like 'find python files'")
        print("  3. Use 'tutorial [command]' to learn commands deeply")
        print("  4. Graduate to running raw bash commands\n")
        
        print("🎯 TIPS:")
        print("  • Be specific: 'find mp3 files' not just 'mp3'")
        print("  • Ask for help: 'teach me grep' or 'how to search files'")
        print("  • Experiment: I won't break your system")
        print("  • Use 'explain' liberally: Learn as you go\n")
    
    def show_cheatsheet(self):
        """Quick reference of common commands"""
        print("\n" + "=" * 60)
        print("📋 BASH CHEAT SHEET")
        print("=" * 60)
        
        categories = {
            'Finding Files': [
                'find . -name "*.ext"     # Find files by extension',
                'find . -type f -mtime -7 # Files modified last week',
                'find . -size +10M        # Files larger than 10MB',
            ],
            'Viewing Files': [
                'ls -lha                  # List all files (detailed)',
                'cat file.txt             # Show file contents',
                'tail -f log.txt          # Follow log file (Ctrl+C to stop)',
            ],
            'Searching Text': [
                'grep "pattern" file      # Search in file',
                'grep -r "pattern" .      # Search in all files',
                'grep -i "pattern" file   # Case-insensitive search',
            ],
            'File Operations': [
                'cp source dest           # Copy file',
                'mv source dest           # Move/rename file',
                'rm file                  # Remove file',
                'mkdir folder             # Create directory',
            ],
            'Navigation': [
                'pwd                      # Where am I?',
                'cd folder                # Go to folder',
                'cd ..                    # Go up one level',
                'cd ~                     # Go home',
            ],
            'System Info': [
                'df -h                    # Disk space',
                'free -h                  # Memory usage',
                'ps aux                   # Running processes',
            ],
        }
        
        for category, commands in categories.items():
            print(f"\n{category}:")
            for cmd in commands:
                print(f"  {cmd}")
        
        print("\n💡 Type 'tutorial [command]' for detailed explanations")
        print("💡 Type 'explain -FLAG' to learn what flags do\n")
    
    def interactive_mode(self):
        """Enhanced interactive mode"""
        print("🎓 TERMINAL COACH v2 - Natural Language Bash Helper")
        print("=" * 60)
        print("Tell me what you want to do, and I'll teach you how.")
        print("Type 'help' for a full guide, or just start asking!")
        print("=" * 60)
        print()
        
        while True:
            try:
                user_input = input("💬 ").strip()
                
                if not user_input:
                    continue
                
                self.session_history.append(user_input)
                
                # Exit commands
                if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                    print("👋 Later! Come back when you need me.")
                    break
                
                # Handle special commands
                if self.handle_special_commands(user_input):
                    print()
                    continue
                
                # Smart matching
                match_type, key, result = self.smart_match(user_input)
                
                if match_type == 'exact':
                    self.handle_exact_match(key, result)
                elif match_type == 'generated':
                    self.handle_generated_match(key, result)
                elif match_type == 'fuzzy':
                    self.handle_fuzzy_match(user_input, result)
                elif match_type == 'partial':
                    self.handle_partial_match(result)
                else:
                    self.handle_no_match(user_input)
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Interrupted. Type 'quit' to exit properly.")
                print()
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def handle_exact_match(self, key, command):
        """Handle exact command match"""
        print(f"\n✅ {key}")
        print(f"📝 Command: {command}")
        self.show_command_breakdown(command)
        self.offer_execution(command)
    
    def handle_generated_match(self, description, command):
        """Handle dynamically generated command"""
        print(f"\n✅ Generated command for: {description}")
        print(f"📝 Command: {command}")
        self.show_command_breakdown(command)
        self.offer_execution(command)
    
    def handle_fuzzy_match(self, query, matches):
        """Handle fuzzy match"""
        print(f"\n🤔 Did you mean one of these?")
        print("-" * 60)
        for i, (key, cmd) in enumerate(matches, 1):
            print(f"{i}. {key}")
            print(f"   → {cmd}\n")
        
        print("Type the number, or ask differently")
        choice = input("→ ").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(matches):
                key, cmd = matches[idx]
                self.handle_exact_match(key, cmd)
    
    def handle_partial_match(self, matches):
        """Handle partial matches"""
        if len(matches) > 10:
            matches = matches[:10]
        
        print(f"\n🤔 Found {len(matches)} possible matches:")
        print("-" * 60)
        for i, (key, cmd) in enumerate(matches, 1):
            print(f"{i}. {key}")
            print(f"   → {cmd}\n")
        
        print("Type the number, or refine your query")
        choice = input("→ ").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(matches):
                key, cmd = matches[idx]
                self.handle_exact_match(key, cmd)
    
    def handle_no_match(self, query):
        """Handle no matches with helpful suggestions"""
        print(f"\n❌ Couldn't understand: '{query}'")
        
        suggestions = self.suggest_learning_path(query)
        if suggestions:
            print("\n💡 Suggestions:")
            for suggestion in suggestions:
                print(f"  • {suggestion}")
        else:
            print("\n💡 Try:")
            print("  • 'help' - See what I can do")
            print("  • 'examples' - Browse available commands")
            print("  • 'cheatsheet' - Quick reference")
            print("  • Be more specific: 'find python files' instead of 'python'")
    
    def show_command_breakdown(self, command):
        """Show detailed breakdown of command"""
        parts = command.split()
        if not parts:
            return
        
        main_cmd = parts[0]
        
        # Show main command explanation
        cmd_explanations = {
            'find': 'Searches for files/directories',
            'grep': 'Searches for text patterns',
            'ls': 'Lists directory contents',
            'cd': 'Changes directory',
            'cp': 'Copies files',
            'mv': 'Moves/renames files',
            'rm': 'Removes files (careful!)',
            'cat': 'Shows file contents',
            'tail': 'Shows end of file',
            'head': 'Shows start of file',
        }
        
        if main_cmd in cmd_explanations:
            print(f"💡 {cmd_explanations[main_cmd]}")
        
        # Show flag explanations
        flags = [p for p in parts if p.startswith('-')]
        if flags:
            print("\n🚩 Flags:")
            for flag in flags:
                explanation = self.explain_flag(flag)
                if explanation:
                    print(f"  {flag}: {explanation}")
    
    def offer_execution(self, command):
        """Offer to run the command"""
        print("\n❓ Want to:")
        print("  y - Run it")
        print("  n - Just show me, don't run")
        print("  m - Let me modify it first")
        
        choice = input("→ ").strip().lower()
        
        if choice == 'y':
            self.run_command(command)
        elif choice == 'm':
            modified = input(f"Modify: {command}\n→ ").strip()
            if modified:
                self.run_command(modified)
    
    def run_command(self, command):
        """Execute bash command with safety checks"""
        self.last_command = command
        
        # Safety check for dangerous commands
        dangerous = ['rm -rf /', 'dd if=', 'mkfs', ':(){:|:&};:', '> /dev/sda']
        if any(d in command for d in dangerous):
            print("\n🚫 DANGEROUS COMMAND DETECTED - NOT RUNNING")
            print("This command could destroy your system!")
            return
        
        # Warn about rm commands
        if 'rm ' in command and '-rf' in command:
            print("\n⚠️  WARNING: This will permanently delete files!")
            confirm = input("Type 'yes' to confirm: ").strip()
            if confirm.lower() != 'yes':
                print("❌ Cancelled")
                return
        
        print(f"\n▶️  Running: {command}")
        print("-" * 60)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                # Truncate very long output
                lines = result.stdout.split('\n')
                if len(lines) > 50:
                    print('\n'.join(lines[:25]))
                    print(f"\n... ({len(lines) - 50} more lines) ...")
                    print('\n'.join(lines[-25:]))
                else:
                    print(result.stdout)
            
            if result.stderr:
                print("⚠️  Errors/Warnings:")
                print(result.stderr)
            
            if result.returncode == 0:
                print("\n✅ Command completed successfully")
            else:
                print(f"\n❌ Command failed with exit code {result.returncode}")
            
        except subprocess.TimeoutExpired:
            print("\n⏱️  Command timed out (30s limit)")
        except Exception as e:
            print(f"\n❌ Error running command: {e}")


def main():
    coach = TerminalCoachV2()
    
    # Check for command-line argument
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        
        # Handle special commands
        if coach.handle_special_commands(query):
            return
        
        # Single query mode
        match_type, key, result = coach.smart_match(query)
        
        if match_type in ['exact', 'generated']:
            print(f"\n✅ Command: {result}")
            coach.show_command_breakdown(result)
        elif match_type == 'fuzzy':
            print(f"\n🤔 Did you mean: {result[0][0]}?")
            print(f"Command: {result[0][1]}")
        elif match_type == 'partial' and result:
            print(f"\n🤔 Possible matches:")
            for key, cmd in result[:3]:
                print(f"  • {key}")
                print(f"    → {cmd}")
        else:
            print(f"\n❌ Couldn't understand: '{query}'")
            print("💡 Try: python terminal_coach.py help")
    else:
        # Interactive mode
        coach.interactive_mode()


if __name__ == "__main__":
    main()