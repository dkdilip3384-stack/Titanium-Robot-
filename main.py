```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

class WebViewWidget(Widget):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)

    def create_webview(self, *args):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Android Native Classes
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        Activity = autoclass('org.kivy.android.PythonActivity').mActivity
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
        LinearLayout = autoclass('android.widget.LinearLayout')
        Color = autoclass('android.graphics.Color')

        @run_on_ui_thread
        def setup_webview():
            # Create WebView instance
            webview = WebView(Activity)
            webview.getSettings().setJavaScriptEnabled(True)
            webview.getSettings().setDomStorageEnabled(True)
            webview.getSettings().setDatabaseEnabled(True)
            webview.getSettings().setLoadWithOverviewMode(True)
            webview.getSettings().setUseWideViewPort(True)
            webview.getSettings().setSupportZoom(True)
            webview.getSettings().setBuiltInZoomControls(True)
            webview.getSettings().setDisplay_ZoomControls(False)
            webview.setWebViewClient(WebViewClient())
            webview.setBackgroundColor(Color.TRANSPARENT)

            # Create a layout to hold the WebView
            layout = LinearLayout(Activity)
            layout.setOrientation(LinearLayout.VERTICAL)
            
            # Add WebView to Activity view hierarchy
            Activity.addContentView(layout, LayoutParams(-1, -1))
            layout.addView(webview, LayoutParams(-1, -1))
            
            # Load Target URL
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
            
            # Prevent Kivy from capturing touch events over WebView
            self.webview = webview

        setup_webview()

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