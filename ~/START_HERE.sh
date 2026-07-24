#!/bin/bash

# START_HERE.sh - The ultimate prank script.
# Purpose: Open a fart soundboard in Chrome and (hopefully) play some sounds.

# Target URL: MyInstants fart soundboard
# Note: Autoplay is heavily restricted by modern browsers (Chrome).
# It usually requires a user click on the page first.
# We'll open the page, and the user (or Mel) will have to click *something* 
# to trigger the audio, which is part of the prank!

URL="https://www.myinstants.com/en/search/?n=fart"

echo "Initializing system modules..."
sleep 1
echo "Connecting to sonic resonance chamber..."
sleep 1
echo "WARNING: HIGH LEVELS OF GAS DETECTED"
sleep 1
echo "Launching entertainment protocol..."

# Open the URL in Chrome on Android
termux-open-url "$URL"

echo "Protocol launched. Good luck, Mel! 😂"
