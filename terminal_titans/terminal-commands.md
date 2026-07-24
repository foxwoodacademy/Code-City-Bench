# Terminal Commands Cheat Sheet

## Navigation

```bash
pwd                    # Print working directory (where am I?)
ls                     # List files and folders
ls -l                  # List with details
ls -la                 # List all (including hidden)
cd folder              # Change to folder
cd ..                  # Go up one level
cd ~                   # Go to home directory
cd /                   # Go to root directory
```

## File Operations

```bash
cat file.txt           # Display file contents
head file.txt          # Show first 10 lines
tail file.txt          # Show last 10 lines
tail -f file.txt       # Follow file (live updates)
less file.txt          # View file (scrollable)
touch file.txt         # Create empty file
echo "text" > file     # Create file with text
echo "text" >> file    # Append text to file
cp file1 file2         # Copy file
cp -r dir1 dir2        # Copy directory
mv old new             # Move/rename file
rm file                # Delete file
rm -r directory        # Delete directory
```

## Directory Operations

```bash
mkdir folder           # Create directory
mkdir -p path/to/dir   # Create nested directories
rmdir folder           # Remove empty directory
rm -r folder           # Remove directory and contents
```

## Searching

```bash
grep "text" file       # Search for text in file
grep -i "text" file    # Case-insensitive search
grep -r "text" .       # Search recursively
grep -n "text" file    # Show line numbers
grep -v "text" file    # Show lines NOT matching
find . -name "*.txt"   # Find files by name
find . -type f         # Find all files
find . -type d         # Find all directories
```

## Text Processing

```bash
wc file                # Count lines, words, characters
wc -l file             # Count lines only
sort file              # Sort lines
sort -r file           # Sort reverse
sort -n file           # Sort numerically
uniq file              # Remove duplicate lines
cut -d',' -f1 file     # Cut first column (CSV)
sed 's/old/new/' file  # Replace text
awk '{print $1}' file  # Print first column
```

## Pipes and Redirection

```bash
command > file         # Redirect output to file (overwrite)
command >> file        # Redirect output to file (append)
command 2> file        # Redirect errors to file
command | command2     # Pipe output to another command
command1 && command2   # Run command2 if command1 succeeds
command1 || command2   # Run command2 if command1 fails
```

## System Information

```bash
whoami                 # Current username
hostname               # Computer name
date                   # Current date and time
uptime                 # How long system has been running
df -h                  # Disk space usage
du -sh folder          # Folder size
ps                     # Running processes
top                    # Live process monitor
kill PID               # Stop process by ID
```

## File Permissions

```bash
chmod +x file          # Make file executable
chmod 644 file         # Set specific permissions
chown user file        # Change file owner
ls -l                  # View permissions
```

## Network

```bash
ping google.com        # Test connection
curl url               # Download from URL
wget url               # Download file
ifconfig               # Network configuration (Mac/Linux)
ipconfig               # Network configuration (Windows)
```

## Shortcuts

```bash
Ctrl + C               # Cancel current command
Ctrl + D               # Exit terminal
Ctrl + L               # Clear screen
Ctrl + A               # Go to start of line
Ctrl + E               # Go to end of line
Ctrl + U               # Delete line before cursor
Ctrl + K               # Delete line after cursor
Ctrl + R               # Search command history
Tab                    # Auto-complete
↑ / ↓                  # Previous/next command
!!                     # Run last command again
```

## History

```bash
history                # Show command history
!42                    # Run command #42 from history
!grep                  # Run last grep command
history | grep "text"  # Search history
```

## Aliases (Shortcuts)

```bash
alias ll='ls -la'      # Create shortcut
alias ..='cd ..'       # Quick navigation
unalias ll             # Remove alias
```

## Variables

```bash
VAR="value"            # Set variable
echo $VAR              # Use variable
export VAR="value"     # Make available to subprocesses
env                    # Show all variables
```

## Investigator Combos

```bash
# Find all email addresses in files
grep -r -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" .

# Find all Ethereum addresses
grep -r -o "0x[a-fA-F0-9]\{40\}" .

# Count unique IP addresses in log
grep -o "[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}" log.txt | sort | uniq | wc -l

# Find large files (over 100MB)
find . -type f -size +100M

# Search for recently modified files
find . -mtime -7

# Create timestamped backup
cp file.txt file-$(date +%Y%m%d).txt

# Monitor log file for errors
tail -f log.txt | grep -i error

# Extract and count unique values
cat data.txt | sort | uniq -c | sort -rn
```

## Quick Tips

1. **Tab completion**: Start typing and press Tab
2. **Command history**: Use ↑ and ↓ arrows
3. **Clear screen**: `Ctrl + L` or type `clear`
4. **Stop command**: `Ctrl + C`
5. **Search history**: `Ctrl + R` then type
6. **Copy/Paste**: Varies by terminal (often Ctrl+Shift+C/V)

## Common Patterns

```bash
# Process all files in directory
for file in *.txt; do
  echo "Processing $file"
  # your command here
done

# Read file line by line
while read line; do
  echo "Line: $line"
done < file.txt

# Conditional execution
if [ -f file.txt ]; then
  echo "File exists"
fi
```

---

**Print this out and keep it handy!**
