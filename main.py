```python
import kivy
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class WebViewApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            self.create_webview()
        return None

    @run_on_ui_thread
    def create_webview(self):
        activity = PythonActivity.mActivity
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setDomStorageEnabled(True)
        webview.getSettings().setAllowFileAccess(True)
        webview.setWebViewClient(WebViewClient())
        
        layout = LinearLayout(activity)
        layout.setOrientation(LinearLayout.VERTICAL)
        layout.addView(webview, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
        
        activity.setContentView(layout)
        webview.loadUrl(self.url)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    WebViewApp().run()
```