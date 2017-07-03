#-*- coding: utf-8 -*-
import os
import sys
import shutil
from PyQt4.QtGui import *
from PIL import Image


def searchPath(dirname):
    searchSubPath = []
    for (path, dir, files) in os.walk(dirname):
        search = path
        searchSubPath.append(search)
        searchSubPath.sort()
    return searchSubPath

def subDirCreate(path, aa, fol):
    print 'def_aa : ' + str(aa)
    print 'def_fol : ' + fol
    if fol not in aa:
        path = path + '\\' + fol
        print 'lowPath : ' + path

def findImg(fileLists):
    images = []
    for fileList in fileLists:
        if fileList.find('.jpg') is not -1:
            images.append(fileList)
        elif fileList.find('.png') is not -1:
            images.append(fileList)
        elif fileList.find('.tif') is not -1:
            images.append(fileList)
        elif fileList.find('.tga') is not -1:
            images.append(fileList)
    return images

def slicePast(init, start, lowHi):
    leng = len(init)
    startF = start[:leng]
    startT = start[leng:]
    startResult = startF + '_' + lowHi + startT
    return startResult


class ImgSizeControl(QWidget):
    def __init__(self, parent=None):
        super(ImgSizeControl, self).__init__(parent)

        self.ori = 'ori_'
        currentPath = os.getcwd()

        self.labelPath = QLabel()
        self.labelPath.setText(currentPath)
        self.btPath = QPushButton(u'경로선택')
        self.btPath.clicked.connect(self.PathDialog)
        self.labelSize = QLabel()
        self.labelSize.setText(u'<b>크기 비율 설정(백분율)</b>')
        self.textSize = QLineEdit()
        self.textSize.setText('20')
        self.labelExe = QLabel()
        self.labelExe.setText(u'<b>지원 포맷은 "jpg, png, tif, tga" 입니다.</b>')
        self.btExe = QPushButton(u'변환실행')
        self.btExe.clicked.connect(self.SizeChange)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(self.labelPath, 0, 0)
        self.gridLayout.addWidget(self.btPath, 0, 1)
        self.gridLayout.addWidget(self.labelSize, 1, 0)
        self.gridLayout.addWidget(self.textSize, 1, 1)
        self.gridLayout.addWidget(self.labelExe, 3, 0)
        self.gridLayout.addWidget(self.btExe, 3, 1)

        self.setLayout(self.gridLayout)
        self.setWindowTitle(u"TMR 텍스춰 이미지 크기 조절 v1.0")
        self.setGeometry(600, 600, 400, 50)

    def PathDialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)

        if dialog.exec_():
            for self.directory in dialog.selectedFiles():
                print (u'선택한 경로 : ' + str(self.directory))
        bold = '<b>' + self.directory + '</b>'
        self.labelPath.setText(bold)

    def SizeChange(self):
        #iniPath = 'R:\\02_Production\\002_Texture'
        iniPath = 'D:\\Work\\Maya\\sourceimages\\000_Textrue'
        start_dir = self.directory
        start_dir.replace('/', '\\')

        searchAllPath = searchPath(iniPath)
        del searchAllPath[0]

        iniPathLen = len(iniPath)
        lowPath = iniPath + '_Low'
        hiPath = iniPath + '_Hi'
        if not os.path.exists(lowPath):
            os.makedirs(lowPath)
        if not os.path.exists(hiPath):
            os.makedirs(hiPath)

        for sp in searchAllPath:
            su = sp[iniPathLen:]

            iniPathNew = iniPath + su
            iniPathNewFiles = os.listdir(iniPathNew)
            iniPathNewFiles.sort()
            iniPathNewImgFile = findImg(iniPathNewFiles)
            iniPathNewImgFile.sort()

            lowPathNew = lowPath + su
            #if not os.path.exists(lowPathNew):
            #    os.makedirs(lowPathNew)
            low = 'Low'
            startLowSlicePast = slicePast(iniPath, start_dir, low)
            startLowSlicePastLen = len(startLowSlicePast)
            lowPathNewF = lowPathNew[:startLowSlicePastLen]

            if lowPathNewF == startLowSlicePast:
                if not os.path.exists(lowPathNew):
                    os.makedirs(lowPathNew)
                for imgFile in iniPathNewImgFile:
                    print imgFile
                    imgFileFullPath = iniPathNew + '\\' + imgFile
                    print imgFileFullPath
                    img_org = Image.open(imgFileFullPath)
                    width_org, height_org = img_org.size
                    ratio = self.textSize.text()
                    factor = float(ratio) / 100
                    width = int(width_org * factor)
                    height = int(height_org * factor)
                    img_anti = img_org.resize((width, height), Image.ANTIALIAS)
                    lowImgFileFullPath = lowPathNew + '\\' + imgFile
                    img_anti.save(lowImgFileFullPath)

            hiPathNew = hiPath + su
            #if not os.path.exists(hiPathNew):
            #    os.makedirs(hiPathNew)
            hi = 'Hi'
            startHiSlicePast = slicePast(iniPath, start_dir, hi)
            startHiSlicePastLen = len(startHiSlicePast)
            hiPathNewF = hiPathNew[:startHiSlicePastLen]

            if hiPathNewF == startHiSlicePast:
                if not os.path.exists(hiPathNew):
                    os.makedirs(hiPathNew)
                for imgFile in iniPathNewImgFile:
                    hiImgFileFullPath = iniPathNew + '\\' + imgFile
                    shutil.copy2(hiImgFileFullPath, hiPathNew)

        state = u'<b>변환 완료</b>'
        self.labelExe.clear()
        self.labelExe.setText(state)

def main():
    app = QApplication(sys.argv)
    ex = ImgSizeControl()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
