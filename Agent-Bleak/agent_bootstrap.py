import os
import json

STATE_DIR = "_agent_state"
CONVERSATION_LOG_FILE = os.path.join(STATE_DIR, "conversation_log.txt")
ENV_STATE_FILE = os.path.join(STATE_DIR, "env_state.json")
PROMPT_GENERATOR_SCRIPT = os.path.join(STATE_DIR, "agent_prompt_generator.py")

def setup_agent_environment():
    """Sets up the necessary directory and files for the agent."""
    if not os.path.exists(STATE_DIR):
        os.makedirs(STATE_DIR)
        print(f"Created directory: {STATE_DIR}")

    if not os.path.exists(CONVERSATION_LOG_FILE):
        with open(CONVERSATION_LOG_FILE, 'w') as f:
            f.write("--- Agent Conversation Log ---\n")
        print(f"Created file: {CONVERSATION_LOG_FILE}")

    if not os.path.exists(ENV_STATE_FILE):
        with open(ENV_STATE_FILE, 'w') as f:
            json.dump({}, f, indent=2)
        print(f"Created file: {ENV_STATE_FILE}")

    # Write the prompt generator script content
    prompt_generator_content = """import json
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

    prompt = f\"\"\"[CONTEXT_START]
{json.dumps(context_data, indent=2)}
[CONTEXT_END]

[USER_QUERY_START]
{user_query}
[USER_QUERY_END]\"\"\"
    return prompt

if __name__ == "__main__":
    print("\\n--- Agent Prompt Generator ---")
    print("This script helps you generate the prompt to send to the AI.")
    print("It automatically includes the current agent state (conversation history, environment variables).")
    user_query = input("Enter your query for the AI: ")

    generated_prompt = generate_prompt(user_query)
    print("\\n--- Copy and paste the following into your AI chat window ---")
    print("```")
    print(generated_prompt)
    print("```")
    print("\\n--- End of Generated Prompt ---")
    print("\\nRemember to run the agent's code output by the AI *before* generating the next prompt.")
"""
    with open(PROMPT_GENERATOR_SCRIPT, 'w') as f:
        f.write(prompt_generator_content)
    print(f"Created prompt generator script: {PROMPT_GENERATOR_SCRIPT}")
    print("\nSetup complete! You can now use 'python _agent_state/agent_prompt_generator.py' to generate your prompts.")

if __name__ == "__main__":
    print("Setting up intelligent agent environment...")
    setup_agent_environment()
    print("\n--- Initial Agent Setup Complete ---")
    print("\nTo start interacting with the AI agent:")
    print("1. Run: `python agent_bootstrap.py` (you've already done this if you're reading this!)")
    print("2. Now, run: `python _agent_state/agent_prompt_generator.py`")
    print("3. When prompted, enter your first query for the AI (e.g., 'Hello agent, what can you do?').")
    print("4. The script will output a block of text wrapped in '```'. Copy *everything* inside these '```' (including the `[CONTEXT_START]` and `[USER_QUERY_START]` tags).")
    print("5. Paste this copied text into your AI chat window and send it.")
    print("\nThis process ensures the AI receives all necessary context for our ongoing conversation.")
    print("After the AI responds with code, you will need to:")
    print("   a. **Execute the AI's provided code snippets.** These will update the agent's local state files (`conversation_log.txt`, `env_state.json`).")
    print("   b. Then, run `python _agent_state/agent_prompt_generator.py` again for your next query.")
    print("\nI am now ready to receive your first context-rich query!")
