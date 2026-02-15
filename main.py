```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

class WebViewApp(App):
    def build(self):
        return Widget()

    def on_start(self):
        if platform == 'android':
            self.init_webview()

    def init_webview(self):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Android Native Classes
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
        LinearLayout = autoclass('android.widget.LinearLayout')
        
        activity = PythonActivity.mActivity

        @run_on_ui_thread
        def create_webview_task():
            # Create WebView instance
            webview = WebView(activity)
            
            # Configure WebView Settings
            settings = webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setLoadWithOverviewMode(True)
            settings.setUseWideViewPort(True)
            settings.setSupportZoom(True)
            settings.setBuiltInZoomControls(True)
            settings.setDisplayZoomControls(False)
            
            # Prevent opening in external browser
            webview.setWebViewClient(WebViewClient())
            
            # Load the specific URL
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
            
            # Add WebView to the Activity's layout without destroying SDL2 surface
            layout = LinearLayout(activity)
            activity.addContentView(webview, LayoutParams(-1, -1))
            
            self.webview = webview

        create_webview_task()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    WebViewApp().run()
```