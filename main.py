```python
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    KeyEvent = autoclass('android.view.KeyEvent')
else:
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class WebViewContainer(Widget):
    def __init__(self, **kwargs):
        super(WebViewContainer, self).__init__(**kwargs)
        self.webview = None
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        activity = PythonActivity.mActivity
        
        self.webview = WebView(activity)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        
        self.webview.setWebViewClient(WebViewClient())
        
        layout = LinearLayout(activity)
        layout.setOrientation(LinearLayout.VERTICAL)
        layout.addView(self.webview, LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        
        activity.setContentView(layout)
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

class MainApp(App):
    def build(self):
        return WebViewContainer()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```