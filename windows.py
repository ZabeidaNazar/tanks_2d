from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QApplication, QInputDialog
from PyQt5.QtGui import QFont

import style
from settings import editor_caption

# QApplication.setAttribute(Qt.AA_DisableHighDpiScaling, True)
# QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, False)

app = QApplication([])


font = QFont()
font.setFamily("fonts/FiraCode-Regular.ttf")
font.setPointSize(16)

def show_mess(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle(editor_caption)
    msg.exec_()


def show_warning(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle(editor_caption)
    msg.exec_()


def get_text_input(text):
    input_dialog = QInputDialog(None)
    input_dialog.setInputMode(QInputDialog.TextInput)
    input_dialog.setWindowTitle(editor_caption)
    input_dialog.setWindowFlag(Qt.WindowStaysOnTopHint)
    input_dialog.setFont(font)
    input_dialog.setLabelText(text)
    input_dialog.setStyleSheet(style.themes["input"])
    ok = input_dialog.exec_()
    res = input_dialog.textValue()
    return res, ok


def get_select_input(items):
    input_dialog = QInputDialog(None)
    input_dialog.setInputMode(QInputDialog.UseListViewForComboBoxItems)
    input_dialog.setWindowTitle(editor_caption)
    input_dialog.setWindowFlag(Qt.WindowStaysOnTopHint)
    input_dialog.setFont(font)
    input_dialog.setComboBoxItems(items)
    input_dialog.setStyleSheet(style.themes["input"])
    ok = input_dialog.exec_()
    res = input_dialog.textValue()
    return res, ok