```python
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

# Only import android-specific libraries if we are on the Android platform
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    
    # Android Classes
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy decorator for non-android platforms to prevent import errors
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        # Get the current activity instance
        activity = PythonActivity.mActivity
        
        # Initialize the WebView
        self.webview = WebView(activity)
        
        # Configure WebView settings for modern web apps
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setLoadsImagesAutomatically(True)
        
        # Set the WebViewClient to handle navigation within the view
        self.webview.setWebViewClient(WebViewClient())
        
        # Load the target URL
        self.webview.loadUrl(self.url)
        
        # Set the WebView as the main view of the activity, 
        # bypassing SDL2 surface conflicts
        activity.setContentView(self.webview)

class MainApp(App):
    def build(self):
        return WebViewWidget()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```