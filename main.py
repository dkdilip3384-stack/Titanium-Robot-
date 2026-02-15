```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

class MainApp(App):
    def build(self):
        return Widget()

    def on_start(self):
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)

    def create_webview(self, *args):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Android classes
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        WebSettings = autoclass('android.webkit.WebSettings')
        Activity = autoclass('org.kivy.android.PythonActivity').mActivity

        @run_on_ui_thread
        def setup_webview():
            webview = WebView(Activity)
            settings = webview.getSettings()
            
            # Enable standard web features for modern React/Next.js apps
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setAllowContentAccess(True)
            settings.setDatabaseEnabled(True)
            settings.setJavaScriptCanOpenWindowsAutomatically(True)
            settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
            
            # Use WebViewClient to prevent external browser from opening
            webview.setWebViewClient(WebViewClient())
            
            # Set the webview as the main content view to avoid SDL2 rendering conflicts
            Activity.setContentView(webview)
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
            
            # Attach webview to the app instance to prevent garbage collection
            self.webview = webview

        setup_webview()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```