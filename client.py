import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebPage


class Client(QWebPage):
    Client.url = ''
    def __init__(self, url):
        Client.url = url
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load())



    @staticmethod
    def on_page_load(self):
        self.app.quit()


client_response = Client("https://google.com")
source = client_response.mainFrame().toHtml()