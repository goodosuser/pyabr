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

import sys, subprocess

from pyabr.core import *

modules = Modules()
files = Files()
control = Control()
colors = Colors()
process = Process()
permissions = Permissions()
pack = Package()
cmd = Commands()
res = Res()

## Check root ##
if not permissions.check_root (files.readall("/proc/info/su")):
    colors.show ("paye","perm","")
    sys.exit(0)

## Check inputs ##
if sys.argv[1:]==[]:
    colors.show ("paye","fail","no inputs.")
    sys.exit(0)

if sys.argv[1]=="cl":
    pack.clean()

elif sys.argv[1]=="pak":
    if files.isfile ("/app/cache/lock"):
        colors.show ("paye","fail","cache has already locked.")
        sys.exit(0)
    else:
        files.create ("/app/cache/lock")

    if sys.argv[2:]==[]:
        colors.show("paye", "fail", "no inputs.")
        sys.exit(0)

    dir = sys.argv[2:]

    for i in dir:
        pack.build(i)

    pack.clean()


elif sys.argv[1]=="upak":
    if files.isfile ("/app/cache/lock"):
        colors.show ("paye","fail","cache has already locked.")
        sys.exit(0)
    else:
        files.create ("/app/cache/lock")

    if sys.argv[1:]==[]:
        colors.show("paye", "fail", "no inputs.")
        sys.exit(0)

    archive = sys.argv[2:]

    if not archive[1:]==[]:
        strv = ''
        for i in archive:
            strv+=f',{i}'

    for i in archive:
        if files.isfile(i):
            pack.unpack(i)
        else:
            colors.show("paye", "fail",  f"{i}: archive not found.")

    pack.clean()

elif sys.argv[1]=="rm":
    if files.isfile ("/app/cache/lock"):
        colors.show ("paye","fail","cache has already locked.")
        sys.exit(0)
    else:
        files.create ("/app/cache/lock")

    if sys.argv[2]==[]:
        colors.show("paye", "fail", "no inputs.")
        sys.exit(0)

    list = control.read_list('/etc/paye/permanetly_applications')

    if not (sys.argv[2:])[1:] == []:
        strv = ''
        for i in (sys.argv[2:]):
            strv +=f',{i}'

    for i in (sys.argv[2:]):
        if not i in list:
            pack.uninstall(i.lower())
        else:
            colors.show ('paye','fail',f"{i}: is a permanetly application that cannot be removed.")

    pack.clean()

elif sys.argv[1]=="get":

    if sys.argv[2]==[]:
        colors.show("paye", "fail", "no inputs.")
        sys.exit(0)


    if not (sys.argv[2:])[1:] == []:
        strv = ''
        for i in sys.argv[2:]:
            strv += f',{i}'
    for i in sys.argv[2:]:
        pack.download (i.lower())

elif sys.argv[1]=="in":
    if files.isfile ("/app/cache/lock"):
        colors.show ("paye","fail","cache has already locked.")
        sys.exit(0)
    else:
        files.create ("/app/cache/lock")

    if sys.argv[2]==[]:
        colors.show("paye", "fail", "no inputs.")
        sys.exit(0)


    if not (sys.argv[2:])[1:]==[]:
        strv = ''
        for i in sys.argv[2:]:
            strv+=f',{i}'

    for i in sys.argv[2:]:
        if files.isfile(f'/app/packages/{i.lower()}.manifest'):
            old = control.read_record('version', f'/app/packages/{i}.manifest')
            new = control.read_record('version', f'/app/mirrors/{i}.manifest')
            if not i=='latest' and old == new:
                colors.show('paye','warning',f'{i}: package is up to date.')
            else:
                pack.download(i.lower())
        else:
            pack.download(i.lower())

    for j in sys.argv[2:]:
        if files.isfile(f'/app/packages/{j.lower()}.manifest'):
            old = control.read_record('version', f'/app/packages/{j}.manifest')
            new = control.read_record('version', f'/app/mirrors/{j}.manifest')
            if not i=='latest' and old == new:
                pass
            else:
                pack.unpack(f"/app/cache/gets/{j.lower()}.pa")
        else:
            pack.unpack(f"/app/cache/gets/{j.lower()}.pa")

    pack.clean()

elif sys.argv[1]=="info":
    if sys.argv[2:]==[]:
        colors.show ('paye','fail','no inputs.')
        sys.exit(0)

    pack = f"/app/packages/{sys.argv[2]}.manifest"
    if files.isfile(pack):

        name = control.read_record ("name",pack)
        build = control.read_record("build", pack)
        version = control.read_record("version", pack)
        unpack = control.read_record("unpack", pack)
        description = control.read_record("description", pack)
        depends = control.read_record("depends", pack)
        license = control.read_record("license", pack)
        copyright = control.read_record("copyright", pack)

        if not (name == None or name == ""):  print(
            f"\t      Package name: {name}" )
        if not (version == None or version == ""):  print(
            f"\t   Package version: {version}" )
        if not (build == None or build == ""):  print(
            f"\t        Build date: {build}" )
        if not (copyright == None or copyright == ""):  print(
            f"\t         Copyright: {copyright}"   )
        if not (license == None or license == ""):  print(
            f"\t          Licensce: {license}"   )
        if not (description == None or description == ""):  print(
            f"\t       Description: {description}"   )
        if not (unpack == None or unpack == ""):  print(
            f"\t      Installed in: {unpack}"   )
    else:
        colors.show ("paye","fail",f"{sys.argv[2]}: package has not already installed.")

elif sys.argv[1]=="ls":
    list = files.list ("/app/packages")
    list.sort()
    for i in list:
        if i.endswith (".manifest"):
            name = control.read_record("name", f"/app/packages/{i}")
            build = control.read_record("build", f"/app/packages/{i}")
            version = control.read_record("version", f"/app/packages/{i}")
            print (f"{name}/{version}/{build}")
    print()

elif sys.argv[1]=='add':
    if sys.argv[2:]==[] or sys.argv[3:]==[]:
        colors.show ('paye','fail','no inputs.')
        sys.exit(0)

    pack.add (sys.argv[2],sys.argv[3])

elif sys.argv[1]=='del':
    if sys.argv[2:]==[]:
        colors.show ('paye','fail','no inputs.')
        sys.exit(0)

    pack.remove (sys.argv[2])

elif sys.argv[1]=='git':
    if sys.argv[2:]==[]:
        colors.show ('paye','fail','no inputs.')
        sys.exit(0)

    pack.gitinstall (sys.argv[2])

elif sys.argv[1]=='up':
    pack.upcloud ()

elif sys.argv[1]=='ir.pyabr.updates':
    pack.download('ir.pyabr.updates')
    pack.unpack('/app/cache/gets/ir.pyabr.updates.pa')

elif sys.argv[1]=='crt':
    if sys.argv[2:]==[]:
        colors.show ('paye','fail','no inputs.')
        sys.exit(0)

    crtype = sys.argv[2]

    if sys.argv[3:]==[]:
        crname = 'untitled'
    else:
        crname = sys.argv[3]

    try:
        if crtype == 'python-console':
            files.copydir(res.get('@temp/python-console'), crname)
        elif crtype == 'python-qt':
            files.copydir(res.get('@temp/python-qt'), crname)
        elif crtype == 'python-quick':
            files.copydir(res.get('@temp/python-console'), crname)
        else:
            files.copydir(res.get('@temp/python-console'), crtype)
    except:
        colors.show('paye','fail',f'cannot create project with {crname} name.')
else:
    colors.show ("paye","fail",f"{sys.argv[1]}: option not found.")