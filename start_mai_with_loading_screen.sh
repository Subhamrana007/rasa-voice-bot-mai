#!/bin/bash
# This script launches the Rasa bot backend and the custom loading screen frontend

RASA_PROJECT_DIR="/home/rana/rasa-voice-bot"
VENV_PYTHON="/home/rana/rasa-voice-bot/venv/bin/python"
# --- Kill any lingering Rasa processes before starting ---
echo "Attempting to stop any existing Rasa processes..."
pkill -f "rasa run"
pkill -f "rasa run actions"
sleep 2 # Give processes a moment to shut down

# --- Start Rasa Backend in Background ---
echo "Starting Rasa Core and Action Servers..."
"$RASA_PROJECT_DIR/run_rasa_core.sh"
"$RASA_PROJECT_DIR/run_rasa_actions.sh"

sleep 5 # Give Rasa a few seconds to start its server

# --- Launch GUI Loading Screen (Frontend) ---
echo "Launching custom loading screen..."
"$VENV_PYTHON" "$RASA_PROJECT_DIR/loading_screen.py"

echo "Rasa bot and loading screen launched. Check rasa_core.log and rasa_actions.log for details."
echo "To interact with the bot, you'll need to use 'rasa shell' in a new terminal, or connect via its API."
