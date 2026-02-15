```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform
from jnius import autoclass, cast

# Android-specific imports
if platform == 'android':
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    AndroidActivity = autoclass('org.kivy.android.PythonActivity')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    WebSettings = autoclass('android.webkit.WebSettings')
else:
    # Dummy for non-android testing
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
        activity = AndroidActivity.mActivity
        
        # Create the WebView
        self.webview = WebView(activity)
        
        # Configure settings for modern web apps (Vercel/React/Next.js)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        settings.setUserAgentString("Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36")
        
        # Prevent opening in external browser
        self.webview.setWebViewClient(WebViewClient())
        
        # Add to the Android view hierarchy
        layout_params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        activity.addContentView(self.webview, layout_params)
        
        # Load the target URL
        self.webview.loadUrl(self.url)

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