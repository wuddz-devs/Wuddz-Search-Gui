import secrets, string, sys, re, time, shutil
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path, PurePath
from subprocess import run, Popen
from os import name, path


class Ui_MainWindow(object):
    def __init__(self):
        self.drv=''
        self.flst=''
        self.sfst=''
        self.slist=''
        self.pkg=str(Path.home().expanduser().joinpath('Downloads','SEARCH'))
        self.lf=Path(self.pkg).joinpath('file.lst')
        self.dr=Path(self.pkg).joinpath('regex_output.txt')
        self.af=Path(self.pkg).joinpath('archive-pwd.txt')
        self.lo=Path(self.pkg).joinpath('list-output.txt')
        Path(self.pkg).mkdir(parents=True, exist_ok=True)
        home=['','Desktop','Documents','Downloads','Music','Pictures','Videos']
        drv=[str(Path.home().expanduser().joinpath(x)) for x in home]
        drv.append(self.pkg)
        if name=='nt':
            self.pf=12
            self.drv=[f'{x}:\\' for x in 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z' if path.exists(f'{x}:')]
        else:
            self.pf=11
            drv.insert(0,'/')
            out=run(['df'], capture_output=True, text=True)
            drvv=re.findall('(/media/\w+/\w+)',str(out))
            if drvv:drv.extend(drvv)
        if self.drv:self.drv.extend(sorted(drv))
        else:self.drv=sorted(drv)
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(QtCore.QSize(781, 642))
        MainWindow.setWindowTitle("Wuddz-Search-Gui")
        MainWindow.closeEvent=lambda event: sys.exit()
        self.frameGeometry=MainWindow.frameGeometry()
        self.cp=QtWidgets.QDesktopWidget().availableGeometry().center()
        self.frameGeometry.moveCenter(self.cp)
        MainWindow.move(self.frameGeometry.topLeft())
        self.icon=QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("wudz-sgui.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(self.icon)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget=QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.searchformat=QtWidgets.QComboBox(self.centralwidget)
        self.searchformat.setGeometry(QtCore.QRect(106, 130, 573, 22))
        self.font=QtGui.QFont()
        self.font.setFamily("Tahoma")
        self.font.setPixelSize(self.pf)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.searchformat.setFont(self.font)
        self.searchformat.setMaxVisibleItems(13)
        self.searchformat.setEditable(True)
        self.searchformat.setPlaceholderText("")
        self.searchformat.setObjectName("searchformat")
        self.searchformat.setToolTip("Input OR Select Search Format")
        self.searchformat.addItem("")
        self.searchformat.setItemText(0, "")
        self.searchformat.addItem("")
        self.searchformat.addItem("")
        self.searchformat.addItem("")
        self.searchformat.addItem("")
        self.searchformat.addItem("")
        self.searchformat.addItem("")
        self.searchformat.addItem("")
        self.searchformat.addItem("")
        self.searchformat.addItem("")
        self.searchformat.addItem("")
        self.searchformat.addItem("")
        self.directoryinput=QtWidgets.QComboBox(self.centralwidget)
        self.directoryinput.setGeometry(QtCore.QRect(106, 152, 573, 23))
        self.directoryinput.setFont(self.font)
        self.directoryinput.setMaxVisibleItems(15)
        self.directoryinput.setEditable(True)
        self.directoryinput.setObjectName("directoryinput")
        self.directoryinput.setToolTip("Input OR Select Search Directory")
        self.listarea=QtWidgets.QListWidget(self.centralwidget)
        self.listarea.setGeometry(QtCore.QRect(0, 196, 781, 404))
        self.listarea.setFont(self.font)
        self.listarea.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(0, 100, 255);")
        self.listarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.listarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.listarea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.listarea.setAutoScroll(False)
        self.listarea.setAutoScrollMargin(10)
        self.listarea.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listarea.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.listarea.setResizeMode(QtWidgets.QListView.Adjust)
        self.listarea.setObjectName("listarea")
        self.label=QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 131, 106, 22))
        self.label.setFont(self.font)
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(0, 255, 0);")
        self.label.setObjectName("label")
        self.label_2=QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 153, 106, 22))
        self.label_2.setFont(self.font)
        self.label_2.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(0, 255, 0);")
        self.label_2.setObjectName("label_2")
        self.label_3=QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(679, 131, 102, 22))
        self.label_3.setFont(self.font)
        self.label_3.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(0, 255, 0);")
        self.label_3.setObjectName("label_3")
        self.label_4=QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(679, 153, 102, 22))
        self.label_4.setFont(self.font)
        self.label_4.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(0, 255, 0);")
        self.label_4.setObjectName("label_4")
        self.plainTextEdit=QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 0, 781, 131))
        self.plainTextEdit.setFont(self.font)
        self.plainTextEdit.setStyleSheet("color: rgb(0, 255, 0);\n"
"background-color: rgb(0, 0, 0);")
        self.plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton=QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(105, 174, 574, 22))
        self.pushButton.setFont(self.font)
        self.pushButton.setStyleSheet("background-color: rgb(153, 153, 153);\n"
"color: rgb(0, 0, 0);")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar=QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 781, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile=QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit=QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuArchive=QtWidgets.QMenu(self.menuBar)
        self.menuArchive.setObjectName("menuArchive")
        self.menuHelp=QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.statusbar=QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setFont(self.font)
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen=QtWidgets.QAction(MainWindow)
        self.actionOpen.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave=QtWidgets.QAction(MainWindow)
        self.actionSave.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionSave.setObjectName("actionSave")
        self.actionQuit=QtWidgets.QAction(MainWindow)
        self.actionQuit.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionQuit.setObjectName("actionQuit")
        self.actionCopy=QtWidgets.QAction(MainWindow)
        self.actionCopy.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionCopy.setObjectName("actionCopy")
        self.actionMove=QtWidgets.QAction(MainWindow)
        self.actionMove.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionMove.setObjectName("actionMove")
        self.actionDelete=QtWidgets.QAction(MainWindow)
        self.actionDelete.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionDelete.setObjectName("actionDelete")
        self.actionParse=QtWidgets.QAction(MainWindow)
        self.actionParse.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionParse.setObjectName("actionParse")
        self.actionArchive_Encryption=QtWidgets.QAction(MainWindow)
        self.actionArchive_Encryption.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionArchive_Encryption.setObjectName("actionArchive_Encryption")
        self.actionArchive_No_Encryption=QtWidgets.QAction(MainWindow)
        self.actionArchive_No_Encryption.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionArchive_No_Encryption.setObjectName("actionArchive_No_Encryption")
        self.actionAbout=QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionMove)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addAction(self.actionParse)
        self.menuArchive.addAction(self.actionArchive_Encryption)
        self.menuArchive.addAction(self.actionArchive_No_Encryption)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuArchive.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.directoryinput.addItem("")
        self.directoryinput.setItemText(0,"")
        self.directoryinput.addItems(self.drv)
        _translate=QtCore.QCoreApplication.translate
        self.searchformat.setItemText(1, _translate("MainWindow", "*"))
        self.searchformat.setItemText(2, _translate("MainWindow", "*.py"))
        self.searchformat.setItemText(3, _translate("MainWindow", "*.txt"))
        self.searchformat.setItemText(4, _translate("MainWindow", "*.jpg"))
        self.searchformat.setItemText(5, _translate("MainWindow", "*.jpeg"))
        self.searchformat.setItemText(6, _translate("MainWindow", "*.png"))
        self.searchformat.setItemText(7, _translate("MainWindow", "*.gif"))
        self.searchformat.setItemText(8, _translate("MainWindow", "*.mp4"))
        self.searchformat.setItemText(9, _translate("MainWindow", "*.mkv"))
        self.searchformat.setItemText(10, _translate("MainWindow", "*.wmv"))
        self.searchformat.setItemText(11, _translate("MainWindow", "*.mp3"))
        self.searchformat.setItemText(12, _translate("MainWindow", "*.exe"))
        self.label.setText(_translate("MainWindow", "Search Format"))
        self.label_2.setText(_translate("MainWindow", "Search Directory"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Search Formats:    [.ext=File Extension]\n"
"*              All Files In Directory\n"
"file.txt      Files Named \"file.txt\"\n"
"*.ext        Files With .ext File Extension  [e.g *.txt Find All Text Files]\n"
"test*        Files With Filename Starting With \"test\"  [.ext Optional e.g test*.jpg]\n"
"*test        Files With Filename Ending With \"test\"  [.ext Optional e.g test*.jpg]\n"
"*test*      Files With \"test\" Anywhere In Filename  [.ext Optional e.g *test*.py]\n"
"*te*st*    Files With \"te\" Followed By \"st\" Anywhere In Filename [.ext Optional e.g *te*st*.py]"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuArchive.setTitle(_translate("MainWindow", "Archive"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Alt+C"))
        self.actionMove.setText(_translate("MainWindow", "Move"))
        self.actionMove.setShortcut(_translate("MainWindow", "Alt+M"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setShortcut(_translate("MainWindow", "Alt+Del"))
        self.actionParse.setText(_translate("MainWindow", "Parse"))
        self.actionParse.setShortcut(_translate("MainWindow", "Alt+P"))
        self.actionArchive_Encryption.setText(_translate("MainWindow", "Encryption"))
        self.actionArchive_Encryption.setShortcut(_translate("MainWindow", "Alt+E"))
        self.actionArchive_No_Encryption.setText(_translate("MainWindow", "No Encryption"))
        self.actionArchive_No_Encryption.setShortcut(_translate("MainWindow", "Alt+N"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.pushButton.clicked.connect(self.search_main)
        self.listarea.itemDoubleClicked.connect(lambda: self.open_file(self.listarea.currentItem()))
        self.listarea.itemClicked.connect(lambda: self.list_selection())
        self.actionOpen.triggered.connect(lambda: self.menu_main('Open'))
        self.actionSave.triggered.connect(lambda: self.menu_main('Save'))
        self.actionQuit.triggered.connect(lambda: sys.exit())
        self.actionCopy.triggered.connect(lambda: self.menu_main('Copy'))
        self.actionMove.triggered.connect(lambda: self.menu_main('Move'))
        self.actionDelete.triggered.connect(lambda: self.menu_main('Delete'))
        self.actionParse.triggered.connect(lambda: self.menu_main('Parse'))
        self.actionAbout.triggered.connect(lambda: self.menu_main('About'))
        self.actionArchive_No_Encryption.triggered.connect(lambda: self.menu_main('Archive_No_E'))
        self.actionArchive_Encryption.triggered.connect(lambda: self.menu_main('Archive_E'))
    
    def list_selection(self):
        try:
            self.sfst=''
            self.slist=''
            rows=self.listarea.selectedItems()
            rows=[str(x) for x in (str(self.listarea.selectedItems()[i].text()) for i in range(len(rows)))]
            self.slist=[re.search("\d  (.*)",str(r).split(' '*4)[0]).group(1) for r in rows]
            self.sfst=[re.search("\d  (.*)",str(r)).group(1) for r in rows]
        except:pass
    
    def menu_main(self,menu):
        obj_btn=''
        obj_cmbox=''
        obj_cmbox_2=''
        obj_lineEdit=''
        self.centralwidget.setStatusTip("")
        plst=['<IPTV_ACCOUNT>','<IPTV_SERVER_URL>','<IP+IP:PORT>','<URL>',
             '<MAC_ADDRESS>','<EMAIL:PASSWORD>','<USER:PASSWORD>','<M3U_URL>']
        wgt=QtWidgets.QWidget()
        if menu=='Open' or menu=='Save' or menu=='Delete' or menu=='Archive_No_E':
            wgt.setFixedSize(QtCore.QSize(573, 43))
            obj_lbl=QtWidgets.QLabel(wgt)
            obj_lbl.setFont(self.font)
            obj_lbl.setStyleSheet("color: rgb(0, 255, 0);\n"
"background-color: rgb(0, 0, 0);")
            obj_cmbox=QtWidgets.QComboBox(wgt)
            obj_cmbox.setFont(self.font)
            obj_cmbox.setMaxVisibleItems(15)
            obj_cmbox.setEditable(True)
            obj_cmbox.addItem("")
            if menu=='Delete':
                obj_lbl.setGeometry(QtCore.QRect(0, 0, 68, 22))
                obj_lbl.setText("File/Folder")
                obj_cmbox.setGeometry(QtCore.QRect(68, 0, 505, 22))
                obj_cmbox.addItem("")
                obj_cmbox.setItemText(0, "")
                obj_cmbox.setItemText(1, "<All OR Selected List Items>")
                obj_cmbox.setToolTip("Input File/Folder Path,\n"
"OR Choose Items Delete")
            elif menu=='Save':
                obj_lbl.setGeometry(QtCore.QRect(0, 0, 25, 22))
                obj_lbl.setText("File")
                obj_cmbox.setGeometry(QtCore.QRect(25, 0, 548, 22))
                obj_cmbox.addItem("")
                obj_cmbox.setItemText(0, "")
                obj_cmbox.setItemText(1, "<Default>")
                obj_cmbox.addItems(self.drv)
                obj_cmbox.setToolTip("Set Output File, OR\n"
"Select '<Default>'\n"
"(i.e Default Output File)\n"
"To Save All, OR Selected \n"
"List Items As Text")
            elif menu=='Archive_No_E':
                obj_lbl.setGeometry(QtCore.QRect(0, 0, 81, 22))
                obj_lbl.setText("Archivename")
                obj_cmbox.setGeometry(QtCore.QRect(81, 0, 492, 22))
                obj_cmbox.addItem("")
                obj_cmbox.addItem("")
                obj_cmbox.setItemText(0, ".7z")
                obj_cmbox.setItemText(1, ".zip")
                obj_cmbox.setItemText(2, ".tar")
                obj_cmbox.setToolTip("Select An Available Archive Type\n"
"To Archive All OR Selected List Items,\n"
"Name Archive Accordingly\n"
"(i.e Name Must Not Be Existing File,\n"
"Specify Full Archive Path OR\n"
"Archive Will Be In Default Folder)")
            else:
                obj_lbl.setGeometry(QtCore.QRect(0, 0, 25, 22))
                obj_lbl.setText("File")
                obj_cmbox.setGeometry(QtCore.QRect(25, 0, 548, 22))
                obj_cmbox.setItemText(0, "")
                obj_cmbox.addItems(self.drv)
                obj_cmbox.setToolTip("Input File Path To Open\n"
"File With Default Program")
            obj_btn=QtWidgets.QPushButton(wgt)
            obj_btn.setGeometry(QtCore.QRect(-1, 20, 575, 24))
            obj_btn.setStyleSheet("background-color: rgb(153, 153, 153);\n"
"color: rgb(0, 0, 0);")
        elif menu=='Copy' or menu=='Move' or menu=='Archive_E' or menu=='Parse':
            wgt.setFixedSize(QtCore.QSize(573, 66))
            obj_lbl=QtWidgets.QLabel(wgt)
            obj_lbl.setFont(self.font)
            obj_lbl.setStyleSheet("color: rgb(0, 255, 0);\n"
"background-color: rgb(0, 0, 0);")
            obj_lbl_2=QtWidgets.QLabel(wgt)
            obj_lbl_2.setFont(self.font)
            obj_lbl_2.setStyleSheet("color: rgb(0, 255, 0);\n"
"background-color: rgb(0, 0, 0);")
            obj_cmbox=QtWidgets.QComboBox(wgt)
            obj_cmbox.setEditable(True)
            obj_cmbox.setFont(self.font)
            obj_cmbox.setMaxVisibleItems(15)
            if menu=='Archive_E':
                obj_lineEdit=QtWidgets.QLineEdit(wgt)
                obj_lbl.setGeometry(QtCore.QRect(0, 0, 62, 22))
                obj_lbl.setText("Password")
                obj_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
                obj_lineEdit.setGeometry(QtCore.QRect(62, 0, 511, 22))
                obj_lineEdit.setFont(self.font)
                obj_lineEdit.setToolTip("Set A Password,\n"
"If No Password Is Set,\n"
"A Randomly Generated\n"
"Password Will Be Used")
                obj_lbl_2.setGeometry(QtCore.QRect(0, 22, 81, 22))
                obj_lbl_2.setText("Archivename")
                obj_cmbox.setGeometry(QtCore.QRect(81, 22, 492, 22))
                obj_cmbox.addItem("")
                obj_cmbox.addItem("")
                obj_cmbox.setItemText(0, ".7z")
                obj_cmbox.setItemText(1, ".zip")
                obj_cmbox.setToolTip("Select An Available Archive Type\n"
"To Archive All OR Selected List Items,\n"
"Name Archive Accordingly\n"
"(i.e Name Must Not Be Existing File,\n"
"Specify Full Archive Path OR\n"
"Archive Will Be In Default Folder)")
            else:
                obj_cmbox.addItem("")
                obj_cmbox.setItemText(0, "")
                obj_cmbox_2=QtWidgets.QComboBox(wgt)
                obj_cmbox_2.setEditable(True)
                obj_cmbox_2.setFont(self.font)
                obj_cmbox_2.setMaxVisibleItems(15)
                obj_cmbox_2.addItem("")
                obj_cmbox_2.setItemText(0, "")
                if menu=='Parse':
                    obj_lbl.setGeometry(QtCore.QRect(0, 0, 41, 22))
                    obj_lbl.setText("Regex")
                    obj_cmbox.setGeometry(QtCore.QRect(41, 0, 532, 22))
                    obj_cmbox.addItems(plst)
                    obj_cmbox.setToolTip("Set A Regex String, OR\n"
"Select Preconfigured Regex Search,\n"
"To Parse All OR Selected List Items,\n"
"For Regex Matches")
                    obj_lbl_2.setGeometry(QtCore.QRect(0, 22, 51, 22))
                    obj_lbl_2.setText("Output")
                    obj_cmbox_2.setGeometry(QtCore.QRect(51, 22, 522, 22))
                    obj_cmbox_2.addItem("")
                    obj_cmbox_2.setItemText(1, "<Default>")
                    obj_cmbox_2.addItems(self.drv)
                    obj_cmbox_2.setToolTip("Set Regex Output File,\n"
"OR Select <Default>\n"
"(i.e Default Output File),\n"
"To Save Regex Matches To")
                else:
                    obj_lbl.setGeometry(QtCore.QRect(0, 0, 47, 22))
                    obj_lbl.setText("Source")
                    obj_cmbox.setGeometry(QtCore.QRect(47, 0, 526, 22))
                    obj_cmbox.addItem("")
                    obj_cmbox.setToolTip("File/Folder To Be\n"
"Copied OR Moved From")
                    obj_cmbox.setItemText(1, "<All OR Selected List Items>")
                    obj_cmbox.addItems(self.drv)
                    obj_lbl_2.setGeometry(QtCore.QRect(0, 22, 73, 22))
                    obj_lbl_2.setText("Destination")
                    obj_cmbox_2.setGeometry(QtCore.QRect(73, 22, 500, 22))
                    obj_cmbox_2.addItems(self.drv)
                    obj_cmbox_2.setToolTip("File/Folder To Be\n"
"Copied OR Moved To")
            obj_btn=QtWidgets.QPushButton(wgt)
            obj_btn.setGeometry(QtCore.QRect(-1, 43, 575, 24))
            obj_btn.setStyleSheet("background-color: rgb(153, 153, 153);\n"
"color: rgb(0, 0, 0);")
        elif menu=='About':
            wgt.setFixedSize(QtCore.QSize(780, 291))
            obj_plainTextEdit=QtWidgets.QPlainTextEdit(wgt)
            obj_plainTextEdit.setGeometry(QtCore.QRect(0, 0, 781, 291))
            obj_plainTextEdit.setFont(self.font)
            obj_plainTextEdit.setStyleSheet("color: rgb(0, 255, 0);\n"
"background-color: rgb(0, 0, 0);")
            obj_plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            obj_plainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            obj_plainTextEdit.setObjectName("plainTextEdit")
            obj_plainTextEdit.setPlainText(
"██╗░░░░░░░██╗██╗░░░██╗██████╗░██████╗░███████╗░░░░░░██████╗░███████╗██╗░░░██╗░██████╗\n"
"██║░░██╗░░██║██║░░░██║██╔══██╗██╔══██╗╚════██║░░░░░░██╔══██╗██╔════╝██║░░░██║██╔════╝\n"
"╚██╗████╗██╔╝██║░░░██║██║░░██║██║░░██║░░███╔═╝█████╗██║░░██║█████╗░░╚██╗░██╔╝╚█████╗░\n"
"░████╔═████║░██║░░░██║██║░░██║██║░░██║██╔══╝░░╚════╝██║░░██║██╔══╝░░░╚████╔╝░░╚═══██╗\n"
"░╚██╔╝░╚██╔╝░╚██████╔╝██████╔╝██████╔╝███████╗░░░░░░██████╔╝███████╗░░╚██╔╝░░██████╔╝\n"
"░░╚═╝░░░╚═╝░░░╚═════╝░╚═════╝░╚═════╝░╚══════╝░░░░░░╚═════╝░╚══════╝░░░╚═╝░░░╚═════╝░\n"
"\n"
"About Me: \n"
"    I\'m just a chill, humble, respectful & approachable guy aka the python-developer Wuddz-Devs ^_o,\n"
"    who enjoys a good laugh, meeting & interacting with other like-minded individuals who are willing to share,\n"
"    while using my imagination, knowledge & skills to create awesome, efficient and user-friendly applications\n"
"    to share with the world or any personal requests if applicable.\n"
"\n"
"Contact Me:\n"
"    Email:          wuddz_devs@protonmail.com\n"
"    Github:        https://github.com/wuddz-devs\n"
"    Reddit:        https://reddit.com/user/wuddz-devs\n"
"    Telegram:    https://t.me/wuddz_devs\n"
"    Youtube:     wuddz-devs\n"
"    Donation:    0x1F1C47dD653Af628D394eac7bAA9Ccf774fd784f  (Ethereum)")
        self.obj_cmbox=obj_cmbox
        self.obj_cmbox_2=obj_cmbox_2
        self.obj_lineEdit=obj_lineEdit
        if menu=='Open':obj_btn.clicked.connect(self.open_file)
        elif menu=='Save':obj_btn.clicked.connect(self.save_list)
        elif menu=='Delete':obj_btn.clicked.connect(self.del_fof)
        elif menu=='Copy' or menu=='Move':obj_btn.clicked.connect(lambda: self.cp_move(menu))
        elif menu=='Parse' in menu:obj_btn.clicked.connect(lambda: self.regex_search())
        elif 'Archive' in menu:obj_btn.clicked.connect(lambda: self.archive_list(menu))
        if obj_btn:
            obj_btn.setFont(self.font)
            obj_btn.setText(menu.split('_')[0])
        wgt.setWindowTitle(menu.split('_')[0])
        wgt.setWindowIcon(self.icon)
        fg=wgt.frameGeometry()
        cp=QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.wgt=wgt
        self.wgt.move(fg.topLeft())
        self.wgt.show()
        self.cw=QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self.wgt)
        self.cw.activated.connect(lambda: self.wgt.close())
    
    def file_size(self,val):
        if val<1024:val=f'{val} B'
        elif val>1024 and val<1048576:val=f'{val/1024:.1f} KB'
        elif val>1048576 and val<1073741824:val=f'{val/1048576:.2f} MB'
        elif val>1073741824:val=f'{val/1073741824:.2f} GB'
        return val
    
    def out_dir(self,epath):
        fld=''
        try:
            if Path(epath.parent).is_dir():fld='valid'
        except:pass
        if not fld:epath=Path(self.pkg).joinpath(epath)
        return epath
    
    def enum_list(self,list):
        eout=[]
        total=0
        for i,f in enumerate([x for x in list if Path(x).exists()],start=1):
            me=''
            try:
                mt=time.ctime(Path.stat(f).st_mtime)
                total+=Path.stat(f).st_size
                fs=self.file_size(Path.stat(f).st_size)
                eout.append(f'{i}  {f}'+' '*4+str(fs)+' '*2+mt)
                me='boss'
            except:pass
            if not me:eout.append(f'{i} {f}')
        total=self.file_size(total)
        eout.append('Total File Size►► '+str(total))
        return eout

    def search_main(self):
        try:
            self.sfst=''
            self.slist=''
            stt="Error Occurred!!"
            self.listarea.clear()
            di=self.directoryinput.currentText()
            sf=self.searchformat.currentText()
            if sf and Path(di).exists():
                self.flst=list(Path(di).rglob(sf))
                self.fst=self.enum_list(self.flst)
                self.listarea.addItem("")
                self.listarea.addItems(self.fst)
                stt="Total Items: "+str(len(self.flst))
        except:pass
        self.centralwidget.setStatusTip(str(stt))
    
    def open_file(self,fto=None):
        try:
            stt="Error Occurred!!"
            if not fto:fto=self.out_dir(self.obj_cmbox.currentText())
            else:fto=re.search('\d  (.*?)    \d',fto.text()).group(1)
            if Path(fto).is_file():
                if name=='nt':
                    if Path(fto).suffix=='.exe':Popen(['start',str(fto)],shell=True)
                    else:Popen([str(fto)],shell=True)
                else:Popen(['open '+str(fto)],shell=True)
                stt="Opened '{}' Successfully".format(fto)
        except:pass
        self.centralwidget.setStatusTip(stt)
        
    def save_list(self):
        try:
            stt="Error Occurred!!"
            slst=self.fst
            if self.sfst:slst=self.sfst
            opath=self.obj_cmbox.currentText()
            if opath=='<Default>':opath=self.lo
            else:opath=self.out_dir(self.obj_cmbox.currentText())
            with open(str(opath), 'w', encoding='utf-8') as ep:
                [ep.write(f'{e}\n') for e in slst]
            stt="List Saved Successfully ►► {}".format(opath)
        except:pass
        self.centralwidget.setStatusTip(stt)
    
    def cp_move(self,menu):
        try:
            stt="Error Occurred!!"
            src=str(self.obj_cmbox.currentText())
            des=str(self.obj_cmbox_2.currentText())
            ev="f'Item(s) Moved Successfully ►► {des}'"
            cpml=self.flst
            if self.slist:cpml=self.slist
            if menu=='Copy':
                ev=ev.replace('Moved','Copied')
                if src=='<All OR Selected List Items>' and Path(des).is_dir():
                    self.list_modes(['shutil.copy(fp,dec)'],cpml,des=des)
                elif Path(src).is_file():shutil.copy(src,self.out_dir(des))
                elif Path(des).is_dir():shutil.copytree(src,des,dirs_exist_ok=True,symlinks=True)
            else:
                if src=='<All OR Selected List Items>' and Path(des).is_dir():
                    self.list_modes(['shutil.move(fp,dec)'],cpml,des=des)
                else:shutil.move(src,des)
            stt=eval(ev)
        except:pass
        self.centralwidget.setStatusTip(stt)
    
    def del_fof(self):
        try:
            stt="Error Occurred!!"
            df=self.obj_cmbox.currentText()
            dlst=self.flst
            if self.slist:dlst=self.slist
            if df=='<All OR Selected List Items>':
                self.list_modes(['Path(fp).unlink()','shutil.rmtree(fp)'],dlst)
                df=(str(df).replace('<','')).replace('>','')
            elif Path(df).is_file():Path(df).unlink()
            else:shutil.rmtree(df)
            stt="Deleted '{}' Successfully".format(df)
        except:pass
        self.centralwidget.setStatusTip(stt)

    def regex_search(self):
        try:
            plst=[]
            rp=self.obj_cmbox.currentText()
            opf=self.obj_cmbox_2.currentText()
            if opf=='<Default>':opf=self.dr
            else:opf=self.out_dir(opf)
            rgp={
            '<IPTV_ACCOUNT>':'(h\w+://[\w\-\.]+:?\w+/?\w+?/c/)(\s+)?(\S+)?(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})',
            '<IPTV_SERVER_URL>':'h\w+://[\w\-\.]+:?\w+/?\w+?/c',
            '<IP+IP:PORT>':'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:?\d{1,5}',
            '<URL>':'\w+://[\w\-\.]+.*$',
            '<MAC_ADDRESS>':'\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}',
            '<EMAIL:PASSWORD>':'[\w\.-]+@[\w\.-]+:[\w\.-]+',
            '<USER:PASSWORD>':'^[\w\.-]+:[\w\.-]+$',
            '<M3U_URL>':'(h\w+://[\w\-\.]+:?\w+/get.php\?username=\S+?&)(\S+?)?(password=\S+?&)'
            }
            if rgp.get(rp):
                rlst=self.flst
                if self.slist:rlst=self.slist
                for file in rlst:
                    if Path(file).is_file():
                        with open(str(file), 'r', encoding="utf8", errors ='replace') as f:
                            if rp=='<IPTV_ACCOUNT>':[plst.append(f'{a.group(1)} {a.group(4).upper()}') for b in (x for x in f) for a in re.finditer(str(rgp[rp]),b)]
                            elif rp=='<M3U_URL>':[plst.append(f'{a.group(1)}{a.group(3).lower()}') for b in (x for x in f) for a in re.finditer(str(rgp[rp]),b)]
                            else:[plst.append(a) for b in (x for x in f) for a in re.compile(str(rgp[rp])).findall(b)]
                if plst:
                    self.regex_output(sorted(set(plst)),opf)
                    return
        except:pass
        self.centralwidget.setStatusTip("Error Occurred!!")

    def regex_output(self,lst,opf):
        with open(opf, 'w', encoding='utf-8') as out:
            [out.write(f'{r}\n') for r in lst]
        self.centralwidget.setStatusTip(str(len(lst))+" Matches Saved ►► "+str(opf))
    
    def archive_list(self,menu):
        stt="Error Occurred!!"
        if self.flst:
            st=[]
            pkk=''
            try:
                ap=self.obj_cmbox.currentText()
                if len(ap.split('.')[0])!=0:
                    ap=self.out_dir(ap)
                    if not Path(ap).exists():
                        alst=self.flst
                        if self.slist:alst=self.slist
                        ndp=[file for file in alst if Path(file).is_file() and not str(alst).count(str(PurePath(file).name))>1]
                        dup=[file for file in alst if Path(file).is_file() and str(alst).count(str(PurePath(file).name))>1]
                        if menu=='Archive_E' and str(Path(ap).suffix) in '.7z,.zip':
                            pkk=self.obj_lineEdit.text()
                            if not pkk:pkk=''.join(secrets.choice((string.ascii_letters+string.digits).strip()) for i in range(32))
                            sub="run(['7z', 'a', '-t'+str(epath).split('.')[1], epath, '@'+lst, '-mx9', '-p'+pkk], capture_output=True, text=True)"
                            pwf=str(Path(ap).stem)
                            with open(str(self.af).replace('archive',pwf), 'w', encoding='utf-8') as ps:
                                ps.write("'"+str(Path(ap).resolve())+"'\n"+str(pkk)+'\n'+'_'*146+'\n\n')
                        elif menu=='Archive_No_E' and str(Path(ap).suffix) in '.7z,.zip,.tar':
                            sub="run(['7z', 'a', '-t'+str(epath).split('.')[1], epath, '@'+lst, '-mx9'], capture_output=True, text=True)"
                        if ndp:st.append(self.list_archive(ap,ndp,sub,pkk=pkk))
                        if dup:st.append(self.list_archive(ap,dup,sub,dpl='yes'))
            except:pass
            if Path(self.lf).exists():Path(self.lf).unlink()
            st=list(filter(None, st))
            if st:stt=st[0]
        self.centralwidget.setStatusTip(stt)
    
    def list_modes(self,lst,elst,des=None):
        for fp in elst:
            dc=0
            if des!=None:
                fn=Path(fp).name
                while Path(des).joinpath(fn).exists():
                    dc+=1
                    fn=str(Path(fp).stem)+f'_{dc}'+str(Path(fp).suffix)
                dec=str(Path(des).joinpath(fn))
            for l in lst:
                try:
                    eval(l)
                except:pass
    
    def list_archive(self,epath,list,sub,dpl=None,pkk=None):
        try:
            lst=str(self.lf)
            with open(lst, 'w', encoding='utf-8') as bn:
                [bn.write(f'{file}\n') for file in list]
            if dpl!=None:sub=sub.replace(" epath,", " epath, '-spf',")
            out=eval(sub)
            if 'Everything is Ok' in str(out) and dpl==None:
                return "Files Archived Successfully ►► {}".format(str(Path(epath).resolve()))
        except:pass


if __name__ == "__main__":
    try:
        import sys
        app=QtWidgets.QApplication(sys.argv)
        app.setStyle('Fusion')
        MainWindow=QtWidgets.QMainWindow()
        ui=Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    except:pass
