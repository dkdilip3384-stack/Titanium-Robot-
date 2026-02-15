```python
from kivy.app import App
from kivy.utils import platform
from kivy.core.window import Window

class DeliveryTrackerApp(App):
    def build(self):
        # Setting a background color to prevent SDL2 black screen issues
        Window.clearcolor = (1, 1, 1, 1)
        return None

    def on_start(self):
        if platform == 'android':
            from jnius import autoclass
            from android.runnable import run_on_ui_thread

            # Android classes
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            Activity = autoclass('org.kivy.android.PythonActivity').mActivity

            @run_on_ui_thread
            def setup_webview():
                # Initialize WebView
                webview = WebView(Activity)
                settings = webview.getSettings()
                
                # Critical settings for modern web apps (Vercel/React/etc)
                settings.setJavaScriptEnabled(True)
                settings.setDomStorageEnabled(True)
                settings.setAllowFileAccess(True)
                settings.setLoadsImagesAutomatically(True)
                settings.setDatabaseEnabled(True)
                
                # Prevent opening links in external browser
                webview.setWebViewClient(WebViewClient())
                
                # Load URL
                webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
                
                # Overlay the WebView onto the Kivy Activity
                Activity.setContentView(webview)

            setup_webview()

if __name__ == '__main__':
    DeliveryTrackerApp().run()
```