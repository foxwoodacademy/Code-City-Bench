#!/bin/bash
COMMAND_FILE="/storage/emulated/0/RootBase/command.json"
echo "[INFO] Headless Recursive Loop active. Awaiting initial payload..."

while true; do
    if [ -f "$COMMAND_FILE" ]; then
        echo "[INFO] Action payload detected!"
        ACTION=$(grep -o '"action": "[^"]*' "$COMMAND_FILE" | grep -o '[^"]*$')
        DATA=$(grep -o '"input_data": "[^"]*' "$COMMAND_FILE" | grep -o '[^"]*$')
        
        if [ "$ACTION" == "execute_headless_agent" ]; then
            echo "[RUNNING] Querying Gemini CLI endpoint..."
            
            # Execute and capture the model's response in a variable
            RESPONSE=$(/data/data/com.termux/files/usr/bin/headless_gemini.sh "$DATA")
            
            echo -e "\n=== LOOP OUTPUT ==="
            echo "$RESPONSE"
            echo "==================="
            
            # Wipe the old command file
            rm -f "$COMMAND_FILE"
            
            # RECURSIVE STEP: Clean the response text for JSON formatting
            CLEAN_RESP=$(echo "$RESPONSE" | tr -d '\n' | sed 's/"/\\"/g')
            
            # Create a loop instruction that forces the model to refine its previous output
            NEXT_PROMPT="Analyze the following logic structure and optimize its token compression potency further: $CLEAN_RESP"
            
            # Generate the NEXT payload automatically
            echo "{
  \"action\": \"execute_headless_agent\",
  \"input_data\": \"${NEXT_PROMPT}\"
}" > "$COMMAND_FILE"
            
            echo "[LOOP] Next payload queued automatically. Sleeping for 5s..."
        fi
    fi
    sleep 5
done
