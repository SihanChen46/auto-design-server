#!/bin/bash

# Run Black
echo "Running Black..."
black .

# Run Flake8
echo "Running Flake8..."
flake8 .
