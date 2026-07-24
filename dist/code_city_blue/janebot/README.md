# 🧠 JaneBot MotherBrain

The central orchestration hub for the MkdMind AI agent swarm. Designed to run on a tablet as a command-and-control center.

## 🚀 Quick Start

### Prerequisites
- Termux (Android)
- Python 3.10+

### Installation
```bash
./scripts/setup.sh
```

### Usage
Type `jane boot` to launch the dashboard.

## 🔒 Environmental Hardening (Tablet Setup)
For optimal performance and persistence, configure your Android tablet with these steps:

1.  **Process Persistence (`termux-wake-lock`):**
    -   Run `termux-wake-lock` in your Termux session. This prevents the device from sleeping and killing background processes. The `jane boot` command now includes this.

2.  **Static Internal IP:**
    -   Go to Android Settings -> Network & Internet -> Wi-Fi.
    -   Tap on your connected Wi-Fi network.
    -   Tap the 'Settings' (gear) icon.
    -   Select 'IP settings' and change from 'DHCP' to 'Static'.
    -   Manually enter an IP address, Gateway, Network prefix length (usually 24), DNS 1 (e.g., 8.8.8.8), and DNS 2 (e.g., 8.8.4.4). Choose an IP outside your router's DHCP range.

3.  **Disable Android Battery Optimization for Termux:**
    -   Go to Android Settings -> Apps -> See all apps -> Termux.
    -   Tap 'Battery' or 'Battery usage'.
    -   Select 'Unrestricted' or 'Don't optimize'. This ensures Termux processes are not killed by the system to save battery.


- `janebot_motherbrain/`: Core Python orchestration logic.
- `swarm_ui/`: Web-based dashboard for real-time monitoring.
- `scripts/`: Automation and setup scripts.
- `docs/`: Technical documentation and task tracking.

## 🛠️ Components
- **MotherBrain**: Central hub for agent registration and task distribution.
- **Message Bus**: High-performance inter-agent communication.
- **Task Queue**: Prioritized work distribution and load balancing.
- **Agent Registry**: Dynamic discovery of swarm nodes.

## 📜 License
MIT License - See [LICENSE](LICENSE) for details.
