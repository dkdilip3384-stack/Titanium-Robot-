```python
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

# Check if we are running on Android
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    # Android class imports
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    # Dummy decorator for non-android platforms to prevent crashes during testing
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class MainWidget(Widget):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        # Delay WebView creation to ensure Window is ready
        Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        # Create WebView instance
        self.webview = WebView(Activity)
        
        # Configure settings for modern web apps (Vercel/React/Next.js compatibility)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDatabaseEnabled(True)
        settings.setLoadsImagesAutomatically(True)
        settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        settings.setUserAgentString("Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36")
        
        # Set WebViewClient to prevent external browser from opening
        self.webview.setWebViewClient(WebViewClient())
        
        # Create a layout and add WebView to it (avoids SDL2 rendering conflicts)
        layout = LinearLayout(Activity)
        params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        layout.addView(self.webview, params)
        
        # Set the activity content to our WebView layout
        Activity.setContentView(layout)
        
        # Load the target URL
        self.webview.loadUrl(self.url)

class TrackingApp(App):
    def build(self):
        return MainWidget()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    TrackingApp().run()
```