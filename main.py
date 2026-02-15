```python
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.utils import platform

# Conditional imports for Android
if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    # Dummy for non-android testing
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class WebViewApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        self.webview = None
        root = Widget() # Placeholder root
        Clock.schedule_once(self.create_webview, 0)
        return root

    @run_on_ui_thread
    def create_webview(self, *args):
        if platform != 'android':
            Logger.info(f"WebView: Platform is {platform}. Open {self.url} in browser.")
            return

        # Initialize WebView
        webview = WebView(Activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        
        # Set Client to handle navigation within the app
        webview.setWebViewClient(WebViewClient())
        
        # Add to Android Activity layout
        layout = LinearLayout(Activity)
        Activity.addContentView(webview, LayoutParams(-1, -1)) # Match parent
        
        webview.loadUrl(self.url)
        self.webview = webview

    def on_pause(self):
        if self.webview:
            self.webview.pauseTimers()
            self.webview.onPause()
        return True

    def on_resume(self):
        if self.webview:
            self.webview.onResume()
            self.webview.resumeTimers()

    def on_stop(self):
        if self.webview:
            # Clean up to prevent memory leaks or SDL2 conflicts
            parent = self.webview.getParent()
            if parent:
                parent.removeView(self.webview)

if __name__ == '__main__':
    WebViewApp().run()
```