#!/usr/bin/env node

/**
 * CODE CITY 2.0 - Node.js Backend Server
 * Pure JavaScript implementation for cross-platform compatibility
 */

const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// Server configuration
const HOST = process.env.HOST || '0.0.0.0';
const PORT = process.env.PORT || 8765;

// Create WebSocket server
const wss = new WebSocket.Server({ host: HOST, port: PORT });

console.log(`🚀 Code City 2.0 Server running on ws://${HOST}:${PORT}`);
console.log(`📡 Platform: ${os.platform()} | Node.js ${process.version}`);

// Client connections
const clients = new Set();
let currentCityData = null;

// Supported file extensions
const SUPPORTED_EXTENSIONS = new Set([
    '.py', '.js', '.ts', '.jsx', '.tsx',
    '.java', '.cpp', '.c', '.h', '.hpp',
    '.go', '.rs', '.rb', '.php', '.html', '.css'
]);

// Maximum file size (1MB for mobile compatibility)
const MAX_FILE_SIZE = 1024 * 1024;

// Skip directories
const SKIP_DIRS = new Set(['node_modules', 'venv', '__pycache__', '.git', 'dist', 'build']);

class CodeCityScanner {
    constructor() {
        this.scanner = this;
    }
    
    async scanCodebase(rootPath) {
        return new Promise((resolve, reject) => {
            try {
                const absolutePath = path.resolve(rootPath);
                
                if (!fs.existsSync(absolutePath)) {
                    reject(new Error(`Path does not exist: ${rootPath}`));
                    return;
                }
                
                const buildings = [];
                const monsters = [];
                const startTime = Date.now();
                
                this._walkDirectory(absolutePath, absolutePath, buildings, monsters, (err) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    const scanTime = ((Date.now() - startTime) / 1000).toFixed(2) + 's';
                    
                    resolve({
                        buildings,
                        monsters,
                        total_files: buildings.length,
                        total_errors: monsters.length,
                        root_path: absolutePath,
                        timestamp: new Date().toISOString(),
                        scan_time: scanTime
                    });
                });
                
            } catch (error) {
                reject(error);
            }
        });
    }
    
    _walkDirectory(root, currentDir, buildings, monsters, callback) {
        let filesProcessed = 0;
        let totalFiles = 0;
        
        // Count total files first
        const countFiles = (dir) => {
            try {
                const files = fs.readdirSync(dir);
                files.forEach(file => {
                    const fullPath = path.join(dir, file);
                    const stat = fs.statSync(fullPath);
                    
                    if (stat.isDirectory()) {
                        if (!this._shouldSkipDirectory(fullPath)) {
                            countFiles(fullPath);
                        }
                    } else {
                        if (this._shouldScanFile(fullPath)) {
                            totalFiles++;
                        }
                    }
                });
            } catch (error) {
                console.warn(`Error counting files in ${dir}:`, error.message);
            }
        };
        
        countFiles(currentDir);
        
        // Process files
        const processFiles = (dir) => {
            try {
                const files = fs.readdirSync(dir);
                files.forEach(file => {
                    const fullPath = path.join(dir, file);
                    const stat = fs.statSync(fullPath);
                    
                    if (stat.isDirectory()) {
                        if (!this._shouldSkipDirectory(fullPath)) {
                            processFiles(fullPath);
                        }
                    } else {
                        if (this._shouldScanFile(fullPath)) {
                            try {
                                const building = this._analyzeFile(fullPath, root);
                                if (building) {
                                    buildings.push(building);
                                    
                                    // Find bugs in this file
                                    const bugs = this._findBugs(fullPath, building);
                                    bugs.forEach(bug => {
                                        const monster = this._createMonster(building, bug);
                                        monsters.push(monster);
                                    });
                                }
                            } catch (error) {
                                console.warn(`Error analyzing ${fullPath}:`, error.message);
                            }
                            
                            filesProcessed++;
                            
                            // Send progress updates
                            const progress = Math.round((filesProcessed / totalFiles) * 100);
                            this._broadcastProgress(progress);
                        }
                    }
                });
            } catch (error) {
                console.warn(`Error processing files in ${dir}:`, error.message);
            }
        };
        
        processFiles(currentDir);
        callback(null);
    }
    
    _shouldSkipDirectory(dirPath) {
        const parts = dirPath.split(path.sep);
        return parts.some(part => SKIP_DIRS.has(part));
    }
    
    _shouldScanFile(filePath) {
        try {
            const stat = fs.statSync(filePath);
            
            // Skip if not a file
            if (!stat.isFile()) return false;
            
            // Skip hidden files
            const parts = filePath.split(path.sep);
            if (parts.some(part => part.startsWith('.'))) return false;
            
            // Skip if too large
            if (stat.size > MAX_FILE_SIZE) return false;
            
            // Check extension
            const ext = path.extname(filePath).toLowerCase();
            return SUPPORTED_EXTENSIONS.has(ext);
            
        } catch (error) {
            return false;
        }
    }
    
    _analyzeFile(filePath, root) {
        try {
            const stats = fs.statSync(filePath);
            const content = fs.readFileSync(filePath, 'utf-8');
            const lines = content.split('\n').length;
            const size = stats.size;
            const complexity = this._calculateComplexity(filePath, content);
            
            // Calculate deterministic position based on filename
            const fileHash = this._hashString(filePath);
            const x = (fileHash % 200) - 100;
            const z = ((fileHash >> 8) % 200) - 100;
            
            // Calculate dimensions based on file characteristics
            const height = Math.max(10, Math.min(150, Math.floor(lines / 2)));
            const width = Math.max(8, Math.min(30, Math.floor(size / 500)));
            const depth = Math.max(8, Math.min(30, complexity));
            
            // Color based on file type
            const color = this._getFileColor(filePath);
            
            return {
                id: filePath,
                name: path.basename(filePath),
                path: path.relative(root, filePath),
                full_path: filePath,
                type: path.extname(filePath).substring(1) || 'file',
                size: size,
                lines: lines,
                complexity: complexity,
                health: 100,
                position: { x, y: 0, z },
                dimensions: { width, height, depth },
                color: color
            };
            
        } catch (error) {
            console.warn(`Error analyzing file ${filePath}:`, error.message);
            return null;
        }
    }
    
    _calculateComplexity(filePath, content) {
        let complexity = 1;
        const lines = content.split('\n');
        const ext = path.extname(filePath);
        
        if (ext === '.py') {
            complexity += (content.match(/def /g) || []).length * 2;
            complexity += (content.match(/class /g) || []).length * 3;
            complexity += (content.match(/if /g) || []).length * 1;
            complexity += (content.match(/for /g) || []).length * 1;
            complexity += (content.match(/while /g) || []).length * 1;
        }
        else if (['.js', '.ts', '.jsx', '.tsx'].includes(ext)) {
            complexity += (content.match(/function/g) || []).length * 2;
            complexity += (content.match(/=>/g) || []).length * 1;
            complexity += (content.match(/class /g) || []).length * 3;
            complexity += (content.match(/if /g) || []).length * 1;
            complexity += (content.match(/for /g) || []).length * 1;
        }
        
        // Add base complexity from lines
        complexity += Math.min(20, Math.floor(lines.length / 20));
        
        return Math.max(1, Math.min(50, complexity));
    }
    
    _getFileColor(filePath) {
        const ext = path.extname(filePath);
        const colors = {
            '.py': '#3776ab',      // Python blue
            '.js': '#f7df1e',      // JavaScript yellow
            '.ts': '#3178c6',      // TypeScript blue
            '.jsx': '#61dafb',     // React cyan
            '.tsx': '#61dafb',     // React cyan
            '.java': '#f89820',    // Java orange
            '.cpp': '#00599c',     // C++ blue
            '.c': '#a8b9cc',       // C gray
            '.go': '#00add8',      // Go cyan
            '.rs': '#ce422b',      // Rust red
            '.rb': '#cc342d',      // Ruby red
            '.php': '#777bb3',     // PHP purple
            '.html': '#e34c26',    // HTML orange
            '.css': '#1572b6'      // CSS blue
        };
        return colors[ext] || '#6c757d';
    }
    
    _findBugs(filePath, building) {
        const bugs = [];
        const ext = path.extname(filePath);
        
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            
            if (ext === '.py') {
                bugs.push(...this._checkPythonBugs(filePath, content));
            }
            else if (['.js', '.ts', '.jsx', '.tsx'].includes(ext)) {
                bugs.push(...this._checkJavascriptBugs(filePath, content));
            }
            
        } catch (error) {
            console.warn(`Error checking bugs in ${filePath}:`, error.message);
        }
        
        return bugs;
    }
    
    _checkPythonBugs(filePath, content) {
        const bugs = [];
        const lines = content.split('\n');
        
        // Check syntax
        try {
            // Simple syntax check - this won't catch all errors but helps
            if (content.includes('def ') && !content.includes(':')) {
                bugs.push({
                    type: 'syntax_error',
                    message: 'Missing colon in function definition',
                    line: lines.findIndex(line => line.includes('def ')) + 1,
                    severity: 9
                });
            }
        } catch (error) {
            // Syntax error
            bugs.push({
                type: 'syntax_error',
                message: 'Syntax error in Python code',
                line: 1,
                severity: 9
            });
        }
        
        // Check for common issues
        lines.forEach((line, index) => {
            const lineNumber = index + 1;
            
            // Line too long
            if (line.length > 120) {
                bugs.push({
                    type: 'line_too_long',
                    message: `Line exceeds 120 characters (${line.length} chars)`,
                    line: lineNumber,
                    severity: 3
                });
            }
            
            // Trailing whitespace
            if (line.trim() !== line && line.trim()) {
                bugs.push({
                    type: 'trailing_whitespace',
                    message: 'Trailing whitespace',
                    line: lineNumber,
                    severity: 2
                });
            }
            
            // Simple unused variable detection
            if (line.includes('=') && !line.trim().startsWith('#') && 
                !line.trim().startsWith('def ') && !line.trim().startsWith('class ')) {
                
                const parts = line.split('=');
                if (parts.length > 1) {
                    const varName = parts[0].trim();
                    if (varName && !varName.startsWith('(')) {
                        const remainingContent = parts.slice(1).join('=');
                        if (!remainingContent.includes(varName) && 
                            content.split(varName).length - 1 === 1) {
                            
                            bugs.push({
                                type: 'unused_variable',
                                message: `Variable "${varName}" may be unused`,
                                line: lineNumber,
                                severity: 4
                            });
                        }
                    }
                }
            }
        });
        
        return bugs;
    }
    
    _checkJavascriptBugs(filePath, content) {
        const bugs = [];
        const lines = content.split('\n');
        
        lines.forEach((line, index) => {
            const lineNumber = index + 1;
            
            // console.log left in code
            if (line.includes('console.log') && !line.split('console.log')[0].includes('//')) {
                bugs.push({
                    type: 'console_log',
                    message: 'console.log() left in code',
                    line: lineNumber,
                    severity: 4
                });
            }
            
            // Loose equality
            if (line.includes('==') && !line.includes('===') && !line.includes('!=')) {
                bugs.push({
                    type: 'loose_equality',
                    message: 'Use === instead of ==',
                    line: lineNumber,
                    severity: 5
                });
            }
        });
        
        return bugs;
    }
    
    _createMonster(building, bug) {
        // Position near the building
        const offsetX = (this._hashString(bug.type) % 20) - 10;
        const offsetZ = (this._hashString(bug.message) % 20) - 10;
        
        return {
            id: `${building.id}_L${bug.line}_${bug.type}`,
            type: bug.type,
            building_id: building.id,
            file_path: building.full_path,
            file_name: building.name,
            position: {
                x: building.position.x + offsetX,
                y: bug.line * 0.5,
                z: building.position.z + offsetZ
            },
            severity: bug.severity,
            message: bug.message,
            line: bug.line,
            health: bug.severity * 10,
            color: this._getMonsterColor(bug.type)
        };
    }
    
    _getMonsterColor(bugType) {
        const colors = {
            'syntax_error': '#ff0000',
            'line_too_long': '#4444ff',
            'trailing_whitespace': '#888888',
            'unused_variable': '#ff8800',
            'console_log': '#ffcc00',
            'loose_equality': '#aa00ff',
            'missing_semicolon': '#ff4444'
        };
        return colors[bugType] || '#ff4444';
    }
    
    _hashString(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        return Math.abs(hash);
    }
    
    _broadcastProgress(progress) {
        const message = JSON.stringify({
            type: 'scan_progress',
            progress: progress
        });
        
        clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(message);
            }
        });
    }
    
    getFileContent(filePath, lineNumber = 1) {
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            const lines = content.split('\n');
            
            // Get context around the error line
            const start = Math.max(0, lineNumber - 5);
            const end = Math.min(lines.length, lineNumber + 5);
            
            return {
                file_path: filePath,
                line_number: lineNumber,
                lines: lines.slice(start, end),
                start_line: start + 1,
                end_line: end + 1
            };
            
        } catch (error) {
            throw new Error(`Failed to read file: ${error.message}`);
        }
    }
}

