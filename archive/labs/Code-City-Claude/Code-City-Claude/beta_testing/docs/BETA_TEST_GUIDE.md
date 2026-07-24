# 🏙️ Code City 2.0 - Beta Testing Guide

**Version**: 2.0.0-beta.1  
**Date**: 2024-07-20  
**Status**: Active Beta Testing

## 🎯 Beta Testing Overview

Welcome to the Code City 2.0 Beta Testing Program! This guide will help you understand the testing process, provide feedback, and report issues.

## 📋 Testing Objectives

### Primary Goals
1. **Functionality Testing**: Verify all features work as intended
2. **Cross-platform Compatibility**: Test on Android, Windows, and Web
3. **Performance Testing**: Evaluate scanning speed and memory usage
4. **User Experience**: Assess UI/UX improvements
5. **Bug Detection**: Validate code analysis accuracy

### Secondary Goals
1. **Mobile Responsiveness**: Test on various screen sizes
2. **Network Conditions**: Test with different connection speeds
3. **Large Codebases**: Test with projects > 1000 files
4. **Edge Cases**: Test unusual file structures and content

## 🚀 Getting Started

### Prerequisites
- **Node.js** v14+ (for backend)
- **Modern Browser** (Chrome, Firefox, Edge, Safari)
- **Codebase to Test** (your own projects or sample projects)
- **Terminal/Command Prompt** access

### Installation

#### Option 1: Quick Setup (Recommended)
```bash
# Navigate to beta testing directory
cd /storage/ED7B-AD5A/root_2026/beta_testing

# Install backend dependencies
cd backend
npm install

# Start the server
npm start

# Open frontend in browser
# Open frontend/index.html in your preferred browser
```

#### Option 2: Manual Setup
```bash
# Install Node.js dependencies globally
npm install -g ws

# Start server manually
node backend/server.js

# Open the HTML file in browser
```

## 🧪 Test Cases

### Test Case 1: Basic Functionality
**Objective**: Verify core functionality works

**Steps**:
1. Start the backend server
2. Open the frontend in browser
3. Connect to the WebSocket server
4. Scan a small codebase (< 50 files)
5. Verify buildings appear in dashboard

**Expected Results**:
- ✅ Server starts without errors
- ✅ WebSocket connection established
- ✅ Scan completes successfully
- ✅ Buildings displayed with correct metadata
- ✅ No console errors

**Pass/Fail**: [ ] Pass [ ] Fail
**Notes**: _______________________________

### Test Case 2: Large Codebase
**Objective**: Test performance with larger projects

**Steps**:
1. Select a large codebase (> 500 files)
2. Start scanning with "Deep" depth
3. Monitor progress bar
4. Observe memory usage
5. Check final results

**Expected Results**:
- ✅ Progress updates regularly
- ✅ Scan completes within reasonable time
- ✅ Memory usage stays stable
- ✅ All files processed correctly
- ✅ No crashes or timeouts

**Pass/Fail**: [ ] Pass [ ] Fail
**Notes**: _______________________________

### Test Case 3: Bug Detection
**Objective**: Validate bug detection accuracy

**Steps**:
1. Create test files with known issues:
   - Python: syntax errors, long lines, unused variables
   - JavaScript: console.log, loose equality
2. Scan the test directory
3. Verify bugs are detected
4. Check bug severity levels

**Expected Results**:
- ✅ Syntax errors detected
- ✅ Style issues flagged
- ✅ Appropriate severity levels
- ✅ Correct line numbers reported
- ✅ No false positives

**Pass/Fail**: [ ] Pass [ ] Fail
**Notes**: _______________________________

### Test Case 4: Cross-platform Testing
**Objective**: Test on different platforms

**Steps**:
1. Test on Android (Termux)
2. Test on Windows
3. Test on Linux
4. Test on Web browsers
5. Compare results

**Expected Results**:
- ✅ Works on all platforms
- ✅ Consistent behavior
- ✅ Platform-specific optimizations work
- ✅ No platform-specific bugs
- ✅ Responsive design adapts

**Pass/Fail**: [ ] Pass [ ] Fail
**Notes**: _______________________________

### Test Case 5: Mobile Responsiveness
**Objective**: Test mobile compatibility

**Steps**:
1. Open on smartphone browser
2. Test portrait and landscape modes
3. Try different screen sizes
4. Test touch interactions
5. Check performance

