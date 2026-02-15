```python
from kivy.app import App
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.clock import Clock

class DeliveryTrackerApp(App):
    def build(self):
        # Return a simple widget as a base to keep Kivy alive
        return Widget()

    def on_start(self):
        if platform == 'android':
            self.init_android_webview()

    def init_android_webview(self):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Reference Android system classes
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity

        @run_on_ui_thread
        def create_webview():
            # Initialize WebView and settings
            webview = WebView(activity)
            settings = webview.getSettings()
            
            # Enable standard web features
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setAllowContentAccess(True)
            settings.setDatabaseEnabled(True)
            settings.setUseWideViewPort(True)
            settings.setLoadWithOverviewMode(True)
            
            # Prevent SDL2/Kivy surface from overlaying or conflicting
            webview.setWebViewClient(WebViewClient())
            
            # Set the WebView as the primary content view of the Android Activity
            # This bypasses SDL2 rendering conflicts for the UI
            activity.setContentView(webview)
            
            # Load the target URL
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

        create_webview()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    DeliveryTrackerApp().run()
```