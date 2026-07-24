# 🛡️ Security Model & Adversarial Standards

## 1. Authentication: The Token System
To prevent unauthorized nodes from joining the swarm, we employ a **Pre-Shared Token (PST)** system:
- **Token Generation**: The Hub generates a cryptographically secure, random URL-safe string.
- **Join Sequence**: An agent must provide this token in the first message of the WebSocket handshake.
- **Rotation**: Tokens can be rotated globally by the Hub, forcing all agents to re-authenticate.

## 2. Payload Validation (The Anti-Crash Layer)
To prevent "Brown Team" injection attacks or crash-inducing payloads, the Hub implements **Strict Type Validation**:
- All incoming JSON is parsed and validated against a `ValidationSchema`.
- If a field is missing or of the wrong type (e.g., a string where an integer is expected), the message is dropped immediately, and the event is logged as a security violation.

## 3. The 7-Hat Adversarial Framework
Every architectural change is vetted through the 7-Hat lens:

| Hat | Perspective | Swarm Application |
| :--- | :--- | :--- |
| **White** | Facts/Data | Measuring latency between Tablet Hub and Windows Node. |
| **Red** | Emotion/Intuition | Ensuring the 'jane boot' command feels instantaneous. |
| **Black** | Risks/Caution | Identifying the Hub as a single point of failure. |
| **Yellow** | Benefits | Reducing agent setup time from minutes to seconds. |
| **Green** | Creativity | Exploring UDP for non-critical heartbeat packets. |
| **Blue** | Process | Mapping the sequence from `join` $ightarrow$ `registry` $ightarrow$ `task`. |
| **Brown** | Adversarial | Attempting to DDoS the Hub with 10k malformed packets. |

## 4. Testing Standards
- **Line Coverage**: $\ge 85	ext{--}95\%$ for all security and transport logic.
- **Fuzzing**: Sending random byte sequences to the WebSocket port to ensure the server doesn't crash.
- **Stress**: Testing 50+ concurrent agent connections on the Samsung tablet's hardware.
