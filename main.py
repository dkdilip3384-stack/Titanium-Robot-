```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

# Only attempt to import android-specific libraries if running on Android
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
else:
    # Fallback for desktop testing (will not show WebView)
    run_on_ui_thread = lambda x: x

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.webview = None
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        # Initialize WebView
        self.webview = WebView(Activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.setWebViewClient(WebViewClient())
        
        # Create a layout container to hold the WebView
        layout = LinearLayout(Activity)
        layout.addView(self.webview, LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        
        # Set the content view of the Android Activity
        Activity.setContentView(layout)
        
        # Load the target URL
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

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