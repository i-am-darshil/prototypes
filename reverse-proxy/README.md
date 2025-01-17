- [ ] Event-driven architecture ✅
- [ ] Use Master-Worker Process Pattern (like nginx uses) ✅
- [ ] Take YAML config ✅
- [ ] Implement Routing - GET, POST, PUT, DELETE ✅
- [ ] Implement Load Balancing ✅
- [ ] Implement Rate Limiting ✅
- [ ] Implement Logging ✅

## Architecture choice

- For **I/O-bound tasks**, **multi-process event-driven architectures** (e.g., Nginx-like) in Python/Node.js are ideal due to their simplicity and fault tolerance. However, Java/C++ can also be used effectively for I/O-bound tasks if you're comfortable with the added complexity of thread synchronization.  

- For **CPU-bound tasks**, **multi-threaded architectures** (Java/C++) excel when shared memory is needed for efficiency. However, **multi-process architectures** remain a valid choice in situations where isolation and fault tolerance are more critical.  

---

### **When to Choose Each Architecture**
 -------------------------------|---------------------------------------|----------------------------------------------
| Workload Type                 | Architecture Choice                   | Example Use Case                             |
|-------------------------------|---------------------------------------|----------------------------------------------|
| **I/O-bound**                 | Multi-process, event-driven           | Reverse proxies, web servers, API gateways.  |
| **CPU-bound + Shared Memory** | Multi-threaded (Java/C++)             | Real-time collaboration, simulations.        |
| **CPU-bound + Isolation**     | Multi-process (Python/C++)            | ML inference, data transformation pipelines. |
 -------------------------------|---------------------------------------|----------------------------------------------

### **Performance Comparison Table**

| Feature                           | Multi-Process (e.g., Nginx)                       | Multi-Threaded (e.g., C++/Java)                     |
|-----------------------------------|---------------------------------------------------|-----------------------------------------------------|
| **Fault Tolerance**               | High (crash in one process doesn’t affect others) | Low (crash in one thread can crash the process)     |
| **Concurrency**                   | High (event-driven handles 10K+ connections)      | High (efficient thread pools can manage many tasks) |
| **Memory Usage**                  | Higher (separate memory per process)              | Lower (shared memory)                               |
| **Context Switching**             | More expensive (process switches)                 | Cheaper (thread switches)                           |
| **Programming Complexity**        | Simpler (no shared memory issues)                 | Complex (requires thread synchronization)           |
| **I/O-Bound Tasks**               | Highly efficient (non-blocking I/O)               | Efficient but requires careful synchronization      |
| **CPU-Bound Tasks**               | Less efficient (no shared memory)                 | Ideal (shared memory, faster execution)             |

### **Practical Examples**

#### **1. Multi-Process Event-Driven Architecture**
**Scenario**: A reverse proxy server handling 10,000+ concurrent HTTP requests.

- **Implementation**: Python with `asyncio` or Node.js  
- **Key Features**:  
  - Processes handle independent client connections using non-blocking I/O.  
  - Fault isolation ensures a crash in one process doesn’t affect others.  

```python
# Python example using asyncio
import asyncio

async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    print(f"Received {message}")
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
```

**Tools like Gunicorn for Python**:  
Gunicorn forks multiple worker processes to handle requests concurrently.  

---

#### **2. Multi-Threaded Architecture**
**Scenario**: An image processing pipeline where each task reads data from a shared queue, processes it, and writes results back.

- **Implementation**: Java with ThreadPoolExecutor  
- **Key Features**:  
  - Threads share a queue to distribute CPU-bound tasks.  
  - Synchronization ensures safe access to shared resources.  

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ImageProcessingServer {
    public static void main(String[] args) {
        ExecutorService executor = Executors.newFixedThreadPool(10);
        for (int i = 0; i < 100; i++) {
            executor.submit(() -> processImage());
        }
        executor.shutdown();
    }

    private static void processImage() {
        System.out.println(Thread.currentThread().getName() + " processing image...");
        // Simulate processing
        try { Thread.sleep(100); } catch (InterruptedException e) { }
    }
}
```

**Practical Application**:  
- Tasks with frequent memory sharing (e.g., accessing a shared data cache or real-time collaborative apps).  

---

#### **3. Multi-Process CPU-Bound Architecture**
**Scenario**: A machine learning inference server handling isolated requests.  

- **Implementation**: Python with `multiprocessing`  
- **Key Features**:  
  - Each process is isolated, allowing fault tolerance.  
  - Ideal for parallel tasks without shared state.  

```python
from multiprocessing import Process

def process_request(request_id):
    print(f"Processing request {request_id}")
    # Simulate CPU-intensive task
    sum(i * i for i in range(10**6))

