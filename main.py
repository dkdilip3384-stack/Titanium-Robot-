```python
import os
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.widget import Widget

# Attempt to import jnius for Android native WebView
if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy decorator for non-android platforms
    def run_on_ui_thread(func):
        return func

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        self.webview = None
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        activity = PythonActivity.mActivity
        
        # Initialize WebView
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.getSettings().setAllowFileAccess(True)
        self.webview.getSettings().setDatabaseEnabled(True)
        self.webview.setWebViewClient(WebViewClient())
        
        # Layout parameters to fill the screen
        layout_params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        
        # Add to the activity layout
        activity.addContentView(self.webview, layout_params)
        self.webview.loadUrl(self.url)

    def on_size(self, *args):
        # Handle orientation changes if necessary
        pass

class DeliveryTrackerApp(App):
    def build(self):
        return WebViewWidget()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    DeliveryTrackerApp().run()
```