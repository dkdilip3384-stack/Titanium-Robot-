```python
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class MainApp(App):
    def build(self):
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)
        return None

    @run_on_ui_thread
    def create_webview(self, *args):
        activity = PythonActivity.mActivity
        self.webview = WebView(activity)
        settings = self.webview.getSettings()
        
        # Enable features required for modern web apps
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setDatabaseEnabled(True)
        settings.setAppCacheEnabled(True)
        settings.setLoadWithOverviewMode(True)
        settings.setUseWideViewPort(True)
        settings.setSupportZoom(True)
        settings.setBuiltInZoomControls(True)
        settings.setDisplayZoomControls(False)
        
        # Set a standard User Agent to prevent mobile blocking
        user_agent = "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Mobile Safari/537.36"
        settings.setUserAgentString(user_agent)
        
        self.webview.setWebViewClient(WebViewClient())
        
        # Replace Kivy's SDL2 view with the Native WebView to avoid conflicts
        activity.setContentView(self.webview)
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

    def on_pause(self):
        return True

    def on_resume(self):
        return True

if __name__ == '__main__':
    MainApp().run()
```