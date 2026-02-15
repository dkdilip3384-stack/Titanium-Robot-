```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

# Only import android specific modules if running on Android
if platform == 'android':
    from android.run_on_ui_thread import run_on_ui_thread
    from jnius import autoclass
else:
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class MainApp(App):
    def build(self):
        self.root = Widget()
        if platform == 'android':
            Clock.schedule_once(self.create_webview, 0)
        return self.root

    @run_on_ui_thread
    def create_webview(self, *args):
        # Access Android API via Pyjnius
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
        LinearLayout = autoclass('android.view.LinearLayout')
        Color = autoclass('android.graphics.Color')

        activity = PythonActivity.mActivity
        
        # Initialize WebView
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.getSettings().setDatabaseEnabled(True)
        self.webview.setWebViewClient(WebViewClient())
        self.webview.setBackgroundColor(Color.TRANSPARENT)
        
        # Define layout parameters for full screen
        layout_params = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        
        # Add the WebView directly to the activity content view to bypass SDL2 GL conflicts
        activity.addContentView(self.webview, layout_params)
        
        # Load the target URL
        self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

    def on_pause(self):
        if platform == 'android' and hasattr(self, 'webview'):
            self.webview.pauseTimers()
            self.webview.onPause()
        return True

    def on_resume(self):
        if platform == 'android' and hasattr(self, 'webview'):
            self.webview.onResume()
            self.webview.resumeTimers()

if __name__ == '__main__':
    MainApp().run()
```