const scanner = new CodeCityScanner();

// WebSocket server event handlers
wss.on('connection', (ws) => {
    console.log('✅ New client connected');
    clients.add(ws);
    
    // Send welcome message
    ws.send(JSON.stringify({
        type: 'connected',
        message: 'Welcome to Code City 2.0!',
        timestamp: new Date().toISOString()
    }));
    
    ws.on('message', async (message) => {
        try {
            const data = JSON.parse(message);
            const action = data.action;
            
            console.log(`📨 Received action: ${action}`);
            
            switch (action) {
                case 'scan':
                    await handleScan(ws, data);
                    break;
                    
                case 'get_file_content':
                    await handleGetFileContent(ws, data);
                    break;
                    
                case 'health':
                    handleHealth(ws);
                    break;
                    
                default:
                    ws.send(JSON.stringify({
                        type: 'error',
                        message: `Unknown action: ${action}`
                    }));
            }
            
        } catch (error) {
            console.error('Error handling message:', error);
            ws.send(JSON.stringify({
                type: 'error',
                message: `Error: ${error.message}`
            }));
        }
    });
    
    ws.on('close', () => {
        console.log('🔴 Client disconnected');
        clients.delete(ws);
    });
    
    ws.on('error', (error) => {
        console.error('WebSocket error:', error);
        clients.delete(ws);
    });
});

