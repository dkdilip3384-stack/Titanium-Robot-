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
    AndroidColor = autoclass('android.graphics.Color')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.view.ViewGroup$LayoutParams')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    run_on_ui_thread = lambda x: x

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        if platform == 'android':
            self.create_webview()

    @run_on_ui_thread
    def create_webview(self):
        # Create the Android WebView directly to bypass SDL2 overlay conflicts
        webview = WebView(Activity)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setDomStorageEnabled(True)
        webview.getSettings().setAllowFileAccess(True)
        webview.getSettings().setUserAgentString("Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36")
        webview.setWebViewClient(WebViewClient())
        webview.loadUrl('https://delivery-tracking-delta.vercel.app/')
        
        # Set the WebView as the main content view of the Android Activity
        Activity.setContentView(webview)

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