```python
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

# Only import android specific modules if running on Android
if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    # Dummy decorator for non-android platforms
    def run_on_ui_thread(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

class MainApp(App):
    def build(self):
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            # Run the WebView initialization on the Android UI Thread to avoid SDL2 conflicts
            Clock.schedule_once(self.create_webview, 0)
        return None  # Return None because we are replacing the view with a native component

    @run_on_ui_thread
    def create_webview(self, *args):
        self.webview = WebView(Activity)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setDatabaseEnabled(True)
        settings.setUserAgentString("Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36")
        
        # This prevents the URL from opening in an external browser
        self.webview.setWebViewClient(WebViewClient())
        
        # Set the WebView as the main view of the Android Activity
        Activity.setContentView(self.webview)
        self.webview.loadUrl(self.url)
        
        # Bind the back button to navigate the WebView history
        Window.bind(on_keyboard=self.back_handler)

    def back_handler(self, window, key, scancode, codepoint, modifier):
        if key == 27:  # 27 is the code for the 'Back' button
            if platform == 'android':
                if self.webview.canGoBack():
                    self.webview.goBack()
                    return True
        return False

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```