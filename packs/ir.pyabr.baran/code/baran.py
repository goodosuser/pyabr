'''
    Pyabr OS

    Python Cloud Operating System Platform (c) 2021 PyFarsi. Free Software GNU General Public License v3.0

    - Informations

    * Name:             Pyabr
    * Founder:          Mani Jamali
    * Developers:       PyFarsi Community
    * Package Manager:  Paye, PyPI
    * License:          GNU General Publice License v3.0

    - Official Website

    * Persian Page:     https://pyabr.ir
    * English Page:     https://en.pyabr.ir
'''
import os,multiprocessing
import subprocess
import sys, hashlib

import PyQt5.QtCore
from pyabr.core import *
from pyabr.quick import *

res = Res()
control = Control()
files = Files()
app = App()
process = Process()
from PyQt5.QtGui import *
from PyQt5.QtQml import *
from PyQt5.QtCore import *
from PyQt5 import QtQml, QtGui, QtCore

application = QGuiApplication(sys.argv)
application.setWindowIcon(QIcon(res.get('@icon/breeze-cloud')))

files.write('/proc/info/id','desktop')

## Get data ##
def getdata (name):
    return control.read_record (name,'/etc/gui')

class Backend (MainApp):
    def runSplash (self):
        self.splash = Splash([self])

    def runLogin (self):
        self.login = Login([self])

    def runEnter (self):
        self.enter = Enter([self,control.read_record("username","/etc/gui")])
        control.write_record('username','guest','/etc/gui')

    def runDesktop (self):
        self.desktop = Desktop([self,control.read_record("username","/etc/gui"),control.read_record("password","/etc/gui")])
        control.write_record('username', 'guest', '/etc/gui')
        control.write_record('password', '*', '/etc/gui')

    def runUnlock (self):
        control.write_record('username', 'guest', '/etc/gui')

    def __init__(self):
        super(Backend,self).__init__()

        app.switch('desktop')
        self.load (res.get('@layout/backend'))
        self.setProperty ('height',int(getdata("height")))
        self.setProperty ('width',int(getdata("width")))
        self.setProperty ('title','Pyabr OS')
        self.setProperty ('visibility',getdata("visibility"))
        self.setProperty('font', QFont(getdata('font'), int(getdata('fontsize'))))

        # Actions

        params = getdata('params')

        control.write_record('params', 'gui', '/etc/gui')

        self.close()

        if params == 'splash':
            self.runSplash()
        elif params == 'login':
            self.runLogin()
        elif params == 'enter':
            self.runEnter()
        elif params == 'desktop':
            self.runDesktop()
        elif params == 'unlock':
            self.runUnlock()
        else:
            QTimer.singleShot(1000, self.runSplash)  ## Run splash after 1s

class Splash (MainApp):
    def runLogin (self):
        self.close()
        self.login = Login([self.Backend])

    def __init__(self,ports):
        super(Splash, self).__init__()

        app.switch('desktop')
        self.Backend = ports[0]
        self.load(res.get('@layout/splash'))
        self.setProperty('height', int(getdata("height")))
        self.setProperty('width', int(getdata("width")))
        self.setProperty('title', 'Pyabr OS')
        self.setProperty('visibility', getdata("visibility"))
        self.setProperty('font', QFont(getdata('font'), int(getdata('fontsize'))))

        QTimer.singleShot(3000, self.runLogin)  ## Run login

