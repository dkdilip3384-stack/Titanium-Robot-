```python
import kivy
from kivy.app import App
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.clock import Clock

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    # Android class mappings
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.view.LinearLayout')
    WebSettings = autoclass('android.webkit.WebSettings')
else:
    # Dummy decorator for non-android platforms
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class MainApp(App):
    def build(self):
        # Return an empty widget as Kivy root; WebView will sit on top or replace view
        return Widget()

    def on_start(self):
        if platform == 'android':
            self.init_webview()

    @run_on_ui_thread
    def init_webview(self):
        # Get the current Android Activity
        activity = PythonActivity.mActivity
        
        # Create WebView instance
        self.webview = WebView(activity)
        
        # Configure WebView settings for modern web apps
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDatabaseEnabled(True)
        settings.setAppCacheEnabled(True)
        settings.setLoadsImagesAutomatically(True)
        settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        
        # Prevent external browser from opening the URL
        self.webview.setWebViewClient(WebViewClient())
        
        # Set the WebView as the main content view to avoid SDL2/OpenGL conflicts
        activity.setContentView(self.webview)
        
        # Load the target URL
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```