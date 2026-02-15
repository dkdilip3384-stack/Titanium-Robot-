```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

# Only import Android specific modules if running on Android
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    # Mock for desktop testing
    def run_on_ui_thread(func):
        return func

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            self.create_webview()

    @run_on_ui_thread
    def create_webview(self):
        # Create the Native Android WebView
        self.webview = WebView(Activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.setWebViewClient(WebViewClient())
        
        # Build the Layout
        layout = LinearLayout(Activity)
        layout.setOrientation(LinearLayout.VERTICAL)
        layout.addView(self.webview, LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        
        # Set as the main view to prevent SDL2/OpenGL conflicts
        Activity.setContentView(layout)
        self.webview.loadUrl(self.url)

class TrackingApp(App):
    def build(self):
        return WebViewWidget()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    TrackingApp().run()
```