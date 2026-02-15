```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

# Conditional imports to prevent crashes on non-Android systems during dev
if platform == 'android':
    from android.run_on_ui_thread import run_on_ui_thread
    from jnius import autoclass, cast
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy decorator for desktop testing
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class MainApp(App):
    def build(self):
        self.webview = None
        # Schedule the WebView creation after the Kivy window is ready
        Clock.schedule_once(self.create_webview, 0)
        return Widget()

    @run_on_ui_thread
    def create_webview(self, *args):
        # Access the Android Activity
        activity = PythonActivity.mActivity
        
        # Initialize WebView
        webview = WebView(activity)
        settings = webview.getSettings()
        
        # Standard configuration for modern web apps
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setJavaScriptCanOpenWindowsAutomatically(True)
        settings.setDatabaseEnabled(True)
        
        # Ensure links stay inside the app
        webview.setWebViewClient(WebViewClient())
        
        # Load the target URL
        webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
        
        # Set the layout and add to activity
        layout = LinearLayout(activity)
        layout.addView(webview, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
        activity.setContentView(layout)
        
        # Keep a reference
        self.webview = webview

    def on_pause(self):
        # Prevent the app from closing when switched to background
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```