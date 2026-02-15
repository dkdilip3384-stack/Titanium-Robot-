```python
import kivy
from kivy.app import App
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.clock import Clock

# Only import Android specific modules if we are running on Android
if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    # Dummy decorator for non-android platforms to prevent crash
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class WebViewApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            self.create_webview()
        return Widget()  # Return empty widget as WebView replaces the view

    @run_on_ui_thread
    def create_webview(self):
        # Create the WebView instance
        webview = WebView(Activity)
        
        # Configure WebView settings
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)  # Required for modern web apps
        settings.setDatabaseEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setMixedContentMode(0) # 0 = MIXED_CONTENT_ALWAYS_ALLOW
        
        # Set the client to prevent opening in external browser
        webview.setWebViewClient(WebViewClient())
        
        # Set the WebView as the main content view of the Android Activity
        Activity.setContentView(webview)
        
        # Load the target URL
        webview.loadUrl(self.url)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    WebViewApp().run()
```