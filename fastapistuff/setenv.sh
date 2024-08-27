#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
    echo "Environment variables set successfully."
else
    echo ".env file not found."
fi