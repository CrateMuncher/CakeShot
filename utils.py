import random
import string
from PySide import QtCore
import datetime
import time

old_time = ""
def get_filename():
    settings = QtCore.QSettings()
    prefix = settings.value("options/naming/prefix", "")
    naming_num = settings.value("options/naming/naming", 3)
    suffix = settings.value("options/naming/suffix", "")
    format_ = settings.value("options/naming/format", "%Y-%m-%d %H:%M:%S")
    amount = settings.value("options/naming/amount", 5)

    naming = ""

    if naming_num == 0:
        naming = ''.join(random.choice(string.digits) for x in range(amount))
    elif naming_num == 1:
        naming = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for x in range(amount))
    elif naming_num == 2:
        try:
            naming = datetime.datetime.now().strftime(format_)
            old_time = naming
        except ValueError:
            naming = ""

    elif naming_num == 3:
        naming = str(int(time.time()))

    return prefix + naming + suffix + ".png"