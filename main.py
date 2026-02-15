```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from jnius import autoclass
from android.runnable import run_on_ui_thread

# Android classes
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        self.create_webview()

    @run_on_ui_thread
    def create_webview(self):
        activity = PythonActivity.mActivity
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setDomStorageEnabled(True)
        webview.getSettings().setAllowFileAccess(True)
        webview.setWebViewClient(WebViewClient())
        activity.setContentView(webview)
        webview.loadUrl(self.url)

class MainApp(App):
    def build(self):
        return WebViewWidget()

if __name__ == '__main__':
    MainApp().run()
```