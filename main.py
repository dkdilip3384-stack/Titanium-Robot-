from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from android.runnable import run_on_ui_thread
from jnius import autoclass, PythonJavaClass

WebView = autoclass('android.webkit.WebView')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

class TitaniumAI(MDApp):
    def build(self):
        Clock.schedule_once(self.init_webview, 0.5)
        return BoxLayout()

    @run_on_ui_thread
    def init_webview(self, *args):
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.loadUrl('https://delivery-tracking-delta.vercel.app/')
        activity.setContentView(self.webview)

if __name__ == '__main__':
    TitaniumAI().run()