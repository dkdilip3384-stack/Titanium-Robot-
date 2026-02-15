```python
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import platform
from kivy.core.window import Window

class DeliveryTrackerApp(App):
    def build(self):
        # Create a basic layout; on Android, the WebView will overlay this.
        return FloatLayout()

    def on_start(self):
        if platform == 'android':
            self.init_android_webview()

    def init_android_webview(self):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Standard Android/Kivy classes
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        WebSettings = autoclass('android.webkit.WebSettings')
        
        activity = PythonActivity.mActivity

        @run_on_ui_thread
        def create_webview():
            # Initialize WebView instance
            webview = WebView(activity)
            settings = webview.getSettings()
            
            # Enable essential features for modern web apps
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setLoadsImagesAutomatically(True)
            settings.setDatabaseEnabled(True)
            settings.setSupportZoom(True)
            settings.setBuiltInZoomControls(True)
            settings.setDisplayZoomControls(False)
            
            # Prevent external browser from opening links
            webview.setWebViewClient(WebViewClient())
            
            # Force the WebView to occupy the full Activity screen to avoid SDL2 conflicts
            activity.setContentView(webview)
            
            # Load target URL
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
            
            # Store reference for back button handling
            self.webview = webview

        create_webview()
        Window.bind(on_keyboard=self.on_back_button)

    def on_back_button(self, window, key, *args):
        # Handle Android physical back button (Key code 27)
        if key == 27:
            if platform == 'android' and hasattr(self, 'webview'):
                if self.webview.canGoBack():
                    self.webview.goBack()
                    return True
        return False

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    DeliveryTrackerApp().run()
```