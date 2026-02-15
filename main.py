```python
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from jnius import autoclass, cast

# Android Native imports
PythonActivity = autoclass('org.kivy.android.PythonActivity')
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
LinearLayout = autoclass('android.widget.LinearLayout')

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        Clock.schedule_once(self.create_webview, 0)

    def create_webview(self, *args):
        activity = PythonActivity.mActivity
        
        # Initialize WebView
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.getSettings().setDatabaseEnabled(True)
        self.webview.getSettings().setAllowFileAccess(True)
        self.webview.getSettings().setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        
        # Set WebViewClient to prevent external browser opening
        self.webview.setWebViewClient(WebViewClient())
        
        # Layout parameters to fill screen
        layout_params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        
        # Create a native layout to hold the WebView
        self.layout = LinearLayout(activity)
        self.layout.addView(self.webview, layout_params)
        
        # Add to the activity content view
        activity.addContentView(self.layout, layout_params)
        
        # Load the URL
        self.webview.loadUrl(self.url)

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