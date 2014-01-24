from PySide import QtCore, QtGui
import sys
import selectionselector


class CakeShot(QtGui.QSystemTrayIcon):
    def __init__(self):
        QtGui.QSystemTrayIcon.__init__(self)
        self.setIcon(QtGui.QIcon("icon/cakeshot.png"))

        self.menu = QtGui.QMenu()
        self.take_screenshot_item = self.menu.addAction("Take Screenshot\tPlaceholder")
        self.take_screenshot_item.triggered.connect(self.take_screenshot)

        self.setContextMenu(self.menu)

        self.show()

    def pre_take_screenshot(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.take_screenshot)
        timer.setInterval(1000)
        timer.start()

    def take_screenshot(self):
        desktop = QtGui.QApplication.desktop()
        print desktop.childAt(QtCore.QPoint(100, 100))

        self.selector = selectionselector.SelectionSelector()
        self.selector.selection_made.connect(self.selection_made)
        self.selector.select()

    def selection_made(self, rect):
        print rect


def main():
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon/cakeshot.png"))
    app.setQuitOnLastWindowClosed(False)

    cs = CakeShot()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()