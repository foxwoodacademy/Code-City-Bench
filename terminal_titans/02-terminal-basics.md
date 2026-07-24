# 💻 Lesson 2: Terminal Mastery for Investigators

## Why Investigators Use the Terminal

**Real Talk**: Every professional forensic investigator uses the terminal daily. Here's why:

1. **Speed**: Type commands faster than clicking menus
2. **Automation**: Run the same steps on 1000 files instantly
3. **Power**: Access tools that don't have graphical interfaces
4. **Documentation**: Easy to record exactly what you did
5. **Remote Work**: Investigate systems you can't physically access

## Advanced Navigation

### Understanding the File System Tree

Your computer's files are organized like a family tree:

```
Root (/)
├── Users/
│   ├── Calvin/
│   │   ├── Documents/
│   │   ├── Desktop/
│   │   └── Downloads/
│   └── OtherUser/
├── Program Files/
└── Windows/ (or System/ on Mac/Linux)
```

### Absolute vs Relative Paths

**Absolute Path**: The complete address from the root
```bash
cd /Users/Calvin/Documents/cases
```
**Translation**: "Go to this exact location"

**Relative Path**: Address from where you currently are
```bash
cd cases
```
**Translation**: "Go to the 'cases' folder from here"

**Example**:
```bash
# You are in: /Users/Calvin/Documents

# Absolute path (works from anywhere)
cd /Users/Calvin/Documents/cases

# Relative path (only works if you're in Documents)
cd cases

# Go up one level
cd ..

# Go up two levels
cd ../..
```

## File Operations for Investigators

### 1. Copying Files (Preserving Evidence)

**Command**: `cp` (copy)

```bash
# Copy a single file
cp evidence.txt evidence-backup.txt

# Copy to a different folder
cp evidence.txt ../backups/

# Copy entire folder
cp -r case-folder/ case-folder-backup/
```

**Why `-r`?**: Means "recursive" - copy folder and everything inside

**Investigator Tip**: Always backup evidence before analyzing!

### 2. Moving/Renaming Files

**Command**: `mv` (move)

```bash
# Rename a file
mv old-name.txt new-name.txt

# Move to different folder
mv evidence.txt ../archived-cases/

# Move and rename at once
mv case1.txt ../completed/case-001-solved.txt
```

### 3. Deleting Files (Be Careful!)

**Command**: `rm` (remove)

```bash
# Delete a file
rm temporary-notes.txt

# Delete a folder and contents
rm -r old-case-folder/

# Delete with confirmation (safer!)
rm -i important-file.txt
```

**⚠️ WARNING**: Deleted files don't go to Recycle Bin! They're gone!

**Investigator Tip**: Never delete original evidence. Archive it instead.

### 4. Searching for Files

**Command**: `find` (search)

```bash
# Find all .txt files in current folder
find . -name "*.txt"

# Find files modified in last 7 days
find . -mtime -7

# Find files larger than 10MB
find . -size +10M
```

**What's `*`?**: A wildcard meaning "anything"
- `*.txt` = any file ending in .txt
- `case-*` = any file starting with case-
- `*evidence*` = any file containing "evidence"

## Text Processing (Super Important for Investigators)

### 1. Searching Inside Files

**Command**: `grep` (search text)

```bash
# Find lines containing "bitcoin" in a file
grep "bitcoin" transactions.txt

# Search all files in folder
grep "suspicious" *.txt

# Case-insensitive search
grep -i "BITCOIN" transactions.txt

# Show line numbers
grep -n "address" evidence.txt
```

**Real Example**:
```bash
# Find all wallet addresses in a file
grep "0x[a-fA-F0-9]\{40\}" evidence.txt
```

### 2. Counting Things

**Command**: `wc` (word count)

```bash
# Count lines in a file
wc -l transactions.txt

# Count words
wc -w report.txt

# Count characters
wc -c evidence.txt
```

**Investigator Use**: "How many transactions in this file?"
```bash
wc -l transactions.csv
```

### 3. Viewing Large Files

**Command**: `head` and `tail`

```bash
# See first 10 lines
head transactions.txt

# See first 50 lines
head -n 50 transactions.txt

# See last 10 lines
tail transactions.txt

# Watch file as it grows (live monitoring!)
tail -f live-log.txt
```

**Real Use**: Monitoring a running investigation
```bash
tail -f audit-log.txt
```

### 4. Sorting Data

**Command**: `sort`

```bash
# Sort lines alphabetically
sort addresses.txt

# Sort numerically
sort -n amounts.txt

# Sort in reverse
sort -r dates.txt

# Remove duplicates
sort -u addresses.txt
```

## Pipes: Combining Commands (This is Where It Gets Powerful!)

**What's a Pipe?**: The `|` symbol connects commands

**Think of it like**: Assembly line in a factory

```bash
# Find all addresses, sort them, remove duplicates
grep "0x" evidence.txt | sort | uniq

# Count how many unique addresses
grep "0x" evidence.txt | sort | uniq | wc -l

# Find suspicious transactions and save to file
grep "mixer" transactions.txt | sort > suspicious.txt
```

**Real Investigation Example**:
```bash
# Find all Bitcoin addresses, sort, count unique ones
cat evidence.txt | grep -o "[13][a-km-zA-HJ-NP-Z1-9]\{25,34\}" | sort | uniq | wc -l
```

**Translation**: 
1. Read evidence.txt
2. Extract Bitcoin addresses
3. Sort them
4. Remove duplicates
5. Count how many

## Redirection: Saving Output

### Output to File

