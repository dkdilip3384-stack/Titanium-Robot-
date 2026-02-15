```python
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock

class MainApp(App):
    def build(self):
        if platform == 'android':
            from jnius import autoclass
            from android.runnable import run_on_ui_thread

            # Android classes
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity

            @run_on_ui_thread
            def setup_webview():
                webview = WebView(activity)
                settings = webview.getSettings()
                settings.setJavaScriptEnabled(True)
                settings.setDomStorageEnabled(True)
                settings.setAllowFileAccess(True)
                settings.setBuiltInZoomControls(False)
                settings.setDisplayZoomControls(False)
                settings.setSupportZoom(False)
                
                # Prevent SDL2 surface from blocking the WebView
                webview.setWebViewClient(WebViewClient())
                webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
                
                # Set the WebView as the main content view of the activity
                activity.setContentView(webview)

            setup_webview()
        return None

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```