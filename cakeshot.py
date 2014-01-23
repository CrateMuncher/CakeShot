from PySide import QtGui
import sys


class CakeShot(QtGui.QSystemTrayIcon):
    def __init__(self):
        QtGui.QSystemTrayIcon.__init__(self)
        self.setIcon(QtGui.QIcon("icon/cakeshot.png"))
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon/cakeshot.png"))

    cs = CakeShot()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()