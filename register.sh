#!/bin/bash
# Registration script for Microsoft Whiteboard Desktop App
# This creates a desktop shortcut that can be pinned to the toolbar

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="whiteboard-app"
DESKTOP_FILE="${APP_NAME}.desktop"
LOCAL_APPS_DIR="$HOME/.local/share/applications"
LOCAL_BIN_DIR="$HOME/.local/bin"

echo "Registering Microsoft Whiteboard Desktop App..."

# Create local directories if they don't exist
mkdir -p "$LOCAL_APPS_DIR"
mkdir -p "$LOCAL_BIN_DIR"

# Copy the run script to local bin
echo "Installing launcher script to $LOCAL_BIN_DIR/$APP_NAME..."
cat > "$LOCAL_BIN_DIR/$APP_NAME" << 'EOF'
#!/bin/bash
# Launcher for Microsoft Whiteboard Desktop App

# Get the directory where this script is located
INSTALL_DIR="$(cd "$(dirname "$0")" && pwd)"

# Run the application with clean environment
exec /usr/bin/env -i \
    HOME="$HOME" \
    USER="$USER" \
    LOGNAME="$LOGNAME" \
    PATH="/usr/local/bin:/usr/bin:/bin" \
    DISPLAY="$DISPLAY" \
    XAUTHORITY="$XAUTHORITY" \
    XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" \
    DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" \
    /usr/bin/python3 "$HOME/.local/share/whiteboard-app/whiteboard.py" "$@"
EOF

chmod +x "$LOCAL_BIN_DIR/$APP_NAME"

# Create app data directory
APP_DATA_DIR="$HOME/.local/share/whiteboard-app"
mkdir -p "$APP_DATA_DIR"

# Copy the Python script to the app data directory
echo "Copying application files..."
cp "$SCRIPT_DIR/whiteboard.py" "$APP_DATA_DIR/"
chmod +x "$APP_DATA_DIR/whiteboard.py"

# Create the desktop entry
echo "Creating desktop entry..."
cat > "$LOCAL_APPS_DIR/$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Microsoft Whiteboard
Comment=Collaborative whiteboard for Microsoft 365
Exec=$LOCAL_BIN_DIR/$APP_NAME
Icon=whiteboard
Terminal=false
Categories=Office;Graphics;Education;
Keywords=whiteboard;drawing;collaboration;microsoft;
StartupNotify=true
StartupWMClass=whiteboard.py
EOF

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    echo "Updating desktop database..."
    update-desktop-database "$LOCAL_APPS_DIR" 2>/dev/null || true
fi

# Try to download and set an icon
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
ICON_SVG_DIR="$HOME/.local/share/icons/hicolor/scalable/apps"
mkdir -p "$ICON_DIR"
mkdir -p "$ICON_SVG_DIR"

# Create a simple SVG icon if we don't have one
if [ ! -f "$ICON_DIR/whiteboard.png" ] && [ ! -f "$ICON_SVG_DIR/whiteboard.svg" ]; then
    echo "Creating application icon..."
    cat > "$ICON_SVG_DIR/whiteboard.svg" << 'SVGEOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="256" height="256" rx="32" fill="#0078D4"/>
  
  <!-- Whiteboard -->
  <rect x="40" y="50" width="176" height="130" rx="8" fill="white"/>
  
  <!-- Pen stroke -->
  <path d="M 70 90 Q 100 70, 130 90 T 180 90" stroke="#FF6B6B" stroke-width="6" fill="none" stroke-linecap="round"/>
  
  <!-- Pen -->
  <rect x="185" y="165" width="35" height="8" rx="2" fill="#FFB84D" transform="rotate(45 202 169)"/>
  <circle cx="202" cy="182" r="6" fill="#333"/>
</svg>
SVGEOF
    
    # Update icon cache if possible
    if command -v gtk-update-icon-cache &> /dev/null; then
        gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
    fi
fi

echo ""
echo "✓ Registration complete!"
echo ""
echo "Microsoft Whiteboard has been added to your applications."
echo ""
echo "To use it:"
echo "  1. Press Super (Windows key) and search for 'Microsoft Whiteboard'"
echo "  2. Click the app to launch it"
echo "  3. Right-click the icon in the toolbar and select 'Add to Favorites'"
echo "     to pin it permanently"
echo ""
echo "You can also run it from terminal with: $APP_NAME"
echo ""
echo "To unregister, run: ./unregister.sh"
echo ""
