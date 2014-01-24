from PySide import QtGui
import json
import requests

class ImgurUploader(object):
    name = "Imgur"
    def upload(self, image_str):
        data = json.load(open("api.json", "r"))
        imgur_keys = data["imgur"]
        id = imgur_keys["client-id"]
        secret = imgur_keys["client-secret"]

        files = {"image": ('image.png', image_str)}
        headers = {"authorization": "Client-ID " + id}
        response = requests.post("https://api.imgur.com/3/image", files=files, headers=headers)
        return response.json()["data"]["link"]

    def show_settings(self):
        dialog = QtGui.QDialog()
        dialog.exec_()