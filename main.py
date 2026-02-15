```python
from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    run_on_ui_thread = lambda x: x

class WebViewApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)
        return Label(text="Loading WebView...")

    @run_on_ui_thread
    def create_webview(self, *args):
        activity = PythonActivity.mActivity
        webview = WebView(activity)
        settings = webview.getSettings()
        
        # Essential settings to fix rendering and script conflicts
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        
        # Prevent opening external browser
        webview.setWebViewClient(WebViewClient())
        
        # Set as main content view to override SDL2 window conflicts
        activity.setContentView(webview)
        webview.loadUrl(self.url)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    WebViewApp().run()
```