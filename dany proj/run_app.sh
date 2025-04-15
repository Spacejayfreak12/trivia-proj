#!/bin/bash

# This script sets the environment variables needed for the persistent public URL
# and then runs the application.

# Default port
PORT=5000

# Check for command line arguments
while getopts p:a:s: flag
do
    case "${flag}" in
        p) PORT=${OPTARG};;
        a) AUTHTOKEN=${OPTARG};;
        s) SUBDOMAIN=${OPTARG};;
    esac
done

# Set environment variables if provided
if [ ! -z "$AUTHTOKEN" ]; then
    export NGROK_AUTHTOKEN=$AUTHTOKEN
    echo "Set NGROK_AUTHTOKEN from parameter"
fi

if [ ! -z "$SUBDOMAIN" ]; then
    export NGROK_SUBDOMAIN=$SUBDOMAIN
    echo "Set NGROK_SUBDOMAIN from parameter"
fi

# Set PORT environment variable
export PORT=$PORT
echo "Using port: $PORT"

# Run the application
python3 app.py

# Cleanup (optional)
# unset NGROK_AUTHTOKEN
# unset NGROK_SUBDOMAIN
# unset PORT 