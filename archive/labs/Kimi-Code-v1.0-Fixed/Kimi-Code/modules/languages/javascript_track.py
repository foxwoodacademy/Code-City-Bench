"""
Kimi-Code: JavaScript Track
Progressive challenges from closures to async architecture.
"""
from typing import List, Dict

JS_CHALLENGES = {
    "basics": [
        {
            "id": "js_basics_001",
            "title": "Closure Fixer",
            "description": "Fix the classic closure-in-loop bug using modern JavaScript.",
            "starter_code": "for (var i = 0; i < 5; i++) {
    setTimeout(() => console.log(i), 100);
}
// Expected: 0, 1, 2, 3, 4
// Actual: 5, 5, 5, 5, 5
",
            "solution": "for (let i = 0; i < 5; i++) {
    setTimeout(() => console.log(i), 100);
}

// Alternative with IIFE:
// for (var i = 0; i < 5; i++) {
//     ((j) => setTimeout(() => console.log(j), 100))(i);
// }
",
            "test_cases": [
                {"input": "Run loop and check console output order", "expected": "0,1,2,3,4"}
            ],
            "hints": [
                "var is function-scoped, let is block-scoped",
                "Each iteration needs its own binding of i",
                "IIFE creates a new scope capturing current value"
            ],
            "concepts": ["closures", "scope", "let_vs_var", "event_loop"],
            "difficulty": 3
        },
        {
            "id": "js_basics_002",
            "title": "Promise Chain Refactor",
            "description": "Convert callback hell to clean async/await with proper error handling.",
            "starter_code": "function getData(callback) {
    setTimeout(() => callback({ id: 1 }), 100);
}
function getMoreData(data, callback) {
    setTimeout(() => callback({ ...data, name: 'Test' }), 100);
}
function getFinalData(data, callback) {
    setTimeout(() => callback({ ...data, status: 'active' }), 100);
}

// Callback hell:
getData(function(a) {
    getMoreData(a, function(b) {
        getMoreData(b, function(c) {
            console.log(c);
        });
    });
});
",
            "solution": "function getData() {
    return new Promise(resolve => setTimeout(() => resolve({ id: 1 }), 100));
}
function getMoreData(data) {
    return new Promise(resolve => setTimeout(() => resolve({ ...data, name: 'Test' }), 100));
}
function getFinalData(data) {
    return new Promise(resolve => setTimeout(() => resolve({ ...data, status: 'active' }), 100));
}

async function fetchUserData() {
    try {
        const a = await getData();
        const b = await getMoreData(a);
        const c = await getFinalData(b);
        return c;
    } catch (error) {
        console.error('Failed to fetch user data:', error);
        throw error;
    }
}

fetchUserData().then(console.log);
",
            "test_cases": [
                {"input": "fetchUserData()", "expected": "{id:1, name:'Test', status:'active'}"}
            ],
            "hints": [
                "Wrap callbacks in Promises for composability",
                "async/await makes asynchronous code read like synchronous",
                "Always use try/catch for error handling in async functions"
            ],
            "concepts": ["promises", "async_await", "error_handling", "refactoring"],
            "difficulty": 3
        },
        {
            "id": "js_basics_003",
            "title": "Array Method Mastery",
            "description": "Implement custom map, filter, and reduce using only for loops.",
            "starter_code": "function customMap(arr, callback) {
    // TODO: Implement without using Array.prototype.map
}

function customFilter(arr, callback) {
    // TODO: Implement without using Array.prototype.filter
}

function customReduce(arr, callback, initialValue) {
    // TODO: Implement without using Array.prototype.reduce
}
",
            "solution": "function customMap(arr, callback) {
    const result = [];
    for (let i = 0; i < arr.length; i++) {
        result.push(callback(arr[i], i, arr));
    }
    return result;
}

function customFilter(arr, callback) {
    const result = [];
    for (let i = 0; i < arr.length; i++) {
        if (callback(arr[i], i, arr)) {
            result.push(arr[i]);
        }
    }
    return result;
}

