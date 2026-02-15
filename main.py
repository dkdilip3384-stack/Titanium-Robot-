```python
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread
    
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    LinearLayout = autoclass('android.widget.LinearLayout')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
else:
    run_on_ui_thread = lambda x: x

class WebViewWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(WebViewWidget, self).__init__(**kwargs)
        self.url = "https://delivery-tracking-delta.vercel.app/"
        if platform == 'android':
            self.create_webview()
        else:
            from kivy.uix.label import Label
            self.add_widget(Label(text="WebView only supported on Android.\nURL: " + self.url))

    @run_on_ui_thread
    def create_webview(self):
        self.webview = WebView(Activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.getSettings().setAllowFileAccess(True)
        self.webview.setWebViewClient(WebViewClient())
        
        layout = LinearLayout(Activity)
        layout.addView(self.webview)
        
        Activity.setContentView(layout)
        self.webview.loadUrl(self.url)

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