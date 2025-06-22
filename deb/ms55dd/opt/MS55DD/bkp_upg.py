#! /usr/bin/python3
# -*- coding utf-8 -*-
# (c) 2022 Fomenko A V

from PyQt5.QtCore import pyqtSignal, QObject

try:
    import sh
except Exception as e:
    print(e)
    print("Install sh.\nUse 'sudo apt install python3-sh'",
          "for Debian-based systems\nor 'sudo pip3 install sh'",
          "for other system.\nFor console mode use key '-c'")
    sys.exit(-1)


class Bkp_Upg(QObject):
    '''
    Upgrade and Backup flash drive in side thread
    '''
    finished = pyqtSignal(bool)

    def __init__(self,
                 type,
                 filename_bkp=None,
                 filename_newImg=None,
                 device=None,
                 password=None,
                 DEBUG_MODE=False):

        QObject.__init__(self)
        self.type = type
        self.password = password
        self.filename_bkp = filename_bkp
        self.filename_newImg = filename_newImg
        self.device = device
        self.DEBUG_MODE = DEBUG_MODE

    def run(self):
        tags = ()

        def sh_do(tags):
            if tags:
                with sh.contrib.sudo(password=self.password, _with=True):
                    sh.dd(tags)
                    sh.sync()

        if self.type.lower() == "upgrade":
            if self.DEBUG_MODE:
                # DEBUG
                tags = ('if={}'.format(self.filename_newImg),
                        'of=/dev/null',
                        'bs=4M')
                sh_do(tags)
            else:
                # NORMAL
                tags = ('if={}'.format(self.filename_newImg),
                        'of={}'.format(self.device),
                        'bs=4M')
                sh_do(tags)

        elif self.type.lower() == "backup":
            if self.DEBUG_MODE:
                # DEBUG
                tags = ('if={}'.format(self.device),
                        'of={}'.format(self.filename_bkp),
                        'bs=4M',
                        'count=1')
                sh_do(tags)
            else:
                # NORMAL
                tags = ('if={}'.format(self.device),
                        'of={}'.format(self.filename_bkp),
                        'bs=4M')
                sh_do(tags)
        elif self.type.lower() == 'bkp_upg':
            if self.DEBUG_MODE:
                # DEBUG
                tags = ('if={}'.format(self.device),
                        'of={}'.format(self.filename_bkp),
                        'bs=4M',
                        'count=1')
                sh_do(tags)
                tags = ('if={}'.format(self.filename_newImg),
                        'of=/dev/null',
                        'bs=4M')
                sh_do(tags)
            else:
                # NORMAL
                tags = ('if={}'.format(self.device),
                        'of={}'.format(self.filename_bkp),
                        'bs=4M')
                sh_do(tags)

                tags = ('if={}'.format(self.filename_newImg),
                        'of={}'.format(self.device),
                        'bs=4M')
                sh_do(tags)

        self.finished.emit(True)