if __name__ == "__main__":
    processes = []
    for i in range(4):  # Assume 4 CPU cores
        p = Process(target=process_request, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
```

**Practical Application**:  
- High-performance tasks where isolation is critical (e.g., financial computations, malware analysis).  

---

### **1. When Can a Crash in One Thread Bring Down the Entire Process?**

In a multi-threaded architecture, threads share the same memory space and other resources (e.g., file descriptors). A crash in one thread can propagate to the entire process if:

1. **Segmentation Faults**:
   - If a thread dereferences invalid memory or accesses memory incorrectly, it can trigger a segmentation fault, crashing the entire process.

2. **Unhandled Exceptions**:
   - An unhandled exception in one thread may cause the process to terminate unless explicitly caught or handled.

3. **Corruption of Shared State**:
   - Bugs like race conditions or improper synchronization can corrupt shared memory. This may lead to undefined behavior, crashes, or deadlocks, impacting all threads in the process.

4. **Exceeding Process-Level Limits**:
   - A thread exhausting resources (e.g., memory, file descriptors) may affect the entire process, causing failures for all threads.

---

### **2. Example: Comparing Process-Based and Thread-Based Reverse Proxy Performance**

#### **Scenario**
You’re designing a reverse proxy server handling high-concurrency traffic (e.g., 10,000 concurrent connections). Let’s compare **multi-process (e.g., Nginx)** and **multi-threaded (e.g., Java/C++)** architectures.

#### **1. Multi-Process Event-Driven Architecture (e.g., Nginx with Python/Node.js)**

- **Setup**:
  - Nginx spawns `N` worker processes (e.g., 4 for a quad-core CPU).
  - Each worker uses **non-blocking I/O** (e.g., `epoll`) to handle thousands of concurrent connections.

- **Performance Characteristics**:
  - **Fault Isolation**: A crash in one worker doesn’t affect others.
  - **Memory Usage**: Processes are more memory-intensive than threads, but modern OS optimizations like copy-on-write minimize this.
  - **Context Switching**: Fewer processes mean less context-switching overhead compared to many threads.
  - **Scalability**: Can handle massive I/O-bound workloads efficiently due to non-blocking I/O.

- **Best Use Cases**:
  - High-concurrency, low-latency web servers (e.g., HTTP reverse proxies).
  - Environments requiring fault tolerance and simplicity.

#### **2. Multi-Threaded Architecture (e.g., C++/Java)**

- **Setup**:
  - A single process spawns `N` threads (e.g., thread pool of 100 threads).
  - Each thread handles connections and tasks, possibly with blocking I/O or event loops.

- **Performance Characteristics**:
  - **Shared Memory Access**: Efficient for scenarios where threads share resources.
  - **Synchronization Overhead**: Requires careful management of locks or thread-safe data structures.
  - **Fault Tolerance**: A crash or memory corruption in one thread can affect the entire process.
  - **Scalability**: Threads are lightweight, allowing more concurrency without excessive memory overhead.

- **Best Use Cases**:
  - CPU-intensive tasks requiring shared memory access (e.g., image/video processing, machine learning inference).
  - I/O-bound workloads where fault isolation isn’t critical.

---

## Rate Limiting
- Implement token based rate-limiting
- To keep things simple, master process will carry out the rate limiting
- If request is allowed, master sends the event to worked to process
- Maintain a mapping of token to rate limited in memory for simplicity. Can be a distributed storage. The stale mappings can be deleted periodically (not implemented) to keep a check on memory.
- Workers can also carry out rate limiting. But will require a shared memory. Preferring to be done by master for simplicity


---

### **1. Key Challenges with Worker Processes**
In a **master-worker process architecture**, the workers are isolated processes, meaning they don't share memory. This introduces a challenge for tasks like **load balancing** and **rate limiting**, which require a **global state** across all requests.

#### **Why Shared State is Important**:
- **Load Balancing**:  
  You need to track which backend servers are currently underloaded, overloaded, or unavailable to efficiently route incoming requests.
- **Rate Limiting**:  
  Requires tracking IP/token usage over time to enforce limits consistently.

---

### **Solution 1: Perform Load Balancing and Rate Limiting in the Master Process**
If the **master process** is responsible for these tasks:
- **Pros**:
  1. Centralized logic ensures a single source of truth for load balancing and rate limiting.
  2. No inter-process communication (IPC) overhead for sharing state between workers.
  3. Simpler worker design; workers only handle request processing after being assigned tasks.
- **Cons**:
  1. The master process becomes a bottleneck if it's overwhelmed with too many incoming requests.
  2. Scalability may be limited because the master handles all pre-processing tasks.
  3. Additional latency might be introduced in transferring requests from the master to the workers.

---

### **Solution 2: Decentralized Load Balancing and Rate Limiting**
If **workers handle load balancing and rate limiting independently**:
- **Implementation**:
  - Use an external, centralized store (e.g., Redis, Memcached) to maintain shared mappings (server load, IP/token rates).
- **Pros**:
  1. Distributes workload, preventing the master from becoming a bottleneck.
  2. Allows workers to operate more autonomously and scales better with more worker processes.
  3. Can handle very high concurrency with distributed state management.
- **Cons**:
  1. Increased complexity due to the need for efficient IPC or external data store synchronization.
  2. Additional latency for every worker to fetch and update shared state.
  3. Potential contention issues in the centralized store.

---

### **Trade-offs Between Master and Worker Load Balancing**
| Feature                          | Master Process Load Balancing         | Worker Process Load Balancing               |
|----------------------------------|---------------------------------------|---------------------------------------------|
| **Scalability**                  | Limited by master capacity            | Scales well with external state management. |
| **Implementation Simplicity**    | Simple (centralized logic)            | Complex (needs shared state sync).          |
| **Fault Tolerance**              | Single point of failure (master)      | Distributed failure tolerance.              |
| **Latency**                      | Higher (extra processing in master)   | Lower (direct processing by workers).       |

---

### **Hybrid Approach**
- A **hybrid approach** can combine the best of both:
  - **Master process handles coarse-grained load balancing**: Assign requests to workers based on server availability, but the mapping doesn't track granular state (e.g., per-IP rate limiting).
  - **Workers handle fine-grained rate limiting**: Use an external shared store to track and enforce IP/token limits.

---

### **Recommendation**
1. **Small to Medium Traffic**:
   - Handle load balancing and rate limiting entirely in the master process. Simplicity outweighs performance concerns for manageable workloads.
   
2. **High Traffic with Scale Requirements**:
   - Use an external store (e.g., Redis) to share mappings of:
     - Backend server loads (for load balancing).
     - IP/token request rates (for rate limiting).
   - Workers fetch and update these mappings directly, reducing the burden on the master process.

---
