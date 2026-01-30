#!/bin/bash
# Build script for Railway deployment

set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
cd backend
python manage.py collectstatic --noinput

echo "Build complete!"
