```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

# Only import pyjnius and android modules if running on Android
if platform == 'android':
    from jnius import autoclass
    from android.run_on_ui_thread import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy decorator for non-android platforms to prevent import errors
    def run_on_ui_thread(func):
        return func

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        if platform == 'android':
            # Delay creation to ensure activity is ready
            Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        # Access the underlying Android Activity
        activity = PythonActivity.mActivity
        
        # Initialize WebView
        webview = WebView(activity)
        settings = webview.getSettings()
        
        # Configure essential settings for modern web apps
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setLoadsImagesAutomatically(True)
        settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        
        # Prevent opening links in external browser
        webview.setWebViewClient(WebViewClient())
        
        # Set the WebView as the main content view of the activity
        # This bypasses SDL2 layout conflicts by putting the WebView on top
        activity.setContentView(webview)
        
        # Load the target URL
        webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

class DeliveryTrackerApp(App):
    def build(self):
        return WebViewWidget()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    DeliveryTrackerApp().run()
```