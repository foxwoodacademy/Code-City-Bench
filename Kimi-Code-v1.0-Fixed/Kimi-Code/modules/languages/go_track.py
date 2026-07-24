"""
Kimi-Code: Go Track
Progressive challenges from goroutines to distributed systems.
"""
from typing import List, Dict

GO_CHALLENGES = {
    "basics": [
        {
            "id": "go_basics_001",
            "title": "Goroutine Race Condition Fix",
            "description": "Fix the race condition in this concurrent counter.",
            "starter_code": "package main

import (
    "fmt"
    "time"
)

var counter int

func increment() {
    for i := 0; i < 1000; i++ {
        counter++
    }
}

func main() {
    go increment()
    go increment()
    time.Sleep(time.Second)
    fmt.Println(counter)
}
",
            "solution": "package main

import (
    "fmt"
    "sync"
    "time"
)

type SafeCounter struct {
    mu      sync.Mutex
    counter int
}

func (c *SafeCounter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.counter++
}

func (c *SafeCounter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.counter
}

func main() {
    c := &SafeCounter{}
    
    var wg sync.WaitGroup
    for i := 0; i < 2; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for j := 0; j < 1000; j++ {
                c.Increment()
            }
        }()
    }
    
    wg.Wait()
    fmt.Println(c.Value())
}

// Alternative with sync/atomic:
// var counter int64
// atomic.AddInt64(&counter, 1)
",
            "test_cases": [
                {"input": "Run with 2 goroutines, 1000 increments each", "expected": "2000"}
            ],
            "hints": [
                "Use sync.Mutex for mutual exclusion",
                "Always defer Unlock after Lock",
                "sync.WaitGroup waits for goroutines to finish"
            ],
            "concepts": ["goroutines", "mutex", "race_conditions", "sync"],
            "difficulty": 4
        },
        {
            "id": "go_basics_002",
            "title": "Channel Pipeline",
            "description": "Build a pipeline using channels: generator → squarer → printer.",
            "starter_code": "package main

import "fmt"

func main() {
    // TODO: Create pipeline with channels
    // 1. Generator produces numbers 1-10
    // 2. Squarer squares each number
    // 3. Printer prints results
}
",
            "solution": "package main

import "fmt"

func generator(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

func squarer(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

func printer(in <-chan int) {
    for n := range in {
        fmt.Println(n)
    }
}

func main() {
    nums := generator(1, 2, 3, 4, 5)
    squares := squarer(nums)
    printer(squares)
}

// With done channel for cancellation:
func generatorWithDone(done <-chan struct{}, nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            select {
            case out <- n:
            case <-done:
                return
            }
        }
    }()
    return out
}
",
            "test_cases": [
                {"input": "generator(1,2,3,4,5) -> squarer -> printer", "expected": "1,4,9,16,25"}
            ],
            "hints": [
                "Channels are typed conduits for goroutine communication",
                "Close channels when done sending",
                "Use range to receive until channel closes"
            ],
            "concepts": ["channels", "pipelines", "goroutines", "select"],
            "difficulty": 4
        }
    ],
    "interfaces": [
        {
            "id": "go_intf_001",
            "title": "Interface Design - Storage Backend",
            "description": "Design a storage interface with multiple implementations (memory, file, mock).",
            "starter_code": "package storage

// TODO: Define Storage interface
// TODO: Implement InMemoryStorage
// TODO: Implement FileStorage
// TODO: Implement MockStorage for testing
",
            "solution": "package storage

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "sync"
)

// Storage defines the interface for all storage backends
type Storage interface {
    Get(key string) (string, error)
    Set(key, value string) error
    Delete(key string) error
    List() ([]string, error)
}

// InMemoryStorage implements Storage in memory
type InMemoryStorage struct {
    mu   sync.RWMutex
    data map[string]string
}

func NewInMemoryStorage() *InMemoryStorage {
    return &InMemoryStorage{data: make(map[string]string)}
}

func (s *InMemoryStorage) Get(key string) (string, error) {
    s.mu.RLock()
    defer s.mu.RUnlock()
    val, ok := s.data[key]
    if !ok {
        return "", fmt.Errorf("key not found: %s", key)
    }
    return val, nil
}

func (s *InMemoryStorage) Set(key, value string) error {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.data[key] = value
    return nil
}

func (s *InMemoryStorage) Delete(key string) error {
    s.mu.Lock()
    defer s.mu.Unlock()
    delete(s.data, key)
    return nil
}

func (s *InMemoryStorage) List() ([]string, error) {
    s.mu.RLock()
    defer s.mu.RUnlock()
    keys := make([]string, 0, len(s.data))
    for k := range s.data {
        keys = append(keys, k)
    }
    return keys, nil
}

// FileStorage implements Storage using JSON file
type FileStorage struct {
    path string
    mu   sync.RWMutex
}

func NewFileStorage(path string) *FileStorage {
    return &FileStorage{path: path}
}

func (s *FileStorage) load() (map[string]string, error) {
    data, err := ioutil.ReadFile(s.path)
    if err != nil {
        return make(map[string]string), nil
    }
    var result map[string]string
    if err := json.Unmarshal(data, &result); err != nil {
        return nil, err
    }
    return result, nil
}

func (s *FileStorage) save(data map[string]string) error {
    bytes, err := json.MarshalIndent(data, "", "  ")
    if err != nil {
        return err
    }
    return ioutil.WriteFile(s.path, bytes, 0644)
}

func (s *FileStorage) Get(key string) (string, error) {
    s.mu.RLock()
    defer s.mu.RUnlock()
    data, err := s.load()
    if err != nil {
        return "", err
    }
    val, ok := data[key]
    if !ok {
        return "", fmt.Errorf("key not found: %s", key)
    }
    return val, nil
}

func (s *FileStorage) Set(key, value string) error {
    s.mu.Lock()
    defer s.mu.Unlock()
    data, err := s.load()
    if err != nil {
        return err
    }
    data[key] = value
    return s.save(data)
}

func (s *FileStorage) Delete(key string) error {
    s.mu.Lock()
    defer s.mu.Unlock()
    data, err := s.load()
    if err != nil {
        return err
    }
    delete(data, key)
    return s.save(data)
}

func (s *FileStorage) List() ([]string, error) {
    s.mu.RLock()
    defer s.mu.RUnlock()
    data, err := s.load()
    if err != nil {
        return nil, err
    }
    keys := make([]string, 0, len(data))
    for k := range data {
        keys = append(keys, k)
    }
    return keys, nil
}

// MockStorage for testing
type MockStorage struct {
    Calls   []string
    Data    map[string]string
    Err     error
}

func NewMockStorage() *MockStorage {
    return &MockStorage{Data: make(map[string]string)}
}

func (m *MockStorage) Get(key string) (string, error) {
    m.Calls = append(m.Calls, "Get:"+key)
    if m.Err != nil {
        return "", m.Err
    }
    return m.Data[key], nil
}

func (m *MockStorage) Set(key, value string) error {
    m.Calls = append(m.Calls, "Set:"+key)
    if m.Err != nil {
        return m.Err
    }
    m.Data[key] = value
    return nil
}

func (m *MockStorage) Delete(key string) error {
    m.Calls = append(m.Calls, "Delete:"+key)
    return nil
}

func (m *MockStorage) List() ([]string, error) {
    m.Calls = append(m.Calls, "List")
    keys := make([]string, 0, len(m.Data))
    for k := range m.Data {
        keys = append(keys, k)
    }
    return keys, nil
}
",
            "test_cases": [
                {"input": "Test all Storage implementations", "expected": "Consistent behavior across backends"}
            ],
            "hints": [
                "Interfaces in Go are implicit - no 'implements' keyword",
                "Design interfaces from the consumer's perspective",
                "Use mock implementations for unit testing"
            ],
            "concepts": ["interfaces", "dependency_injection", "testing", "polymorphism"],
            "difficulty": 5
        }
    ],
    "microservices": [
        {
            "id": "go_micro_001",
            "title": "Circuit Breaker Pattern",
            "description": "Implement a circuit breaker for resilient HTTP calls.",
            "starter_code": "package circuit

import (
    "errors"
    "sync"
    "time"
)

// TODO: Implement CircuitBreaker
// States: Closed, Open, HalfOpen
// Config: failureThreshold, timeout, halfOpenMaxCalls
",
            "solution": "package circuit

import (
    "errors"
    "sync"
    "time"
)

var ErrCircuitOpen = errors.New("circuit breaker is open")

type State int

const (
    StateClosed State = iota
    StateOpen
    StateHalfOpen
)

type Config struct {
    FailureThreshold    int
    Timeout             time.Duration
    HalfOpenMaxCalls    int
    SuccessThreshold    int
}

type CircuitBreaker struct {
    config          Config
    state           State
    failures        int
    successes       int
    lastFailureTime time.Time
    halfOpenCalls   int
    mu              sync.RWMutex
}

func New(config Config) *CircuitBreaker {
    return &CircuitBreaker{config: config, state: StateClosed}
}

func (cb *CircuitBreaker) Call(fn func() error) error {
    cb.mu.Lock()
    
    switch cb.state {
    case StateOpen:
        if time.Since(cb.lastFailureTime) > cb.config.Timeout {
            cb.state = StateHalfOpen
            cb.halfOpenCalls = 0
            cb.successes = 0
        } else {
            cb.mu.Unlock()
            return ErrCircuitOpen
        }
    case StateHalfOpen:
        if cb.halfOpenCalls >= cb.config.HalfOpenMaxCalls {
            cb.mu.Unlock()
            return ErrCircuitOpen
        }
        cb.halfOpenCalls++
    }
    
    cb.mu.Unlock()
    
    err := fn()
    
    cb.mu.Lock()
    defer cb.mu.Unlock()
    
    if err != nil {
        cb.recordFailure()
    } else {
        cb.recordSuccess()
    }
    
    return err
}

func (cb *CircuitBreaker) recordFailure() {
    cb.failures++
    cb.lastFailureTime = time.Now()
    
    switch cb.state {
    case StateClosed:
        if cb.failures >= cb.config.FailureThreshold {
            cb.state = StateOpen
        }
    case StateHalfOpen:
        cb.state = StateOpen
        cb.halfOpenCalls = 0
    }
}

func (cb *CircuitBreaker) recordSuccess() {
    cb.failures = 0
    
    switch cb.state {
    case StateHalfOpen:
        cb.successes++
        if cb.successes >= cb.config.SuccessThreshold {
            cb.state = StateClosed
            cb.halfOpenCalls = 0
        }
    }
}

func (cb *CircuitBreaker) State() State {
    cb.mu.RLock()
    defer cb.mu.RUnlock()
    return cb.state
}
",
            "test_cases": [
                {"input": "Fail 5 times, then success", "expected": "Circuit opens, then half-open, then closed"}
            ],
            "hints": [
                "Three states: Closed (normal), Open (failing), HalfOpen (testing)",
                "Track failures and time since last failure",
                "In HalfOpen, allow limited calls to test recovery"
            ],
            "concepts": ["circuit_breaker", "resilience", "state_machine", "microservices"],
            "difficulty": 7
        }
    ]
}

def get_challenges(track: str, difficulty_range: tuple = None) -> List[Dict]:
    challenges = GO_CHALLENGES.get(track, [])
    if difficulty_range:
        min_d, max_d = difficulty_range
        challenges = [c for c in challenges if min_d <= c["difficulty"] <= max_d]
    return challenges

def get_all_tracks() -> List[str]:
    return list(GO_CHALLENGES.keys())

def get_challenge_by_id(challenge_id: str) -> Dict:
    for track in GO_CHALLENGES.values():
        for challenge in track:
            if challenge["id"] == challenge_id:
                return challenge
    return None