```bash
# Save output to file (overwrite)
ls > file-list.txt

# Append to file
echo "New evidence found" >> case-notes.txt

# Save errors to file
command 2> errors.txt

# Save both output and errors
command > output.txt 2>&1
```

### Input from File

```bash
# Use file as input
sort < unsorted-data.txt

# Process file line by line
while read line; do
  echo "Processing: $line"
done < addresses.txt
```

## Practical Investigation Scenarios

### Scenario 1: Extract All Email Addresses

```bash
# From a text file
grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" evidence.txt > emails.txt
```

### Scenario 2: Find Largest Files (Looking for Hidden Data)

```bash
# Find 10 largest files
find . -type f -exec ls -lh {} \; | sort -k 5 -hr | head -10
```

### Scenario 3: Timeline of File Modifications

```bash
# List files by modification time
ls -lt

# Show detailed timestamps
ls -lt --time-style=full-iso
```

### Scenario 4: Search Multiple Files for Evidence

```bash
# Search all text files for wallet addresses
grep -r "0x[a-fA-F0-9]\{40\}" . --include="*.txt"
```

## Practice Exercise: Your First Real Investigation

You've found a text file with mixed data. Extract useful information:

```bash
# 1. Create sample evidence file
cat > evidence.txt << EOF
Transaction from 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
Contact: suspect@email.com
Amount: 1.5 BTC
Transaction from 0x1234567890123456789012345678901234567890
Contact: witness@email.com
Amount: 0.5 BTC
Suspicious activity detected
Transaction from 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
EOF

# 2. Extract all Ethereum addresses
grep -o "0x[a-fA-F0-9]\{40\}" evidence.txt

# 3. Extract all email addresses
grep -E -o "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}" evidence.txt

# 4. Find lines with "suspicious"
grep -i "suspicious" evidence.txt

# 5. Count total transactions
grep -c "Transaction" evidence.txt

# 6. Create investigation report
echo "=== Investigation Report ===" > report.txt
echo "Date: $(date)" >> report.txt
echo "" >> report.txt
echo "Addresses Found:" >> report.txt
grep -o "0x[a-fA-F0-9]\{40\}" evidence.txt | sort | uniq >> report.txt
echo "" >> report.txt
echo "Contacts:" >> report.txt
grep -E -o "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}" evidence.txt >> report.txt

# 7. View your report
cat report.txt
```

**Congratulations!** You just processed evidence like a real investigator! 🎉

## Keyboard Shortcuts (Save Time!)

```bash
Ctrl + C        # Cancel current command
Ctrl + D        # Exit terminal
Ctrl + L        # Clear screen
Ctrl + A        # Go to start of line
Ctrl + E        # Go to end of line
Ctrl + U        # Delete line before cursor
Ctrl + K        # Delete line after cursor
Ctrl + R        # Search command history
Tab             # Auto-complete
↑ / ↓           # Previous/next command
```

## Command History

```bash
# See previous commands
history

# Run command #42 from history
!42

# Run last command again
!!

# Run last command that started with "grep"
!grep

# Search history
Ctrl + R, then type search term
```

## Creating Aliases (Shortcuts for Common Commands)

```bash
# Create shortcut for long command
alias ll='ls -lah'
alias cases='cd ~/forensics-practice/cases'
alias backup='cp -r . ../backup-$(date +%Y%m%d)'

# Now you can just type:
ll          # Instead of ls -lah
cases       # Jump to cases folder
backup      # Backup current folder
```

## Environment Variables

```bash
# See all variables
env

# See specific variable
echo $HOME
echo $PATH

# Set your own variable
export CASE_DIR="/Users/Calvin/cases"

# Use it
cd $CASE_DIR
```

## Practice Exercises

### Exercise 1: File Detective
```bash
# Create test files
mkdir test-investigation
cd test-investigation
echo "evidence1" > file1.txt
echo "evidence2" > file2.txt
echo "evidence3" > file3.txt

# Your tasks:
# 1. List all files
# 2. Count total files
# 3. Search for "evidence" in all files
# 4. Create backup of all files
# 5. Rename file1.txt to evidence-001.txt
```

### Exercise 2: Data Extraction
```bash
# Create sample data
cat > transactions.txt << EOF
2024-01-01,0xABC,100
2024-01-02,0xDEF,200
2024-01-03,0xABC,150
2024-01-04,0xGHI,300
EOF

# Your tasks:
# 1. Find all unique addresses
# 2. Calculate total amount (hint: use awk or manual)
# 3. Find transactions over 150
# 4. Sort by date
```

## Checkpoint Quiz

1. What's the difference between `>` and `>>`?
2. What does the pipe `|` do?
3. How do you search for text in files?
4. What command finds files by name?
5. How do you see the last 20 lines of a file?
6. What does `*` mean in `*.txt`?
7. How do you cancel a running command?

**Answers at bottom**

## Next Steps

✅ You can navigate the file system  
✅ You can search and process text  
✅ You can combine commands with pipes  
✅ You're ready for real investigations!  

**Next Lesson**: `03-first-investigation.md` - Solve your first case!

---

**Time to Complete**: 1-2 hours  
**Difficulty**: ⭐⭐⭐☆☆ (Medium)  
**Prerequisites**: Lesson 01  
**Next Lesson**: `03-first-investigation.md`

---

## Quiz Answers

1. `>` overwrites file, `>>` appends to file
2. Sends output of one command as input to another
3. `grep "search-term" filename`
4. `find . -name "filename"`
5. `tail -n 20 filename`
6. Wildcard - matches any characters
7. `Ctrl + C`
