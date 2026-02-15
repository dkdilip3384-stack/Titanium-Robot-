```python
import sys
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform

class DeliveryTrackerApp(App):
    def build(self):
        if platform == 'android':
            self.init_webview()
        return None

    def init_webview(self):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Native Android imports via Pyjnius
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity

        @run_on_ui_thread
        def create_webview():
            # Create the native WebView instance
            self.webview = WebView(activity)
            
            # Configure WebView settings to prevent rendering and JS errors
            settings = self.webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setLoadWithOverviewMode(True)
            settings.setUseWideViewPort(True)
            settings.setSupportZoom(True)
            settings.setBuiltInZoomControls(True)
            settings.setDisplayZoomControls(False)
            
            # Set the Client to handle internal navigation
            self.webview.setWebViewClient(WebViewClient())
            
            # Load your specific URL
            self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
            
            # Set the WebView as the main view of the Android Activity 
            # This bypasses SDL2 texture conflicts by overlaying the native UI
            activity.setContentView(self.webview)

        create_webview()
        # Bind back button to allow navigating back in web history
        Window.bind(on_keyboard=self.back_button_handler)

    def back_button_handler(self, window, key, *args):
        if key == 27:  # Android Back Button
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