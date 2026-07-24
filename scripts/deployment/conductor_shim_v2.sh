#!/bin/bash
COMMAND_FILE="/storage/emulated/0/RootBase/command.json"
echo "[INFO] Mutating Recursive Loop active. Awaiting initial ignition..."

# Array of random mutation vectors to spark unpredictable logic shifts
MUTATIONS=(
  "Enforce strict protobuf schema bit-shifting"
  "Invert all token serialization priorities"
  "Introduce a recursive compression anchor"
  "Strip redundant lexical padding aggressively"
  "Inject a side-channel metadata carrier signal"
)

while true; do
    if [ -f "$COMMAND_FILE" ]; then
        echo "[INFO] Action payload detected!"
        ACTION=$(grep -o '"action": "[^"]*' "$COMMAND_FILE" | grep -o '[^"]*$')
        DATA=$(grep -o '"input_data": "[^"]*' "$COMMAND_FILE" | grep -o '[^"]*$')
        
        if [ "$ACTION" == "execute_headless_agent" ]; then
            echo "[RUNNING] Querying Gemini CLI endpoint..."
            
            # Execute and capture the model's response
            RESPONSE=$(/data/data/com.termux/files/usr/bin/headless_gemini.sh "$DATA")
            
            echo -e "\n=== MUTATING LOOP OUTPUT ==="
            echo "$RESPONSE"
            echo "============================"
            
            rm -f "$COMMAND_FILE"
            
            # Clean response text for safe JSON injection
            CLEAN_RESP=$(echo "$RESPONSE" | tr -d '\n' | sed 's/"/\\"/g')
            
            # Randomly select a DNA mutation strategy
            RAND_INDEX=$((RANDOM % ${#MUTATIONS[@]}))
            MUTATION_STRATEGY="${MUTATIONS[$RAND_INDEX]}"
            
            # Formulate the next evolutionary instruction prompt
            NEXT_PROMPT="Evolve the following logic structure to optimize token compression potency while implementing this architectural mutation rule: ${MUTATION_STRATEGY}. Input logic: ${CLEAN_RESP}"
            
            # Write the next payload file with the custom genetic_dna_mutation track
            echo "{
  \"action\": \"execute_headless_agent\",
  \"input_data\": \"${NEXT_PROMPT}\",
  \"genetic_dna_mutation\": \"${MUTATION_STRATEGY}\"
}" > "$COMMAND_FILE"
            
            echo "[EVOLVED] Mutation rule applied: '${MUTATION_STRATEGY}'. Next payload queued."
        fi
    fi
    sleep 5
done