async function handleScan(ws, data) {
    const folderPath = data.path || process.cwd();
    
    try {
        console.log(`🔍 Scanning codebase at: ${folderPath}`);
        
        // Send scanning status
        ws.send(JSON.stringify({
            type: 'scanning',
            message: 'Scanning codebase...',
            path: folderPath
        }));
        
        // Perform scan
        const cityData = await scanner.scanCodebase(folderPath);
        currentCityData = cityData;
        
        console.log(`✅ Scan complete: ${cityData.buildings.length} files, ${cityData.monsters.length} bugs`);
        
        // Send city data
        ws.send(JSON.stringify({
            type: 'city_data',
            data: cityData,
            timestamp: new Date().toISOString()
        }));
        
    } catch (error) {
        console.error('Scan error:', error);
        ws.send(JSON.stringify({
            type: 'error',
            message: `Scan failed: ${error.message}`
        }));
    }
}

async function handleGetFileContent(ws, data) {
    const filePath = data.file_path;
    const lineNumber = data.line_number || 1;
    
    try {
        const content = scanner.getFileContent(filePath, lineNumber);
        
        ws.send(JSON.stringify({
            type: 'file_content',
            data: content
        }));
        
    } catch (error) {
        ws.send(JSON.stringify({
            type: 'error',
            message: `Failed to read file: ${error.message}`
        }));
    }
}

function handleHealth(ws) {
    ws.send(JSON.stringify({
        type: 'health',
        status: 'healthy',
        timestamp: new Date().toISOString(),
        clients: clients.size,
        platform: os.platform(),
        node_version: process.version
    }));
}

// Handle process termination
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down Code City server...');
    wss.close();
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Shutting down Code City server...');
    wss.close();
    process.exit(0);
});

console.log('🏙️ Code City 2.0 Server ready!');
console.log('💡 Connect your frontend to ws://localhost:8765');