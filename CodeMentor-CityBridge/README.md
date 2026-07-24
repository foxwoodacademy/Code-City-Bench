# CodeMentor-CityBridge

Connects your VS Code extension (CodeMentor-MVP) to your gamified debugger (Code City).

## Start
./start.sh

## Stop
./stop.sh

## Test
curl http://127.0.0.1:8766/health

## How it works
- Mentor sends code explanations → bridge → city queue (monsters spawn)
- City sends damage reports → bridge → mentor log (tutor adapts)
- No file moves. No restructure. Both repos stay independent.
