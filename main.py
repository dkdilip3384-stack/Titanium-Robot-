```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.window import Window

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            Clock.schedule_once(self.init_webview, 0)

    def init_webview(self, *args):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Android Classes
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        Activity = autoclass('org.kivy.android.PythonActivity').mActivity

        @run_on_ui_thread
        def create_webview():
            # Initialize WebView instance
            self.webview = WebView(Activity)
            settings = self.webview.getSettings()
            
            # Essential settings for modern web apps
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setLoadsImagesAutomatically(True)
            settings.setDatabaseEnabled(True)
            settings.setSupportZoom(False)
            
            # Prevent opening external browser
            self.webview.setWebViewClient(WebViewClient())
            
            # Map the WebView to the Activity's content view
            Activity.setContentView(self.webview)
            self.webview.loadUrl(self.url)

        create_webview()
        # Bind the back button to handle browser history
        Window.bind(on_keyboard=self.back_handler)

    def back_handler(self, window, key, *args):
        if key == 27:  # Escape/Back key
            from android.runnable import run_on_ui_thread
            @run_on_ui_thread
            def check_back():
                if self.webview.canGoBack():
                    self.webview.goBack()
                else:
                    from jnius import autoclass
                    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
                    Activity.finish()
            check_back()
            return True
        return False

class TrackingApp(App):
    def build(self):
        return WebViewWidget()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    TrackingApp().run()
```