function customReduce(arr, callback, initialValue) {
    let accumulator = initialValue !== undefined ? initialValue : arr[0];
    const startIndex = initialValue !== undefined ? 0 : 1;
    for (let i = startIndex; i < arr.length; i++) {
        accumulator = callback(accumulator, arr[i], i, arr);
    }
    return accumulator;
}
",
            "test_cases": [
                {"input": "customMap([1,2,3], x => x * 2)", "expected": "[2,4,6]"},
                {"input": "customFilter([1,2,3,4], x => x > 2)", "expected": "[3,4]"},
                {"input": "customReduce([1,2,3,4], (a,b) => a + b, 0)", "expected": "10"}
            ],
            "hints": [
                "Map: create new array, push transformed values",
                "Filter: create new array, conditionally push",
                "Reduce: track accumulator, update with each element"
            ],
            "concepts": ["array_methods", "higher_order_functions", "iteration"],
            "difficulty": 3
        }
    ],
    "dom": [
        {
            "id": "js_dom_001",
            "title": "Event Delegation Pattern",
            "description": "Implement efficient event handling for dynamic lists using delegation.",
            "starter_code": "// Inefficient: attaches listener to each item
const items = document.querySelectorAll('.list-item');
items.forEach(item => {
    item.addEventListener('click', handleClick);
});

// Problem: New items added dynamically won't have listeners
",
            "solution": "// Efficient: Single listener on parent
document.querySelector('.list-container').addEventListener('click', function(e) {
    const item = e.target.closest('.list-item');
    if (!item) return;
    
    if (item.matches('.delete-btn')) {
        handleDelete(item);
    } else if (item.matches('.edit-btn')) {
        handleEdit(item);
    } else {
        handleSelect(item);
    }
});

function handleDelete(item) {
    item.remove();
}

function handleEdit(item) {
    const text = item.querySelector('.text');
    text.contentEditable = true;
    text.focus();
}

function handleSelect(item) {
    document.querySelectorAll('.list-item').forEach(i => i.classList.remove('selected'));
    item.classList.add('selected');
}
",
            "test_cases": [
                {"input": "Click dynamically added item", "expected": "Event handled correctly"},
                {"input": "Click delete button", "expected": "Item removed from DOM"}
            ],
            "hints": [
                "Attach one listener to the parent container",
                "Use event.target.closest() to find the relevant element",
                "Check e.target.matches() for specific sub-elements"
            ],
            "concepts": ["event_delegation", "dom", "memory_management", "dynamic_content"],
            "difficulty": 4
        }
    ],
    "async": [
        {
            "id": "js_async_001",
            "title": "Promise.all with Timeout",
            "description": "Implement a function that races promises against a timeout.",
            "starter_code": "function fetchWithTimeout(url, timeout = 5000) {
    // TODO: Return promise that rejects if timeout exceeded
}

function fetchAllWithTimeout(urls, timeout = 5000) {
    // TODO: Fetch all URLs, fail fast if any timeout
}
",
            "solution": "function fetchWithTimeout(url, timeout = 5000) {
    return Promise.race([
        fetch(url),
        new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Timeout')), timeout)
        )
    ]);
}

async function fetchAllWithTimeout(urls, timeout = 5000) {
    const promises = urls.map(url => fetchWithTimeout(url, timeout));
    return Promise.all(promises);
}

// Usage with error handling
async function loadData(urls) {
    try {
        const responses = await fetchAllWithTimeout(urls, 3000);
        const data = await Promise.all(responses.map(r => r.json()));
        return data;
    } catch (error) {
        console.error('Failed to load data:', error.message);
        throw error;
    }
}
",
            "test_cases": [
                {"input": "fetchWithTimeout('slow-endpoint', 100)", "expected": "Error: Timeout"},
                {"input": "fetchAllWithTimeout(['/api/1', '/api/2'], 5000)", "expected": "[data1, data2]"}
            ],
            "hints": [
                "Promise.race resolves/rejects with the first settled promise",
                "Create a timeout promise that rejects after N ms",
                "Promise.all fails fast - one rejection fails everything"
            ],
            "concepts": ["promises", "timeout", "race", "fetch", "error_handling"],
            "difficulty": 5
        }
    ],
    "node": [
        {
            "id": "js_node_001",
            "title": "Stream Transform Pipeline",
            "description": "Create a transform stream that processes CSV data line by line.",
            "starter_code": "const { Transform } = require('stream');

class CSVParser extends Transform {
    constructor(options = {}) {
        super({ objectMode: true });
        // TODO: Initialize parser state
    }
    
    _transform(chunk, encoding, callback) {
        // TODO: Parse CSV line, emit objects
    }
}
",
            "solution": "const { Transform } = require('stream');

class CSVParser extends Transform {
    constructor(options = {}) {
        super({ objectMode: true });
        this.headers = options.headers || [];
        this.delimiter = options.delimiter || ',';
        this.buffer = '';
        this.lineCount = 0;
    }
    
    _transform(chunk, encoding, callback) {
        this.buffer += chunk.toString();
        const lines = this.buffer.split('\n');
        this.buffer = lines.pop(); // Keep incomplete line
        
        for (const line of lines) {
            if (!line.trim()) continue;
            
            const values = line.split(this.delimiter).map(v => v.trim());
            
            if (this.lineCount === 0 && !this.headers.length) {
                this.headers = values;
            } else {
                const record = {};
                this.headers.forEach((h, i) => {
                    record[h] = values[i] || null;
                });
                this.push(record);
            }
            this.lineCount++;
        }
        callback();
    }
    
    _flush(callback) {
        if (this.buffer.trim()) {
            // Process remaining buffer
            const values = this.buffer.split(this.delimiter);
            const record = {};
            this.headers.forEach((h, i) => {
                record[h] = values[i] || null;
            });
            this.push(record);
        }
        callback();
    }
}

// Usage
const fs = require('fs');
fs.createReadStream('data.csv')
    .pipe(new CSVParser())
    .on('data', record => console.log(record))
    .on('end', () => console.log('Done'));
",
            "test_cases": [
                {"input": "Parse 'name,age\nAlice,30\nBob,25'", "expected": "[{name:'Alice',age:'30'}, {name:'Bob',age:'25'}]"}
            ],
            "hints": [
                "Use buffer to handle partial lines across chunks",
                "First line (or options) defines headers",
                "_flush handles remaining data in buffer"
            ],
            "concepts": ["streams", "transform", "csv_parsing", "node"],
            "difficulty": 6
        }
    ]
}

def get_challenges(track: str, difficulty_range: tuple = None) -> List[Dict]:
    challenges = JS_CHALLENGES.get(track, [])
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges

def get_all_tracks() -> List[str]:
    return list(JS_CHALLENGES.keys())

def get_challenge_by_id(challenge_id: str) -> Dict:
    for track in JS_CHALLENGES.values():
        for challenge in track:
            if challenge["id"] == challenge_id:
                return challenge
    return None
