```python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

class MainApp(App):
    def build(self):
        if platform == 'android':
            from jnius import autoclass
            from android.runnable import run_on_ui_thread

            # Native Android Classes
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            Activity = autoclass('org.kivy.android.PythonActivity').mActivity
            LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
            LinearLayout = autoclass('android.widget.LinearLayout')
            Color = autoclass('android.graphics.Color')

            @run_on_ui_thread
            def create_webview():
                # Initialize WebView
                self.webview = WebView(Activity)
                self.webview.getSettings().setJavaScriptEnabled(True)
                self.webview.getSettings().setDomStorageEnabled(True)
                self.webview.getSettings().setDatabaseEnabled(True)
                self.webview.setWebViewClient(WebViewClient())
                self.webview.setBackgroundColor(Color.TRANSPARENT)
                
                # Create a layout to house the WebView
                layout = LinearLayout(Activity)
                layout.setOrientation(LinearLayout.VERTICAL)
                layout.addView(self.webview, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
                
                # Set the layout as the main content view to bypass SDL2 rendering conflicts
                Activity.setContentView(layout)
                
                # Load the URL
                self.webview.loadUrl("https://delivery-tracking-delta.vercel.app/")

            create_webview()
        
        # Return an empty widget as the Kivy root; the native WebView sits on top
        return Widget()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    MainApp().run()
```