# Quick Start Guide

## Installation (30 seconds)

```bash
./register.sh
```

## Finding the App

1. **Press Super Key** (Windows key) or click Activities
2. **Type**: `whiteboard`
3. **Click**: Microsoft Whiteboard icon

## Pin to Toolbar

1. Launch the app (see above)
2. **Right-click** the icon in your toolbar
3. Select **"Add to Favorites"** or **"Pin to Dash"**

## Uninstall

```bash
./unregister.sh
```

## Keyboard Shortcuts

- **F11**: Toggle fullscreen
- **Ctrl+Q**: Quit
- **Ctrl+R**: Reload

## Troubleshooting

### App won't start from terminal?

Make sure `~/.local/bin` is in your PATH, or use the full path:
```bash
~/.local/bin/whiteboard-app
```

### App not showing in menu?

Log out and log back in, or run:
```bash
update-desktop-database ~/.local/share/applications
```

### Need system-wide install?

Use the system install script instead:
```bash
sudo ./install.sh
```
