import secrets, string, sys, re, time, shutil, signal, platform
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path, PurePath
from subprocess import run, Popen, DEVNULL
from os import rename, path, kill, getpid


class WorkerSignals(QtCore.QObject):
    finished=QtCore.pyqtSignal(object)


class Worker(QtCore.QRunnable):
    def __init__(self, fn, *args):
        super().__init__()
        self.fn=fn
        self.args=args
        self.signals=WorkerSignals()
    
    def run(self):
        res=self.fn(*self.args)
        self.signals.finished.emit(res)


class Search_Gui(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drv=['']
        for i in ['sfst','slist','flst','fst','rows','ctask']:
            exec(f'self.{i}=""')
        self.free=True
        self.name=platform.system()
        self.kp={'Windows':'taskkill /F /IM 7z.exe','Linux':'killall -9 7z','Darwin':'killall 7z'}
        self.sf=["","*","*.py","*.txt","*.jpg","*.jpeg","*.png","*.gif","*.mp4","*.mkv","*.wmv","*.mp3","*.exe"]
        self.ico=str((Path(__file__).absolute().parent).joinpath('wudz-sgui.ico'))
        self.pkg=str(Path.home().expanduser().joinpath('Downloads','SEARCH'))
        self.lf=Path(self.pkg).joinpath('file.lst')
        self.dr=Path(self.pkg).joinpath('regex_output.txt')
        self.af=Path(self.pkg).joinpath('archive-pwd.txt')
        self.lo=Path(self.pkg).joinpath('list-output.txt')
        if not Path(self.pkg).exists():Path(self.pkg).mkdir(parents=True, exist_ok=True)
        home=['','Desktop','Documents','Downloads','Music','Pictures','Videos']
        drv=[str(Path.home().expanduser().joinpath(x)) for x in home]
        drv.append(self.pkg)
        if self.name=='Windows':
            self.drv.extend([f'{x}:\\' for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if path.exists(f'{x}:')])
        else:
            drv.insert(0,'/')
            out=run(['df'], capture_output=True, text=True)
            drvv=re.findall('(/media/\w+/\w+)',str(out))
            if drvv:drv.extend(drvv)
        self.drv.extend(sorted(drv))
        self.la=[
            "Search Formats:    [.ext=File Extension]",
            "*              All Files In Directory",
            "file.txt      Files Named 'file.txt'",
            "*.ext        Files With .ext File Extension  [e.g *.txt Find All Text Files]",
            "test*        Files With Filename Starting With 'test'  [.ext Optional e.g test*.jpg]",
            "*test        Files With Filename Ending With 'test'  [.ext Optional e.g test*.jpg]",
            "*test*      Files With 'test' Anywhere In Filename  [.ext Optional e.g *test*.py]",
            "*te*st*    Files With 'te' Followed By 'st' Anywhere In Filename [.ext Optional e.g *te*st*.py]"]
        self.setupUi()
    
    def setupUi(self):
        self.setMinimumSize(QtCore.QSize(825, 664))
        self.setWindowTitle("Wuddz-Search-Gui")
        self.icon=QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(self.ico), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)
        self.frameGeometry=self.frameGeometry()
        self.cp=QtWidgets.QDesktopWidget().availableGeometry().center()
        self.frameGeometry.moveCenter(self.cp)
        self.move(self.frameGeometry.topLeft())
        self.centralwidget=QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.font=QtGui.QFont()
        self.font.setFamily("Tahoma")
        self.font.setPointSize(10)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.ui_layout()
        self.ui_menu()
        self.label_main()
        self.searchformat=self.set_params(widget='QComboBox',obj=self.centralwidget,
mi=13,name='searchformat',tt="Input OR Select Search Format",items=self.sf)
        self.directoryinput=self.set_params(widget='QComboBox',obj=self.centralwidget,
mi=15,name='directoryinput',tt="Input OR Select Search Directory",items=self.drv)
        self.searchformat.installEventFilter(self)
        self.directoryinput.installEventFilter(self)
        self.searchbtn=self.lbtn_widget(widget="QPushButton",obj=self.centralwidget,name="searchbtn",text="Search")
        self.listarea=self.list_widget(widget='QListWidget',obj=self.centralwidget,name='listarea')
        self.hdoc=self.list_widget(widget='QListWidget',obj=self.centralwidget,name='hdoc',items=self.la)
        self.statusBar=self.set_params(widget='QStatusBar',name='statusBar',obj=self.centralwidget)
        self.ui_layout_add()
        self.centralwidget.setLayout(self.windowLayout)
        self.setCentralWidget(self.centralwidget)
        self.threadpool=QtCore.QThreadPool.globalInstance()
        self.searchbtn.clicked.connect(self.search_main)
        self.listarea.itemDoubleClicked.connect(lambda: self.open_file(self.listarea.currentItem()))
        self.listarea.itemSelectionChanged.connect(lambda: self.list_selection())
        self.actionOpen.triggered.connect(lambda: self.menu_main('Open'))
        self.actionSave.triggered.connect(lambda: self.menu_main('Save'))
        self.actionQuit.triggered.connect(lambda: self.closeEvent(QtGui.QCloseEvent))
        self.actionCopy.triggered.connect(lambda: self.menu_main('Copy'))
        self.actionMove.triggered.connect(lambda: self.menu_main('Move'))
        self.actionDelete.triggered.connect(lambda: self.menu_main('Delete'))
        self.actionRename.triggered.connect(lambda: self.menu_main('Rename'))
        self.actionParse.triggered.connect(lambda: self.menu_main('Parse'))
        self.actionAbout.triggered.connect(lambda: self.menu_main('About'))
        self.actionNo_Encryption.triggered.connect(lambda: self.menu_main('Archive_No_E'))
        self.actionEncryption.triggered.connect(lambda: self.menu_main('Archive_E'))
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def ui_layout(self):
        ld={'window':'QtWidgets.QVBoxLayout','text':'QtWidgets.QVBoxLayout',
            'dir':'QtWidgets.QGridLayout','list':'QtWidgets.QVBoxLayout'}
        for k,v in ld.items():
            exec(f'self.{k}Layout={v}()')
            exec(f'self.{k}Layout.setContentsMargins(1,1,1,4)')
            exec(f'self.{k}Layout.setSpacing(1)')
    
    def ui_menu(self):
        ad={'File':['Open__Ctrl+O','Save__Ctrl+S','Quit__Ctrl+Q'],
            'Edit':['Copy__Alt+C','Move__Alt+M','Delete__Alt+Del','Rename__Alt+R','Parse__Alt+P'],
            'Archive':['Encryption__Alt+E','No Encryption__Alt+N'],
            'Help':['About__Alt+H']}
        self.menuBar=self.set_params(widget='QMenuBar',name='menuBar',obj=self.centralwidget)
        for k,v in ad.items():
            exec(f'self.menu{k}=self.set_params(name="menu{k}",obj=self.menuBar,widget="QMenu")')
            exec(f'self.menu{k}.setTitle("{k}")')
            exec(f'self.menuBar.addAction(self.menu{k}.menuAction())')
            for i in v:
                h=i.replace(' ','_').split('__')
                exec(f'self.action{h[0]}=QtWidgets.QAction(self.centralwidget)')
                exec(f'self.action{h[0]}.setObjectName("action{h[0]}")')
                exec(f'self.action{h[0]}.setText("{h[0]}")')
                exec(f'self.action{h[0]}.setShortcut("{h[1]}")')
                exec(f'self.action{h[0]}.setShortcutContext(QtCore.Qt.ApplicationShortcut)')
                exec(f'self.menu{k}.addAction(self.action{h[0]})')
    
    def label_main(self):
        sd={0:'Search Format',1:' '*28,2:'Search Directory',3:' '*28,4:' '*28,5:' '*28}
        for k,v in sd.items():
            exec(f'self.label_{k}=self.lbtn_widget(widget="QLabel",obj=self.centralwidget,name="label_{k}",text="{v}")')
    
    def lbtn_widget(self,**kwargs):
        ss={'QLabel':"background-color: rgb(0, 0, 0); color: rgb(0, 255, 0);",
            'QPushButton':"background-color: rgb(153, 153, 153); color: rgb(0, 0, 0);"}
        kwargs['style']=ss[kwargs['widget']]
        return self.set_params(**kwargs)
    
    def ui_layout_add(self):
        wd={'window':['menuBar'],'text':['hdoc'],
            'dir':['label_0@0-0','searchformat@0-1','label_1@0-2',
                   'label_2@1-0','directoryinput@1-1','label_3@1-2',
                   'label_4@2-0','searchbtn@2-1','label_5@2-2'],
            'list':['listarea','statusBar']}
        for k,v in wd.items():
            for i in v:
                if k=='dir':
                    wid=i.split('@')[0]
                    grd=(i.split('@')[1]).split('-')
                    exec(f'self.{k}Layout.addWidget(self.{wid},{grd[0]},{grd[1]})')
                    if grd[1]=='1':self.dirLayout.setColumnStretch(1,2)
                else:exec(f'self.{k}Layout.addWidget(self.{i})')
        for w in wd.keys():
            if w!='window':exec(f'self.windowLayout.addLayout(self.{w}Layout)')
    
    def set_params(self,**kwargs):
        var=kwargs['name']
        if kwargs.get('widget'):var=eval(f'QtWidgets.{kwargs["widget"]}')(kwargs["obj"])
        var.setFont(self.font)
        var.setObjectName(str(var))
        if kwargs.get('style'):var.setStyleSheet(kwargs["style"])
        if kwargs.get('geom'):exec(f'var.setGeometry(QtCore.QRect({kwargs["geom"]}))')
        if kwargs.get('text'):var.setText(kwargs['text'])
        if kwargs.get('tt'):var.setToolTip(kwargs['tt'])
        if kwargs.get('items'):var.addItems(kwargs['items'])
        if kwargs.get('mi'):var.setMaxVisibleItems(kwargs['mi'])
        if kwargs.get('widget'):
            if kwargs['widget']=='QPushButton':var.setDefault(True)
            elif kwargs['widget']=='QComboBox':var.setEditable(True)
        return var
    
    def list_widget(self,**kwargs):
        ld={'listarea':"background-color: rgb(0, 0, 0); color: rgb(0, 100, 255);",
            'hdoc':"background-color: rgb(0, 0, 0); color: rgb(0, 255, 0);"}
        kwargs['style']=ld[kwargs['name']]
        lwd=self.set_params(**kwargs)
        if kwargs['name']=='hdoc':
            lwd.setMaximumHeight(lwd.sizeHintForRow(0)*lwd.count()+2*lwd.frameWidth())
        else:lwd.installEventFilter(self)
        lwd.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        lwd.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        lwd.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        lwd.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        lwd.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        lwd.setResizeMode(QtWidgets.QListView.Adjust)
        return lwd
    
    def closeEvent(self,event):
        try:
            self.out.terminate()
        except:pass
        kill(getpid(), signal.SIGTERM)
    
    def eventFilter(self,source,event):
        if source is self.listarea and self.listarea:
            if event.type()==QtCore.QEvent.ContextMenu:
                menu=QtWidgets.QMenu()
                sv=menu.addAction('Save')
                cp=menu.addAction('Copy')
                mv=menu.addAction('Move')
                dl=menu.addAction('Delete')
                rn=menu.addAction('Rename')
                pr=menu.addAction('Parse')
                en=menu.addAction('Encryption')
                ne=menu.addAction('No Encryption')
                trig=menu.exec_(event.globalPos())
                item=source.itemAt(event.pos())
                if trig==sv:self.menu_main('Save')
                elif trig==cp:self.menu_main('Copy')
                elif trig==mv:self.menu_main('Move')
                elif trig==dl:self.menu_main('Delete')
                elif trig==rn:self.menu_main('Rename')
                elif trig==pr:self.menu_main('Parse')
                elif trig==en:self.menu_main('Archive_E')
                elif trig==ne:self.menu_main('Archive_No_E')
                return True
            elif event.type()==QtCore.QEvent.KeyPress and event.matches(QtGui.QKeySequence.InsertParagraphSeparator):
                self.open_file('d')
        elif source is self.searchformat or source is self.directoryinput:
            if event.type()==QtCore.QEvent.KeyPress and event.matches(QtGui.QKeySequence.InsertParagraphSeparator):
                self.search_main()
        return super().eventFilter(source,event)
    
    def menu_main(self,menu):
        obj_btn=''
        obj_cmbox=''
        obj_cmbox_2=''
        obj_lineEdit=''
        plst=['<IPTV_ACCOUNT>','<IPTV_SERVER_URL>','<IP+IP:PORT>','<URL>',
             '<MAC_ADDRESS>','<EMAIL:PASSWORD>','<USER:PASSWORD>','<M3U_URL>']
        wgt=QtWidgets.QDialog()
        wgt.setWindowTitle(menu.split('_')[0])
        wgt.setWindowIcon(self.icon)
        if menu=='About':
            wgt.setFixedSize(QtCore.QSize(732, 300))
            obj_plainTextEdit=self.set_params(widget='QPlainTextEdit',name='obj_plainTextEdit',obj=wgt,
style="color: rgb(0, 255, 0); background-color: rgb(0, 0, 0);",geom='0, 0, 732, 300')
            obj_plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            obj_plainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            obj_plainTextEdit.setPlainText(
"Source: \n"
"    https://github.com/wuddz-devs/Wuddz-Search-Gui\n"
"\n"
"About Me: \n"
"    I\'m just a chill, humble, respectful & approachable guy aka the python-developer Wuddz-Devs,\n"
"    who enjoys a good laugh, meeting & interacting with other like-minded individuals,\n"
"    who are willing to share, while using my imagination, knowledge & skills to create awesome,\n"
"    efficient and user-friendly applications, to share with the world\n"
"    or any personal requests if applicable.\n"
"\n"
"Contact Me:\n"
"    Email:          wuddz_devs@protonmail.com\n"
"    Github:        https://github.com/wuddz-devs\n"
"    Reddit:        https://reddit.com/user/wuddz-devs\n"
"    Telegram:    https://t.me/wuddz_devs\n"
"    Youtube:     wuddz-devs\n"
"    Donation:    0x1F1C47dD653Af628D394eac7bAA9Ccf774fd784f  (Ethereum)")
        else:
            wgt.setFixedSize(QtCore.QSize(574, 43))
            obj_lbl=self.lbtn_widget(widget='QLabel',name='obj_lbl',obj=wgt)
            obj_cmbox=self.set_params(widget='QComboBox',obj=wgt,mi=15,name='obj_cmbox')
            obj_btn=self.lbtn_widget(widget='QPushButton',name='obj_btn',obj=wgt,geom='-1, 20, 575, 24')
            if menu=='Delete':
                obj_lbl=self.set_params(name=obj_lbl,geom='0, 0, 80, 22',text="File/Folder")
                obj_cmbox=self.set_params(name=obj_cmbox,geom='80, 0, 494, 22',
items=["","<All OR Selected List Items>"],tt="Input File/Folder Path,\nOR Delete Selected Items")
            elif menu=='Save':
                obj_lbl=self.set_params(name=obj_lbl,geom='0, 0, 29, 22',text='File')
                obj_cmbox=self.set_params(name=obj_cmbox,geom='29, 0, 545, 22',items=["","<Default>"]+self.drv[1:])
                obj_cmbox.setToolTip("Set Output File, OR\n"
"Select '<Default>'\n"
"(i.e Default Output File)\n"
"To Save All, OR Selected \n"
"List Items As Text")
            elif menu=='Archive_No_E':
                obj_lbl=self.set_params(name=obj_lbl,geom='0, 0, 96, 22',text='Archivename')
                obj_cmbox=self.set_params(name=obj_cmbox,geom='96, 0, 478, 22',items=[".7z",".zip",".tar"])
                obj_cmbox.setToolTip("Select An Available Archive Type\n"
"To Archive All OR Selected List Items,\n"
"Name Archive Accordingly\n"
"(i.e Name Must Not Be Existing File,\n"
"Specify Full Archive Path OR\n"
"Archive Will Be In Default Folder)")
            elif menu=='Open':
                obj_lbl=self.set_params(name=obj_lbl,geom='0, 0, 29, 22',text='File')
                obj_cmbox=self.set_params(name=obj_cmbox,geom='29, 0, 545, 22',items=self.drv)
                obj_cmbox.setToolTip("Input File Path To Open\nFile With Default Program")
            elif menu in 'Copy,Move,Archive_E,Rename,Parse':
                wgt.setFixedSize(QtCore.QSize(574, 66))
                obj_lbl_2=self.lbtn_widget(widget='QLabel',name='obj_lbl_2',obj=wgt)
                obj_btn.setGeometry(QtCore.QRect(-1, 43, 575, 24))
                if menu=='Archive_E':
                    obj_lbl=self.set_params(name=obj_lbl,geom='0, 0, 72, 22',text='Password')
                    obj_lbl_2=self.set_params(name=obj_lbl_2,geom='0, 22, 96, 22',text='Archivename')
                    obj_lineEdit=self.set_params(widget='QLineEdit',name='obj_lineEdit',obj=wgt,geom='72, 0, 502, 22')
                    obj_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
                    obj_lineEdit.setToolTip("Set A Password,\n"
"If No Password Is Set,\n"
"A Randomly Generated\n"
"Password Will Be Used")
                    obj_cmbox=self.set_params(name=obj_cmbox,geom='96, 22, 478, 22',items=[".7z",".zip"])
                    obj_cmbox.setToolTip("Select An Available Archive Type\n"
"To Archive All OR Selected List Items,\n"
"Name Archive Accordingly\n"
"(i.e Name Must Not Be Existing File,\n"
"Specify Full Archive Path OR\n"
"Archive Will Be In Default Folder)")
                else:
                    obj_cmbox_2=self.set_params(widget='QComboBox',obj=wgt,mi=15,name='obj_cmbox_2')
                    if menu=='Rename':
                        obj_lbl=self.set_params(name=obj_lbl,geom='0, 0, 32, 22',text='Old')
                        obj_cmbox=self.set_params(name=obj_cmbox,geom='32, 0, 542, 22',items=['','<Selected List Item>']+self.drv[1:])
                        obj_cmbox.setToolTip("Source File/Folder\nTo Be Renamed")
                        obj_lbl_2=self.set_params(name=obj_lbl_2,geom='0, 22, 32, 22',text='New')
                        obj_cmbox_2=self.set_params(name=obj_cmbox_2,geom='32, 22, 542, 22')
                        obj_cmbox_2.setToolTip("Set New File/Folder Name")
                    elif menu=='Parse':
                        obj_lbl=self.set_params(name=obj_lbl,geom='0, 0, 47, 22',text='Regex')
                        obj_cmbox=self.set_params(name=obj_cmbox,geom='47, 0, 527, 22',items=['']+plst)
                        obj_cmbox.setToolTip("Set A Regex String, OR\n"
"Select Preconfigured Regex Search,\n"
"To Parse All OR Selected List Items,\n"
"For Regex Matches")
                        obj_lbl_2=self.set_params(name=obj_lbl_2,geom='0, 22, 55, 22',text='Output')
                        obj_cmbox_2=self.set_params(name=obj_cmbox_2,geom='55, 22, 519, 22',items=["","<Default>"]+self.drv[1:])
                        obj_cmbox_2.setToolTip("Set Regex Output File,\n"
"OR Select <Default>\n"
"(i.e Default Output File),\n"
"To Save Regex Matches To")
                    else:
                        obj_lbl=self.set_params(name=obj_lbl,geom='0, 0, 52, 22',text='Source')
                        obj_cmbox=self.set_params(name=obj_cmbox,geom='52, 0, 522, 22',
items=["","<All OR Selected List Items>"]+self.drv[1:],tt="File/Folder To Be\nCopied OR Moved From")
                        obj_lbl_2=self.set_params(name=obj_lbl_2,geom='0, 22, 86, 22',text='Destination')
                        obj_cmbox_2=self.set_params(name=obj_cmbox_2,geom='86, 22, 488, 22',items=self.drv)
                        obj_cmbox_2.setToolTip("File/Folder To Be\nCopied OR Moved To")
        self.obj_cmbox=obj_cmbox
        self.obj_cmbox_2=obj_cmbox_2
        self.obj_lineEdit=obj_lineEdit
        if obj_btn:obj_btn.setText(menu.split('_')[0])
        if menu=='Open':obj_btn.clicked.connect(self.open_file)
        elif menu=='Rename':obj_btn.clicked.connect(self.rename_file)
        elif menu!='About':obj_btn.clicked.connect(lambda: self.thread_params(menu))
        fg=wgt.frameGeometry()
        cp=QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.wgt=wgt
        self.wgt.move(fg.topLeft())
        self.wgt.show()
        self.cw=QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self.wgt)
        self.cw.activated.connect(lambda: self.wgt.close())
    
    def thread_run(self,**var):
        if self.free:
            self.ctask=var['msg']
            self.free=False
            exec(f"self.worker=Worker({var['fn']},{var['arg']})")
            self.worker.signals.finished.connect(self.thread_result)
            self.threadpool.start(self.worker)
        self.statusbar_msg(self.ctask)
    
    def thread_params(self,menu):
        self.wgt.close()
        fd={'Save':'save_list','Delete':'del_fof','Copy':'cp_move','Move':'cp_move',
            'Parse':'regex_search','Archive_E':'archive_list','Archive_No_E':'archive_list'}
        md={'Save':'Saving...','Delete':'Deleting...','Copy':'Copying...','Move':'Moving...',
            'Parse':'Parsing...','Archive_No_E':'Archiving...','Archive_E':'Archiving...'}
        if menu in 'Copy,Move,Archive_E,Archive_No_E':
            self.thread_run(fn=f'self.{fd[menu]}',menu=menu,msg=md[menu],arg="var['menu']")
        else:self.thread_run(fn=f'self.{fd[menu]}',msg=md[menu],arg='')
    
    def thread_result(self,lst):
        self.ctask=''
        self.free=True
        if type(lst)==tuple:
            if type(lst[0])==str:
                self.statusbar_msg(lst[0])
                if lst[1]:
                    if self.rows:[self.listarea.takeItem(self.listarea.row(s)) for s in self.rows]
                    else:self.listarea.clear()
            else:self.list_add(lst[0],lst[1])
        else:self.statusbar_msg(lst)
    
    def list_add(self,fst,flst):
        self.fst=fst
        self.flst=flst
        if flst:self.listarea.addItems(fst)
        self.statusBar.showMessage(f"Total Items: {len(flst)}")
    
    def list_selection(self):
        try:
            self.sfst=''
            self.slist=''
            self.rows=self.listarea.selectedItems()
            rows=[str(x) for x in (str(self.listarea.selectedItems()[i].text()) for i in range(len(self.rows)))]
            self.slist=[re.search(r'(\/.*\.[\w:]+\S)',str(r)).group(1) for r in rows]
            self.sfst=[re.search('\d+  ((\/.*\.[\w:]+)(.*))',str(r)).group(1) for r in rows]
        except:pass
    
    def file_size(self,val):
        if val<1024:val=f'{val} B'
        elif val>1024 and val<1048576:val=f'{val/1024:.1f} KB'
        elif val>1048576 and val<1073741824:val=f'{val/1048576:.2f} MB'
        elif val>1073741824:val=f'{val/1073741824:.2f} GB'
        return val
    
    def out_dir(self,epath):
        if str(epath)!=str(Path(epath).absolute()):epath=Path(self.pkg).joinpath(epath)
        return epath
    
    def enum_list(self,di,sf):
        flst=[]
        lst=[]
        cnt=0
        tot=0
        for fn in Path(di).rglob(sf):
            if Path(fn).exists():
                flst.append(fn)
                cnt+=1
                tl,ls=self.enum_sub(fn,cnt)
                tot+=tl
                lst.append(ls)
        lst.append('Total File Size►► '+str(self.file_size(tot)))
        return lst,flst
    
    def enum_sub(self,fn,cnt):
        tl=0
        try:
            mt=time.ctime(Path.stat(fn).st_mtime)
            tl=Path.stat(fn).st_size
            fs=self.file_size(tl)
            return tl,f'{cnt}  {fn}'+' '*4+str(fs)+' '*2+mt
        except Exception:return tl,f'{cnt}  {fn}'
    
    def search_main(self):
        self.listarea.clear()
        di=self.directoryinput.currentText()
        sf=self.searchformat.currentText()
        if sf and di and self.free:
            self.thread_run(fn='self.enum_list',di=di,sf=sf,msg='Searching...',arg='var["di"],var["sf"]')
    
    def statusbar_msg(self,msg=None,t=0):
        if not msg:
            msg='Error Occurred!!'
            t=10000
        self.statusBar.showMessage(msg,t)
    
    def open_file(self,fto=None):
        if fto and len(self.slist)==1:fto=self.slist[0]
        elif not fto:
            self.wgt.close()
            fto=self.obj_cmbox.currentText()
        if Path(fto).is_file():
            if self.name=='Windows':
                if Path(fto).suffix=='.exe':Popen(['start',str(fto)],shell=True)
                else:Popen([str(fto)],shell=True)
            else:Popen(['open '+str(fto)],shell=True)
            self.statusbar_msg("Opened '{}' Successfully".format(fto))
        else:self.statusbar_msg()
    
    def rename_file(self):
        sr=False
        self.wgt.close()
        sf=self.obj_cmbox.currentText()
        nf=self.obj_cmbox_2.currentText()
        if sf and nf:
            if sf=='<Selected List Item>' and len(self.slist)==1:sr=self.rename_sub(self.slist[0],nf,sls='b')
            elif sf!='<Selected List Item>':sr=self.rename_sub(self.out_dir(sf),nf)
        if not sr:self.statusbar_msg()
    
    def rename_sub(self,sf,nf,sls=None):
        if Path(sf).exists():
            nf=Path(sf).parent.joinpath(nf)
            try:
                rename(sf,nf)
            except:pass
            if Path(nf).exists():
                self.statusbar_msg(f'"{Path(sf).name}" Renamed To "{Path(nf).name}" Successfully')
                if sls:self.rows[0].setText(self.enum_sub(nf,self.listarea.currentRow()+1)[1])
                return True
    
    def file_list(self,lst,slst):
        if slst:lst=slst
        return lst
    
    def save_list(self):
        slst=self.file_list(self.fst,self.sfst)
        op=self.obj_cmbox.currentText()
        if slst and op:
            if op=='<Default>':op=self.lo
            op=self.out_dir(op)
            if self.write_file(op,slst):
                return "List Saved Successfully ►► {}".format(op)
    
    def write_file(self,fp,lst):
        try:
            with open(fp, 'w', encoding='utf-8') as fw:
                [fw.write(f'{l}\n') for l in lst]
        except Exception:return False
        return True
    
    def cp_move(self,menu):
        try:
            src=str(self.obj_cmbox.currentText())
            des=str(self.obj_cmbox_2.currentText())
            cd={'Copy':'Copied','Move':'Moved'}
            cpml=self.file_list(self.flst,self.slist)
            if src and des:
                des=self.out_dir(des)
                if src!='<All OR Selected List Items>':src=self.out_dir(src)
                if src=='<All OR Selected List Items>':
                    typ='Item(s)'
                    if cpml and menu=='Copy':cpml=[c for c in cpml if Path(c).is_file()]
                    if cpml:self.list_modes([f'shutil.{menu.lower()}(fp,dec)'],cpml,des=des)
                    else:raise TypeError
                else:
                    if Path(src).is_file() and Path(des).is_dir():typ='File'
                    elif Path(src).is_dir():typ='Folder'
                    if typ=='Folder' and menu=='Copy':shutil.copytree(src,des)
                    elif typ:exec(f'shutil.{menu.lower()}(src,des)')
                return f'{typ} {cd[menu]} Successfully ►► {des}'
        except:pass
    
    def del_fof(self):
        dlst=[]
        try:
            df=self.obj_cmbox.currentText()
            if df=='<All OR Selected List Items>':
                dlst=self.file_list(self.flst,self.slist)
                self.list_modes(['Path(fp).unlink()','shutil.rmtree(fp)'],dlst)
                df=(str(df).replace('<','')).replace('>','')
            elif Path(df).is_file():Path(df).unlink()
            else:shutil.rmtree(df,ignore_errors=False,onerror=None)
            return "Deleted '{}' Successfully".format(df), dlst
        except:pass
    
    def regex_search(self):
        try:
            plst=[]
            rp=self.obj_cmbox.currentText()
            opf=self.obj_cmbox_2.currentText()
            if opf=='<Default>':opf=self.dr
            elif opf:opf=self.out_dir(opf)
            rgp={
            '<IPTV_ACCOUNT>':'(h\w+://[\w\-\.]+:?\w+/?\w+?/c)(\s+)?(\S+)?(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})',
            '<IPTV_SERVER_URL>':'h\w+://[\w\-\.]+:?\w+/?\w+?/c',
            '<IP+IP:PORT>':'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:?\d{1,5}',
            '<URL>':'\w+://[\w\-\.]+.*$',
            '<MAC_ADDRESS>':'\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}',
            '<EMAIL:PASSWORD>':'[\w\.-]+@[\w\.-]+:[\w\.-]+',
            '<USER:PASSWORD>':'^[\w\.-]+:[\w\.-]+$',
            '<M3U_URL>':'(h\w+://[\w\-\.]+:?\w+/get.php\?username=\S+?&)(\S+?)?(password=\S+?&)'
            }
            if rp and opf:
                rlst=self.file_list(self.flst,self.slist)
                for r in rlst:
                    if Path(r).is_file():
                        with open(str(r), 'r', encoding="utf8", errors ='replace') as f:
                            if rp=='<IPTV_ACCOUNT>':
                                [plst.append(f'{a.group(1)} {a.group(4).upper()}') for b in (x for x in f) for a in re.finditer(str(rgp[rp]),b)]
                            elif rp=='<M3U_URL>':
                                [plst.append(f'{a.group(1)}{a.group(3).lower()}') for b in (x for x in f) for a in re.finditer(str(rgp[rp]),b)]
                            else:
                                if rgp.get(rp):rp=rgp[rp]
                                [plst.append(a) for b in (x for x in f) for a in re.compile(str(rp)).findall(b)]
                if plst and self.write_file(opf,sorted(set(plst))):
                    return f'{len(plst)} Matches Saved ►► {opf}'
        except:pass
    
    def archive_list(self,menu):
        if self.flst:
            st=[]
            pkk=''
            try:
                ap=self.obj_cmbox.currentText()
                if str(Path(ap).suffix) in '.7z,.zip,.tar' and not Path(ap).exists():
                    ap=self.out_dir(ap)
                    alst=self.file_list(self.flst,self.slist)
                    dup,ndp=self.archive_sub(alst)
                    if menu=='Archive_E' and str(Path(ap).suffix)!='.tar':
                        pkk=self.obj_lineEdit.text()
                        if not pkk:pkk=''.join(secrets.choice((string.ascii_letters+string.digits).strip()) for i in range(32))
                        sub=['7z', 'a', '-t'+str(Path(ap).suffix)[1:], str(ap), '@'+str(self.lf), '-mx9', '-mhe', '-p'+pkk]
                        if str(Path(ap).suffix)=='.zip':sub=str(sub).replace(" '-mhe',",'')
                        pwf=str(Path(ap).stem)
                        with open(str(self.af).replace('archive',pwf), 'w', encoding='utf-8') as ps:
                            ps.write("'"+str(Path(ap).resolve())+"'\n"+str(pkk)+'\n'+'_'*146+'\n\n')
                    elif menu=='Archive_No_E':
                        sub=['7z', 'a', '-t'+str(Path(ap).suffix)[1:], str(ap), '@'+str(self.lf), '-mx9']
                    if ndp:st.append(self.list_archive(ap,ndp,sub,pkk=pkk))
                    if dup:st.append(self.list_archive(ap,dup,sub,pkk=pkk,dpl='yes'))
            except:pass
            if Path(self.lf).exists():Path(self.lf).unlink()
            st=list(filter(None, st))
            if st:return st[0]
    
    def archive_sub(self,lst):
        dup=[]
        ndup=[]
        for file in lst:
            if Path(file).is_file():
                if str(lst).count(str(PurePath(file).name))>1:dup.append(file)
                else:ndup.append(file)
        return dup, ndup
    
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
            self.write_file(lst,list)
            if dpl!=None:sub=str(sub).replace(" epath,", " epath, '-spf',")
            self.out=Popen(sub,shell=False,stdout=PIPE,stderr=PIPE,universal_newlines=True)
            if 'Everything is Ok' in str(self.out.communicate()[0]) and dpl==None:
                return "Files Archived Successfully ►► {}".format(str(Path(epath).resolve()))
        except:pass

def gui_main():
    QtWidgets.QApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app=QtWidgets.QApplication([])
    app.setStyle('Fusion')
    ws=Search_Gui()
    ws.show()
    sys.exit(app.exec_())
