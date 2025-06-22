#! /opt/MS55DD/venv_ms55dd/bin/python
# -*- coding utf-8 -*-
# (c) 2022 Fomenko A V

import os
import re

from os.path import isfile, join

try:
    import sh
except Exception as e:
    print(e)
    print("Install sh.\nUse 'sudo apt install python3-sh'",
          "for Debian-based systems\nor 'sudo pip3 install sh'",
          "for other system.\nFor console mode use key '-c'")
    sys.exit(-1)

try:
    from PyQt5 import QtWidgets, QtGui, QtCore
    from PyQt5.QtWidgets import QApplication as QApp
    from PyQt5.QtWidgets import QMainWindow as QMW
    from PyQt5.QtCore import QThread, pyqtSignal, QObject
except Exception as e:
    print(e)
    print("Install PyQt5.\nUse 'sudo apt install python3-pyqt5'",
          "for Debian-based systems\nor 'sudo pip3 install pyqt5'",
          "for other system.\nFor console mode use key '-c'")
    sys.exit(-1)


from bkp_upg import Bkp_Upg
from md5_calc import MD5_calc
from design import Ui_MainWindow as UMW


class MS55DD(QMW, UMW):
    def __init__(self, DEBUG=False):
        super().__init__()
        self.setupUi(self)

        # image file full pathes
        self.pathes_img = {}
        # MD5 summs
        self.MD5_summs = {}
        # image just filename without full path
        self.image_filename = ''
        # selected device name
        self.device = ''
        # sudo pass
        self.sudo_pass = ''

        # dialogs
        self.f_dialog = QtWidgets.QFileDialog()
        self.sudo_dialog = QtWidgets.QInputDialog()

        self.error_dialog = QtWidgets.QMessageBox(self)
        self.error_dialog.setWindowTitle('WARNING')
        self.error_dialog.setIcon(QtWidgets.QMessageBox.Warning)

        # Control Settings
        self.textEdit_OUTPUT.setReadOnly(True)
        self.lineEdit_IMAGE.setReadOnly(True)
        self.lineEdit_MD5.setReadOnly(True)

        # Window Icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/opt/MS55DD/MS55DD.png"),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setIconSize(QtCore.QSize(64, 64))

        # Signals
        self.btn_Backup.clicked.connect(self.backup)
        self.btn_MD5.clicked.connect(self.click_md5)
        self.btn_Upgrade.clicked.connect(self.upgrade)
        self.btn_Open.clicked.connect(self.browse_folder)
        self.btn_RefreshList.clicked.connect(self.refresh)
        self.btn_Bkp_Upg.clicked.connect(self.backup_upgrade)
        self.listWidget_FLASH.itemClicked.connect(self.click_item_flash)
        self.listWidget_IMAGE.itemClicked.connect(self.click_item_image)

        # =====DEBUG=====
        self.DEBUG = DEBUG
        # self.DEBUG = True
        self.DEBUG_MODE()
        # =====DEBUG=====

    def DEBUG_MODE(self):
        '''
        DEBUG MODE
        '''
        if not self.DEBUG:
            return

        self.error_dialog_show('DEBUG MODE')
        self.setWindowTitle("MS55DD | DEBUG MODE")

    def backup_upgrade(self):
        '''
        Backup and Upgrade
        '''
        if not self.chek_device():
            return

        if not self.chek_image_filename():
            return

        file = self.get_bkp_file_name()
        if not file:
            return

        password = self.get_sudo_password()
        if not password:
            return

        self.thread = QThread()
        # create object which will be moved to another thread
        # self, type, filename, device, password, DEBUG_MODE=False)
        self.go = Bkp_Upg(type='bkp_upg',
                          filename_bkp=file,
                          filename_newImg=self.pathes_img[self.image_filename],
                          device=self.device,
                          password=password,
                          DEBUG_MODE=self.DEBUG)
        # move object to another thread
        self.go.moveToThread(self.thread)
        # connect signals from this object to slot in GUI thread
        self.go.finished.connect(self.end_Bkp_Upg_thread)
        self.go.finished.connect(self.thread.quit)

        self.go.finished.connect(self.go.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.go.run)
        # start thread
        self.thread.start()

        # shadow
        self.centralwidget.setEnabled(False)
        self.textEdit_OUTPUT.append('Backup and upgrade start...')
        self.textEdit_OUTPUT.append('Working....................')

    def upgrade(self):
        '''
        Upgrade function
        '''
        if not self.chek_device():
            return

        if not self.chek_image_filename():
            return

        password = self.get_sudo_password()
        if not password:
            return

        self.thread = QThread()
        # self, type, filename, device, password, DEBUG_MODE=False)
        self.go = Bkp_Upg(type='upgrade',
                          filename_newImg=self.pathes_img[self.image_filename],
                          device=self.device,
                          password=password,
                          DEBUG_MODE=self.DEBUG)
        self.go.moveToThread(self.thread)
        self.go.finished.connect(self.end_Bkp_Upg_thread)
        self.go.finished.connect(self.thread.quit)
        self.go.finished.connect(self.go.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.go.run)
        self.thread.start()

        # shadow
        self.centralwidget.setEnabled(False)
        self.textEdit_OUTPUT.append('Upgrade start...')
        self.textEdit_OUTPUT.append('Working.........')

    def backup(self):
        '''
        Backup function
        '''
        if not self.chek_device():
            return

        file = self.get_bkp_file_name()
        if not file:
            return

        password = self.get_sudo_password()
        if not password:
            return

        self.thread = QThread()
        # self, type, filename, device, password, DEBUG_MODE=False)
        self.go = Bkp_Upg(type='backup',
                          filename_bkp=file,
                          device=self.device,
                          password=password,
                          DEBUG_MODE=self.DEBUG)
        self.go.moveToThread(self.thread)
        self.go.finished.connect(self.end_Bkp_Upg_thread)
        self.go.finished.connect(self.thread.quit)
        self.go.finished.connect(self.go.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.go.run)
        self.thread.start()

        # shadow
        self.centralwidget.setEnabled(False)
        self.textEdit_OUTPUT.append('Backup start...')
        self.textEdit_OUTPUT.append('Working........')

    def chek_image_filename(self):
        '''
        Check selected image filename
        '''
        if not self.pathes_img:
            self.error_dialog_show('Select files for upgrade')
            return

        # filename = self.lineEdit_IMAGE.text()
        if not self.image_filename:
            self.error_dialog_show('Select file for upgrade')
            return
        return True

    def chek_device(self):
        '''
        Check device name
        '''
        if not self.device:
            self.device = self.lineEdit_DEVICE.text()

        if not re.match('/dev/sd[a-z]$', self.device):
            self.error_dialog_show('Select a flash drive image.<br>' +
                                   'Or type flash drive name manually.<br>' +
                                   '(/dev/sda or /dev/sdb or ...)')
            return
        return True

    def get_bkp_file_name(self):
        '''
        Get backup filename
        '''
        file, ok = self.f_dialog.getSaveFileName(self,
                                                 'Save as *.iso',
                                                 os.environ['HOME'],
                                                 "*.iso")
        if not file or not ok:
            self.error_dialog_show('Input a filename for backup image')
            return
        return file

    def get_sudo_password(self):
        '''
        Getting a sudo password and chek it
        '''
        if self.sudo_pass:
            return self.sudo_pass

        echo = QtWidgets.QLineEdit.EchoMode.Password
        password, ok = self.sudo_dialog.getText(self,
                                                'Password',
                                                'Sudo password:',
                                                echo=echo)

        if not password or not ok:
            self.error_dialog_show('Input a sudo password')
            return False

        try:
            sh.contrib.sudo.ls(password=password)
        except:
            self.error_dialog_show('Input a correct sudo password')
            return False

        self.sudo_pass = password
        return self.sudo_pass

    def end_Bkp_Upg_thread(self, flag):
        '''
        Work after BKP_UPG thread working
        '''
        if flag:
            self.textEdit_OUTPUT.append('Ready<br>=====')
            self.centralwidget.setEnabled(True)

    def error_dialog_show(self, text):
        '''
        Show warning message window
        '''
        self.error_dialog.setText(text)
        self.error_dialog.exec_()

    def click_md5(self):
        '''
        Calculate MD5 cheksumm and output it
        '''
        self.lineEdit_MD5.clear()
        if not self.pathes_img:
            self.error_dialog_show('Select files for calculating MD5 ')
            return

        if not self.image_filename:
            self.error_dialog_show('Select file for calculating MD5 ')
            return

        if self.MD5_summs.get(self.pathes_img[self.image_filename]):
            self.lineEdit_MD5.setText(self.MD5_summs.get(
                self.pathes_img[self.image_filename]))
            return

        self.thread_md5 = QThread()

        self.md5_go = MD5_calc(self.pathes_img[self.image_filename])
        self.md5_go.moveToThread(self.thread_md5)

        self.md5_go.md5_summ.connect(self.end_calculating_md5)
        self.md5_go.md5_summ.connect(self.thread_md5.quit)
        self.md5_go.md5_summ.connect(self.thread_md5.deleteLater)

        self.thread_md5.started.connect(self.md5_go.run)
        self.thread_md5.started.connect(self.thread_md5.deleteLater)
        self.thread_md5.start()

        # Shadow
        self.btn_MD5.setText('Calculating MD5 cheksum...')
        self.btn_MD5.setEnabled(False)
        self.btn_Open.setEnabled(False)

    def end_calculating_md5(self, md5_summ):
        '''
        Work after md5_sum calculating thread working
        '''
        if md5_summ:
            self.lineEdit_MD5.setText(list(md5_summ.values())[0])
            self.MD5_summs.update(md5_summ)
            self.btn_MD5.setText('Calculate MD5 cheksum')
            self.btn_MD5.setEnabled(True)
            self.btn_Open.setEnabled(True)

    def refresh(self):
        '''
        Getting list of block devices
        Put it in to the list view
        '''
        self.listWidget_FLASH.clear()
        s = sh.lsblk('-P', '-o', 'name,size', '-p', '-d')
        self.listWidget_FLASH.addItems(s.split("\n")[:-1])

    def click_item_flash(self, item):
        '''
        Select a device name, put it in to the lineedit
        '''
        s = item.text().split(' ')
        self.device = s[0][6:-1]
        self.lineEdit_DEVICE.setText(self.device)

    def browse_folder(self):
        '''
        Select and browse folder with image files
        Put image filename to listview and fullpathes to pathes_img var
        '''
        self.listWidget_IMAGE.clear()
        dirr = self.f_dialog.getExistingDirectory(self,
                                                  'Choose directory',
                                                  os.environ['HOME'])
        if dirr:
            for file_name in os.listdir(dirr):
                if isfile(join(dirr, file_name)):
                    self.listWidget_IMAGE.addItem(file_name)
                    self.pathes_img[file_name] = join(dirr, file_name)

    def click_item_image(self, item):
        '''
        Select an image filename, put it in to the lineedit
        '''
        self.image_filename = item.text()
        self.lineEdit_MD5.clear()
        self.lineEdit_IMAGE.setText(self.image_filename)

        if self.MD5_summs.get(self.pathes_img.get(self.image_filename)):
            self.lineEdit_MD5.setText(self.MD5_summs.get(
                self.pathes_img.get(self.image_filename)))
            return
