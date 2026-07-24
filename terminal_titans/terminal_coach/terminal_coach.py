#!/usr/bin/env python3
"""
Terminal Coach - Natural Language Bash Helper
Translates what you want into actual bash commands

Built by: Mike + Claude (Thread 5, Nov 22 2025, 5:30am)
Purpose: Help Mike navigate bash without memorizing syntax
"""

import os
import sys
import subprocess
from pathlib import Path

class TerminalCoach:
    """
    Your bash wingman. Tell it what you want in plain English,
    it gives you the command and explains what it does.
    """
    
    def __init__(self):
        self.command_map = self._build_command_map()
        self.last_command = None
        
    def _build_command_map(self):
        """Map natural language to bash commands"""
        return {
            # File finding
            'find python files': 'find . -name "*.py" -type f',
            'find files modified today': 'find . -type f -mtime 0',
            'find files modified this week': 'find . -type f -mtime -7',
            'find large files': 'find . -type f -size +10M',
            'find empty files': 'find . -type f -empty',
            'find directories': 'find . -type d',
            
            # File operations
            'list files': 'ls -lh',
            'list all files': 'ls -lha',
            'list files by date': 'ls -lht',
            'show file tree': 'tree -L 2',
            'count files': 'ls -1 | wc -l',
            'disk usage': 'du -sh *',
            'show disk space': 'df -h',
            
            # Text operations
            'search in files': 'grep -r "PATTERN" .',
            'search python files': 'grep -r "PATTERN" --include="*.py" .',
            'count lines': 'wc -l',
            'show first lines': 'head -n 10',
            'show last lines': 'tail -n 10',
            'follow log file': 'tail -f',
            
            # Process management
            'show running processes': 'ps aux',
            'find process': 'ps aux | grep',
            'kill process': 'kill -9',
            'show system resources': 'top -n 1',
            
            # Network
            'show network connections': 'netstat -tuln',
            'check internet': 'ping -c 4 google.com',
            'download file': 'curl -O',
            'show my ip': 'curl ifconfig.me',
            
            # Archive operations
            'compress folder': 'tar -czf archive.tar.gz',
            'extract archive': 'tar -xzf',
            'zip folder': 'zip -r archive.zip',
            'unzip file': 'unzip',
            
            # Git operations
            'git status': 'git status',
            'git commit': 'git commit -m "MESSAGE"',
            'git push': 'git push origin main',
            'git pull': 'git pull origin main',
            'show git log': 'git log --oneline -10',
            
            # System info
            'show system info': 'uname -a',
            'show storage': 'df -h',
            'show memory': 'free -h',
            'current directory': 'pwd',
            'home directory': 'cd ~',
            
            # Permissions
            'make executable': 'chmod +x',
            'change permissions': 'chmod 755',
            'change owner': 'chown user:group',
            'show permissions': 'ls -l',
            
            # Package management (Termux)
            'install package': 'pkg install',
            'update packages': 'pkg update && pkg upgrade',
            'search package': 'pkg search',
            'list installed': 'pkg list-installed',
            
            # Useful shortcuts
            'clear screen': 'clear',
            'command history': 'history',
            'previous directory': 'cd -',
            'parent directory': 'cd ..',
            'create directory': 'mkdir -p',
            'remove directory': 'rm -rf',
            'copy recursive': 'cp -r',
            'move files': 'mv',
            
            # Mike's specific needs
            'find context files': 'find /storage/emulated/0/context_system -type f',
            'show recent snapshots': 'ls -lht /storage/emulated/0/context_system/context_history/',
            'backup everything': 'tar -czf backup_$(date +%Y%m%d).tar.gz /storage/emulated/0/context_system',
            'find my python code': 'find /storage/emulated/0/root_2025 -name "*.py" -type f',
        }
    
    def find_closest_match(self, query):
        """Find closest command match to user's query"""
        query_lower = query.lower().strip()
        
        # Exact match
        if query_lower in self.command_map:
            return query_lower, self.command_map[query_lower]
        
        # Partial match
        matches = []
        for key in self.command_map:
            if any(word in key for word in query_lower.split()):
                matches.append((key, self.command_map[key]))
        
        return matches
    
    def explain_command(self, command):
        """Explain what a bash command does"""
        explanations = {
            'find': 'Searches for files/directories matching criteria',
            'grep': 'Searches for text patterns in files',
            'ls': 'Lists directory contents',
            'cd': 'Changes current directory',
            'pwd': 'Prints current working directory',
            'cat': 'Displays file contents',
            'head': 'Shows first lines of file',
            'tail': 'Shows last lines of file (use -f to follow)',
            'cp': 'Copies files/directories',
            'mv': 'Moves or renames files',
            'rm': 'Removes files/directories (BE CAREFUL!)',
            'mkdir': 'Creates new directory',
            'chmod': 'Changes file permissions',
            'chown': 'Changes file ownership',
            'tar': 'Creates/extracts archives',
            'zip': 'Compresses files',
            'unzip': 'Extracts zip files',
            'ps': 'Shows running processes',
            'kill': 'Terminates a process',
            'top': 'Real-time system monitor',
            'df': 'Shows disk space usage',
            'du': 'Shows directory sizes',
            'wc': 'Counts lines/words/characters',
            'curl': 'Transfers data from URLs',
            'wget': 'Downloads files from web',
            'git': 'Version control operations',
            'pkg': 'Termux package manager',
        }
        
        # Get first word (the main command)
        main_cmd = command.split()[0] if command else ''
        
        return explanations.get(main_cmd, 'Command not in my explanation database')
    
    def break_down_command(self, command):
        """Break down command into parts and explain each"""
        parts = command.split()
        if not parts:
            return []
        
        breakdown = []
        main_cmd = parts[0]
        
        breakdown.append(f"Command: {main_cmd}")
        breakdown.append(f"  → {self.explain_command(main_cmd)}")
        
        # Explain common flags
        flags = {
            '-r': 'Recursive (includes subdirectories)',
            '-f': 'Force (no confirmation) or Follow (for tail)',
            '-l': 'Long format (detailed info)',
            '-h': 'Human readable (sizes in KB/MB/GB)',
            '-a': 'All (including hidden files)',
            '-n': 'Number (specify count)',
            '-t': 'Sort by time',
            '-v': 'Verbose (show details)',
            '-i': 'Interactive (ask before acting)',
            '-p': 'Parents (create parent directories)',
            '-name': 'Search by filename',
            '-type': 'Search by type (f=file, d=directory)',
            '-mtime': 'Modified time (in days)',
            '-size': 'File size',
        }
        
        for part in parts[1:]:
            if part.startswith('-'):
                explanation = flags.get(part, 'Flag/option')
                breakdown.append(f"  {part}: {explanation}")
        
        return breakdown
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("🎓 TERMINAL COACH - Natural Language Bash Helper")
        print("=" * 60)
        print("Tell me what you want to do in plain English.")
        print("Type 'examples' to see what I can help with.")
        print("Type 'explain COMMAND' to understand a bash command.")
        print("Type 'run COMMAND' to execute a command.")
        print("Type 'quit' to exit.")
        print("=" * 60)
        print()
        
        while True:
            try:
                user_input = input("💬 What do you want to do? ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Later, brother!")
                    break
                
                elif user_input.lower() == 'examples':
                    self.show_examples()
                
                elif user_input.lower().startswith('explain '):
                    cmd = user_input[8:].strip()
                    self.show_explanation(cmd)
                
                elif user_input.lower().startswith('run '):
                    cmd = user_input[4:].strip()
                    self.run_command(cmd)
                
                elif user_input.lower() == 'again':
                    if self.last_command:
                        self.run_command(self.last_command)
                    else:
                        print("❌ No previous command to repeat")
                
                else:
                    self.handle_natural_language(user_input)
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Interrupted. Later!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_examples(self):
        """Show example queries"""
        print("\n📚 EXAMPLE QUERIES:")
        print("-" * 60)
        
        categories = {
            'Finding Files': [
                'find python files',
                'find files modified today',
                'find large files'
            ],
            'Listing & Viewing': [
                'list files by date',
                'show file tree',
                'disk usage'
            ],
            'Searching': [
                'search in files',
                'search python files'
            ],
            'System Info': [
                'show system info',
                'show running processes',
                'show memory'
            ],
            'Mike\'s Shortcuts': [
                'find context files',
                'show recent snapshots',
                'find my python code'
            ]
        }
        
        for category, examples in categories.items():
            print(f"\n{category}:")
            for ex in examples:
                print(f"  • {ex}")
    
    def show_explanation(self, command):
        """Explain what a command does"""
        print(f"\n📖 EXPLAINING: {command}")
        print("-" * 60)
        
        breakdown = self.break_down_command(command)
        for line in breakdown:
            print(line)
    
    def handle_natural_language(self, query):
        """Convert natural language to bash command"""
        result = self.find_closest_match(query)
        
        if isinstance(result, tuple):
            # Exact match
            key, command = result
            print(f"\n✅ Found exact match: '{key}'")
            print(f"📝 Command: {command}")
            print(f"💡 Explanation: {self.explain_command(command)}")
            
            breakdown = self.break_down_command(command)
            if len(breakdown) > 1:
                print("\n🔍 Breakdown:")
                for line in breakdown:
                    print(f"  {line}")
            
            # Ask if they want to run it
            print("\n❓ Want to run this? (y/n/modify)")
            choice = input("→ ").strip().lower()
            
            if choice == 'y':
                self.run_command(command)
            elif choice == 'modify':
                modified = input(f"Modify command: {command}\n→ ").strip()
                if modified:
                    self.run_command(modified)
        
        elif isinstance(result, list) and result:
            # Multiple matches
            print(f"\n🤔 Found {len(result)} possible matches:")
            print("-" * 60)
            
            for i, (key, command) in enumerate(result, 1):
                print(f"{i}. {key}")
                print(f"   → {command}")
                print()
            
            print("Type the number to use that command, or 'none' to cancel")
            choice = input("→ ").strip()
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(result):
                    key, command = result[idx]
                    print(f"\n📝 Using: {command}")
                    self.run_command(command)
        
        else:
            print(f"\n❌ Couldn't find a match for: '{query}'")
            print("💡 Try 'examples' to see what I can help with")
    
    def run_command(self, command):
        """Execute bash command with safety checks"""
        self.last_command = command
        
        # Safety check for dangerous commands
        dangerous = ['rm -rf /', 'dd if=', 'mkfs', ':(){:|:&};:']
        if any(d in command for d in dangerous):
            print("🚫 DANGEROUS COMMAND DETECTED - NOT RUNNING")
            print("This command could destroy your system!")
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
    coach = TerminalCoach()
    
    # Check for command-line argument
    if len(sys.argv) > 1:
        # Single query mode
        query = ' '.join(sys.argv[1:])
        coach.handle_natural_language(query)
    else:
        # Interactive mode
        coach.interactive_mode()


if __name__ == "__main__":
    main()