```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

class MainApp(App):
    def build(self):
        if platform == 'android':
            Clock.schedule_once(self.init_webview, 0)
        return Widget()

    def init_webview(self, *args):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Android Native Classes
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        WebSettings = autoclass('android.webkit.WebSettings')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity

        @run_on_ui_thread
        def create_and_show():
            # Initialize WebView instance
            webview = WebView(activity)
            settings = webview.getSettings()
            
            # Configure settings to prevent rendering/logic conflicts
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
            settings.setCacheMode(WebSettings.LOAD_DEFAULT)
            
            # Force URL to open inside the app, not in external browser
            webview.setWebViewClient(WebViewClient())
            
            # Use the full activity window to avoid SDL2 surface overlay issues
            activity.setContentView(webview)
            
            # Load the target URL
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

        create_and_show()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```