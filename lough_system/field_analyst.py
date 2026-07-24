import time
import os
import requests
import field_bridge

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "qwen/qwen3-8b:free"
POLL_LIMIT = 20
SLEEP_SECONDS = 60

def get_analyst_observation(event_summary):
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY not set."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        f"Given these recent field events:\n{event_summary}\n\n"
        "What pattern or anomaly is most worth flagging? Respond in one sentence."
    )

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error calling OpenRouter: {e}"

def main():
    print(f"[ANALYST] Starting field_analyst.py (interval: {SLEEP_SECONDS}s)...")
    
    if not OPENROUTER_API_KEY:
        print("[ANALYST] ERROR: OPENROUTER_API_KEY environment variable is not set.")
        return

    while True:
        try:
            # 1. Poll recent events
            events = field_bridge.poll(limit=POLL_LIMIT)
            
            if events:
                # 2. Format summary
                # We reverse because poll returns newest first, but a chronological summary is better for LLM context
                summary_lines = []
                for e in reversed(events):
                    line = f"[{e['time_str']}] {e['source_layer']} -> {e['event_type']} @ {e['location']}"
                    summary_lines.append(line)
                
                event_summary = "\n".join(summary_lines)

                # 3. Ask LLM
                observation = get_analyst_observation(event_summary)
                
                # 4. Print and Emit
                print(f"[ANALYST] {observation}")
                field_bridge.emit(
                    event_type="analyst.observation",
                    location="analyst_agent",
                    source="analyst",
                    payload={"observation": observation}
                )
            else:
                print("[ANALYST] No events to analyze.")

        except Exception as e:
            print(f"[ANALYST] Loop error: {e}")

        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