**Expected Results**:
- ✅ Layout adapts to screen size
- ✅ Touch targets are large enough
- ✅ No horizontal scrolling needed
- ✅ Performance acceptable
- ✅ All features accessible

**Pass/Fail**: [ ] Pass [ ] Fail
**Notes**: _______________________________

## 📝 Feedback Form

### General Feedback

**Overall Experience (1-5)**: ⭐️⭐️⭐️⭐️⭐️

**What did you like most?**
_______________________________

**What needs improvement?**
_______________________________

**Any unexpected behaviors?**
_______________________________

### Feature-specific Feedback

**Dashboard**:
- [ ] Easy to understand
- [ ] Visually appealing
- [ ] Useful statistics
- [ ] Needs improvement: ___________

**Scanner**:
- [ ] Fast scanning
- [ ] Clear progress updates
- [ ] Good configuration options
- [ ] Needs improvement: ___________

**Search**:
- [ ] Quick results
- [ ] Relevant matches
- [ ] Easy navigation
- [ ] Needs improvement: ___________

**File Preview**:
- [ ] Helpful for debugging
- [ ] Good code highlighting
- [ ] Easy to read
- [ ] Needs improvement: ___________

## 🐛 Bug Report Template

**Bug Title**: _______________________________

**Description**:
_______________________________

**Steps to Reproduce**:
1. _______________________________
2. _______________________________
3. _______________________________

**Expected Behavior**:
_______________________________

**Actual Behavior**:
_______________________________

**Severity**: [ ] Critical [ ] High [ ] Medium [ ] Low

**Platform**: [ ] Android [ ] Windows [ ] Linux [ ] Web

**Browser/OS Version**: _______________________________

**Additional Notes**:
_______________________________

## 📊 Performance Metrics

### Scan Performance

| Codebase Size | Files | Time | Memory Usage |
|---------------|-------|------|--------------|
| Small (<50)   |       |      |              |
| Medium (50-500)|     |      |              |
| Large (>500)  |       |      |              |

### UI Performance

| Action | Time | Smoothness (1-5) |
|--------|------|------------------|
| Tab Switching | | |
| Building Click | | |
| Search | | |
| File Preview | | |

## 🎨 Design Feedback

**Visual Design (1-5)**: ⭐️⭐️⭐️⭐️⭐️

**Color Scheme**:
- [ ] Appealing
- [ ] Professional
- [ ] Easy to read
- [ ] Needs adjustment: ___________

**Animations**:
- [ ] Smooth
- [ ] Appropriate speed
- [ ] Enhance experience
- [ ] Distracting/needs adjustment

**Layout**:
- [ ] Well organized
- [ ] Intuitive navigation
- [ ] Good use of space
- [ ] Needs improvement: ___________

## 🔧 Technical Feedback

**Backend Performance**:
- [ ] Fast response times
- [ ] Stable connection
- [ ] Good error handling
- [ ] Needs optimization: ___________

**Frontend Performance**:
- [ ] Quick rendering
- [ ] Smooth interactions
- [ ] Minimal lag
- [ ] Needs optimization: ___________

**Code Quality**:
- [ ] Well structured
- [ ] Easy to understand
- [ ] Good comments
- [ ] Needs refactoring: ___________

## 📅 Testing Schedule

### Week 1: Core Functionality
- [ ] Basic setup and installation
- [ ] Dashboard functionality
- [ ] Scanner performance
- [ ] Bug detection accuracy

### Week 2: Advanced Features
- [ ] Search functionality
- [ ] File preview
- [ ] Settings persistence
- [ ] Error handling

### Week 3: Cross-platform Testing
- [ ] Android (Termux)
- [ ] Windows
- [ ] Linux
- [ ] Web browsers

### Week 4: Performance & Stress Testing
- [ ] Large codebases
- [ ] Memory usage
- [ ] Long-running sessions
- [ ] Concurrent users

## 📬 Submission Instructions

1. **Save Feedback**: Save this file with your responses
2. **Create Issue**: For bugs, create GitHub issues
3. **Submit Form**: Email completed form to beta@codecity.ai
4. **Include Logs**: Attach any relevant log files
5. **Screenshots**: Include visual evidence for UI issues

## 🙏 Thank You!

Your participation in this beta testing program is invaluable. Your feedback will directly shape the final release of Code City 2.0 and help us create the best possible experience for developers worldwide.

**Beta Testing Team**
Code City Development

---

*Confidential: This document and its contents are for beta testing purposes only.*