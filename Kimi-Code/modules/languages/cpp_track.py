"""
Kimi-Code: C++ Track
Progressive challenges from memory management to embedded systems.
"""
from typing import List, Dict

CPP_CHALLENGES = {
    "basics": [
        {
            "id": "cpp_basics_001",
            "title": "Smart Pointer Implementation",
            "description": "Implement a basic unique_ptr with move semantics.",
            "starter_code": "template<typename T>
class UniquePtr {
    T* ptr;
public:
    // TODO: Implement constructor, destructor, move semantics
    // Disable copy
};
",
            "solution": "template<typename T>
class UniquePtr {
    T* ptr;

public:
    explicit UniquePtr(T* p = nullptr) : ptr(p) {}
    
    ~UniquePtr() {
        delete ptr;
    }
    
    // Move constructor
    UniquePtr(UniquePtr&& other) noexcept : ptr(other.ptr) {
        other.ptr = nullptr;
    }
    
    // Move assignment
    UniquePtr& operator=(UniquePtr&& other) noexcept {
        if (this != &other) {
            delete ptr;
            ptr = other.ptr;
            other.ptr = nullptr;
        }
        return *this;
    }
    
    // Disable copy
    UniquePtr(const UniquePtr&) = delete;
    UniquePtr& operator=(const UniquePtr&) = delete;
    
    T* get() const { return ptr; }
    T& operator*() const { return *ptr; }
    T* operator->() const { return ptr; }
    
    explicit operator bool() const { return ptr != nullptr; }
    
    T* release() {
        T* tmp = ptr;
        ptr = nullptr;
        return tmp;
    }
    
    void reset(T* p = nullptr) {
        T* old = ptr;
        ptr = p;
        delete old;
    }
};
",
            "test_cases": [
                {"input": "UniquePtr<int> p(new int(42)); *p", "expected": "42"},
                {"input": "UniquePtr<int> p2 = std::move(p); p.get()", "expected": "nullptr"}
            ],
            "hints": [
                "Rule of 5: destructor, copy ctor, copy assign, move ctor, move assign",
                "Delete copy operations to enforce unique ownership",
                "Move operations should null out the source pointer"
            ],
            "concepts": ["smart_pointers", "move_semantics", "raii", "rule_of_five"],
            "difficulty": 5
        },
        {
            "id": "cpp_basics_002",
            "title": "Template Metaprogramming - Factorial",
            "description": "Compute factorial at compile time using template metaprogramming.",
            "starter_code": "// TODO: Implement compile-time factorial
// factorial<5>::value should equal 120

template<int N>
struct factorial {
    // TODO
};
",
            "solution": "// Compile-time factorial using template specialization
template<int N>
struct factorial {
    static constexpr int value = N * factorial<N - 1>::value;
};

template<>
struct factorial<0> {
    static constexpr int value = 1;
};

// C++14/17 constexpr function (preferred modern approach):
constexpr int factorial_func(int n) {
    return n <= 1 ? 1 : n * factorial_func(n - 1);
}

// C++20 consteval (guaranteed compile-time):
consteval int factorial_consteval(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

// Usage:
// static_assert(factorial<5>::value == 120);
// constexpr auto val = factorial_func(5);
",
            "test_cases": [
                {"input": "factorial<5>::value", "expected": "120"},
                {"input": "factorial<0>::value", "expected": "1"}
            ],
            "hints": [
                "Use template specialization for base case",
                "static constexpr ensures compile-time evaluation",
                "Modern C++ prefers constexpr functions over TMP"
            ],
            "concepts": ["templates", "metaprogramming", "constexpr", "specialization"],
            "difficulty": 6
        }
    ],
    "memory": [
        {
            "id": "cpp_mem_001",
            "title": "Custom Allocator",
            "description": "Implement a pool allocator for fixed-size objects.",
            "starter_code": "template<size_t BlockSize, size_t NumBlocks>
class PoolAllocator {
    // TODO: Implement pool allocator
    // Pre-allocate NumBlocks * BlockSize bytes
    // Hand out blocks on allocate(), return to free list on deallocate()
};
",
            "solution": "#include <cstddef>
#include <cstdlib>
#include <new>

template<size_t BlockSize, size_t NumBlocks>
class PoolAllocator {
    union Block {
        char data[BlockSize];
        Block* next;
    };
    
    Block* pool;
    Block* free_list;
    
public:
    PoolAllocator() {
        pool = static_cast<Block*>(std::malloc(sizeof(Block) * NumBlocks));
        if (!pool) throw std::bad_alloc();
        
        // Initialize free list
        for (size_t i = 0; i < NumBlocks - 1; ++i) {
            pool[i].next = &pool[i + 1];
        }
        pool[NumBlocks - 1].next = nullptr;
        free_list = &pool[0];
    }
    
    ~PoolAllocator() {
        std::free(pool);
    }
    
    void* allocate() {
        if (!free_list) throw std::bad_alloc();
        
        Block* block = free_list;
        free_list = free_list->next;
        return block;
    }
    
    void deallocate(void* ptr) {
        if (!ptr) return;
        
        Block* block = static_cast<Block*>(ptr);
        block->next = free_list;
        free_list = block;
    }
    
    // Disable copy/move
    PoolAllocator(const PoolAllocator&) = delete;
    PoolAllocator& operator=(const PoolAllocator&) = delete;
};
",
            "test_cases": [
                {"input": "PoolAllocator<64, 100> alloc; auto p = alloc.allocate()", "expected": "Valid pointer"},
                {"input": "alloc.deallocate(p); auto p2 = alloc.allocate()", "expected": "Same address reused"}
            ],
            "hints": [
                "Use union to overlay data and next pointer",
                "Maintain a singly-linked free list",
                "Pre-allocate all memory in constructor"
            ],
            "concepts": ["allocator", "memory_pool", "union", "free_list"],
            "difficulty": 7
        }
    ],
    "multithreading": [
        {
            "id": "cpp_mt_001",
            "title": "Lock-Free Stack",
            "description": "Implement a lock-free stack using atomic compare-and-swap.",
            "starter_code": "#include <atomic>

template<typename T>
class LockFreeStack {
    struct Node {
        T data;
        Node* next;
    };
    
    std::atomic<Node*> head;
    
public:
    // TODO: Implement push and pop using CAS
};
",
            "solution": "#include <atomic>

template<typename T>
class LockFreeStack {
    struct Node {
        T data;
        Node* next;
    };
    
    std::atomic<Node*> head;
    
public:
    void push(const T& value) {
        Node* new_node = new Node{value, nullptr};
        new_node->next = head.load(std::memory_order_relaxed);
        
        while (!head.compare_exchange_weak(
            new_node->next,
            new_node,
            std::memory_order_release,
            std::memory_order_relaxed))
        {
            // CAS failed, new_node->next updated with current head
            // Retry with updated next pointer
        }
    }
    
    bool pop(T& result) {
        Node* old_head = head.load(std::memory_order_acquire);
        
        while (old_head != nullptr) {
            if (head.compare_exchange_weak(
                old_head,
                old_head->next,
                std::memory_order_release,
                std::memory_order_relaxed))
            {
                result = old_head->data;
                delete old_head;
                return true;
            }
            // CAS failed, old_head updated with current head
            // Retry
        }
        return false;
    }
    
    ~LockFreeStack() {
        T dummy;
        while (pop(dummy)) {}
    }
};
",
            "test_cases": [
                {"input": "Push 1000 items from 10 threads, pop all", "expected": "All items accounted for, no crashes"}
            ],
            "hints": [
                "Use compare_exchange_weak for CAS loop (spurious failures OK)",
                "Memory ordering: release on write, acquire on read",
                "ABA problem: consider hazard pointers for production"
            ],
            "concepts": ["lock_free", "atomic", "cas", "memory_ordering"],
            "difficulty": 9
        }
    ]
}

def get_challenges(track: str, difficulty_range: tuple = None) -> List[Dict]:
    challenges = CPP_CHALLENGES.get(track, [])
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges

def get_all_tracks() -> List[str]:
    return list(CPP_CHALLENGES.keys())

def get_challenge_by_id(challenge_id: str) -> Dict:
    for track in CPP_CHALLENGES.values():
        for challenge in track:
            if challenge["id"] == challenge_id:
                return challenge
    return None
