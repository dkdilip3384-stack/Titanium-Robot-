```python
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform

# Global reference for the webview to prevent garbage collection
webview = None

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    # Android class imports
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    
    class AndroidWebView:
        def __init__(self, url):
            self.url = url
            self.create_webview()

        @run_on_ui_thread
        def create_webview(self):
            global webview
            webview = WebView(Activity)
            settings = webview.getSettings()
            
            # Enable core features for modern web apps
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setLoadsImagesAutomatically(True)
            settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
            settings.setSupportZoom(True)
            settings.setBuiltInZoomControls(True)
            settings.setDisplayZoomControls(False)
            
            # Handle page navigation within the webview
            webview.setWebViewClient(WebViewClient())
            
            # Create a layout to house the webview
            layout = LinearLayout(Activity)
            layout.setOrientation(LinearLayout.VERTICAL)
            layout.addView(webview, LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
            
            # Set the activity's content view to our webview layout
            # This bypasses SDL2 drawing issues by making the WebView the primary view
            Activity.setContentView(layout)
            webview.loadUrl(self.url)

        @run_on_ui_thread
        def on_resume(self):
            if webview:
                webview.onResume()

        @run_on_ui_thread
        def on_pause(self):
            if webview:
                webview.onPause()

class DeliveryTrackerApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            self.webview_handler = AndroidWebView(self.url)
        return Widget() # Return empty widget as WebView replaces UI

    def on_pause(self):
        if platform == 'android' and hasattr(self, 'webview_handler'):
            self.webview_handler.on_pause()
        return True

    def on_resume(self):
        if platform == 'android' and hasattr(self, 'webview_handler'):
            self.webview_handler.on_resume()

if __name__ == '__main__':
    DeliveryTrackerApp().run()
```