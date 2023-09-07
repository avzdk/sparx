from sparxdb import SparxDb, Object, Attribute, Diagram, Package, DiagramObject
import tomllib


def exRead():
    sdb=SparxDb(conf['connstr'])
    classes=sdb.getObjects(type="Class")
    myclass=classes[1]
    myattribute=myclass.attributes[0]
    print(myclass)
    print(myattribute)
    print(myattribute.tags[0])

def exAddNew():
    sdb=SparxDb(conf['connstr'])
    newobj=Object(Name="My New Class", Object_Type="Class", Package_ID=2)
    sdb.add(newobj)

def exQuery():
    sdb=SparxDb(conf['connstr'])
    stmt=sdb.select(Object).where(Object.Name=="Folder2")
    result=sdb.session.execute(stmt)
    folder=result.fetchone()[0]
    print(folder.Name)
    #print(folder.children)
    folder.Name="Folder3"
    sdb.commit()

def exCreateDiagram():
    sdb=SparxDb(conf['connstr'])
    print(conf['connstr'])
    archioDiagram=Diagram(Name="My New Archi Diagram",Diagram_Type="Logical",StyleEx="MDGDgm=ArchiMate3::Application;",Package_ID=2)
    classDiagram=Diagram(Name="My New Classe Diagram",Diagram_Type="Logical",Package_ID=2)
    sdb.add(archioDiagram)
    diagramobjekt=DiagramObject()
    #sdb.add(classDiagram)

def exCreatePackage():
    sdb=SparxDb(conf['connstr'])
    package=Package(Name="Folder3",Parent_ID=1,icon=4)
    sdb.add(package)

def exGetPackage():
    sdb=SparxDb(conf['connstr'])
    stmt=sdb.select(Package).where(Package.Name=="Folder2")
    result=sdb.session.execute(stmt)
    folder=result.fetchone()[0]
    print(folder.Name)
    folder.Name="Folder2"
    sdb.commit()
    for object in folder.objects:
        print(object)
    


if __name__ == '__main__':
    try:
        with open("conf_dev.toml", "rb") as f: conf = tomllib.load(f)
    except FileNotFoundError:
        with open("conf.toml", "rb") as f: conf = tomllib.load(f)

    #exRead()
    #exAddNew()
    #exQuery()
    #exCreateDiagram()
    exCreatePackage()
    #exGetPackage()