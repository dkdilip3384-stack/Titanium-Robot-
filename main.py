```python
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock

class MainApp(App):
    def build(self):
        if platform == 'android':
            self.start_webview()
        return None  # Return None because we are overlaying native Android WebView

    def start_webview(self):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Import Android-specific classes via Pyjnius
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        WebSettings = autoclass('android.webkit.WebSettings')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity

        @run_on_ui_thread
        def create_webview():
            # Initialize WebView instance
            webview = WebView(activity)
            settings = webview.getSettings()
            
            # Configure WebView for modern web apps
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setLoadsImagesAutomatically(True)
            settings.setDatabaseEnabled(True)
            settings.setSupportZoom(False)
            
            # Ensure links open inside the app, not in the system browser
            webview.setWebViewClient(WebViewClient())
            
            # Load the target URL
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
            
            # Set the WebView as the primary content view to resolve SDL2 surface conflicts
            activity.setContentView(webview)

        create_webview()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```