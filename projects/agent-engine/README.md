# AgentForge

AgentForge is a modular framework for building, configuring, and managing specialized agentic engines, including scouts, worker agents, and personas.

## Architecture

- `core/`: Foundational logic for engine orchestration and communication.
- `agents/`: Base classes and implementations for specific agent types.
- `personas/`: Configuration-driven persona definitions.

## Getting Started

1. Define a persona in `personas/`.
2. Instantiate an agent using the `core/` engine.
3. Deploy agent into a workflow.
