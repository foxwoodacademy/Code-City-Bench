#!/usr/bin/env bash

# Syntax General Intelligence - Ollama Model Setup
# Creates the bridge models for Thoth swarms

echo "════════════════════════════════════════"
echo "  Syntax General Intelligence - Model Setup"
echo "  Bridge models for Thoth swarm coordination"
echo "════════════════════════════════════════"
echo ""

# Check if ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install Ollama first."
    echo "   Visit: https://ollama.ai"
    exit 1
fi

# Check if base model exists
if ! ollama list | grep -q "qwen2.5-coder"; then
    echo "🔍 Base model qwen2.5-coder:1.5b not found. Pulling..."
    ollama pull qwen2.5-coder:1.5b
    if [ $? -ne 0 ]; then
        echo "❌ Failed to pull base model. Check your internet connection."
        exit 1
    fi
fi

echo "✅ Base model available. Creating syntax bridge models..."
echo ""

# Create Syntax General Intelligence model
echo "🧠 Creating syntax-general-intelligence..."
if ollama create syntax-general-intelligence -f syntax-general-intelligence.Modelfile; then
    echo "✅ syntax-general-intelligence created successfully"
else
    echo "❌ Failed to create syntax-general-intelligence"
fi

# Create Thoth Coordinator model
echo "🎭 Creating thoth-coordinator..."
if ollama create thoth-coordinator -f thoth-coordinator.Modelfile; then
    echo "✅ thoth-coordinator created successfully"
else
    echo "❌ Failed to create thoth-coordinator"
fi

# Create Codex Bridge model
echo "🌉 Creating codex-bridge..."
if ollama create codex-bridge -f codex-bridge.Modelfile; then
    echo "✅ codex-bridge created successfully"
else
    echo "❌ Failed to create codex-bridge"
fi

echo ""
echo "📋 Available models:"
ollama list

echo ""
echo "════════════════════════════════════════"
echo "  OpenClaw Configuration"
echo "════════════════════════════════════════"
echo ""
echo "To use with OpenClaw, add this to your config:"
echo ""
echo "export OLLAMA_API_KEY=\"syntax-bridge\""
echo ""
echo "Then configure OpenClaw models:"
echo "openclaw config set models.providers.ollama.apiKey \"OLLAMA_API_KEY\""
echo "openclaw config set models.providers.ollama.baseUrl \"http://127.0.0.1:11434\""
echo ""
echo "Use in agents:"
echo 'openclaw config set agents.defaults.model.primary "ollama/syntax-general-intelligence"'
echo ""
echo "════════════════════════════════════════"
echo "  Setup Complete!"
echo "════════════════════════════════════════"
