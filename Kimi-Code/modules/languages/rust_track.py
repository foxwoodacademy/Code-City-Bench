"""
Kimi-Code: Rust Track
Progressive challenges from ownership to unsafe code and macros.
"""
from typing import List, Dict

RUST_CHALLENGES = {
    "basics": [
        {
            "id": "rust_basics_001",
            "title": "Ownership Transfer Fix",
            "description": "Fix ownership issues in this string manipulation code.",
            "starter_code": "fn process(s: String) -> String {
    let t = s;
    s.push_str(" world");
    t
}
",
            "solution": "fn process(mut s: String) -> String {
    s.push_str(" world");
    s
}

// Or if you need both:
fn process_both(s: String) -> (String, String) {
    let t = s.clone();
    (s, t)
}
",
            "test_cases": [
                {"input": "process(String::from("hello"))", "expected": ""hello world""}
            ],
            "hints": [
                "In Rust, ownership moves by default",
                "Use clone() if you need multiple owners",
                "Or take ownership, modify, and return"
            ],
            "concepts": ["ownership", "move_semantics", "borrowing"],
            "difficulty": 3
        },
        {
            "id": "rust_basics_002",
            "title": "Lifetime Annotations",
            "description": "Add proper lifetime annotations to this function that returns the longer string.",
            "starter_code": "fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
",
            "solution": "fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// Alternative with explicit lifetimes:
fn longest_explicit<'a, 'b>(x: &'a str, y: &'b str) -> String {
    if x.len() > y.len() {
        x.to_string()
    } else {
        y.to_string()
    }
}
",
            "test_cases": [
                {"input": "longest("hello", "world!")", "expected": ""world!""},
                {"input": "longest("longer", "short")", "expected": ""longer""}
            ],
            "hints": [
                "The returned reference must live as long as both inputs",
                "Use 'a to indicate all references share the same lifetime",
                "If lifetimes differ, consider returning an owned String"
            ],
            "concepts": ["lifetimes", "borrowing", "references"],
            "difficulty": 4
        },
        {
            "id": "rust_basics_003",
            "title": "Result and Option Chaining",
            "description": "Refactor nested match statements using ? operator and combinators.",
            "starter_code": "fn read_config(path: &str) -> Result<String, Box<dyn std::error::Error>> {
    let content = std::fs::read_to_string(path);
    match content {
        Ok(text) => {
            match text.lines().next() {
                Some(first) => Ok(first.to_string()),
                None => Err("Empty file".into())
            }
        }
        Err(e) => Err(e.into())
    }
}
",
            "solution": "use std::io;

fn read_config(path: &str) -> Result<String, Box<dyn std::error::Error>> {
    let text = std::fs::read_to_string(path)?;
    let first = text.lines().next().ok_or("Empty file")?;
    Ok(first.to_string())
}

// Even more idiomatic with custom error:
#[derive(Debug)]
enum ConfigError {
    Io(io::Error),
    EmptyFile,
}

impl From<io::Error> for ConfigError {
    fn from(e: io::Error) -> Self {
        ConfigError::Io(e)
    }
}

