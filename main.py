from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from android.runnable import run_on_ui_thread
from jnius import autoclass, PythonJavaClass
from kivy.core.window import Window
from android.permissions import request_permissions, Permission
import requests

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
WebChromeClient = autoclass('android.webkit.WebChromeClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

class TitaniumSupreme(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        Window.bind(on_keyboard=self.on_back_button)
        request_permissions([Permission.INTERNET, Permission.ACCESS_FINE_LOCATION, Permission.CAMERA])
        Clock.schedule_once(self.init_webview, 1)
        return BoxLayout()

    @run_on_ui_thread
    def init_webview(self, *args):
        self.webview = WebView(activity)
        s = self.webview.getSettings()
        s.setJavaScriptEnabled(True)
        s.setDomStorageEnabled(True)
        s.setGeolocationEnabled(True)
        s.setMixedContentMode(0) 
        
        class SupremeClient(PythonJavaClass):
            __javainterfaces__ = ['android/webkit/WebViewClient']
            __javacontext__ = 'app'
            def shouldOverrideUrlLoading(self, view, url):
                view.loadUrl(url)
                return True
                
        self.webview.setWebViewClient(SupremeClient())
        self.webview.setWebChromeClient(WebChromeClient())
        self.webview.loadUrl('https://delivery-tracking-delta.vercel.app/')
        activity.setContentView(self.webview)

    def on_back_button(self, window, key, *args):
        if key == 27 and hasattr(self, 'webview') and self.webview.canGoBack():
            self.webview.goBack()
            return True
        return False

if __name__ == '__main__':
    TitaniumSupreme().run()