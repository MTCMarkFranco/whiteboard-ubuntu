#!/bin/bash
# Clean launcher script for Microsoft Whiteboard Desktop App
# This script ensures a clean environment without snap interference

# Unset all snap-related environment variables
unset SNAP
unset SNAP_NAME
unset SNAP_REVISION
unset SNAP_INSTANCE_NAME
unset SNAP_INSTANCE_KEY

# Unset all VS Code snap backup variables
for var in $(env | grep -o '^[^=]*_VSCODE_SNAP_ORIG' 2>/dev/null); do
    unset "$var"
done

# Clear snap paths from critical environment variables
export GTK_PATH=""
export LOCPATH=""
export GIO_MODULE_DIR=""
export GSETTINGS_SCHEMA_DIR=""
export GTK_IM_MODULE_FILE=""
export XDG_DATA_DIRS="/usr/local/share:/usr/share"
export XDG_CONFIG_DIRS="/etc/xdg"

# Clear any LD_LIBRARY_PATH that might point to snap
unset LD_LIBRARY_PATH
unset LD_PRELOAD

# Run the application with system Python in a clean environment
exec /usr/bin/env -i \
    HOME="$HOME" \
    USER="$USER" \
    LOGNAME="$LOGNAME" \
    PATH="/usr/local/bin:/usr/bin:/bin" \
    DISPLAY="$DISPLAY" \
    XAUTHORITY="$XAUTHORITY" \
    XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" \
    DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" \
    /usr/bin/python3 "$(cd "$(dirname "$0")" && pwd)/whiteboard.py" "$@"
