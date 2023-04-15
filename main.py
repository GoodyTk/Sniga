from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)

from PIL import Image, ImageFilter
import os 
from PyQt5.QtGui import QPixmap

app = QApplication([])
window = QWidget()
window.resize(700,500)
window.setWindowTitle("Easy Editor")

"""Інтерфейс програми"""
btn_folder = QPushButton("Папка")
list_files = QListWidget()
main_label = QLabel("Зображення")

btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_mirror = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_left = QPushButton("Вліво")
btn_bw = QPushButton("Ч/Б")
btn_blure = QPushButton("Размыть")
col1 = QVBoxLayout()
col1.addWidget(btn_folder)
col1.addWidget(list_files)

col2 = QVBoxLayout()
col2.addWidget(main_label)

row1 = QHBoxLayout()
row1.addWidget(btn_left)
row1.addWidget(btn_right)
row1.addWidget(btn_mirror)
row1.addWidget(btn_sharp)
row1.addWidget(btn_bw)
row1.addWidget(btn_blure)
col2.addLayout(row1)
main_layout = QHBoxLayout()#
main_layout.addLayout(col1,20)
main_layout.addLayout(col2,80)
window.setLayout(main_layout)
window.show()


"""Функционал програми"""
workdir = ""#шлях до вибранної папки

def chooseWorkdir():#функція вибору папки
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):#функія фільтрування тільки картинок
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def showFileNamesList():
    extensions = ["jpg", "png", "jpeg", "bnp", "gif"]
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_files.clear()
    for filename in filenames:
        list_files.addItem(filename)

class ImageProcessor:#класс для обробки зображеннь
    def __init__(self):#Инициализация
        self.image = None#створення картинки
        self.dir = None#шлях до папки
        self.filename = None#имя картинки
        self.save_dir = "Modified/"#папка для обробленних фото
    def loadImage(self, dir, filename):#завантаження классу
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        main_label.hide()
        pixmapimage = QPixmap(path)
        a,b = 10, 20
        w,h = main_label.width(), main_label.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        main_label.setPixmap(pixmapimage)
        main_label.show()
    def saveImage(self):#сохранение картинки в папку 
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def do_lef(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_blure(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
workimage = ImageProcessor()

def showChosenImage():#показ вибранної картинки
    if list_files.currentRow() >= 0:
        filename = list_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workdir, filename)
        workimage.showImage(image_path)
        


list_files.currentRowChanged.connect(showChosenImage)
btn_folder.clicked.connect(showFileNamesList)
btn_left.clicked.connect(workimage.do_lef)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_bw.clicked.connect(workimage.do_bw)
btn_blure.clicked.connect(workimage.do_blure)
app.exec()
