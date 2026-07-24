#!/usr/bin/env python3
"""
MotherBrain Swarm Comms Bridge - Human/Agent Interface Layer
Upgraded with Global Swarm 'Buzz' Broadcast capabilities.
Path: /storage/emulated/0/RootBase/data/motherbrain/api/comms_bridge.py
"""

import sys
import json
import time
from pathlib import Path

# Anchor onto the matrix path
API_DIR = Path("/storage/emulated/0/RootBase/data/motherbrain/api")
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

try:
    from swarm_bus import SwarmNode
except ImportError:
    print("❌ Critical System Error: swarm_bus.py must be in the same directory.")
    sys.exit(1)

class HumanBridge:
    def __init__(self):
        # Establish the user as an immutable destination node on the bus
        self.node = SwarmNode(node_name="operator", capabilities=["manual_approval", "executive_override"])
        self.width = 74

    def check_inbound_suggestions(self):
        """Polls the incoming queue to see what your swarm agents are asking or suggesting."""
        messages = self.node.read_inbound_queue()
        if not messages:
            print("\n📬 \033[1;34m[Comms Bridge]:\033[0m No pending agent requests or suggestions.")
            return

        print(f"\n🔔 \033[1;35mRECEIVED {len(messages)} SWARM SUGGESTIONS/REQUESTS:\033[0m")
        print("━" * self.width)

        for idx, msg in enumerate(messages, 1):
            sender = msg.get("sender", "unknown_agent").upper()
            event = msg.get("event", "NOTIFICATION")
            payload = msg.get("payload", {})
            
            print(f" [{idx}] \033[1;36mFROM:\033[0m {sender} | \033[1;33mTYPE:\033[0m {event}")
            print(f"     \033[1;32mMessage/Suggestion:\033[0m {payload.get('text', 'No context provided.')}")
            
            if event == "REQUEST_APPROVAL" and "target_file" in payload:
                print(f"     ⚠️ \033[1;31mACTION REQUIRED:\033[0m Requesting permission to alter: {payload.get('target_file')}")
            
            print("─" * self.width)

    def dispatch_command(self, target_node: str, task_command: str):
        """Allows the human user to inject an absolute task or override straight into an agent's stream."""
        payload = {"text": task_command}
        success = self.node.broadcast(target_node=target_node, event_type="HUMAN_DIRECTIVE", payload=payload)
        if success:
            print(f"🚀 \033[1;32mDirective broadcasted to network node: [{target_node}]\033[0m")
        else:
            print(f"❌ \033[1;31mTransmission failure to node: [{target_node}]\033[0m")

    def buzz_all_agents(self, emergency_directive: str):
        """Finds every online agent registered in the system map and issues a system-wide broadcast interrupt."""
        active_network = self.node.discover_network()
        if not active_network:
            print("\n💨 \033[1;33m[Buzz Warning]:\033[0m No active agents are currently registered on the swarm bus.")
            return

        print(f"\n⚡ \033[1;31m💥 BUZZING SYSTEM: BROADCASTING SIGNAL TO EVERY ACTIVE AGENT...💥\033[0m")
        print("━" * self.width)

        count = 0
        for target_node in active_network.keys():
            # Skip sending a message back to ourselves
            if target_node == "operator":
                continue
                
            payload = {
                "text": f"SYSTEM-WIDE OVERRIDE NOTIFICATION: {emergency_directive}",
                "global_interrupt": True
            }
            
            success = self.node.broadcast(target_node=target_node, event_type="SYSTEM_BUZZ_ALERT", payload=payload)
            if success:
                print(f" 📡 \033[1;36m[BROADCAST SUCCEDED] ->\033[0m Alert queued into node: \033[1;32m{target_node}\033[0m")
                count += 1
            else:
                print(f" ⚠️ \033[1;33m[BROADCAST FAILED]   ->\033[0m Destination line dropped: {target_node}")

        print("━" * self.width)
        print(f"📊 Buzz distribution loop complete. Intercepted \033[1;35m{count}\033[0m active system processes.\n")


def main():
    bridge = HumanBridge()
    if len(sys.argv) < 2:
        bridge.check_inbound_suggestions()
        sys.exit(0)

    # Command Router Execution
    if sys.argv[1] == "send" and len(sys.argv) >= 4:
        target = sys.argv[2]
        command_string = " ".join(sys.argv[3:])
        bridge.dispatch_command(target, command_string)
    elif sys.argv[1] == "buzz" and len(sys.argv) >= 3:
        broadcast_string = " ".join(sys.argv[2:])
        bridge.buzz_all_agents(broadcast_string)
    else:
        print("💡 Usage Commands:")
        print("  python3 comms_bridge.py                     -> Checks incoming agent suggestions.")
        print("  python3 comms_bridge.py send <node> <text>  -> Commands a single agent.")
        print("  python3 comms_bridge.py buzz <directive>    -> Buzzes EVERY agent in the system simultaneously.")

if __name__ == "__main__":
    main()
