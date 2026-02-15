```python
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

# Only import android-specific modules if running on Android
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    AndroidColor = autoclass('android.graphics.Color')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy decorator for non-android platforms
    def run_on_ui_thread(func):
        return func

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.webview = None
        # Delay creation to ensure window is initialized
        Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        if platform != 'android':
            print("WebView only supported on Android.")
            return

        activity = PythonActivity.mActivity
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.getSettings().setAllowFileAccess(True)
        self.webview.getSettings().setUserAgentString("Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36")
        self.webview.setWebViewClient(WebViewClient())
        self.webview.setBackgroundColor(AndroidColor.TRANSPARENT)
        
        # Set the WebView as the main view to avoid SDL2/OpenGL conflicts
        activity.setContentView(self.webview)
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

class DeliveryTrackingApp(App):
    def build(self):
        return WebViewWidget()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    DeliveryTrackingApp().run()
```