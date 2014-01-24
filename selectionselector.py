from PySide import QtCore, QtGui


class SelectionSelector(QtGui.QGraphicsView):
    selection_made = QtCore.Signal(QtCore.QRect)

    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("background:transparent;")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)

        self.setScene(self.scene)
        self.setWindowTitle("CakeShot")

        self.pixmap = QtGui.QPixmap(QtGui.QApplication.desktop().width(), QtGui.QApplication.desktop().height())

        self.origin = None
        self.mouse_down_last = False

        QtGui.QApplication.instance().installEventFilter(self)
    def select(self):
        self.showFullScreen()
        self.pixmap_item = self.scene.addPixmap(self.pixmap)
        self.draw_overlay()
        self.grabKeyboard()
        self.grabMouse()


    def draw_overlay(self):
        self.pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(self.pixmap)
        painter.fillRect(0, 0, QtGui.QApplication.desktop().width(), QtGui.QApplication.desktop().height(),
                         QtGui.QColor(0, 0, 0, 127))
        if self.origin is not None:
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)

            from_pos = self.origin
            to_pos = QtGui.QCursor.pos()

            painter.fillRect(QtCore.QRect(from_pos, to_pos), QtGui.QColor(0, 0, 0, 0))

            txt = str(abs(from_pos.x() - to_pos.x())) + "x" + str(abs(from_pos.y() - to_pos.y()))

            font = QtGui.QFont()
            font.setStyleHint(QtGui.QFont.SansSerif)
            font.setPointSize(32)
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QtGui.QColor(127, 127, 127, 127))

            painter.drawText(QtCore.QRect(from_pos, to_pos), QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter, txt)
        self.pixmap_item.setPixmap(self.pixmap)

    def eventFilter(self, obj, evt): # I couldn't get normal events to work, so here's a workaround
        if type(evt) is QtGui.QMouseEvent:
            if QtGui.QApplication.mouseButtons() == QtCore.Qt.LeftButton:
                if not self.mouse_down_last:
                    # Mouse down
                    self.mouse_down_last = True
                    self.origin = QtGui.QCursor.pos()
            else:
                if self.mouse_down_last:
                    # Mouse up
                    self.mouse_down_last = False
                    self.hide()

                    settings = QtCore.QSettings()

                    QtCore.QTimer.singleShot(int(settings.value("options/delay", 250)), self.send_final)
            self.draw_overlay()
        return False

    def send_final(self): # Worst name ever
        self.selection_made.emit(QtCore.QRect(self.origin, QtGui.QCursor.pos()))
        self.destroy()