```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from jnius import autoclass, cast
from android.runnable import run_on_ui_thread

# Import necessary Android classes
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
WebSettings = autoclass('android.webkit.WebSettings')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class WebViewApp(App):
    def build(self):
        # Create a dummy widget to satisfy Kivy's requirement
        return Widget()

    def on_start(self):
        self.create_webview()

    @run_on_ui_thread
    def create_webview(self):
        # Get the current Android activity context
        activity = PythonActivity.mActivity
        
        # Initialize WebView
        self.webview = WebView(activity)
        
        # Configure WebView settings for maximum compatibility
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setAllowContentAccess(True)
        settings.setDatabaseEnabled(True)
        settings.setSupportZoom(True)
        settings.setBuiltInZoomControls(True)
        settings.setDisplayZoomControls(False)
        
        # Set a standard UserAgent to avoid bot detection
        user_agent = "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
        settings.setUserAgentString(user_agent)

        # Handle page navigation within the WebView itself, not the browser
        self.webview.setWebViewClient(WebViewClient())
        
        # Load the target URL
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
        
        # Set the WebView as the main view of the activity (overriding SDL2 surface)
        activity.setContentView(self.webview)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    WebViewApp().run()
```