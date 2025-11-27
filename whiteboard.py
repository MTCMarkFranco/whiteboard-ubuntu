#!/usr/bin/env python3
"""
Microsoft Whiteboard Desktop Application for Ubuntu
A minimal, fullscreen GTK application that displays Microsoft Whiteboard with touch support.
"""

import gi
import signal
import sys

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, WebKit2, Gdk

class WhiteboardApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Microsoft Whiteboard")
        
        # Set up window properties
        self.set_default_size(1920, 1080)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.fullscreen()
        
        # Create WebKit2 WebView with optimized settings
        self.webview = WebKit2.WebView()
        
        # Configure WebKit settings for optimal performance
        settings = self.webview.get_settings()
        settings.set_enable_javascript(True)
        settings.set_enable_webgl(True)
        settings.set_enable_webaudio(True)
        settings.set_enable_media_stream(True)
        settings.set_enable_accelerated_2d_canvas(True)
        settings.set_enable_write_console_messages_to_stdout(True)
        settings.set_javascript_can_access_clipboard(True)
        settings.set_enable_back_forward_navigation_gestures(True)
        settings.set_hardware_acceleration_policy(WebKit2.HardwareAccelerationPolicy.ALWAYS)
        
        # Enable touch events and smooth scrolling
        settings.set_enable_smooth_scrolling(True)
        
        # Set user agent to ensure proper Microsoft authentication
        settings.set_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Configure web context for cookies and storage
        web_context = self.webview.get_context()
        web_context.set_cache_model(WebKit2.CacheModel.WEB_BROWSER)
        
        # Enable persistent cookie storage for authentication
        cookie_manager = web_context.get_cookie_manager()
        import os
        cookie_file = os.path.expanduser("~/.local/share/whiteboard-app/cookies.txt")
        os.makedirs(os.path.dirname(cookie_file), exist_ok=True)
        cookie_manager.set_persistent_storage(
            cookie_file,
            WebKit2.CookiePersistentStorage.TEXT
        )
        cookie_manager.set_accept_policy(WebKit2.CookieAcceptPolicy.ALWAYS)
        
        # Connect signals
        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.on_key_press)
        self.webview.connect("load-changed", self.on_load_changed)
        self.webview.connect("create", self.on_create_web_view)
        self.webview.connect("decide-policy", self.on_decide_policy)
        
        # Add webview to window
        self.add(self.webview)
        
        # Load Microsoft Whiteboard
        self.webview.load_uri("https://whiteboard.microsoft.com")
        
        # Show all widgets
        self.show_all()
        
        # Set window icon
        try:
            self.set_icon_name("whiteboard-app")
        except:
            pass
    
    def on_key_press(self, widget, event):
        """Handle keyboard shortcuts"""
        # F11 to toggle fullscreen
        if event.keyval == Gdk.KEY_F11:
            if self.is_fullscreen:
                self.unfullscreen()
                self.is_fullscreen = False
            else:
                self.fullscreen()
                self.is_fullscreen = True
            return True
        
        # Ctrl+Q or Alt+F4 to quit
        if ((event.state & Gdk.ModifierType.CONTROL_MASK) and 
            event.keyval == Gdk.KEY_q):
            self.destroy()
            return True
        
        # Ctrl+R to reload
        if ((event.state & Gdk.ModifierType.CONTROL_MASK) and 
            event.keyval == Gdk.KEY_r):
            self.webview.reload()
            return True
        
        return False
    
    def on_load_changed(self, webview, load_event):
        """Handle page load events"""
        if load_event == WebKit2.LoadEvent.FINISHED:
            print("Page loaded successfully")
    
    def on_create_web_view(self, webview, navigation_action):
        """Handle popup windows (for authentication dialogs)"""
        # Create new window for popups (e.g., Microsoft login)
        popup_window = Gtk.Window()
        popup_window.set_default_size(800, 600)
        popup_window.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        popup_window.set_transient_for(self)
        
        popup_webview = WebKit2.WebView.new_with_related_view(webview)
        popup_webview.connect("ready-to-show", lambda w: popup_window.show_all())
        popup_webview.connect("close", lambda w: popup_window.destroy())
        
        popup_window.add(popup_webview)
        
        return popup_webview
    
    def on_decide_policy(self, webview, decision, decision_type):
        """Handle navigation policy decisions"""
        if decision_type == WebKit2.PolicyDecisionType.NEW_WINDOW_ACTION:
            # Allow new windows for authentication
            decision.use()
            return True
        elif decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:
            # Allow all navigation (including Microsoft auth redirects)
            decision.use()
            return True
        return False

def main():
    """Main entry point"""
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    # Check if WebKit2GTK is available
    try:
        app = WhiteboardApp()
        app.is_fullscreen = True
        Gtk.main()
    except Exception as e:
        print(f"Error starting application: {e}", file=sys.stderr)
        print("\nPlease ensure WebKit2GTK is installed:", file=sys.stderr)
        print("  sudo apt-get install gir1.2-webkit2-4.0", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
