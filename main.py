from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.clock import Clock

class WebViewApp(App):
    def build(self):
        if platform == 'android':
            Clock.schedule_once(self.init_webview, 0)
        return Widget()

    def init_webview(self, *args):
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        Activity = autoclass('org.kivy.android.PythonActivity').mActivity

        @run_on_ui_thread
        def create_and_show():
            webview = WebView(Activity)
            settings = webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setBuiltInZoomControls(True)
            settings.setDisplayZoomControls(False)
            settings.setSupportZoom(True)
            
            webview.setWebViewClient(WebViewClient())
            webview.loadUrl("https://delivery-tracking-delta.vercel.app/")
            Activity.setContentView(webview)

        create_and_show()

if __name__ == '__main__':
    WebViewApp().run()