```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.clock import Clock

class WebViewApp(App):
    def build(self):
        return BoxLayout()

    def on_start(self):
        if platform == 'android':
            self.start_android_webview()

    def start_android_webview(self):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Android API Imports
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        Activity = autoclass('org.kivy.android.PythonActivity').mActivity
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
        LinearLayout = autoclass('android.widget.LinearLayout')

        @run_on_ui_thread
        def create_webview():
            # Initialize WebView
            webview = WebView(Activity)
            settings = webview.getSettings()
            
            # Enable standard web features to avoid loading failures
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setDatabaseEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
            settings.setSupportZoom(True)
            settings.setBuiltInZoomControls(True)
            settings.setDisplayZoomControls(False)
            
            # Prevent opening external browser
            webview.setWebViewClient(WebViewClient())
            
            # Create a layout to hold the WebView
            layout = LinearLayout(Activity)
            layout.setOrientation(LinearLayout.VERTICAL)
            layout.addView(webview, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
            
            # Attach to the main Android Activity window
            Activity.setContentView(layout)
            
            # Load the specific URL
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

        create_webview()

if __name__ == '__main__':
    WebViewApp().run()
```