```python
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

# Conditionally import Android-specific modules to prevent build-time or desktop-run errors
if platform == 'android':
    from android.runnable import run_on_ui_thread
    from jnius import autoclass
else:
    # Fallback for non-android platforms
    def run_on_ui_thread(func):
        return func

class TitaniumAI(MDApp):
    def build(self):
        # Schedule the webview initialization after the Kivy window is ready
        Clock.schedule_once(self.init_webview, 0)
        # Return a simple widget; the Android native view will overlay/replace this
        return Widget()

    @run_on_ui_thread
    def init_webview(self, *args):
        if platform == 'android':
            # Get the necessary Android classes
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            activity = PythonActivity.mActivity

            # Initialize the WebView
            self.webview = WebView(activity)
            self.webview.getSettings().setJavaScriptEnabled(True)
            self.webview.getSettings().setDomStorageEnabled(True)  # Added for modern web app compatibility
            self.webview.setWebViewClient(WebViewClient())  # Ensures links open inside the app, not a browser
            
            # Load the target URL
            self.webview.loadUrl('https://delivery-tracking-delta.vercel.app/')
            
            # Set the native WebView as the content view of the Android Activity
            activity.setContentView(self.webview)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    TitaniumAI().run()
```