fn read_config_clean(path: &str) -> Result<String, ConfigError> {
    let text = std::fs::read_to_string(path)?;
    text.lines().next()
        .map(|s| s.to_string())
        .ok_or(ConfigError::EmptyFile)
}
",
            "test_cases": [
                {"input": "read_config("test.txt") with 'hello\nworld'", "expected": "Ok("hello")"},
                {"input": "read_config("empty.txt")", "expected": "Err(EmptyFile)"}
            ],
            "hints": [
                "? operator unwraps Ok or returns Err early",
                "ok_or converts Option to Result with custom error",
                "map transforms Some value without unwrapping"
            ],
            "concepts": ["error_handling", "result", "option", "question_mark"],
            "difficulty": 4
        }
    ],
    "ownership": [
        {
            "id": "rust_own_001",
            "title": "Smart Pointer Implementation",
            "description": "Implement a simple Rc-like reference counted smart pointer.",
            "starter_code": "use std::ptr::NonNull;

struct MyRc<T> {
    // TODO: Implement reference counting
}

impl<T> MyRc<T> {
    fn new(value: T) -> Self {
        // TODO
    }
}
",
            "solution": "use std::ptr::NonNull;
use std::alloc::{alloc, dealloc, Layout};

struct RcBox<T> {
    ref_count: usize,
    value: T,
}

struct MyRc<T> {
    ptr: NonNull<RcBox<T>>,
}

impl<T> MyRc<T> {
    fn new(value: T) -> Self {
        let box_layout = Layout::new::<RcBox<T>>();
        let ptr = unsafe { alloc(box_layout) as *mut RcBox<T> };
        if ptr.is_null() {
            panic!("Allocation failed");
        }
        unsafe {
            (*ptr).ref_count = 1;
            (*ptr).value = value;
        }
        MyRc {
            ptr: unsafe { NonNull::new_unchecked(ptr) },
        }
    }
    
    fn clone(&self) -> Self {
        unsafe {
            (*self.ptr.as_ptr()).ref_count += 1;
        }
        MyRc { ptr: self.ptr }
    }
    
    fn count(&self) -> usize {
        unsafe { (*self.ptr.as_ptr()).ref_count }
    }
}

impl<T> std::ops::Deref for MyRc<T> {
    type Target = T;
    fn deref(&self) -> &T {
        unsafe { &(*self.ptr.as_ptr()).value }
    }
}

impl<T> Drop for MyRc<T> {
    fn drop(&mut self) {
        unsafe {
            let ref_count = &mut (*self.ptr.as_ptr()).ref_count;
            *ref_count -= 1;
            if *ref_count == 0 {
                let layout = Layout::new::<RcBox<T>>();
                dealloc(self.ptr.as_ptr() as *mut u8, layout);
            }
        }
    }
}
",
            "test_cases": [
                {"input": "let rc = MyRc::new(42); *rc", "expected": "42"},
                {"input": "let rc2 = rc.clone(); rc2.count()", "expected": "2"}
            ],
            "hints": [
                "Use NonNull for owning raw pointers",
                "Increment count on clone, decrement on drop",
                "Deallocate only when count reaches 0"
            ],
            "concepts": ["smart_pointers", "reference_counting", "unsafe", "drop_trait"],
            "difficulty": 7
        }
    ],
    "concurrency": [
        {
            "id": "rust_conc_001",
            "title": "Thread-Safe Counter",
            "description": "Implement a thread-safe counter using Arc and Mutex.",
            "starter_code": "use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = 0;
    let mut handles = vec![];
    
    for _ in 0..10 {
        let handle = thread::spawn(move || {
            counter += 1;
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("Result: {}", counter);
}
",
            "solution": "use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];
    
    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("Result: {}", *counter.lock().unwrap());
}

// Alternative with RwLock for read-heavy workloads:
use std::sync::RwLock;

fn read_heavy_counter() {
    let counter = Arc::new(RwLock::new(0));
    
    // Many readers
    let readers: Vec<_> = (0..100)
        .map(|_| {
            let counter = Arc::clone(&counter);
            thread::spawn(move || {
                let _ = counter.read().unwrap();
            })
        })
        .collect();
    
    // Few writers
    let writers: Vec<_> = (0..5)
        .map(|_| {
            let counter = Arc::clone(&counter);
            thread::spawn(move || {
                let mut num = counter.write().unwrap();
                *num += 1;
            })
        })
        .collect();
}
",
            "test_cases": [
                {"input": "Run with 10 threads, each incrementing 1000 times", "expected": "Result: 10000"}
            ],
            "hints": [
                "Arc enables shared ownership across threads",
                "Mutex provides exclusive access to data",
                "Always clone Arc, not the Mutex itself"
            ],
            "concepts": ["concurrency", "arc", "mutex", "threading"],
            "difficulty": 5
        }
    ]
}

def get_challenges(track: str, difficulty_range: tuple = None) -> List[Dict]:
    challenges = RUST_CHALLENGES.get(track, [])
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges

def get_all_tracks() -> List[str]:
    return list(RUST_CHALLENGES.keys())

def get_challenge_by_id(challenge_id: str) -> Dict:
    for track in RUST_CHALLENGES.values():
        for challenge in track:
            if challenge["id"] == challenge_id:
                return challenge
    return None
