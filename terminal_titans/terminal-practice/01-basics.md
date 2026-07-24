# Terminal Practice: The Basics

## Exercise 1: Navigation

**Goal**: Learn to move around your file system

```bash
# 1. Where are you right now?
pwd

# 2. What's in this folder?
ls

# 3. Create a test folder
mkdir my-test-folder

# 4. Go into it
cd my-test-folder

# 5. Confirm you're there
pwd

# 6. Go back up
cd ..

# 7. Delete the test folder
rmdir my-test-folder
```

**Expected Result**: You should be back where you started

## Exercise 2: Creating Files

**Goal**: Learn to create and edit files

```bash
# 1. Create a file with text
echo "This is my first file" > test.txt

# 2. Read the file
cat test.txt

# 3. Add more text
echo "This is line 2" >> test.txt

# 4. Read it again
cat test.txt

# 5. Create multiple files at once
touch file1.txt file2.txt file3.txt

# 6. List all files
ls

# 7. Clean up
rm test.txt file1.txt file2.txt file3.txt
```

## Exercise 3: Searching

**Goal**: Find specific text in files

```bash
# 1. Create a file with multiple lines
cat > evidence.txt << EOF
Line 1: Normal activity
Line 2: Suspicious transaction detected
Line 3: Normal activity
Line 4: Another suspicious transaction
Line 5: Normal activity
EOF

# 2. Search for "suspicious"
grep "suspicious" evidence.txt

# 3. Search case-insensitive
grep -i "SUSPICIOUS" evidence.txt

# 4. Count matches
grep -c "suspicious" evidence.txt

# 5. Show line numbers
grep -n "suspicious" evidence.txt
```

**Challenge**: Can you find all lines that DON'T contain "Normal"?
<details>
<summary>Click for answer</summary>

```bash
grep -v "Normal" evidence.txt
```
</details>

## Exercise 4: Pipes and Redirection

**Goal**: Combine commands for powerful results

```bash
# 1. Create sample data
cat > addresses.txt << EOF
0xABC123
0xDEF456
0xABC123
0xGHI789
0xDEF456
EOF

# 2. Sort the addresses
sort addresses.txt

# 3. Remove duplicates
sort addresses.txt | uniq

# 4. Count unique addresses
sort addresses.txt | uniq | wc -l

# 5. Save results to new file
sort addresses.txt | uniq > unique-addresses.txt

# 6. Verify
cat unique-addresses.txt
```

## Exercise 5: Real-World Scenario

**Scenario**: You have a log file with mixed data. Extract useful information.

```bash
# 1. Create mock log file
cat > investigation-log.txt << EOF
2024-01-01 10:00:00 User logged in from 192.168.1.1
2024-01-01 10:05:00 Transaction: 0xABC123 sent 1.5 ETH
2024-01-01 10:10:00 ALERT: Suspicious activity detected
2024-01-01 10:15:00 Transaction: 0xDEF456 sent 0.5 ETH
2024-01-01 10:20:00 User logged out
2024-01-01 10:25:00 ALERT: Multiple failed login attempts
EOF

# 2. Extract all alerts
grep "ALERT" investigation-log.txt

# 3. Extract all transactions
grep "Transaction" investigation-log.txt

# 4. Extract all wallet addresses
grep -o "0x[A-Z0-9]*" investigation-log.txt

# 5. Create summary report
echo "=== Investigation Summary ===" > summary.txt
echo "" >> summary.txt
echo "Alerts:" >> summary.txt
grep "ALERT" investigation-log.txt >> summary.txt
echo "" >> summary.txt
echo "Transactions:" >> summary.txt
grep "Transaction" investigation-log.txt >> summary.txt

# 6. View your report
cat summary.txt
```

**Congratulations!** You just processed evidence like a real investigator!

## Self-Check Quiz

1. What command shows your current directory?
2. How do you create a new folder?
3. What's the difference between `>` and `>>`?
4. How do you search for text in a file?
5. What does the pipe `|` do?

<details>
<summary>Click for answers</summary>

1. `pwd`
2. `mkdir folder-name`
3. `>` overwrites, `>>` appends
4. `grep "search-term" filename`
5. Sends output of one command as input to another
</details>

## Next Steps

✅ Completed basic terminal exercises  
➡️ Move to `02-advanced.md` for more challenges  
➡️ Or try `../crypto-practice/` to learn about cryptocurrency

---

**Time**: 30 minutes  
**Difficulty**: ⭐⭐☆☆☆