class Login (MainApp):
    def shutdown_ (self):
        subprocess.call(['poweroff'])

    def restart_ (self):
        subprocess.call(['reboot'])

    def sleep_ (self):
        self.sleep = Sleep()

    def lang_(self):
        pass

    def clean(self):
        self._username.setProperty('enabled',True)
        self._username.setProperty('placeholderText',res.get('@string/username_placeholder'))

    def next_(self):
        if self._username.property("text")=='':
            pass
        elif self._username.property("text")=='guest' and files.readall('/etc/guest'):
            self.close()
            self.desktop = Desktop([self.Backend, self._username.property("text"),'*'])
        elif files.isfile(f'/etc/users/{self._username.property("text")}'):
            self.close()
            self.enter = Enter([self.Backend,self._username.property("text")])
        else:
            self._username.setProperty('text','')
            self._username.setProperty("placeholderText",res.get('@string/user_not_found'))
            self._username.setProperty('enabled',False)
            QTimer.singleShot(3000,self.clean)

    NameRole = QtCore.Qt.UserRole + 1000
    LabelRole = QtCore.Qt.UserRole + 1001
    LogoRole = QtCore.Qt.UserRole + 1002

    def create_model(self):
        model = QtGui.QStandardItemModel()
        roles = {self.NameRole: b"name", self.LabelRole: b'label', self.LogoRole: b'logo'}
        model.setItemRoleNames(roles)
        for name in files.list('/usr/share/locales'):
                it = QtGui.QStandardItem(name)
                it.setData(name, self.NameRole)
                namex = control.read_record('name', f'/usr/share/locales/{name}')
                it.setData(namex, self.LabelRole)
                it.setData('../../../'+res.get(control.read_record('logo', f'/usr/share/locales/{name}')), self.LogoRole)
                model.appendRow(it)
        return model

    def __init__(self,ports):
        super(Login, self).__init__()

        app.switch('desktop')

        self.Backend = ports[0]

        self.langModel = self.create_model()
        self.rootContext().setContextProperty("Lang", self.langModel)

        self.load(res.get('@layout/login'))

        if not self.rootObjects():
            sys.exit(-1)

        self.setProperty('height', int(getdata("height")))
        self.setProperty('width', int(getdata("width")))
        self.setProperty('visibility', getdata("visibility"))
        self.setProperty('font', QFont(getdata('font'), int(getdata('fontsize'))))
        self.setProperty('title', 'Pyabr OS')

        # Connects

        self._submenu = self.findChild( 'submenu')
        self._submenu.setProperty('title',res.get('@string/etcmenu'))
        self._shutdown = self.findChild('shutdown')
        self._shutdown.setProperty('text',res.get('@string/escape'))
        self._shutdown.triggered.connect (self.shutdown_)
        self._restart = self.findChild( 'restart')
        self._restart.setProperty('text', res.get('@string/restart'))
        self._restart.triggered.connect(self.restart_)
        self._sleep = self.findChild( 'sleep')
        self._sleep.setProperty('text', res.get('@string/sleep'))
        self._sleep.triggered.connect(self.sleep_)
        self._next = self.findChild( 'next')
        self._username = self.findChild( 'username')
        self._username.setProperty("placeholderText",res.get('@string/username_placeholder'))
        self._next.clicked.connect(self.next_)
        self._next.setProperty('text',res.get('@string/next_text'))
        self._lang = self.findChild( 'lang')
        self._lang.setProperty('title', res.get('@string/keyless'))
        self._exit = self.findChild( 'exit')
        self._exit.setProperty('title', res.get('@string/powermenu'))
        self._background = self.findChild( 'background')
        self._background.setProperty('source', res.qmlget(getdata("login.background")))
        self._virtualkeyboard = self.findChild('virtualkeyboard')
        self._virtualkeyboard.setProperty('text',res.get('@string/vkey'))

class Sleep (MainApp):
    def __init__(self):
        super(Sleep, self).__init__()

        app.switch('desktop')

        self.load(res.get('@layout/sleep'))
        if not self.rootObjects():
            sys.exit(-1)

        # Get data

        self.setProperty('height', int(getdata("height")))
        self.setProperty('width', int(getdata("width")))
        self.setProperty('visibility', getdata("visibility"))
        self.setProperty('font', QFont(getdata('font'), int(getdata('fontsize'))))
        self.setProperty('title', 'Pyabr OS')


        # Connects
        self._wakeup = self.findChild( 'wakeup')
        self._wakeup.clicked.connect (self.close)

