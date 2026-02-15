```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.logger import Logger
from android.runnable import run_on_ui_thread
from jnius import autoclass

# Android native classes
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
LinearLayout = autoclass('android.widget.LinearLayout')
Activity = autoclass('org.kivy.android.PythonActivity').mActivity

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.webview = None
        # Schedule the creation on the next frame to ensure the window is ready
        Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        # Create the native WebView
        self.webview = WebView(Activity)
        
        # Configure WebView Settings for modern web apps (Vercel/React/Next.js)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setDatabaseEnabled(True)
        settings.setUserAgentString("Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Mobile Safari/537.36")
        
        # Prevent opening in external browser
        self.webview.setWebViewClient(WebViewClient())
        
        # Add the WebView to the Activity's content view
        # This replaces the Kivy SDL2 layout to prevent rendering conflicts
        Activity.setContentView(self.webview, LayoutParams(
            LayoutParams.MATCH_PARENT, 
            LayoutParams.MATCH_PARENT
        ))
        
        # Load the target URL
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

class MainApp(App):
    def build(self):
        return WebViewWidget()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```