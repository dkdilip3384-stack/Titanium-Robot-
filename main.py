```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

class MainApp(App):
    def build(self):
        return Widget()

    def on_start(self):
        if platform == 'android':
            self.init_webview()

    def init_webview(self):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Android classes
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
        LinearLayout = autoclass('android.widget.LinearLayout')
        WebSettings = autoclass('android.webkit.WebSettings')

        @run_on_ui_thread
        def create_webview():
            activity = PythonActivity.mActivity
            
            # Initialize WebView
            webview = WebView(activity)
            settings = webview.getSettings()
            
            # Configure settings to prevent rendering/JS conflicts
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setDatabaseEnabled(True)
            settings.setUseWideViewPort(True)
            settings.setLoadWithOverviewMode(True)
            settings.setSupportZoom(True)
            settings.setBuiltInZoomControls(True)
            settings.setDisplayZoomControls(False)
            
            # Keep navigation inside the app
            webview.setWebViewClient(WebViewClient())
            
            # Create a layout to hold the webview and set it as content view
            # This bypasses SDL2 rendering conflicts for the web container
            layout = LinearLayout(activity)
            layout.setOrientation(LinearLayout.VERTICAL)
            activity.setContentView(layout)
            layout.addView(webview, LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
            
            # Load the specific URL
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

        create_webview()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```