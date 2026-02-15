```python
from kivy.app import App
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.clock import Clock

class WebViewApp(App):
    def build(self):
        if platform == 'android':
            # Delay the WebView creation to ensure the window is initialized
            Clock.schedule_once(self.create_webview, 0)
        return Widget()

    def create_webview(self, *args):
        from android.runnable import run_on_ui_thread
        from jnius import autoclass

        @run_on_ui_thread
        def _setup_webview():
            # Get Android system classes
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity

            # Initialize WebView instance
            webview = WebView(activity)
            
            # Configure settings to prevent SDL2 conflicts and support modern JS
            settings = webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setDatabaseEnabled(True)
            settings.setLoadWithOverviewMode(True)
            settings.setUseWideViewPort(True)
            settings.setSupportZoom(True)
            settings.setBuiltInZoomControls(True)
            settings.setDisplayZoomControls(False)
            
            # Set WebViewClient to handle navigation within the widget
            webview.setWebViewClient(WebViewClient())
            
            # Use the activity's main content view to display the WebView
            # This bypasses SDL2 rendering issues for pure web apps
            activity.setContentView(webview)
            
            # Load the target URL
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

        _setup_webview()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    WebViewApp().run()
```