```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

# Configuration for Android-specific components
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    
    # Android Classes
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy decorator for non-android platforms
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class MainWidget(Widget):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.webview = None
        # Delay creation to ensure the window is initialized
        Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        if platform == 'android':
            activity = PythonActivity.mActivity
            self.webview = WebView(activity)
            
            # Configure WebView Settings for modern web apps (Vercel/Next.js compatibility)
            settings = self.webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setDatabaseEnabled(True)
            settings.setUserAgentString("Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36")
            
            # Set Client to handle internal navigation
            self.webview.setWebViewClient(WebViewClient())
            
            # Load Target URL
            self.webview.loadUrl('https://delivery-tracking-delta.vercel.app/')
            
            # This line solves SDL2 conflicts by setting the WebView as the primary activity view
            activity.setContentView(self.webview)

class DeliveryTrackerApp(App):
    def build(self):
        return MainWidget()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    DeliveryTrackerApp().run()
```