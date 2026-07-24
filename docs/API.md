# 🔌 Network Protocol Specification (API)

## 1. Connection Handshake
**Endpoint**: `ws://<HUB_IP>:8765`

### Join Request (Agent $ightarrow$ Hub)
```json
{
  "type": "join",
  "token": "secure_token_here"
}
```

### Join Response (Hub $ightarrow$ Agent)
**Success**:
```json
{
  "status": "authorized",
  "agent_id": "agent-uuid-123"
}
```
**Failure**:
```json
{
  "status": "unauthorized",
  "reason": "Invalid token"
}
```

## 2. Message Format
All communication uses the standardized `Message` object.

### Schema
| Field | Type | Description |
| :--- | :--- | :--- |
| `message_id` | String | UUID for tracking and responses. |
| `message_type` | Enum | `TASK`, `RESPONSE`, `HEARTBEAT`, `BROADCAST`, `ERROR`, `DISCOVERY`, `STATUS`, `STREAM`. |
| `sender` | String | ID of the sending agent/hub. |
| `recipient` | String \| Null | ID of the target agent (Null for broadcast). |
| `topic` | String | Routing topic (e.g., `system.heartbeat`). |
| `payload` | Object | The actual data content. |
| `timestamp` | Float | Epoch time of creation. |
| `priority` | Integer | 0-10 (10 highest). |

### Example: Task Dispatch (Hub $ightarrow$ Agent)
```json
{
  "message_id": "task-abc-123",
  "message_type": "TASK",
  "sender": "motherbrain",
  "recipient": "agent-01",
  "topic": "compute.heavy",
  "payload": {
    "task_id": "t-99",
    "description": "Calculate Pi to 1M digits",
    "timeout": 60.0
  },
  "timestamp": 1715530000.0,
  "priority": 8
}
```
