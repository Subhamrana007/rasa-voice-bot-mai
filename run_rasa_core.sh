#!/bin/bash
# This script runs the Rasa Core server in the background

# Path to your virtual environment's Python
VENV_PYTHON="/home/rana/bot/rasa_env_310/bin/python"

# Path to Rasa project
RASA_PROJECT_DIR="/home/rana/bot"

# Log file for Rasa Core output
LOG_FILE="$RASA_PROJECT_DIR/rasa_core.log"

cd "$RASA_PROJECT_DIR" || exit

# Remove old log file
rm -f "$LOG_FILE"

# Run Rasa server in the background, logging output
nohup "$VENV_PYTHON" -m rasa run --enable-api --cors "*" --log-file "$LOG_FILE" > /dev/null 2>&1 &

echo "Rasa Core server started in background. Logs: $LOG_FILE"