from PySide import QtCore, QtGui
import cakeshot
import utils


class SettingsWindow(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(SettingsWindow, self).__init__(*args, **kwargs)

        self.options_tab = OptionsTab(self)
        self.uploaders_tab = UploadersTab(self)

        tabs = QtGui.QTabWidget()
        tabs.addTab(self.options_tab, "Options")
        tabs.addTab(self.uploaders_tab, "Uploaders")

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(tabs)

        self.setLayout(hbox)
        self.setWindowTitle("CakeShot")
        self.show()

class OptionsTab(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(OptionsTab, self).__init__(*args, **kwargs)

        self.settings = QtCore.QSettings()

        self.delay_spinner = QtGui.QSpinBox(self)
        self.delay_spinner.setMinimum(0)
        self.delay_spinner.setMaximum(5000)
        self.delay_spinner.setValue(self.settings.value("options/delay", 250))

        self.prefix_edit = QtGui.QLineEdit()
        self.prefix_edit.setText(self.settings.value("options/naming/prefix", ""))
        self.prefix_edit.textChanged.connect(self.update_naming)

        self.suffix_edit = QtGui.QLineEdit()
        self.suffix_edit.setText(self.settings.value("options/naming/suffix", ""))
        self.suffix_edit.textChanged.connect(self.update_naming)

        self.naming = QtGui.QComboBox()
        self.naming.addItem("Random numbers")
        self.naming.addItem("Random letters")
        self.naming.addItem("Time")
        self.naming.addItem("Unix timestamp")
        self.naming.setCurrentIndex(self.settings.value("options/naming/naming", 3))
        self.naming.currentIndexChanged.connect(self.update_naming)

        self.format = QtGui.QLineEdit()
        self.format.setText(self.settings.value("options/naming/format", "%Y-%m-%d %H:%M:%S"))
        self.format.textChanged.connect(self.update_naming)

        self.amount = QtGui.QSpinBox()
        self.amount.setValue(self.settings.value("options/naming/amount", 5))
        self.amount.valueChanged.connect(self.update_naming)

        self.naming_example = QtGui.QLabel()

        self.save_button = QtGui.QPushButton("Save")
        self.save_button.clicked.connect(self.save)

        form = QtGui.QFormLayout()
        form.addRow("Screenshot delay (ms)", self.delay_spinner)
        form.addRow("Naming prefix", self.prefix_edit)
        form.addRow("Naming", self.naming)
        form.addRow("Date format", self.format)
        form.addRow("Digit/character amount", self.amount)
        form.addRow("Naming suffix", self.suffix_edit)
        form.addRow("Naming example", self.naming_example)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(form)
        vbox.addWidget(self.save_button)

        self.setLayout(vbox)

        self.update_naming()

    def update_naming(self):
        self.save()
        naming = utils.get_filename()
        self.naming_example.setText(naming)

        if self.naming.currentIndex() == 0:
            self.amount.setEnabled(True)
            self.format.setEnabled(False)
        elif self.naming.currentIndex() == 1:
            self.amount.setEnabled(True)
            self.format.setEnabled(False)
        elif self.naming.currentIndex() == 2:
            self.amount.setEnabled(False)
            self.format.setEnabled(True)
        elif self.naming.currentIndex() == 3:
            self.amount.setEnabled(False)
            self.format.setEnabled(False)

    def save(self):
        self.settings.setValue("options/naming/amount", self.amount.value())
        self.settings.setValue("options/delay", self.delay_spinner.value())
        self.settings.setValue("options/naming/prefix", self.prefix_edit.text())
        self.settings.setValue("options/naming/naming", self.naming.currentIndex())
        self.settings.setValue("options/naming/suffix", self.suffix_edit.text())
        self.settings.setValue("options/naming/format", self.format.text())

class UploadersTab(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(UploadersTab, self).__init__(*args, **kwargs)
        settings = QtCore.QSettings()

        self.uploaders_list = QtGui.QListWidget()
        for uploader in cakeshot.CakeShot.uploaders:
            self.uploaders_list.addItem(QtGui.QListWidgetItem(uploader.name))
        self.uploaders_list.item(settings.value("options/uploaders/uploader", 0)).setSelected(True)
        self.uploaders_list.currentItemChanged.connect(self.save)

        self.settings_btn = QtGui.QPushButton("Settings")
        self.settings_btn.clicked.connect(self.open_settings)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.uploaders_list)
        vbox.addWidget(self.settings_btn)

        self.setLayout(vbox)

    def open_settings(self):
        uploader = cakeshot.CakeShot.uploaders[self.uploaders_list.currentIndex().row()]
        uploader().show_settings()

    def save(self):
        settings = QtCore.QSettings()
        settings.setValue("options/uploaders/uploader", self.uploaders_list.currentIndex().row())