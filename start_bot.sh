#!/bin/bash

# An improved script to start and automatically clean up the Rasa bot.

# Navigate to the script's directory to ensure paths are correct
cd "$(dirname "$0")"

# Activate the virtual environment
source venv/bin/activate

# --- Smart Cleanup Function ---
# This function will run automatically when the script is told to exit,
# including when you close the terminal window.
cleanup() {
    echo ""
    echo "--- Terminal closed, shutting down all bot processes ---"
    
    # This command finds and kills the Rasa server and any Python scripts
    # that were started by this script. The '-P $$' part is key, as it
    # targets only the children of this specific script.
    pkill -P $$
    
    echo "--- Bot shut down successfully ---"
}

# --- Trap Signals ---
# This tells the script to run our 'cleanup' function when it receives
# a signal to close (EXIT), hang up (HUP), or interrupt (INT, from Ctrl+C).
trap cleanup EXIT HUP INT

# --- Start the Bot Processes ---

# 1. Start the Rasa server in the background
echo "Starting Rasa server in the background..."
rasa run --enable-api --cors "*" &

# Wait for a few seconds to give the server time to start up
sleep 15

# 2. Start the voice interface in the background
echo "Starting voice interface in the background..."
python voice_interface.py &

# --- Wait for User ---
# The script will now wait here. You can interact with your bot.
# When you close the terminal, the 'trap' will activate the 'cleanup' function.
echo "--- Bot is running. Close this terminal to stop the bot. ---"
wait

