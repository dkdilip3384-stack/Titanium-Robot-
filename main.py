```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.core.window import Window
from kivy.clock import Clock

class WebViewApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            from android.runnable import run_on_ui_thread
            self.init_webview()
        return Widget()

    @run_on_ui_thread
    def init_webview(self):
        from jnius import autoclass
        
        # Accessing Android System Classes
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
        LinearLayout = autoclass('android.widget.LinearLayout')
        
        activity = PythonActivity.mActivity
        
        # Initialize WebView
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.getSettings().setUserAgentString("Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 Mobile Safari/537.36")
        self.webview.setWebViewClient(WebViewClient())
        
        # Prevent SDL2 from conflicting with WebView Layout
        layout = LinearLayout(activity)
        layout.addView(self.webview, LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        activity.setContentView(layout)
        
        self.webview.loadUrl(self.url)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    WebViewApp().run()
```