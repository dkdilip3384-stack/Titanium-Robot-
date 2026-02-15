```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.window import Window

class WebViewApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)
        return Widget()

    def create_webview(self, *args):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Android classes
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        WebSettings = autoclass('android.webkit.WebSettings')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity

        @run_on_ui_thread
        def setup_webview():
            webview = WebView(activity)
            settings = webview.getSettings()
            
            # Enable features for modern web apps (React/Vercel)
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setDatabaseEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
            settings.setCacheMode(WebSettings.LOAD_DEFAULT)
            settings.setUserAgentString("Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36")

            # Prevent SDL2/Kivy layout overlap
            webview.setWebViewClient(WebViewClient())
            activity.setContentView(webview)
            webview.loadUrl(self.url)
            
            # Handle Android Back Button
            self.webview = webview
            Window.bind(on_keyboard=self.on_key_down)

        setup_webview()

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 27:  # Back button
            if platform == 'android' and hasattr(self, 'webview'):
                if self.webview.canGoBack():
                    self.webview.goBack()
                    return True
        return False

if __name__ == '__main__':
    WebViewApp().run()
```