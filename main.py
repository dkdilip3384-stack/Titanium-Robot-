```python
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock
from kivy.logger import Logger

# On Android, we bridge to the native Android WebView using Pyjnius
# This bypasses SDL2 rendering conflicts by placing the native view over the SDL2 window
if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    KeyEvent = autoclass('android.view.KeyEvent')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    # Dummy for non-android platforms to prevent crash during dev
    def run_on_ui_thread(func):
        return func

class WebViewContainer(Widget):
    def __init__(self, **kwargs):
        super(WebViewContainer, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        self.webview = None
        if platform == 'android':
            self.create_webview()

    @run_on_ui_thread
    def create_webview(self):
        activity = PythonActivity.mActivity
        
        # Initialize WebView
        self.webview = WebView(activity)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDatabaseEnabled(True)
        settings.setAppCacheEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setLoadsImagesAutomatically(True)
        settings.setSupportZoom(True)
        settings.setBuiltInZoomControls(True)
        settings.setDisplayZoomControls(False)
        
        # Prevent opening in external browser
        self.webview.setWebViewClient(WebViewClient())
        
        # Set layout parameters to fill the screen
        layout_params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        
        # Add WebView directly to the activity content
        activity.addContentView(self.webview, layout_params)
        self.webview.loadUrl(self.url)

    @run_on_ui_thread
    def on_back_button(self):
        if self.webview and self.webview.canGoBack():
            self.webview.goBack()
            return True
        return False

class DeliveryTrackerApp(App):
    def build(self):
        self.root_widget = WebViewContainer()
        return self.root_widget

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def _on_keyboard_handler(self, window, key, scancode, codepoint, modifier):
        # Handle Android back button (key 27)
        if key == 27:
            if self.root_widget.on_back_button():
                return True
        return False

if __name__ == '__main__':
    app = DeliveryTrackerApp()
    from kivy.core.window import Window
    Window.bind(on_keyboard=app._on_keyboard_handler)
    app.run()
```