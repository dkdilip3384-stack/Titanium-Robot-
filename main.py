```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy wrapper for non-android platforms to prevent import errors
    def run_on_ui_thread(func):
        return func

class WebViewApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)
        return Widget()

    @run_on_ui_thread
    def create_webview(self, *args):
        activity = PythonActivity.mActivity
        webview = WebView(activity)
        settings = webview.getSettings()
        
        # Enable essential features for modern web apps
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        
        # Prevent opening in external browser
        webview.setWebViewClient(WebViewClient())
        
        # Set the WebView as the main content view to avoid SDL2 conflicts
        activity.setContentView(webview)
        webview.loadUrl(self.url)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    WebViewApp().run()
```