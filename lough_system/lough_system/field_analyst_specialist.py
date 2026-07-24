"""
field_analyst_specialist.py

A specialized background agent that operates in different analytical personas to observe and interpret field events.

This agent cycles through personas, polls relevant events, and uses an LLM to generate insights, which are then logged back into the event stream.

Dependencies:
- standard library (time, os, requests)
- field_bridge (local module)
- event_registry (local module)
"""

import time
import os
import requests
import field_bridge
import event_registry

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# Model specified in the prompt
MODEL = "qwen/qwen3-8b:free"
POLL_LIMIT = 20
SLEEP_SECONDS = 60

CORE_PERSONAS = {
    "behavioral": {
        "name": "Behavioral Analyst",
        "prompt_template": "Given these recent field events, which suggest potential agent behavior, what cognitive pattern or intent is most noteworthy? Respond in one sentence.",
        "event_type": event_registry.BEHAVIOR_NAMESPACE["intent"],
        "location": "analyst.behavioral",
        "source": "analyst_behavioral",
        "relevant_event_types": [
            event_registry.BEHAVIOR_NAMESPACE["intent"],
            event_registry.BEHAVIOR_NAMESPACE["bias"],
            event_registry.BEHAVIOR_NAMESPACE["mental"],
            event_registry.BEHAVIOR_NAMESPACE["deviation"],
            event_registry.SYSTEM_NAMESPACE["usage"],
            event_registry.SYSTEM_NAMESPACE["error"]
        ]
    },
    "defense": {
        "name": "Defense Procurement Analyst",
        "prompt_template": "Given these recent field events, which relate to defense procurement and subcontracting, what critical compliance, fiscal, or performance issue is most pressing? Respond in one sentence.",
        "event_type": event_registry.DIB_NAMESPACE["contract"],
        "location": "analyst.dib",
        "source": "analyst_dib",
        "relevant_event_types": [
            event_registry.DIB_NAMESPACE["contract"],
            event_registry.DIB_NAMESPACE["compliance"],
            event_registry.DIB_NAMESPACE["fiscal"],
            event_registry.DIB_NAMESPACE["milestone"],
            event_registry.SYSTEM_NAMESPACE["usage"],
            event_registry.SYSTEM_NAMESPACE["error"]
        ]
    }
}

PERSONAS = {
    **CORE_PERSONAS,
    **event_registry.get_personas(),
}
PERSONA_KEYS = list(PERSONAS.keys())
current_persona_index = 0

def get_analyst_observation(event_summary, persona_config):
    """Generates an observation from the LLM based on event summary and persona.

    Args:
        event_summary (str): A formatted string summarizing recent events.
        persona_config (dict): Configuration for the current analyst persona.

    Returns:
        str: The LLM's observation or an error message.
    """
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY not set."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        f"{persona_config['prompt_template']}\n\n"
        f"Recent Events:\n{event_summary}\n"
    )

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        
        # Ensure expected structure exists before accessing
        if result and 'choices' in result and result['choices'] and 'message' in result['choices'][0] and 'content' in result['choices'][0]['message']:
            return result['choices'][0]['message']['content'].strip()
        else:
            return f"Error: Unexpected response format from OpenRouter. Result: {result}"

    except requests.exceptions.RequestException as e:
        return f"Network error calling OpenRouter: {e}"
    except Exception as e:
        return f"Error processing OpenRouter response: {e}"

def main():
    print(f"[ANALYST] Starting specialized field_analyst.py (interval: {SLEEP_SECONDS}s)...")
    
    if not OPENROUTER_API_KEY:
        print("[ANALYST] ERROR: OPENROUTER_API_KEY environment variable is not set. Exiting.")
        return

    global current_persona_index

    while True:
        try:
            current_persona_key = PERSONA_KEYS[current_persona_index]
            persona_config = PERSONAS[current_persona_key]
            print(f"[ANALYST] Operating as: {persona_config['name']} ({current_persona_key})")

            events = []
            relevant_types = persona_config.get("relevant_event_types", [])
            if relevant_types:
                seen_ids = set()
                for event_type in relevant_types:
                    for event in field_bridge.poll(event_type=event_type, limit=POLL_LIMIT):
                        if event["id"] not in seen_ids:
                            events.append(event)
                            seen_ids.add(event["id"])
                events = sorted(events, key=lambda e: e["timestamp"], reverse=True)[:POLL_LIMIT]
            else:
                events = field_bridge.poll(limit=POLL_LIMIT)
            
            if events:
                summary_lines = []
                for e in reversed(events):
                    time_str = e.get('time_str', 'N/A')
                    source_layer = e.get('source_layer', 'unknown')
                    event_type = e.get('event_type', 'N/A')
                    location = e.get('location', 'N/A')
                    
                    line = f"[{time_str}] {source_layer:>16} -> {event_type:<32} @ {location}"
                    summary_lines.append(line)
                
                event_summary = "\n".join(summary_lines)

                # 3. Get observation from LLM
                observation = get_analyst_observation(event_summary, persona_config)
                
                # 4. Print observation and emit it back into the event stream
                print(f"[ANALYST] Observation: {observation}")
                field_bridge.emit(
                    event_type=persona_config["event_type"],
                    location=persona_config["location"],
                    source=persona_config["source"],
                    payload={
                        "observation": observation,
                        "persona": current_persona_key,
                        "raw_event_count": len(events)
                    }
                )
            else:
                print("[ANALYST] No events to analyze in this cycle.")

        except Exception as e:
            print(f"[ANALYST] General loop error: {e}")
            # Emit a system error if the main loop encounters an unhandled exception
            try:
                field_bridge.emit(
                    event_type=event_registry.SYSTEM_NAMESPACE["error"],
                    location="analyst_agent",
                    source="analyst",
                    payload={
                        "error": type(e).__name__,
                        "message": str(e),
                        "persona": current_persona_key,
                        "raw_event_count": len(events) if 'events' in locals() else 0
                    }
                )
            except Exception as emit_e:
                print(f"[ANALYST] Failed to emit system error event: {emit_e}")

        current_persona_index = (current_persona_index + 1) % len(PERSONA_KEYS)
        next_key = PERSONA_KEYS[current_persona_index]
        print(f"[ANALYST] Next persona: {PERSONAS[next_key]['name']}")

        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
