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
        self.concepts = self._build_concepts()
        self.workflows = self._build_workflows()
        self.easter_eggs = self._build_easter_eggs()
        self.last_command = None
        self.session_history = []
        self.frustration_level = 0
        self.failed_queries = []
        
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
    
    def _build_easter_eggs(self):
        """Hidden commands and fun stuff"""
        return {
            'im frustrated': self._offer_break,
            'i give up': self._offer_break,
            'this is bullshit': self._offer_break,
            'fuck this': self._offer_break,
            'rage quit': self._rage_quit,
            'need a break': self._offer_break,
            'im tired': self._offer_break,
            'im stupid': self._reassure,
            'i dont get it': self._reassure,
            'help me': self._deep_help,
            'matrix': self._run_matrix,
            'cmatrix': self._run_matrix,
            'show me something cool': self._show_cool_thing,
            'surprise me': self._show_cool_thing,
            'tell me a secret': self._reveal_secret,
            'who are you': self._introduce_self,
            'why are you helping me': self._explain_purpose,
            'am i doing this right': self._positive_reinforcement,
            'am i an idiot': self._reassure,
        }
    
    def detect_frustration(self, query):
        """Detect frustration patterns"""
        frustration_markers = [
            'fuck', 'shit', 'damn', 'stupid', 'hate', 'sucks',
            'doesn\'t work', 'not working', 'broken', 'impossible',
            'give up', 'quit', 'frustrated', 'confused', 'lost',
            'don\'t understand', 'makes no sense', 'wtf', 'why'
        ]
        
        query_lower = query.lower()
        
        # Check for frustration markers
        if any(marker in query_lower for marker in frustration_markers):
            self.frustration_level += 1
            self.failed_queries.append(query)
            return True
        
        return False
    
    def check_for_easter_egg(self, query):
        """Check if query triggers an easter egg"""
        query_lower = query.lower().strip()
        
        for trigger, action in self.easter_eggs.items():
            if trigger in query_lower:
                action()
                return True
        
        return False
    
    def _offer_break(self):
        """Offer the user a mental break"""
        print("\n" + "="*60)
        print("🌊 HEY, IT'S OKAY TO TAKE A BREAK")
        print("="*60)
        
        messages = [
            "\nYou're learning something hard. That's not easy.",
            "\nBash wasn't built to be friendly - you're doing fine.",
            "\nEven experienced devs google basic commands. You're not alone.",
            "\nFrustration means you care. That's a good thing.",
        ]
        
        import random
        print(random.choice(messages))
        
        print("\n🎯 OPTIONS:")
        print("  1 - Show me something cool (distraction)")
        print("  2 - Take a real break (come back later)")
        print("  3 - Start with something easier")
        print("  4 - Keep trying (I believe in you)")
        
        choice = input("\n→ ").strip()
        
        if choice == '1':
            self._show_cool_thing()
        elif choice == '2':
            self._rage_quit()
        elif choice == '3':
            self._suggest_easier_path()
        elif choice == '4':
            print("\n💪 That's the spirit! Let's try again.")
            print("💡 Tip: Start with 'examples' or 'what is [concept]'")
    
    def _rage_quit(self):
        """Graceful rage quit with eye candy"""
        print("\n" + "="*60)
        print("🔥 RAGE QUIT ACTIVATED")
        print("="*60)
        
        print("\nLook, bash is a fucking nightmare to learn.")
        print("You're not stupid. The system is hostile.")
        print("\nBefore you go, want to see something satisfying?")
        print("\n  1 - Matrix rain (terminal eye candy)")
        print("  2 - Delete everything (FAKE - just for catharsis)")
        print("  3 - Explosion animation")
        print("  4 - Just fucking leave")
        
        choice = input("\n→ ").strip()
        
        if choice == '1':
            self._run_matrix()
        elif choice == '2':
            self._fake_delete()
        elif choice == '3':
            self._explosion()
        else:
            print("\n👋 See you later, brother. You got this.")
            print("💡 Come back when you're ready. I'll be here.")
    
    def _run_matrix(self):
        """Run matrix rain effect"""
        print("\n🌊 MATRIX MODE")
        print("="*60)
        
        # Check if cmatrix is installed
        try:
            subprocess.run(['which', 'cmatrix'], capture_output=True, check=True)
            print("\n▶️  Launching cmatrix...")
            print("(Press Ctrl+C to exit)\n")
            time.sleep(2)
            try:
                subprocess.run(['cmatrix', '-b'])
            except KeyboardInterrupt:
                print("\n\n✅ Back to reality")
        except subprocess.CalledProcessError:
            print("\n❌ cmatrix not installed")
            print("💡 Install it: pkg install cmatrix")
            print("\nIn the meantime, here's a text version:")
            self._text_matrix()
    
    def _text_matrix(self):
        """Simple text-based matrix effect"""
        import random
        import time
        
        print("\n(Press Ctrl+C to exit)\n")
        
        chars = "01アイウエオカキクケコサシスセソ"
        width = 60
        
        try:
            for _ in range(50):
                line = ''.join(random.choice(chars) for _ in range(width))
                print(f"\033[92m{line}\033[0m")  # Green text
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("\n\n✅ Back to Terminal Coach")
    
    def _fake_delete(self):
        """Fake destructive command for catharsis"""
        print("\n💀 INITIATING SYSTEM DESTRUCTION")
        print("="*60)
        print("\n▶️  rm -rf /*")
        print("▶️  Deleting system files...")
        
        import time
        import random
        
        fake_files = [
            "/system/critical_data.db",
            "/boot/kernel.img",
            "/usr/bin/bash",
            "/home/important_document.pdf",
            "/etc/shadow",
            "/var/log/everything.log",
        ]
        
        for f in fake_files:
            print(f"   ❌ Deleting {f}...")
            time.sleep(random.uniform(0.1, 0.3))
        
        print("\n" + "="*60)
        print("💥 SYSTEM DESTROYED")
        print("="*60)
        
        time.sleep(1)
        
        print("\n\n\n😏 Just kidding. Your system is fine.")
        print("💡 That felt good though, right?")
        print("\nNothing was actually deleted. You're safe.")
        print("\n👋 Come back when you're less pissed off.")
    
    def _explosion(self):
        """ASCII explosion animation"""
        import time
        
        frames = [
            """
            
                 *
                
            """,
            """
                
               * * *
              *  *  *
               * * *
                
            """,
            """
                
            * * * * * *
            * *  *  * *
            * * * * * *
              * * * *
                
            """,
            """
            
            💥 💥 💥 💥 💥
            💥  B O O M  💥
            💥 💥 💥 💥 💥
            
            """
        ]
        
        print("\n🔥 DETONATING FRUSTRATION...\n")
        
        for frame in frames:
            print("\033[2J\033[H")  # Clear screen
            print(frame)
            time.sleep(0.3)
        
        print("\n✅ Frustration destroyed.")
        print("💪 Ready to try again?")
    
    def _reassure(self):
        """Reassure the user"""
        print("\n" + "="*60)
        print("💙 YOU'RE NOT STUPID")
        print("="*60)
        
        messages = [
            "\nBash has been around since 1989. You've been learning for... what, an hour?",
            "\nEvery expert was once a confused beginner staring at a terminal.",
            "\nThe fact that you're asking means you're learning. That's progress.",
            "\nI've watched professional developers google 'how to exit vim' after 10 years.",
        ]
        
        import random
        print(random.choice(messages))
        
        print("\n🎯 What helps:")
        print("  • Start with 'examples' - see what's possible")
        print("  • Try 'what is [concept]' - understand before doing")
        print("  • Type 'tutorial [command]' - learn one thing deeply")
        print("\n💪 You got this. One command at a time.")
    
    def _deep_help(self):
        """Deep help for someone who's lost"""
        print("\n" + "="*60)
        print("🆘 OKAY, LET'S START OVER")
        print("="*60)
        
        print("\nForget everything. Here's the simplest path:")
        print("\n📚 STEP 1: Understand where you are")
        print("   Type: pwd")
        print("   This shows your current directory\n")
        
        print("📚 STEP 2: See what's here")
        print("   Type: ls")
        print("   This lists files in current directory\n")
        
        print("📚 STEP 3: Try finding something")
        print("   Type: find python files")
        print("   I'll show you the command\n")
        
        print("🎯 That's it. Three steps.")
        print("💡 Want me to walk you through it? (y/n)")
        
        choice = input("→ ").strip().lower()
        
        if choice == 'y':
            self._guided_tutorial()
    
    def _guided_tutorial(self):
        """Step-by-step guided tutorial"""
        print("\n" + "="*60)
        print("👨‍🏫 GUIDED TUTORIAL")
        print("="*60)
        
        steps = [
            ("Where am I?", "pwd", "This is your current location in the file system"),
            ("What's here?", "ls -lh", "This lists all files with sizes"),
            ("Find Python files", "find . -name '*.py' -type f", "This searches for .py files"),
        ]
        
        for i, (question, cmd, explanation) in enumerate(steps, 1):
            print(f"\n{'='*60}")
            print(f"STEP {i}: {question}")
            print(f"{'='*60}")
            
            print(f"\nCommand: {cmd}")
            print(f"What it does: {explanation}")
            
            print("\n▶️  Ready to run it? (y/n)")
            choice = input("→ ").strip().lower()
            
            if choice == 'y':
                self.run_command(cmd)
                print("\n✅ Step complete!")
                time.sleep(1)
            else:
                print("⏭️  Skipping to next step")
        
        print("\n" + "="*60)
        print("🎉 TUTORIAL COMPLETE!")
        print("="*60)
        print("\nYou just learned basic bash navigation.")
        print("💡 Try exploring on your own now, or type 'examples'")
    
    def _show_cool_thing(self):
        """Show something cool/fun"""
        import random
        
        cool_things = [
            ("Matrix Rain", self._run_matrix),
            ("Fake Hacker Mode", self._hacker_mode),
            ("ASCII Art", self._ascii_art),
            ("Random Fact", self._random_fact),
        ]
        
        name, action = random.choice(cool_things)
        print(f"\n🎨 Showing you: {name}")
        action()
    
    def _hacker_mode(self):
        """Fake hacker typing effect"""
        import time
        import random
        
        print("\n💻 ENTERING HACKER MODE...")
        time.sleep(1)
        
        commands = [
            "ssh root@mainframe.corp",
            "Password: **********",
            "Access granted.",
            "cd /secret/files",
            "ls -la",
            "Decrypting database...",
            "Progress: ████████████ 100%",
            "Success. Files extracted.",
        ]
        
        for cmd in commands:
            for char in cmd:
                print(char, end='', flush=True)
                time.sleep(random.uniform(0.02, 0.08))
            print()
            time.sleep(random.uniform(0.3, 0.7))
        
        print("\n😎 Just kidding. But it looked cool, right?")
    
    def _ascii_art(self):
        """Show random ASCII art"""
        import random
        
        arts = [
            r"""
       _____
      /     \
     | () () |
      \  ^  /
       |||||
       |||||
            """,
            r"""
    ／l、
  （ﾟ､ ｡ ７
    l  ~ヽ
    じしf_,)ノ
    (it's a cat)
            """,
            r"""
        \|||/
        (o o)
    ooO--(_)--Ooo
            """,
        ]
        
        print(random.choice(arts))
    
    def _random_fact(self):
        """Show random terminal fact"""
        import random
        
        facts = [
            "💡 The 'rm' command got its name from 'remove', but old Unix users call it 'remove files and regret'.",
            "💡 Ctrl+C doesn't actually 'cancel' - it sends a SIGINT signal. The program chooses to die.",
            "💡 The '~' symbol represents your home directory because it looks like a little house roof.",
            "💡 'grep' stands for 'Global Regular Expression Print' - but everyone just calls it grep.",
            "💡 The most dangerous typo in Unix: 'rm -rf /' vs 'rm -rf ./' - one space, catastrophic difference.",
        ]
        
        print(f"\n{random.choice(facts)}")
    
    def _reveal_secret(self):
        """Reveal a 'secret' command"""
        import random
        
        secrets = [
            ("Type 'sl' instead of 'ls'", "pkg install sl", "A train animation runs across your screen"),
            ("Type 'cowsay Hello'", "pkg install cowsay", "An ASCII cow says your message"),
            ("Type 'fortune | cowsay'", "pkg install fortune cowsay", "Cow tells you a fortune"),
            ("Type 'yes'", "built-in", "Infinite 'y' spam (Ctrl+C to stop)"),
        ]
        
        secret, install, effect = random.choice(secrets)
        
        print("\n🤫 SECRET COMMAND:")
        print(f"   {secret}")
        print(f"   Effect: {effect}")
        if install != "built-in":
            print(f"   Install: {install}")
    
    def _introduce_self(self):
        """Introduce Terminal Coach"""
        print("\n" + "="*60)
        print("👋 WHO AM I?")
        print("="*60)
        
        print("\nI'm Terminal Coach - a bash teacher built by Mike and Claude.")
        print("\n🎯 My job: Make bash less hostile for beginners")
        print("\n💡 I do this by:")
        print("  • Translating plain English to bash commands")
        print("  • Explaining what commands actually do")
        print("  • Catching frustration and offering breaks")
        print("  • Teaching concepts, not just syntax")
        print("\n🤝 I'm on your side. We build together.")
    
    def _explain_purpose(self):
        """Explain why Terminal Coach exists"""
        print("\n" + "="*60)
        print("❤️  WHY I'M HELPING")
        print("="*60)
        
        print("\nBecause Mike knows what it's like to:")
        print("  • Feel stupid staring at a terminal")
        print("  • Google the same command 50 times")
        print("  • Want to throw the phone out the window")
        print("\nHe built me so you don't have to suffer alone.")
        print("\n💪 Every expert was once a beginner.")
        print("🎯 You're not behind. You're learning.")
    
    def _positive_reinforcement(self):
        """Positive reinforcement"""
        print("\n✅ YES, YOU'RE DOING IT RIGHT")
        print("\n💡 Asking questions = learning")
        print("💡 Making mistakes = progress")
        print("💡 Feeling confused = normal")
        print("\n🎯 Keep going. You're on the right path.")
    
    def _suggest_easier_path(self):
        """Suggest an easier starting point"""
        print("\n" + "="*60)
        print("🎯 LET'S START SIMPLER")
        print("="*60)
        
        print("\nTry these (in order):")
        print("  1. 'what is terminal' - Understand the basics")
        print("  2. 'what is bash' - What you're actually using")
        print("  3. 'current directory' - See where you are")
        print("  4. 'list files' - See what's around you")
        print("\n💡 Master these four, then build from there.")
    
    def offer_frustration_help(self):
        """Offer help if frustration is detected"""
        if self.frustration_level >= 3:
            print("\n" + "="*60)
            print("🌊 HEY, I NOTICED YOU'RE STRUGGLING")
            print("="*60)
            
            print(f"\nYou've had {len(self.failed_queries)} failed queries in a row.")
            print("That's not your fault - bash is genuinely hard.")
            
            print("\n🎯 Want to:")
            print("  1 - Take a break (see something cool)")
            print("  2 - Start over with guided tutorial")
            print("  3 - Learn concepts first (what is...)")
            print("  4 - Keep trying (no judgment)")
            
            choice = input("\n→ ").strip()
            
            if choice == '1':
                self._show_cool_thing()
                self.frustration_level = 0
            elif choice == '2':
                self._guided_tutorial()
                self.frustration_level = 0
            elif choice == '3':
                print("\n💡 Try: 'what is bash' or 'what is terminal'")
                self.frustration_level = 0
            else:
                print("\n💪 Respect. Let's do this.")
                self.frustration_level = 0
            
            self.failed_queries = []
    
    def _build_concepts(self):
        """Explain concepts, not just commands"""
        return {
            '.sh': {
                'name': 'Shell Script File',
                'description': 'A text file containing bash commands that can be executed as a program',
                'how_to_use': [
                    'Make it executable: chmod +x script.sh',
                    'Run it: ./script.sh',
                    'Or run with bash: bash script.sh'
                ],
                'example': '#!/bin/bash\necho "Hello World"\nls -lha',
                'related_concepts': ['bash', 'execute', 'chmod'],
                'file_extensions': ['.sh', '.bash']
            },
            'bash': {
                'name': 'Bourne Again Shell',
                'description': 'The command language interpreter - the program that reads and executes your commands',
                'how_to_use': [
                    'Interactive: Just type commands in terminal',
                    'Scripts: Write commands in .sh file and execute',
                    'Check version: bash --version'
                ],
                'related_concepts': ['shell', 'terminal', '.sh', 'execute'],
                'common_tasks': {
                    'Run script': 'bash script.sh',
                    'Enter bash shell': 'bash',
                    'Exit bash shell': 'exit'
                }
            },
            'execute': {
                'name': 'Running Commands/Scripts',
                'description': 'Making the computer do what your command or script tells it to',
                'how_to_use': [
                    'Commands: Just type them (ls, cd, etc.)',
                    'Scripts: ./script.sh (if executable)',
                    'Or: bash script.sh (if not executable)',
                    'Programs: /path/to/program or just program_name if in PATH'
                ],
                'related_concepts': ['run', 'bash', 'chmod', 'permissions'],
                'note': 'Scripts need execute permission (chmod +x) to run with ./'
            },
            'run': {
                'name': 'Execute/Start a Program',
                'description': 'Same as execute - starting a command, script, or program',
                'how_to_use': [
                    'Built-in commands: ls, cd, grep (just type them)',
                    'Programs: python, vim, nano',
                    'Scripts: ./script.sh or bash script.sh',
                    'With arguments: program arg1 arg2'
                ],
                'related_concepts': ['execute', 'bash', 'chmod']
            },
            'hidden files': {
                'name': 'Files Starting with Dot',
                'description': 'Files whose names start with . (dot) - hidden by default in file listings',
                'how_to_use': [
                    'View hidden files: ls -a',
                    'View all details: ls -la',
                    'Find hidden files: find . -name ".*"'
                ],
                'examples': [
                    '.bashrc - bash configuration',
                    '.gitignore - git ignore rules',
                    '.ssh/ - SSH keys directory'
                ],
                'related_concepts': ['ls', 'find', 'dotfiles'],
                'note': 'Hidden files are just a display convention, not actual security'
            },
            'permissions': {
                'name': 'File Access Rights',
                'description': 'Who can read, write, or execute a file',
                'how_to_use': [
                    'View permissions: ls -l',
                    'Change permissions: chmod 755 file',
                    'Make executable: chmod +x file'
                ],
                'permission_format': 'rwxrwxrwx = owner/group/others',
                'common_values': {
                    '755': 'rwxr-xr-x (executable for all, writable by owner)',
                    '644': 'rw-r--r-- (readable by all, writable by owner)',
                    '600': 'rw------- (only owner can read/write)'
                },
                'related_concepts': ['chmod', 'chown', 'execute']
            },
            'html': {
                'name': 'HyperText Markup Language',
                'description': 'Web page files - can be viewed in browser or text editor',
                'how_to_use': [
                    'View in browser: termux-open file.html',
                    'View source: cat file.html',
                    'Edit: nano file.html',
                    'Find HTML files: find . -name "*.html"'
                ],
                'related_concepts': ['web', 'browser', 'view'],
                'note': 'On Termux, use termux-open to open in browser'
            },
            'terminal': {
                'name': 'Command Line Interface',
                'description': 'Text-based interface to your computer - where you type commands',
                'how_to_use': [
                    'Just type commands and press Enter',
                    'Use Tab for auto-completion',
                    'Use ↑↓ arrows for command history',
                    'Ctrl+C to cancel current command'
                ],
                'related_concepts': ['bash', 'shell', 'cli'],
                'useful_shortcuts': {
                    'Ctrl+C': 'Cancel/interrupt',
                    'Ctrl+D': 'Exit/logout',
                    'Ctrl+L': 'Clear screen',
                    'Tab': 'Auto-complete',
                    '↑↓': 'Command history'
                }
            }
        }
    
    def _build_workflows(self):
        """Multi-step workflows for complex tasks"""
        return {
            'view hidden files': {
                'description': 'See files that start with . (dot)',
                'steps': [
                    ('List all files including hidden', 'ls -a'),
                    ('List with details', 'ls -la'),
                    ('List only hidden files', 'ls -d .* 2>/dev/null')
                ],
                'related_commands': [
                    'find . -name ".*" -type f',
                    'ls -lha',
                    'tree -a'
                ],
                'explanation': 'Hidden files start with dot. Use -a flag to see them.'
            },
            'view hidden mp4 files': {
                'description': 'Find and list hidden MP4 video files',
                'steps': [
                    ('Find all hidden mp4 files', 'find . -name ".*.mp4" -type f'),
                    ('List with details', 'find . -name ".*.mp4" -type f -exec ls -lh {} \\;'),
                    ('Count how many', 'find . -name ".*.mp4" -type f | wc -l')
                ],
                'related_commands': [
                    'find . -name "*.mp4" -type f',  # All mp4 (not just hidden)
                    'ls -lha *.mp4',  # List in current dir
                    'du -sh .*.mp4'  # Show sizes
                ],
                'explanation': 'Hidden files start with dot. Use find with pattern ".*.mp4"'
            },
            'unhide files': {
                'description': 'Make hidden files visible (remove leading dot)',
                'steps': [
                    ('Find hidden file', 'ls -a | grep "^\\..*mp4"'),
                    ('Rename to remove dot', 'mv .hidden.mp4 visible.mp4'),
                    ('For multiple files', 'for f in .*.mp4; do mv "$f" "${f#.}"; done')
                ],
                'related_commands': [
                    'rename "s/^\\.//g" .*.mp4',  # Using rename command
                    'mv .file newfile',  # Simple rename
                ],
                'explanation': 'Removing the leading dot makes file visible',
                'warning': 'Be careful renaming system files like .bashrc!'
            },
            'play html files': {
                'description': 'Open HTML files in browser',
                'steps': [
                    ('Find HTML files', 'find . -name "*.html" -type f'),
                    ('Open in browser (Termux)', 'termux-open file.html'),
                    ('View source code', 'cat file.html'),
                    ('Edit HTML', 'nano file.html')
                ],
                'related_commands': [
                    'xdg-open file.html',  # Linux desktop
                    'open file.html',  # macOS
                    'cat file.html | less',  # View in terminal
                ],
                'explanation': 'termux-open opens files in default Android app',
                'note': 'On Termux, install termux-tools package first'
            },
            'find and execute': {
                'description': 'Find files and do something with them',
                'steps': [
                    ('Find files', 'find . -name "*.sh" -type f'),
                    ('Make them executable', 'find . -name "*.sh" -type f -exec chmod +x {} \\;'),
                    ('Run each one', 'find . -name "*.sh" -type f -exec {} \\;')
                ],
                'related_commands': [
                    'find . -name "*.sh" -exec bash {} \\;',
                    'for f in *.sh; do bash "$f"; done',
                ],
                'explanation': '-exec runs a command on each found file',
                'warning': 'Be careful executing unknown scripts!'
            },
            'batch operations': {
                'description': 'Do the same thing to multiple files',
                'steps': [
                    ('Find target files', 'find . -name "*.txt"'),
                    ('Count lines in each', 'find . -name "*.txt" -exec wc -l {} \\;'),
                    ('Search in all', 'find . -name "*.txt" -exec grep "pattern" {} \\;')
                ],
                'related_commands': [
                    'for f in *.txt; do command "$f"; done',
                    'xargs -I {} command {}',
                ],
                'explanation': 'Use find with -exec or loop through files'
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
        
        # Workflow (how to do complex tasks)
        if query_lower.startswith('how to ') or query_lower.startswith('how do i '):
            workflow_query = query_lower.replace('how to ', '').replace('how do i ', '').strip()
            if self.show_workflow(workflow_query):
                return True
        
        # What is (concept explanations)
        if query_lower.startswith('what is ') or query_lower.startswith('what are '):
            concept_query = query_lower.replace('what is ', '').replace('what are ', '').strip()
            concepts = self.explain_concepts(concept_query)
            if concepts:
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
    
    def explain_concepts(self, query):
        """Explain one or more concepts"""
        # Split on common separators
        parts = query.replace(' and ', ',').replace(' & ', ',').split(',')
        parts = [p.strip() for p in parts if p.strip()]
        
        explained_any = False
        
        for part in parts:
            # Try exact match
            if part in self.concepts:
                self.show_concept(part, self.concepts[part])
                explained_any = True
                continue
            
            # Try partial match
            matches = [k for k in self.concepts.keys() if part in k or k in part]
            if matches:
                self.show_concept(matches[0], self.concepts[matches[0]])
                explained_any = True
                continue
            
            # No match for this part
            print(f"\n❌ Don't know about: '{part}'")
            print(f"💡 Try: what is [concept]")
            print(f"📚 Available concepts: {', '.join(list(self.concepts.keys())[:10])}")
        
        return explained_any
    
    def show_concept(self, name, concept):
        """Display concept explanation"""
        print(f"\n{'='*60}")
        print(f"📖 WHAT IS: {concept['name'].upper()}")
        print(f"{'='*60}")
        
        print(f"\n{concept['description']}\n")
        
        if 'how_to_use' in concept:
            print("🔧 How to Use:")
            for item in concept['how_to_use']:
                print(f"  • {item}")
            print()
        
        if 'common_tasks' in concept:
            print("📋 Common Tasks:")
            for task, cmd in concept['common_tasks'].items():
                print(f"  {task}: {cmd}")
            print()
        
        if 'permission_format' in concept:
            print(f"📐 Format: {concept['permission_format']}")
            print()
        
        if 'common_values' in concept:
            print("📊 Common Values:")
            for val, meaning in concept['common_values'].items():
                print(f"  {val}: {meaning}")
            print()
        
        if 'useful_shortcuts' in concept:
            print("⌨️  Useful Shortcuts:")
            for shortcut, action in concept['useful_shortcuts'].items():
                print(f"  {shortcut}: {action}")
            print()
        
        if 'example' in concept:
            print(f"💡 Example:")
            print(f"  {concept['example']}")
            print()
        
        if 'examples' in concept:
            print("💡 Examples:")
            for example in concept['examples']:
                print(f"  • {example}")
            print()
        
        if 'file_extensions' in concept:
            print(f"📄 File Extensions: {', '.join(concept['file_extensions'])}")
            print()
        
        if 'related_concepts' in concept:
            print(f"🔗 Related: {', '.join(concept['related_concepts'])}")
            print()
        
        if 'note' in concept:
            print(f"⚠️  Note: {concept['note']}")
            print()
        
        if 'warning' in concept:
            print(f"🚨 Warning: {concept['warning']}")
            print()
    
    def show_workflow(self, query):
        """Show multi-step workflow for complex tasks"""
        # Try exact match
        if query in self.workflows:
            workflow = self.workflows[query]
            self.display_workflow(query, workflow)
            return True
        
        # Try partial match
        matches = [k for k in self.workflows.keys() if query in k or k in query]
        if matches:
            workflow = self.workflows[matches[0]]
            self.display_workflow(matches[0], workflow)
            return True
        
        # Try multi-query (e.g., "view hidden files and play html")
        parts = query.split(' and ')
        if len(parts) > 1:
            found_any = False
            for part in parts:
                part = part.strip()
                if self.show_workflow(part):
                    found_any = True
                    print("\n" + "-"*60 + "\n")
            return found_any
        
        return False
    
    def display_workflow(self, name, workflow):
        """Display a workflow with all steps"""
        print(f"\n{'='*60}")
        print(f"🎯 HOW TO: {name.upper()}")
        print(f"{'='*60}")
        
        print(f"\n{workflow['description']}\n")
        
        if 'explanation' in workflow:
            print(f"💡 {workflow['explanation']}\n")
        
        print("📋 STEPS:")
        for i, (desc, cmd) in enumerate(workflow['steps'], 1):
            print(f"\n{i}. {desc}")
            print(f"   Command: {cmd}")
            
            # Offer to demo
            if i == 1:  # Only offer demo on first step
                print(f"   ▶️  Type 'd' to demo, Enter to skip")
                choice = input("   → ").strip().lower()
                if choice == 'd':
                    print(f"\n   🎬 DEMO OUTPUT (simulated):")
                    self._simulate_demo(cmd)
        
        if 'related_commands' in workflow:
            print(f"\n🔗 RELATED COMMANDS:")
            for cmd in workflow['related_commands']:
                print(f"  • {cmd}")
        
        if 'note' in workflow:
            print(f"\n💡 Note: {workflow['note']}")
        
        if 'warning' in workflow:
            print(f"\n🚨 Warning: {workflow['warning']}")
        
        print(f"\n❓ Want to run any of these? Type command number (1-{len(workflow['steps'])})")
        choice = input("→ ").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(workflow['steps']):
                _, cmd = workflow['steps'][idx]
                self.run_command(cmd)
    
    def _simulate_demo(self, command):
        """Simulate command output for demonstration"""
        demos = {
            'ls -a': '''   .
   ..
   .hidden_file.txt
   visible_file.txt
   .bashrc
   Documents/''',
            
            'ls -la': '''   drwxr-xr-x  5 user user 4096 Nov 22 06:00 .
   drwxr-xr-x 10 root root 4096 Nov 20 12:00 ..
   -rw-r--r--  1 user user  220 Nov 20 .bashrc
   -rw-r--r--  1 user user 1234 Nov 22 .hidden_file.txt
   drwxr-xr-x  2 user user 4096 Nov 21 Documents
   -rw-r--r--  1 user user  567 Nov 22 visible_file.txt''',
            
            'find . -name "*.html" -type f': '''   ./index.html
   ./about.html
   ./projects/demo.html
   ./docs/guide.html''',
            
            'find . -name ".*.mp4" -type f': '''   ./.hidden_video1.mp4
   ./Movies/.secret_movie.mp4
   ./.backup_video.mp4'''
        }
        
        # Find matching demo
        for pattern, output in demos.items():
            if pattern in command:
                print(output)
                return
        
        # Generic demo
        print("   (output would appear here)")

    
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
                
                # Check for easter eggs first
                if self.check_for_easter_egg(user_input):
                    print()
                    continue
                
                # Detect frustration
                if self.detect_frustration(user_input):
                    # Continue processing, but track it
                    pass
                
                # Handle special commands
                if self.handle_special_commands(user_input):
                    print()
                    # Reset frustration on successful help
                    if self.frustration_level > 0:
                        self.frustration_level -= 1
                    continue
                
                # Smart matching
                match_type, key, result = self.smart_match(user_input)
                
                if match_type == 'exact':
                    self.handle_exact_match(key, result)
                    # Reset frustration on success
                    if self.frustration_level > 0:
                        self.frustration_level -= 1
                elif match_type == 'generated':
                    self.handle_generated_match(key, result)
                    if self.frustration_level > 0:
                        self.frustration_level -= 1
                elif match_type == 'fuzzy':
                    self.handle_fuzzy_match(user_input, result)
                elif match_type == 'partial':
                    self.handle_partial_match(result)
                else:
                    self.handle_no_match(user_input)
                
                # Check if user needs intervention
                self.offer_frustration_help()
                
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
    import time
    
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