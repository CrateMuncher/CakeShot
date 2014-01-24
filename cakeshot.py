from PySide import QtCore, QtGui
import sys
import time
import imguruploader
import selectionselector
import settings


class CakeShot(QtGui.QSystemTrayIcon):
    uploaders = [imguruploader.ImgurUploader]
    def __init__(self):
        QtGui.QSystemTrayIcon.__init__(self)
        self.setIcon(QtGui.QIcon("icon/cakeshot.png"))

        self.menu = QtGui.QMenu()
        self.take_screenshot_item = self.menu.addAction("Take Screenshot\tPlaceholder")
        self.take_screenshot_item.triggered.connect(self.take_screenshot)

        self.open_settings_item = self.menu.addAction("Settings")
        self.open_settings_item.triggered.connect(self.open_settings)

        self.setContextMenu(self.menu)

        self.show()

    def pre_take_screenshot(self):
        timer = QtCore.QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.take_screenshot)
        timer.start(1000)

    def take_screenshot(self):
        desktop = QtGui.QApplication.desktop()
        print desktop.childAt(QtCore.QPoint(100, 100))

        self.selector = selectionselector.SelectionSelector()
        self.selector.selection_made.connect(self.selection_made)
        self.selector.select()

    def selection_made(self, rect):
        sound = QtGui.QSound("snd/shutter.wav")
        sound.play()

        screenshot = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), rect.x(), rect.y(), rect.width(),
                                              rect.height())

        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QBuffer.ReadWrite)
        screenshot.save(buffer, "PNG")
        buffer.seek(0)

        data = buffer.data()

        uploader = CakeShot.uploaders[QtCore.QSettings().value("options/uploaders/uploader")]()
        try:
            link = uploader.upload(data.data())
            self.showMessage("Upload Complete!", link)
            QtGui.QApplication.clipboard().setText(link)
        except BaseException as e:
            self.showMessage("An error occured :(", e.message, QtGui.QSystemTrayIcon.Critical)

    def open_settings(self):
        self.settings_window = settings.SettingsWindow()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("CakeShot")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("CrateMuncher")
    app.setOrganizationDomain("cratemuncher.net")
    app.setWindowIcon(QtGui.QIcon("icon/cakeshot.png"))
    app.setQuitOnLastWindowClosed(False)

    cs = CakeShot()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()