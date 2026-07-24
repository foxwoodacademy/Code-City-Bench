# 🏗️ System Architecture: Distributed Swarm Fabric

## 1. High-Level Overview
The Distributed Swarm Fabric transforms `janebot_motherbrain` from a local process manager into a network-aware hub. The architecture follows a **Hub-and-Spoke** model where the Samsung Tablet acts as the central authority (the Hub) and all other devices act as Agents (the Spokes).

## 2. The ZeroClaw Transport Layer
### 2.1 WebSocket Communication
We utilize WebSockets for three primary reasons:
1. **Full-Duplex**: The Hub can push tasks to agents without waiting for a request.
2. **Low Overhead**: Minimal header size compared to HTTP/REST.
3. **Cross-Platform**: Native support across Windows, Linux, and Android.

### 2.2 Message Lifecycle
1. **Handshake**: Agent connects $ightarrow$ Sends Join Token $ightarrow$ Hub validates via `SecurityManager`.
2. **Registration**: Hub adds `AgentInfo` to `AgentRegistry` with the active WebSocket endpoint.
3. **Routing**: `MessageBus` identifies the recipient $ightarrow$ `WebSocketBus` transmits the JSON-serialized `Message`.
4. **Execution**: Agent processes task $ightarrow$ Returns `RESPONSE` message $ightarrow$ Hub updates `TaskQueue`.

## 3. Core Components Integration
### 3.1 Networked MessageBus
The `MessageBus` is no longer just a local event emitter. It now acts as a router:
- **Local Messages**: Handled via async callbacks.
- **Remote Messages**: Serialized and pushed through the `WebSocketBus`.

### 3.2 Networked AgentRegistry
The registry now tracks **Network Endpoints**. It monitors connection health via WebSocket pings. If a socket closes, the agent is automatically marked `offline`.

### 3.3 Distributed TaskQueue
The `TaskQueue` manages priority-based distribution. When a worker assigns a task to a remote agent, the `WebSocketBus` ensures delivery, and the queue awaits an async response via a unique `message_id` mapping.

## 4. Failure Modes & Resilience
- **Network Partition**: If the Hub loses connection, agents enter "Autonomous Mode" (if configured) or wait for reconnection.
- **Malformed Payloads**: The `SecurityManager` validates all incoming packets against a schema before they enter the `MessageBus`.
- **Node Crash**: Heartbeat timeouts in the `AgentRegistry` ensure that tasks are requeued if an agent dies mid-execution.