class Enter (MainApp):
    def shutdown_ (self):
        subprocess.call(['poweroff'])

    def restart_ (self):
        subprocess.call(['reboot'])

    def sleep_ (self):
        self.sleep = Sleep()

    def lang_(self):
        pass

    def clean(self):
        self._password.setProperty('enabled',True)
        self._password.setProperty('placeholderText', res.get('@string/password_placeholder'))

    def login_(self):
        if self._password.property("text")=='':
            pass
        elif control.read_record('code',f'/etc/users/{self.username}')==hashlib.sha3_512(self._password.property("text").encode()).hexdigest():
            self.close()
            self.desktop = Desktop([self.Backend,self.username,self._password.property("text")])
        else:
            self._password.setProperty('text','')
            self._password.setProperty("placeholderText","رمزعبور نادرست می باشد")
            self._password.setProperty('enabled',False)
            QTimer.singleShot(3000,self.clean)

    NameRole = QtCore.Qt.UserRole + 1000
    LabelRole = QtCore.Qt.UserRole + 1001
    LogoRole = QtCore.Qt.UserRole + 1002

    def create_model(self):
        model = QtGui.QStandardItemModel()
        roles = {self.NameRole: b"name", self.LabelRole: b'label', self.LogoRole: b'logo'}
        model.setItemRoleNames(roles)
        for name in files.list('/usr/share/locales'):
            it = QtGui.QStandardItem(name)
            it.setData(name, self.NameRole)
            namex = control.read_record('name', f'/usr/share/locales/{name}')
            it.setData(namex, self.LabelRole)
            it.setData('../../../'+res.get(control.read_record('logo', f'/usr/share/locales/{name}')), self.LogoRole)
            model.appendRow(it)
        return model

    def logout_(self):
        self.close()

        # Remove all tmp
        files.removedirs('/tmp')
        files.mkdir('/tmp')

        # Remove all ids
        app.endall()

        # Remove all switchs
        process.endall()

        # Logout
        System ("/vmabr gui-login")

    def getdata(self, name):
        x = control.read_record(name, f'/etc/users/{self.username}')
        if x == '' or x == None:
            x = getdata(name)

        return x

    def __init__(self, ports):
        super(Enter, self).__init__()

        app.switch('desktop')

        self.Backend = ports[0]
        self.username = ports[1]

        self.langModel = self.create_model()
        self.rootContext().setContextProperty("Lang", self.langModel)

        self.load(res.get('@layout/enter'))
        if not self.rootObjects():
            sys.exit(-1)

        # Get data

        self.setProperty('height', int(getdata("height")))
        self.setProperty('width', int(getdata("width")))
        self.setProperty('visibility', getdata("visibility"))
        self.setProperty('font', QFont(getdata('font'), int(getdata('fontsize'))))
        self.setProperty('title', 'Pyabr OS')

        # Connects

        self._submenu = self.findChild( 'submenu')
        self._submenu.setProperty('title',res.get('@string/etcmenu'))
        self._shutdown = self.findChild( 'shutdown')
        self._shutdown.setProperty('text',res.get('@string/escape'))
        self._shutdown.triggered.connect(self.shutdown_)
        self._restart = self.findChild( 'restart')
        self._restart.setProperty('text', res.get('@string/restart'))
        self._restart.triggered.connect(self.restart_)
        self._sleep = self.findChild( 'sleep')
        self._sleep.setProperty('text', res.get('@string/sleep'))
        self._sleep.triggered.connect(self.sleep_)
        self._login = self.findChild( 'login')
        self._password = self.findChild( 'password')
        self._password.setProperty('placeholderText',res.get('@string/password_placeholder'))
        self._login.clicked.connect(self.login_)
        self._login.setProperty('text',res.get('@string/enter_text'))
        self._lang = self.findChild( 'lang')
        self._lang.setProperty('title', res.get('@string/keyless'))
        self._logout = self.findChild( 'logout')
        self._logout.setProperty('text',res.get('@string/signout'))
        self._logout.triggered.connect(self.logout_)
        self._exit = self.findChild( 'exit')
        self._exit.setProperty('title', res.get('@string/powermenu'))
        self._account = self.findChild('account')
        self._account.setProperty('title',self.getdata("fullname"))
        self._background = self.findChild( 'background')
        self._background.setProperty('source', res.qmlget(self.getdata("enter.background")))
        self._profile = self.findChild('profile')
        self._profile.setProperty('source',res.qmlget(self.getdata("profile")))
        self._virtualkeyboard = self.findChild('virtualkeyboard')
        self._virtualkeyboard.setProperty('text',res.get('@string/vkey'))

