```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

# Only import android specific modules if running on Android
if platform == 'android':
    from android.runnable import run_on_ui_thread
    from jnius import autoclass
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy decorator for non-android platforms to prevent import errors
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class WebViewApp(App):
    def build(self):
        self.root = Widget()
        return self.root

    def on_start(self):
        if platform == 'android':
            self.create_webview()

    @run_on_ui_thread
    def create_webview(self):
        # Access the underlying Android Activity
        activity = PythonActivity.mActivity
        
        # Create the Native Android WebView
        self.webview = WebView(activity)
        
        # Configure WebView settings for modern web apps (React/Vercel)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setLoadWithOverviewMode(True)
        settings.setUseWideViewPort(True)
        settings.setSupportZoom(True)
        settings.setBuiltInZoomControls(False)
        
        # Prevent opening external browser; stay inside the app
        self.webview.setWebViewClient(WebViewClient())
        
        # Load the specific Vercel URL
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
        
        # Set the WebView as the main view of the activity (avoids SDL2 layer conflicts)
        activity.setContentView(self.webview)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    WebViewApp().run()
```