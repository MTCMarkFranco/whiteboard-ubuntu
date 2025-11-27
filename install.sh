#!/bin/bash
# Installation script for Microsoft Whiteboard Desktop App

set -e

echo "Installing Microsoft Whiteboard Desktop App..."

# Check if running on Ubuntu/Debian
if ! command -v apt-get &> /dev/null; then
    echo "Error: This script requires apt-get (Ubuntu/Debian)"
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    gir1.2-webkit2-4.1 \
    libwebkit2gtk-4.1-0

# Make the script executable
chmod +x whiteboard.py

# Copy the application to /usr/local/bin
echo "Installing application..."
sudo cp whiteboard.py /usr/local/bin/whiteboard-app
sudo chmod +x /usr/local/bin/whiteboard-app

# Install desktop entry
echo "Installing desktop entry..."
sudo cp whiteboard-app.desktop /usr/share/applications/

# Create icon directory if it doesn't exist
sudo mkdir -p /usr/share/icons/hicolor/scalable/apps

# Copy icon if it exists
if [ -f "icon.svg" ]; then
    sudo cp icon.svg /usr/share/icons/hicolor/scalable/apps/whiteboard-app.svg
elif [ -f "icon.png" ]; then
    sudo cp icon.png /usr/share/pixmaps/whiteboard-app.png
fi

# Update desktop database
sudo update-desktop-database /usr/share/applications/ 2>/dev/null || true

# Update icon cache
sudo gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true

echo ""
echo "Installation complete!"
echo ""
echo "You can now launch the app by:"
echo "  1. Searching for 'Microsoft Whiteboard' in your applications menu"
echo "  2. Running 'whiteboard-app' from the terminal"
echo ""
echo "Keyboard shortcuts:"
echo "  F11       - Toggle fullscreen"
echo "  Ctrl+Q    - Quit"
echo "  Ctrl+R    - Reload"
echo ""
