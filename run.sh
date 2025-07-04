#!/bin/bash

# Define names
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirement.txt"
MAIN_FILE="constructor.py"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "[ERROR] No requirements.txt found. Skipping dependency installation."
fi

# Step 4: Run the main Python script
if [ -f "$MAIN_FILE" ]; then
    echo "Running $MAIN_FILE..."
    python "$MAIN_FILE"
else
    echo "[ERROR] $MAIN_FILE not found. Cannot run script."
fi
