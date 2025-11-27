#!/usr/bin/env python3
"""
Microsoft Whiteboard Desktop Application for Ubuntu
A minimal, fullscreen GTK application that displays Microsoft Whiteboard with touch support.
"""

import gi
import signal
import sys

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.1')

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
        settings.set_hardware_acceleration_policy(WebKit2.HardwareAccelerationPolicy.ALWAYS)
        
        # Enable touch events and smooth scrolling
        settings.set_enable_smooth_scrolling(True)
        
        # Disable kinetic scrolling to prevent container from capturing touch events
        settings.set_enable_back_forward_navigation_gestures(False)
        
        # Set user agent to report device WITH pen support but not as a touch device
        # This makes Microsoft Whiteboard treat all input as pen/mouse, not touch gestures
        settings.set_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Configure web context for cookies and storage
        web_context = self.webview.get_context()
        web_context.set_cache_model(WebKit2.CacheModel.WEB_BROWSER)
        
        # Get user content manager to inject scripts at document start
        user_content_manager = self.webview.get_user_content_manager()
        
        # Inject script to convert touch/pointer input into mouse events before the page loads
        touch_to_mouse_script = """
            // Run at document start - before Microsoft Whiteboard registers its handlers
            (function() {
                console.log('[TouchCapture] Initializing touch-to-mouse injector');
                let activeTouchId = null;
                let activeTarget = null;
                let lastCoords = { x: 0, y: 0 };
                let suppressScroll = false;
                const POINTER_ID = 9999;

                function resolveTarget(touch) {
                    if (activeTarget && activeTarget.isConnected) {
                        return activeTarget;
                    }
                    const hitTarget = document.elementFromPoint(touch.clientX, touch.clientY);
                    activeTarget = hitTarget || document.body;
                    return activeTarget;
                }

                function dispatchPointerEvent(type, touch, buttonsValue) {
                    const target = resolveTarget(touch);
                    const eventInit = {
                        bubbles: true,
                        cancelable: true,
                        clientX: touch.clientX,
                        clientY: touch.clientY,
                        screenX: touch.screenX,
                        screenY: touch.screenY,
                        pointerId: POINTER_ID,
                        pointerType: 'mouse',
                        isPrimary: true,
                        buttons: buttonsValue,
                        button: 0,
                        pressure: buttonsValue ? 0.5 : 0
                    };
                    const event = new PointerEvent(type, eventInit);
                    target.dispatchEvent(event);
                }

                function dispatchMouseEvent(type, touch) {
                    const target = resolveTarget(touch);
                    const eventInit = {
                        bubbles: true,
                        cancelable: true,
                        clientX: touch.clientX,
                        clientY: touch.clientY,
                        screenX: touch.screenX,
                        screenY: touch.screenY,
                        buttons: type === 'mouseup' ? 0 : 1,
                        button: 0,
                        which: 1
                    };
                    lastCoords = { x: touch.clientX, y: touch.clientY };
                    const event = new MouseEvent(type, eventInit);
                    target.dispatchEvent(event);
                }

                function consumeEvent(evt) {
                    evt.preventDefault();
                    evt.stopPropagation();
                    evt.stopImmediatePropagation();
                    suppressScroll = true;
                    clearTimeout(consumeEvent._scrollTimer);
                    consumeEvent._scrollTimer = setTimeout(() => suppressScroll = false, 250);
                    return false;
                }

                window.addEventListener('touchstart', function(event) {
                    if (activeTouchId !== null) {
                        return consumeEvent(event);
                    }
                    const touch = event.changedTouches[0];
                    if (!touch) {
                        return consumeEvent(event);
                    }
                    activeTouchId = touch.identifier;
                    activeTarget = touch.target;
                    console.log('[TouchCapture] touchstart -> mousedown', {
                        id: activeTouchId,
                        x: touch.clientX,
                        y: touch.clientY
                    });
                    dispatchPointerEvent('pointerover', touch, 0);
                    dispatchPointerEvent('pointerenter', touch, 0);
                    dispatchPointerEvent('pointerdown', touch, 1);
                    dispatchMouseEvent('mousedown', touch);
                    return consumeEvent(event);
                }, true);

                window.addEventListener('touchmove', function(event) {
                    if (activeTouchId === null) {
                        return consumeEvent(event);
                    }
                    const touch = Array.from(event.changedTouches).find(t => t.identifier === activeTouchId);
                    if (!touch) {
                        return consumeEvent(event);
                    }
                    dispatchPointerEvent('pointermove', touch, 1);
                    dispatchMouseEvent('mousemove', touch);
                    return consumeEvent(event);
                }, true);

                function endTouch(touch) {
                    console.log('[TouchCapture] touchend -> mouseup', {
                        id: activeTouchId,
                        x: touch.clientX,
                        y: touch.clientY
                    });
                    dispatchPointerEvent('pointerup', touch, 0);
                    dispatchPointerEvent('pointerleave', touch, 0);
                    dispatchPointerEvent('pointerout', touch, 0);
                    dispatchMouseEvent('mouseup', touch);
                    activeTouchId = null;
                    activeTarget = null;
                }

                window.addEventListener('touchend', function(event) {
                    if (activeTouchId === null) {
                        return consumeEvent(event);
                    }
                    const touch = Array.from(event.changedTouches).find(t => t.identifier === activeTouchId);
                    if (!touch) {
                        return consumeEvent(event);
                    }
                    endTouch(touch);
                    return consumeEvent(event);
                }, true);

                window.addEventListener('touchcancel', function(event) {
                    if (activeTouchId === null) {
                        return consumeEvent(event);
                    }
                    const touch = Array.from(event.changedTouches).find(t => t.identifier === activeTouchId);
                    if (touch) {
                        endTouch(touch);
                    } else if (activeTarget) {
                        const synthetic = { clientX: lastCoords.x, clientY: lastCoords.y, screenX: lastCoords.x, screenY: lastCoords.y, target: activeTarget };
                        dispatchMouseEvent('mouseup', synthetic);
                    }
                    return consumeEvent(event);
                }, true);

                // Block pointer events originating from touch so only mouse events remain
                const pointerBlocker = function(event) {
                    if (event.pointerType === 'touch') {
                        event.preventDefault();
                        event.stopPropagation();
                        event.stopImmediatePropagation();
                    }
                };
                window.addEventListener('pointerdown', pointerBlocker, true);
                window.addEventListener('pointermove', pointerBlocker, true);
                window.addEventListener('pointerup', pointerBlocker, true);
                window.addEventListener('pointercancel', pointerBlocker, true);

                // Prevent wheel/scroll events while finger drawing
                window.addEventListener('wheel', function(event) {
                    if (suppressScroll) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                }, { passive: false, capture: true });

                window.addEventListener('scroll', function(event) {
                    if (suppressScroll) {
                        window.scrollTo(0, 0);
                        event.preventDefault();
                        event.stopPropagation();
                    }
                }, true);

                document.documentElement.style.overscrollBehavior = 'none';
                document.documentElement.style.touchAction = 'none';
                document.body.style.overscrollBehavior = 'none';
                document.body.style.touchAction = 'none';

                console.log('[TouchCapture] Touch-to-mouse injector ready');
            })();
        """
        
        script = WebKit2.UserScript(
            touch_to_mouse_script,
            WebKit2.UserContentInjectedFrames.ALL_FRAMES,
            WebKit2.UserScriptInjectionTime.START,
            None,
            None
        )
        user_content_manager.add_script(script)
        
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
        
        # Add webview directly to window
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
