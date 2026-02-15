```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

# Only import Android-specific modules if running on Android
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    # Android API classes
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy decorator for non-android platforms to prevent errors
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class MainApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        # We return a dummy widget because we will overlay the native WebView
        root = Widget()
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)
        return root

    @run_on_ui_thread
    def create_webview(self, *args):
        # Get the main activity context
        activity = PythonActivity.mActivity
        
        # Initialize WebView
        self.webview = WebView(activity)
        settings = self.webview.getSettings()
        
        # Configure settings to prevent conflicts and ensure site loads
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setJavaScriptCanOpenWindowsAutomatically(True)
        
        # Set WebViewClient to prevent opening external browser
        self.webview.setWebViewClient(WebViewClient())
        
        # Use a Layout to hold the WebView to ensure proper SDL2 layering
        layout = LinearLayout(activity)
        layout.addView(self.webview, LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        
        # Set the activity content to our native layout
        # This replaces the Kivy SDL2 view with the native Android View
        activity.setContentView(layout)
        
        # Load the target URL
        self.webview.loadUrl(self.url)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```