class Unlock (MainApp):
    def clean(self):
        self._password.setProperty('enabled',True)

    def unlock_(self):
        if self._password.property("text")=='':
            pass
        elif control.read_record('code',f'/etc/users/{self.Env.username}')==hashlib.sha3_512(self._password.property("text").encode()).hexdigest():
            self.close()
        else:
            self._password.setProperty('text','')
            self._password.setProperty("placeholderText","رمزعبور نادرست می باشد")
            self._password.setProperty('enabled',False)
            QTimer.singleShot(3000,self.clean)

    def getdata(self, name):
        x = control.read_record(name, f'/etc/users/{self.Env.username}')
        if x == '' or x == None:
            x = getdata(name)

        return x

    NameRole = QtCore.Qt.UserRole + 1000
    LabelRole = QtCore.Qt.UserRole + 1001
    LogoRole = QtCore.Qt.UserRole + 1002

    def create_model(self):
        model = QtGui.QStandardItemModel()
        roles = {self.NameRole: b"name", self.LabelRole: b'label', self.LogoRole: b'logo'}
        model.setItemRoleNames(roles)
        for name in files.list('/usr/share/locales'):
            it = QtGui.QStandardItem(name)
            it.setData(name, self.NameRole)
            namex = control.read_record('name', f'/usr/share/locales/{name}')
            it.setData(namex, self.LabelRole)
            it.setData('../../../'+res.get(control.read_record('logo', f'/usr/share/locales/{name}')), self.LogoRole)
            model.appendRow(it)
        return model

    def __init__(self, ports):
        super(Unlock, self).__init__()

        app.switch('desktop')

        self.Backend = ports[0]
        self.Env = ports[1]

        self.langModel = self.create_model()
        self.rootContext().setContextProperty("Lang", self.langModel)

        self.load(res.get('@layout/unlock'))
        if not self.rootObjects():
            sys.exit(-1)

        # Get data

        self.setProperty('height', int(getdata("height")))
        self.setProperty('width', int(getdata("width")))
        self.setProperty('visibility', getdata("visibility"))
        self.setProperty('font', QFont(getdata('font'), int(getdata('fontsize'))))
        self.setProperty('title', 'Pyabr OS')

        # Connects
        self._password = self.findChild( 'password')
        self._password.setProperty('placeholderText',res.get('@string/password_placeholder'))
        self._unlock = self.findChild('login')
        self._unlock.setProperty('text',res.get('@string/unlock_text'))
        self._unlock.clicked.connect(self.unlock_)
        self._background = self.findChild( 'background')
        self._background.setProperty('source', res.qmlget(self.getdata("unlock.background")))
        self._profile = self.findChild( 'profile')
        self._profile.setProperty('source', res.qmlget(self.getdata("profile")))
        self._submenu = self.findChild('submenu')
        self._submenu.setProperty('title',res.get('@string/etcmenu'))
        self._virtualkeyboard = self.findChild( 'virtualkeyboard')
        self._virtualkeyboard.setProperty('text', res.get('@string/vkey'))
        self._lang = self.findChild( 'lang')
        self._lang.setProperty('title', res.get('@string/keyless'))

class Lock (MainApp):
    def unlock_(self):
        self.close()
        if not self.Env.username=='guest':
            self.unlock = Unlock([self.Backend,self.Env])

    def getdata (self,name):
        x = control.read_record(name,f'/etc/users/{self.Env.username}')
        if x=='' or x==None:
            x = getdata(name)

        return x

    def __init__(self, ports):
        super(Lock, self).__init__()

        app.switch('desktop')

        self.Backend = ports[0]
        self.Env = ports[1]

        self.load(res.get('@layout/lock'))
        if not self.rootObjects():
            sys.exit(-1)

        # Get data

        self.setProperty('height', int(getdata("height")))
        self.setProperty('width', int(getdata("width")))
        self.setProperty('visibility', getdata("visibility"))
        self.setProperty('font', QFont(getdata('font'), int(getdata('fontsize'))))
        self.setProperty('title', 'Pyabr OS')

        # Connects
        self._unlock = self.findChild('unlock')
        self._unlock.clicked.connect (self.unlock_)

        self._background = self.findChild( 'background')
        self._background.setProperty('source', res.qmlget(self.getdata("lock.background")))


