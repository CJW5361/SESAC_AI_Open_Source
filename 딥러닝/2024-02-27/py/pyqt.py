import sys
from pathlib import Path

FILE = Path(__file__).resolve()
path = str(FILE.parents[1])
sys.path.append(str(path))

#sys.path.append('c:/users/hrPark/desktop/py/')

import sysInfoTitle

python_title_printer=sysInfoTitle.PythonTitlePrinter()
#print(python_title_printer.sysInfo())
info=python_title_printer.sysInfo()

# print(info)
# https://wikidocs.net/21944
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap

import sys
from PyQt5.QtWidgets import QApplication, QWidget,QLabel
from PyQt5.QtGui import QPixmap

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')
        self.setGeometry(500, 200, 500, 400)  # 창의 초기 크기와 위치 설정

        # 이미지 라벨 생성
        label2 = QLabel(self)
        pixmap = QPixmap('1.png')
        label2.setPixmap(pixmap)
        
    
        window_width = self.width()
        window_height = self.height()
        pixmap_width = pixmap.width()
        pixmap_height = pixmap.height()
        x_position = (window_width - pixmap_width) / 2
        y_position = (window_height - pixmap_height) / 2
        label2.move(x_position, y_position)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())


# class MyApp(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         line=QLabel('-'*100,self)
#         line.move(0, 0)
#         line=QLabel('-'*100,self)
#         line.move(0, 80)
        
#         label1 = QLabel(info, self)
#         label1.move(5, 10)
       
#         self.setWindowTitle('python PyQt5')
#         self.move(500, 200, 800, 900)
        
#         label2=QLabel(self)
#         pixmap=QPixmap('1.png')
#         label2.setPixmap(pixmap)
#         label2.move(400,450)
        
        
#         # btn1=QPushButton('Load',self)
#         # btn1.setFixedSize(200,30)
#         # btn1.move(300,100)
#         self.show()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     sys.exit(app.exec_())
