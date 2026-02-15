```python
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window

# Handle Android-specific imports
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    KeyEvent = autoclass('android.view.KeyEvent')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    # Dummy decorator for non-android platforms to prevent crash during dev
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class WebViewContainer(Widget):
    def __init__(self, **kwargs):
        super(WebViewContainer, self).__init__(**kwargs)
        self.webview = None
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        self.webview = WebView(Activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.getSettings().setAllowFileAccess(True)
        self.webview.getSettings().setBuiltInZoomControls(False)
        self.webview.getSettings().setDisplayZoomControls(False)
        self.webview.getSettings().setSupportZoom(False)
        self.webview.setWebViewClient(WebViewClient())
        
        # Set the URL
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
        
        # Layout the WebView to fill the screen
        layout = LinearLayout(Activity)
        layout.addView(self.webview)
        Activity.setContentView(layout)

class TrackingApp(App):
    def build(self):
        self.container = WebViewContainer()
        Window.bind(on_keyboard=self.on_back_button)
        return self.container

    def on_back_button(self, window, key, *args):
        # Handle the Android back button (key 27)
        if key == 27:
            if platform == 'android' and self.container.webview:
                if self.container.webview.canGoBack():
                    self.container.webview.goBack()
                    return True
        return False

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    TrackingApp().run()
```