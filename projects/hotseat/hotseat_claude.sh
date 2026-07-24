#!/data/data/com.termux/files/usr/bin/bash
source ~/.bashrc

if [ -z "$GROQ_API_KEY" ]; then
  echo "Error: GROQ_API_KEY is not set."
  exit 1
fi

echo "🧠 Hotseat - Technical Advisory Session"
echo "Type your question. Ctrl+C to exit."
echo "----------------------------------------"
while true; do
  read -p "You: " INPUT
  RESPONSE=$(curl -s https://api.groq.com/openai/v1/chat/completions \
    -H "Authorization: Bearer $GROQ_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"llama-3.1-8b-instant\",\"messages\":[{\"role\":\"system\",\"content\":\"You are a technical advisor for recursive self-improvement engines and agentic systems.\"},{\"role\":\"user\",\"content\":\"$INPUT\"}]}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['choices'][0]['message']['content'])")
  echo ""
  echo "Advisor: $RESPONSE"
  echo ""
done
