#!/bin/bash
# Unregistration script for Microsoft Whiteboard Desktop App

set -e

APP_NAME="whiteboard-app"
DESKTOP_FILE="${APP_NAME}.desktop"
LOCAL_APPS_DIR="$HOME/.local/share/applications"
LOCAL_BIN_DIR="$HOME/.local/bin"
APP_DATA_DIR="$HOME/.local/share/whiteboard-app"

echo "Unregistering Microsoft Whiteboard Desktop App..."

# Remove launcher script
if [ -f "$LOCAL_BIN_DIR/$APP_NAME" ]; then
    echo "Removing launcher script..."
    rm "$LOCAL_BIN_DIR/$APP_NAME"
fi

# Remove desktop entry
if [ -f "$LOCAL_APPS_DIR/$DESKTOP_FILE" ]; then
    echo "Removing desktop entry..."
    rm "$LOCAL_APPS_DIR/$DESKTOP_FILE"
fi

# Remove app data directory
if [ -d "$APP_DATA_DIR" ]; then
    echo "Removing application files..."
    rm -rf "$APP_DATA_DIR"
fi

# Remove icon
if [ -f "$HOME/.local/share/icons/hicolor/scalable/apps/whiteboard.svg" ]; then
    echo "Removing icon..."
    rm "$HOME/.local/share/icons/hicolor/scalable/apps/whiteboard.svg"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    echo "Updating desktop database..."
    update-desktop-database "$LOCAL_APPS_DIR" 2>/dev/null || true
fi

# Update icon cache
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
fi

echo ""
echo "✓ Unregistration complete!"
echo "Microsoft Whiteboard has been removed from your applications."
echo ""
