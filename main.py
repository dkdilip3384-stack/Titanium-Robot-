```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from android.run_on_ui_thread import run_on_ui_thread
from jnius import autoclass

# Android classes
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
Activity = autoclass('org.kivy.android.PythonActivity').mActivity

class AndroidWebView:
    def __init__(self, url):
        self.url = url
        self.webview = None
        self.create_webview()

    @run_on_ui_thread
    def create_webview(self):
        self.webview = WebView(Activity)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDatabaseEnabled(True)
        settings.setLoadWithOverviewMode(True)
        settings.setUseWideViewPort(True)
        settings.setSupportZoom(True)
        settings.setBuiltInZoomControls(True)
        settings.setDisplayZoomControls(False)
        
        self.webview.setWebViewClient(WebViewClient())
        Activity.setContentView(self.webview)
        self.webview.loadUrl(self.url)

class MainApp(App):
    def build(self):
        # We trigger the WebView creation immediately
        self.webview_handler = AndroidWebView("https://delivery-tracking-delta.vercel.app/")
        return Widget() # Return an empty widget as WebView takes over the Activity view

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```