class Shells:
    def __init__(self, ports):
        super(Shells, self).__init__()

        app.switch('desktop')

class MenuApplications:

    def __init__(self, ports):
        super(MenuApplications, self).__init__()

        app.switch('desktop')

class Desktop (MainApp):
    def shutdown_ (self):
        subprocess.call(['poweroff'])

    def restart_ (self):
        subprocess.call(['reboot'])

    def sleep_ (self):
        self.sleep = Sleep()

    def logout_(self):
        self.close()

        # Remove all tmp
        files.removedirs('/tmp')
        files.mkdir('/tmp')

        # Remove all ids
        app.endall()

        # Remove all switchs
        process.endall()

        # Logout
        System ("/vmabr gui-login")

    def switchuser_(self):
        System("/vmabr gui-login")

    def lock_(self):
        self.lock = Lock([self.Backend,self])

    NameRole = QtCore.Qt.UserRole + 1000
    LabelRole = QtCore.Qt.UserRole + 1001
    LogoRole = QtCore.Qt.UserRole + 1002
    pins = 0

    def create_model(self,dir_path,category):
        model = QtGui.QStandardItemModel()
        roles = {self.NameRole: b"name",self.LabelRole: b'label',self.LogoRole: b'logo'}
        model.setItemRoleNames(roles)
        for name in files.list(dir_path):
            categoryx = control.read_record('category',f'{dir_path}/{name}')
            hidden = control.read_record('hidden',f'{dir_path}/{name}')
            if categoryx==category and not hidden=='Yes':
                it = QtGui.QStandardItem(name)
                it.setData(name, self.NameRole)
                namex = control.read_record(f'name[{getdata("locale")}]',f'{dir_path}/{name}')
                if namex=='' or namex==None:
                    namex = control.read_record(f'name[en]', f'{dir_path}/{name}')
                it.setData(namex,self.LabelRole)
                it.setData('../../../'+res.get(control.read_record('logo',f'{dir_path}/{name}')),self.LogoRole)
                model.appendRow(it)
        return model

    def create_model2(self):
        model = QtGui.QStandardItemModel()
        roles = {self.NameRole: b"name", self.LabelRole: b'label', self.LogoRole: b'logo'}
        model.setItemRoleNames(roles)
        for name in files.list('/usr/share/locales'):
            it = QtGui.QStandardItem(name)
            it.setData(name, self.NameRole)
            namex = control.read_record('name', f'/usr/share/locales/{name}')
            it.setData(namex, self.LabelRole)
            it.setData('../../../'+res.get(control.read_record('logo', f'/usr/share/locales/{name}')), self.LogoRole)
            model.appendRow(it)
        return model


    def create_model3(self):
        model = QtGui.QStandardItemModel()
        roles = {self.NameRole: b"name", self.LabelRole: b'label', self.LogoRole: b'logo'}
        model.setItemRoleNames(roles)
        for name in files.list('/usr/share/applications'):
            if res.etc(name.replace('.desk',''),'pin')=='Yes':
                self.pins+=1
                it = QtGui.QStandardItem(name)
                it.setData(name, self.NameRole)
                namex = control.read_record(f'name[{getdata("locale")}]', f'/usr/share/applications/{name}')
                if namex == '' or namex == None:
                    namex = control.read_record(f'name[en]', f'/usr/share/applications/{name}')
                it.setData(namex, self.LabelRole)
                it.setData('../../../'+res.get(control.read_record('logo', f'/usr/share/applications/{name}')), self.LogoRole)
                model.appendRow(it)
        return model

    def create_model4(self,dir_path):
        model = QtGui.QStandardItemModel()
        roles = {self.NameRole: b"name",self.LabelRole: b'label',self.LogoRole: b'logo'}
        model.setItemRoleNames(roles)
        for name in files.list(dir_path):
            hidden = control.read_record('hidden',f'{dir_path}/{name}')
            if not hidden=='Yes':
                it = QtGui.QStandardItem(name)
                it.setData(name, self.NameRole)
                namex = control.read_record(f'name[{getdata("locale")}]',f'{dir_path}/{name}')
                if namex=='' or namex==None:
                    namex = control.read_record(f'name[en]', f'{dir_path}/{name}')
                it.setData(namex,self.LabelRole)
                it.setData('../../../'+res.get(control.read_record('logo',f'{dir_path}/{name}')),self.LogoRole)
                model.appendRow(it)
        return model

    def getdata (self,name):
        try:
            x = control.read_record(name,f'/etc/users/{self.username}')
            if x=='' or x==None:
                x = getdata(name)
        except:
            x = res.get('@string/guest')

        return x

    def getnamex (self,database):
        try:
            x = control.read_record(f'name[{self.getdata("locale")}]', database)
            if x=='' or x==None:
                x = control.read_record(f'name[en]', database)
        except:
            x = control.read_record(f'name[en]', database)
        return x

    def signal (self):
        if not files.isfile('/proc/info/sig'):
            files.create('/proc/info/sig')

        if files.readall('/proc/info/sig')=='sleep':
            files.create('/proc/info/sig')
            self.sleep_()

        elif files.readall('/proc/info/sig')=='shutdown':
            files.create('/proc/info/sig')
            self.shutdown_()

        elif files.readall('/proc/info/sig') == 'restart':
            files.create('/proc/info/sig')
            self.restart_()

        elif files.readall('/proc/info/sig')=='lock':
            files.create('/proc/info/sig')
            self.lock_()

        elif files.readall('/proc/info/sig')=='logout':
            files.create('/proc/info/sig')
            self.logout_()

        elif files.readall('/proc/info/sig')=='switchuser':
            files.create('/proc/info/sig')
            self.switchuser_()

    def loop (self):
        # Applications starts in background
        if not self._background_app.property('text')=='':
            self._menuApps.setProperty('visible', False)
            self.menuClicked = False
            app.switch('desktop')
            app.start(self._background_app.property('text').replace('.desk',''),'')
            app.switch('desktop')

        # Check signals #
        self.signal()

        self._background_app.setProperty('text','')
        QTimer.singleShot(1,self.loop)

    def startup (self):
        # Startup applications
        lists = control.read_list('/etc/suapp')
        for i in lists:
            app.start(i, '')

    def bashrc (self):
        if self.username=='guest':
            f = open('/root/.bashrc','w')
            f.write('''cd /stor
python3 vmabr.pyc user guest''')
            f.close()
        else:
            f = open('/root/.bashrc','w')
            f.write(f'''cd /stor
python3 vmabr.pyc user {self.username} {self.password}''')
            f.close()

    menuClicked = False

    def menuApps_(self):
        if self.menuClicked:
            self._menuApps.setProperty('visible',False)
            self.menuClicked = False
        else:
            self._menuApps.setProperty('visible', True)
            self.menuClicked = True

    def __init__(self,ports):
        super(Desktop, self).__init__()
        app.switch('desktop')
        self.Backend = ports[0]
        self.username = ports[1]
        self.password = ports[2]
        self.modelDevelop = self.create_model('/usr/share/applications','develop')
        self.rootContext().setContextProperty("EntryDevelop", self.modelDevelop)
        self.modelGames = self.create_model('/usr/share/applications', 'games')
        self.rootContext().setContextProperty("EntryGames", self.modelGames)
        self.modelInternet = self.create_model('/usr/share/applications', 'internet')
        self.rootContext().setContextProperty("EntryInternet", self.modelInternet)
        self.modelMultimedia = self.create_model('/usr/share/applications', 'multimedia')
        self.rootContext().setContextProperty("EntryMultimedia", self.modelMultimedia)
        self.modelOthers = self.create_model('/usr/share/applications', 'others')
        self.rootContext().setContextProperty("EntryOthers", self.modelOthers)
        self.modelSystem = self.create_model('/usr/share/applications', 'system')
        self.rootContext().setContextProperty("EntrySystem", self.modelSystem)
        self.modelTools = self.create_model('/usr/share/applications', 'tools')
        self.rootContext().setContextProperty("EntryTools", self.modelTools)
        self.modelDockApplications = self.create_model3()
        self.rootContext().setContextProperty('EntryDockApplications',self.modelDockApplications)
        self.modelLang = self.create_model2()
        self.rootContext().setContextProperty("Lang", self.modelLang)

        self.modelAllApplications = self.create_model4('/usr/share/applications')
        self.rootContext().setContextProperty('EntryAppApplications', self.modelAllApplications)

        self.load(res.get('@layout/desktop'))
        if not self.rootObjects():
            sys.exit(-1)
        self.setProperty('height',int(getdata("height")))
        self.setProperty('width', int(getdata("width")))
        self.setProperty('visibility', getdata("visibility"))
        self.setProperty('font', QFont(getdata('font'), int(getdata('fontsize'))))
        self.setProperty('title','Pyabr OS')
        self._submenu = self.findChild('submenu')
        self._submenu.setProperty('title',res.get('@string/etcmenu'))
        self._shutdown = self.findChild( 'shutdown')
        self._shutdown.triggered.connect(self.shutdown_)
        self._shutdown.setProperty('text',res.get('@string/escape'))
        self._restart = self.findChild( 'restart')
        self._restart.triggered.connect(self.restart_)
        self._restart.setProperty('text', res.get('@string/restart'))
        self._sleep = self.findChild( 'sleep')
        self._sleep.setProperty('text', res.get('@string/sleep'))
        self._sleep.triggered.connect(self.sleep_)
        self._logout = self.findChild( 'logout')
        self._logout.triggered.connect(self.logout_)
        self._logout.setProperty('text',res.get('@string/signout'))
        self._switchuser = self.findChild( 'switchuser')
        self._switchuser.triggered.connect(self.switchuser_)
        self._switchuser.setProperty('text',res.get('@string/switchuser'))
        self._applications = self.findChild( 'applications')
        self._applications.setProperty('title',res.get('@string/apps'))
        self._lock = self.findChild('lock')
        self._lock.triggered.connect (self.lock_)
        self._lock.setProperty('text',res.get('@string/lock'))
        self._developcat = self.findChild('developcat')
        self._developcat.setProperty('title',self.getnamex("/usr/share/categories/develop.cat"))
        self._gamescat = self.findChild( 'gamescat')
        self._gamescat.setProperty('title',self.getnamex('/usr/share/categories/games.cat'))
        self._internetcat = self.findChild( 'internetcat')
        self._internetcat.setProperty('title', self.getnamex('/usr/share/categories/internet.cat'))
        self._multimediacat = self.findChild( 'multimediacat')
        self._multimediacat.setProperty('title', self.getnamex('/usr/share/categories/multimedia.cat'))
        self._otherscat = self.findChild( 'otherscat')
        self._otherscat.setProperty('title', self.getnamex('/usr/share/categories/others.cat'))
        self._systemcat = self.findChild( 'systemcat')
        self._virtualkeyboard = self.findChild('virtualkeyboard')
        self._virtualkeyboard.setProperty('text',res.get('@string/vkey'))
        self._systemcat.setProperty('title', self.getnamex('/usr/share/categories/system.cat'))
        self._toolscat = self.findChild( 'toolscat')
        self._toolscat.setProperty('title', self.getnamex('/usr/share/categories/tools.cat'))
        self._background = self.findChild( 'background')
        self._background.setProperty('source', res.qmlget(self.getdata("desktop.background")))
        self._exit = self.findChild('exit')
        self._exit.setProperty('title', res.get('@string/powermenu'))
        self._lang = self.findChild('lang')
        self._lang.setProperty('title', res.get('@string/keyless'))
        self._account = self.findChild('account')
        self._account.setProperty('title',self.getdata("fullname"))
        self._account_setting = self.findChild('account_setting')
        self._account_setting.setProperty('text',res.get('@string/accountsettings'))
        self._background_app = self.findChild('background_app')
        self._toolbar = self.findChild('toolbar')
        self.toolbar_height = self._toolbar.property('height')
        self._toolbar.setProperty('width',self.pins*self.toolbar_height)
        self._btnMenu = self.findChild ('btnMenu')
        self._btnMenu.clicked.connect (self.menuApps_)
        self._menuApps = self.findChild ('menuApps')

        # Start up applications
        self.startup()
        # Main Loop
        self.loop()

class Application:
    def __init__(self, ports):
        super(Application, self).__init__()

        app.switch('desktop')

desktop = Backend()
sys.exit(application.exec())