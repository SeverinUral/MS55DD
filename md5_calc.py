#! /usr/bin/python3
# -*- coding utf-8 -*-
# (c) 2022 Fomenko A V

import hashlib

from PyQt5.QtCore import pyqtSignal, QObject


class MD5_calc(QObject):
    '''
    Calculate MD5 sum in side thread
    '''
    md5_summ = pyqtSignal(dict)

    def __init__(self, file_name):

        QObject.__init__(self)
        self.filename = file_name

    def run(self):
        md5 = hashlib.new('md5')
        chunk = 1

        with open(self.filename, "rb") as f:
            while chunk:
                chunk = f.read(8192)
                md5.update(chunk)

        self.md5_summ.emit({self.filename: md5.hexdigest()})
        # self.md5_summ.emit()
