```python
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

class MainApp(App):
    def build(self):
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)
        return None

    def create_webview(self, *args):
        from jnius import autoclass
        from android.run_on_ui_thread import run_on_ui_thread

        # Import Android Native Classes
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        WebSettings = autoclass('android.webkit.WebSettings')
        activity = PythonActivity.mActivity

        @run_on_ui_thread
        def setup_webview():
            webview = WebView(activity)
            settings = webview.getSettings()
            
            # Enable features for modern web apps
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setDatabaseEnabled(True)
            settings.setLoadsImagesAutomatically(True)
            settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
            
            # Prevent opening in external browser
            webview.setWebViewClient(WebViewClient())
            
            # Load URL
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
            
            # Set as the primary view to bypass SDL2 rendering conflicts
            activity.setContentView(webview)
            self.webview = webview

        setup_webview()

    def on_pause(self):
        # Necessary to prevent app termination on background
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```