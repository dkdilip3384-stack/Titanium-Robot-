```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.clock import Clock

# Only import android specific modules if running on Android
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
else:
    run_on_ui_thread = lambda x: x

class MainApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        root = BoxLayout()
        if platform != 'android':
            from kivy.uix.label import Label
            root.add_widget(Label(text="WebView is only supported on Android.\nURL: " + self.url))
        return root

    def on_start(self):
        if platform == 'android':
            self.create_webview()

    @run_on_ui_thread
    def create_webview(self):
        activity = PythonActivity.mActivity
        webview = WebView(activity)
        
        # Configure settings to prevent common crashes and JS errors
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setDatabaseEnabled(True)
        settings.setMixedContentMode(0) # MIXED_CONTENT_ALWAYS_ALLOW
        
        # Standard WebViewClient to handle navigation within the widget
        webview.setWebViewClient(WebViewClient())
        
        # Set the WebView as the primary content view to avoid SDL2 rendering conflicts
        activity.setContentView(webview)
        webview.loadUrl(self.url)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```