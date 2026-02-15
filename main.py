```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.utils import platform

# This part handles the Android-specific WebView integration
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy for non-android platforms to prevent import errors during local dev
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class WebViewApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        self.root = BoxLayout()
        # Schedule the WebView creation after the Kivy window is initialized
        Clock.schedule_once(self.create_webview, 0)
        return self.root

    @run_on_ui_thread
    def create_webview(self, *args):
        activity = PythonActivity.mActivity
        
        # Initialize WebView
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setDomStorageEnabled(True)
        webview.getSettings().setDatabaseEnabled(True)
        webview.getSettings().setAppCacheEnabled(True)
        webview.getSettings().setLoadsImagesAutomatically(True)
        webview.getSettings().setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        
        # Prevent opening external browser
        webview.setWebViewClient(WebViewClient())
        
        # Create Layout Params to fill the screen
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
        layout_params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        
        # Load the Target URL
        webview.loadUrl(self.url)
        
        # Add to the Android Activity View
        activity.addContentView(webview, layout_params)
        
        # Store reference to prevent garbage collection and handle back button
        self.webview = webview

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    WebViewApp().run()
```