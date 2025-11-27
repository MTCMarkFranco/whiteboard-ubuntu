# Microsoft Whiteboard Desktop App for Ubuntu

A lightweight, high-performance desktop application for Ubuntu GNOME that provides a fullscreen Microsoft Whiteboard experience with touch support.

## Features

- **Fullscreen Experience**: Minimal chrome for maximum whiteboard space
- **Touch Support**: Full touch input support for drawing and interaction
- **Hardware Acceleration**: WebKit2GTK with GPU acceleration for smooth performance
- **Microsoft Authentication**: Full support for Microsoft SSO and authentication flows
- **Persistent Sessions**: Automatic cookie storage keeps you logged in
- **Keyboard Shortcuts**: Quick access to common functions

## Requirements

- Ubuntu 20.04 or later (or compatible Debian-based distribution)
- Python 3.6+
- GTK 3.0
- WebKit2GTK 4.0

## Installation

### Quick Install

Run the installation script:

```bash
chmod +x install.sh
./install.sh
```

### Manual Installation

1. Install dependencies:

```bash
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    gir1.2-webkit2-4.0 \
    libwebkit2gtk-4.0-37
```

2. Make the script executable:

```bash
chmod +x whiteboard.py
```

3. Run the application:

```bash
./whiteboard.py
```

4. (Optional) Install system-wide:

```bash
sudo cp whiteboard.py /usr/local/bin/whiteboard-app
sudo cp whiteboard-app.desktop /usr/share/applications/
```

## Usage

### Launching

- **From Applications Menu**: Search for "Microsoft Whiteboard"
- **From Terminal**: Run `whiteboard-app` or `./whiteboard.py`

### Keyboard Shortcuts

- **F11**: Toggle fullscreen mode
- **Ctrl+Q**: Quit application
- **Ctrl+R**: Reload whiteboard

### First Run

On first launch, you'll be prompted to sign in with your Microsoft account. The app will:
1. Open the Microsoft Whiteboard website
2. Display the Microsoft authentication dialog
3. Store your session securely for future launches

## Technical Details

### Architecture

- **GUI Framework**: GTK 3.0
- **Web Engine**: WebKit2GTK 4.0
- **Language**: Python 3
- **Hardware Acceleration**: Enabled for 2D canvas, WebGL, and WebAudio

### Performance Optimizations

1. **Hardware Acceleration**: Always-on GPU acceleration for rendering
2. **Cache Model**: Full web browser caching for faster load times
3. **Smooth Scrolling**: Enhanced touch and scroll performance
4. **Persistent Storage**: Cookie and session persistence for instant login

### Authentication

The app uses WebKit2's cookie manager to securely store Microsoft authentication tokens in:
```
~/.local/share/whiteboard-app/cookies.txt
```

This ensures you stay logged in between sessions while maintaining security.

### Touch Support

Touch events are fully supported through WebKit2GTK and GTK's native touch handling. All touch gestures work as expected:
- Single touch for drawing
- Two-finger pinch to zoom
- Two-finger pan to scroll
- Touch and hold for context menus

## Troubleshooting

### Application won't start

Ensure all dependencies are installed:
```bash
sudo apt-get install gir1.2-webkit2-4.0 python3-gi
```

### Authentication issues

Clear stored cookies:
```bash
rm -rf ~/.local/share/whiteboard-app/cookies.txt
```

### Performance issues

1. Verify hardware acceleration is working:
   - Check if `libgl1-mesa-dri` is installed
   - Ensure your graphics drivers are up to date

2. Close other resource-intensive applications

### Touch not working

Ensure your display supports touch input:
```bash
xinput list
```

Look for your touch device in the list. If it's not detected, check your hardware drivers.

## Uninstallation

```bash
sudo rm /usr/local/bin/whiteboard-app
sudo rm /usr/share/applications/whiteboard-app.desktop
rm -rf ~/.local/share/whiteboard-app
```

## Security Notes

- The app stores authentication cookies locally in your home directory
- All communication with Microsoft services uses HTTPS
- No data is stored or transmitted by this application itself
- All functionality is provided by the official Microsoft Whiteboard web app

## License

This is a wrapper application for Microsoft Whiteboard. Microsoft Whiteboard and its services are subject to Microsoft's terms of service.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues with:
- **This app**: Open an issue in this repository
- **Microsoft Whiteboard functionality**: Contact Microsoft Support
- **Ubuntu/GTK issues**: Consult Ubuntu documentation

## Changelog

### Version 1.0.0
- Initial release
- Fullscreen GTK application
- WebKit2GTK integration
- Touch support
- Microsoft authentication support
- Hardware acceleration
- Persistent session storage
