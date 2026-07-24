#!/data/data/com.termux/files/usr/bin/bash
# Claude-4-Prez - Persistent Bot Wrapper
# Freeze/thaw loop - survives session drops

STATE_FILE="/storage/emulated/0/RootBase/lucrative_engines/Claude-4-Prez/alerts-as-a-service/data/bot_state.json"
BOT_DIR="/storage/emulated/0/RootBase/lucrative_engines/Claude-4-Prez/alerts-as-a-service"

echo "🧠 Claude-4-Prez Wrapper Starting..."

while true; do
  echo "🚀 Thawing bot..."
  cd $BOT_DIR && source ~/.bashrc && node src/index.js

  EXIT_CODE=$?
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  echo "💾 Bot exited with code $EXIT_CODE at $TIMESTAMP"
  echo "{\"state\":\"frozen\",\"exit_code\":$EXIT_CODE,\"frozen_at\":\"$TIMESTAMP\"}" > $STATE_FILE

  echo "❄️  Frozen. Thawing in 10 seconds..."
  sleep 10
done
