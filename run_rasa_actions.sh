#!/bin/bash
# This script runs the Rasa Action Server in the background

# Path to your virtual environment's Python
VENV_PYTHON="/home/rana/bot/rasa_env_310/bin/python"

# Path to Rasa project
RASA_PROJECT_DIR="/home/rana/bot"

# Log file for Action Server output
LOG_FILE="$RASA_PROJECT_DIR/rasa_actions.log"

cd "$RASA_PROJECT_DIR" || exit

# Remove old log file
rm -f "$LOG_FILE"

# Run Action server in the background, logging output
nohup "$VENV_PYTHON" -m rasa run actions --actions actions > /dev/null 2>&1 &

echo "Rasa Action server started in background. Logs: $LOG_FILE"