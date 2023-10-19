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
    return newobj

def exQuery():
    sdb=SparxDb(conf['connstr'])
    stmt=sdb.select(Object).where(Object.Name=="Folder2")
    result=sdb.session.execute(stmt)
    folder=result.fetchone()[0]
    print(folder.Name)
    #print(folder.children)
    folder.Name="Folder3"
    sdb.commit()
    return folder

def exCreateDiagram():
    sdb=SparxDb(conf['connstr'])
    print(conf['connstr'])
    archioDiagram=Diagram(Name="My New Archi Diagram",Diagram_Type="Logical",StyleEx="MDGDgm=ArchiMate3::Application;",Package_ID=2)
    sdb.add(archioDiagram)
    return archioDiagram

def exCreatePackage():
    sdb=SparxDb(conf['connstr'])
    package=Package(Name="Folder3",Parent_ID=1,icon=4)
    sdb.add(package)
    sdb.commit()
    return package

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
    return folder
    

def exComplex():
    sdb=SparxDb(conf['connstr'])
    package=Package(Name="TestFolder",Parent_ID=1,icon=4)
    sdb.add(package)
    diagram1=Diagram(Name="Diagram1",Diagram_Type="Logical",StyleEx="MDGDgm=ArchiMate3::Application;",Package_ID=package.Package_ID)
    sdb.add(diagram1)
    diagram2=Diagram(Name="Diagram2",Diagram_Type="Logical",StyleEx="MDGDgm=ArchiMate3::Application;",Package_ID=package.Package_ID)
    sdb.add(diagram2)
    newobj=Object(Name="System1", Object_Type="Component", Package_ID=package.Package_ID)
    newobj.Stereotype="ArchiMate_ApplicationComponent"
    sdb.add(newobj)
    newobj.set_child_diagram(diagram2)
    diagramobject=DiagramObject(diagram=diagram1,object=newobj)
    sdb.add(diagramobject)
    diagramobject.setColor(r=200,g=100,b=50)
    sdb.commit()

def exGetConnectors():
    sdb=SparxDb(conf['connstr'])
    connectors=sdb.getConnectors(type="Association")
    for connector in connectors:
        print(f"{connector.Name} ")
    return connectors

def exSetConnectorTag():
    sdb=SparxDb(conf['connstr'])
    connectors=sdb.getConnectors(type="Association")
    for connector in connectors:
        connector.tag_update(tagname="MyTag",value="MyValue")
    sdb.commit()
    return connectors

def exGetChildren():
    sdb=SparxDb(conf['connstr'])
    object=sdb.getObject(name="KompA") 
    children=object.getChildren()
    for child in children:
        print(child.Name)

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
    #exComplex()
    #exGetConnectors()
    #exSetConnectorTag()
    exGetChildren()
