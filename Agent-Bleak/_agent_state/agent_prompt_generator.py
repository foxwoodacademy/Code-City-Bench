import json
import os
import datetime

# Determine the absolute path to the _agent_state directory
# This script is expected to be inside _agent_state, so its parent is the base directory.
STATE_DIR_ABSOLUTE = os.path.dirname(os.path.abspath(__file__))

def generate_prompt(user_query):
    conv_log_path = os.path.join(STATE_DIR_ABSOLUTE, 'conversation_log.txt')
    conversation_history = ""
    if os.path.exists(conv_log_path):
        with open(conv_log_path, 'r') as f:
            conversation_history = f.read()

    env_state_path = os.path.join(STATE_DIR_ABSOLUTE, 'env_state.json')
    env_state = {}
    if os.path.exists(env_state_path):
        try:
            with open(env_state_path, 'r') as f:
                env_state = json.load(f)
        except json.JSONDecodeError:
            print("Warning: env_state.json is malformed. Starting with empty state for this prompt.")
            env_state = {}

    context_data = {
        "conversation_history": conversation_history,
        "env_state": env_state,
        "current_timestamp": datetime.datetime.now().isoformat()
    }

    prompt = f"""[CONTEXT_START]
{json.dumps(context_data, indent=2)}
[CONTEXT_END]

[USER_QUERY_START]
{user_query}
[USER_QUERY_END]"""
    return prompt

if __name__ == "__main__":
    print("\n--- Agent Prompt Generator ---")
    print("This script helps you generate the prompt to send to the AI.")
    print("It automatically includes the current agent state (conversation history, environment variables).")
    user_query = input("Enter your query for the AI: ")

    generated_prompt = generate_prompt(user_query)
    print("\n--- Copy and paste the following into your AI chat window ---")
    print("```")
    print(generated_prompt)
    print("```")
    print("\n--- End of Generated Prompt ---")
    print("\nRemember to run the agent's code output by the AI *before* generating the next prompt.")
