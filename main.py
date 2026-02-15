from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from android.runnable import run_on_ui_thread
from jnius import autoclass, PythonJavaClass
from kivy.core.window import Window
from android.permissions import request_permissions, Permission

# Android Components
WebView = autoclass('android.webkit.WebView')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

class TitaniumFinal(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber" # Victory Gold
        Window.bind(on_keyboard=self.on_back_button)
        request_permissions([Permission.INTERNET])
        Clock.schedule_once(self.init_webview, 0.5)
        return BoxLayout()

    @run_on_ui_thread
    def init_webview(self, *args):
        self.webview = WebView(activity)
        s = self.webview.getSettings()
        s.setJavaScriptEnabled(True)
        s.setDomStorageEnabled(True)
        s.setDatabaseEnabled(True)
        s.setGeolocationEnabled(True)
        s.setAllowFileAccess(True)
        s.setMixedContentMode(0) 
        
        class WebClient(PythonJavaClass):
            __javainterfaces__ = ['android/webkit/WebViewClient']
            __javacontext__ = 'app'
            def shouldOverrideUrlLoading(self, view, url):
                view.loadUrl(url)
                return True
                
        self.webview.setWebViewClient(WebClient())
        self.webview.loadUrl('https://delivery-tracking-delta.vercel.app/')
        activity.setContentView(self.webview)

    def on_back_button(self, window, key, *args):
        if key == 27 and hasattr(self, 'webview') and self.webview.canGoBack():
            self.webview.goBack()
            return True
        return False

if __name__ == '__main__':
    TitaniumFinal().run()