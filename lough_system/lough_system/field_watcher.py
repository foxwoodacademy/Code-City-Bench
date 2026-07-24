import time
import sys
sys.path.insert(0, '/data/data/com.termux/files/home/lough_system')
import field_bridge

RED       = "\033[31m"
GOLD      = "\033[33m"
DIM_WHITE = "\033[2;37m"
CYAN      = "\033[36m"
RESET     = "\033[0m"

COLORS = {
    "zeroclaw":    RED,
    "jane":        GOLD,
    "field_bridge": DIM_WHITE,
    "manual":      CYAN,
}

def main():
    last_timestamp = time.time()
    print(f"[WATCHER] Live since {time.strftime('%H:%M:%S')} — Ctrl+C to exit\n")

    try:
        while True:
            events = field_bridge.poll(since=last_timestamp)

            if events:
                for event in reversed(events):
                    source = event['source_layer']
                    color  = COLORS.get(source, "")
                    reset  = RESET if color else ""
                    print(f"{color}[{event['time_str']}] {source:>16} → {event['event_type']:<32} @ {event['location']}{reset}")

                    if event['timestamp'] > last_timestamp:
                        last_timestamp = event['timestamp']

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[WATCHER] Exiting.")

if __name__ == "__main__":
    main()
