```python
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform

# Specific imports for Android native WebView integration
if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    KeyEvent = autoclass('android.view.KeyEvent')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    # Dummy decorator for non-android platforms to prevent crash during local testing
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        self.webview = None
        
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        # Initialize native WebView to resolve SDL2 rendering conflicts
        self.webview = WebView(Activity)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setAllowContentAccess(True)
        settings.setDatabaseEnabled(True)
        settings.setUserAgentString("Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Mobile Safari/537.36")
        
        # Ensure links stay inside the app
        self.webview.setWebViewClient(WebViewClient())
        
        # Add to the activity layout directly to bypass SDL surface layering issues
        Activity.setContentView(self.webview)
        self.webview.loadUrl(self.url)

class MainApp(App):
    def build(self):
        self.root_widget = WebViewWidget()
        Window.bind(on_keyboard=self.handle_back_button)
        return self.root_widget

    def handle_back_button(self, window, key, *args):
        # Key 27 is the Android Back Button
        if key == 27:
            if platform == 'android' and self.root_widget.webview:
                if self.root_widget.webview.canGoBack():
                    self.root_widget.webview.goBack()
                    return True 
        return False

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```