```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

class MainApp(App):
    def build(self):
        if platform == 'android':
            from jnius import autoclass
            # Access Android Native Classes
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            LinearLayout = autoclass('android.widget.LinearLayout')
            LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
            
            self.activity = PythonActivity.mActivity
            
            # Use Clock to ensure we run on the UI Thread to prevent SDL2 conflicts
            Clock.schedule_once(self.create_webview, 0)
        return Widget()

    def create_webview(self, *args):
        from jnius import autoclass
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        LinearLayout = autoclass('android.widget.LinearLayout')
        
        # Initialize WebView
        self.webview = WebView(self.activity)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDatabaseEnabled(True)
        settings.setAppCacheEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setAllowContentAccess(True)
        settings.setLoadWithOverviewMode(True)
        settings.setUseWideViewPort(True)
        
        # Prevent opening in external browser
        self.webview.setWebViewClient(WebViewClient())
        
        # Create a layout to hold the WebView natively over the SDL2 surface
        layout = LinearLayout(self.activity)
        self.activity.setContentView(layout)
        layout.addView(self.webview)
        
        # Load the target URL
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

    def on_pause(self):
        # Prevent the app from closing when backgrounded
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```