import os
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from android.runnable import run_on_ui_thread
from jnius import autoclass, cast, PythonJavaClass
from kivy.core.window import Window
from android.permissions import request_permissions, Permission

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
WebChromeClient = autoclass('android.webkit.WebChromeClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

class TitaniumV45GodBot(App):
    def build(self):
        Window.bind(on_keyboard=self.on_back_button)
        self.root_layout = BoxLayout(orientation='vertical', padding=40)
        self.dialogue_label = Label(
            text='வணக்கம் திலீப் குமார்!\nஉங்கள் சிஸ்டம் தயாராகிறது...',
            halign='center', valign='middle', font_size='18sp',
            color=(0, 0.9, 1, 1), text_size=(Window.width * 0.8, None)
        )
        self.root_layout.add_widget(self.dialogue_label)
        request_permissions([Permission.INTERNET, Permission.ACCESS_FINE_LOCATION, Permission.CAMERA])
        Clock.schedule_once(self.init_webview, 2.5)
        return self.root_layout

    @run_on_ui_thread
    def init_webview(self, *args):
        self.webview = WebView(activity)
        s = self.webview.getSettings()
        s.setJavaScriptEnabled(True)
        s.setDomStorageEnabled(True)
        s.setGeolocationEnabled(True)
        s.setMixedContentMode(0) 
        
        class MyClient(PythonJavaClass):
            __javainterfaces__ = ['android/webkit/WebViewClient']
            __javacontext__ = 'app'
            def shouldOverrideUrlLoading(self, view, url):
                view.loadUrl(url) 
                return True
                
        self.webview.setWebViewClient(WebViewClient())
        self.webview.setWebChromeClient(WebChromeClient())
        self.webview.loadUrl('https://delivery-tracking-delta.vercel.app/')
        activity.setContentView(self.webview)

    def on_back_button(self, window, key, *args):
        if key == 27 and hasattr(self, 'webview') and self.webview.canGoBack():
            self.webview.goBack()
            return True
        return False

if __name__ == '__main__':
    TitaniumV45GodBot().run()