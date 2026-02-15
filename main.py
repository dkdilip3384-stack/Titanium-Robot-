```python
import kivy
from kivy.app import App
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window

# Logic for Android Native WebView to avoid SDL2 conflicts
if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    android_activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    # Fallback for desktop testing
    run_on_ui_thread = lambda x: x

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        self.webview = WebView(android_activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.getSettings().setDatabaseEnabled(True)
        self.webview.getSettings().setAllowFileAccess(True)
        self.webview.setWebViewClient(WebViewClient())
        self.webview.loadUrl(self.url)
        android_activity.setContentView(self.webview)

class DeliveryTrackerApp(App):
    def build(self):
        self.bind(on_start=self.post_build)
        return WebViewWidget()

    def post_build(self, *args):
        if platform == 'android':
            Window.bind(on_keyboard=self.back_handler)

    def back_handler(self, window, key, *args):
        # Handle Android back button to navigate webview history
        if key == 27:
            if platform == 'android':
                self.check_back_history()
                return True
        return False

    @run_on_ui_thread
    def check_back_history(self):
        # Logic to go back in browser instead of closing app
        view = App.get_running_app().root.webview
        if view.canGoBack():
            view.goBack()
        else:
            android_activity.finish()

if __name__ == '__main__':
    DeliveryTrackerApp().run()
```