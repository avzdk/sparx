from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, create_engine, select, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

class SparxDb:
    #sdb=SparxDb("mysql+pymysql://user:password@sparxdb.server.com/database?charset=utf8mb4")

    def __init__(self,connectionstr=""):
        self.engine = create_engine(connectionstr)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        self.session = self.session()       

    def select(self,obj):
        return select(obj)  
    
    def getObjects(self,type=None):
         if type==None : 
             result=self.session.query(Object).all()   
         else:
            result=self.session.query(Object).filter(Object.Object_Type==type).all()   
         return result
    
    def commit(self):
        return self.session.commit()
    
    def _createStdXref(self,element):
        if element.Stereotype=="ArchiMate_ApplicationComponent":
            newxref1=Xref()
            newxref1.Name="CustomProperties"
            newxref1.Type="element property"
            newxref1.Description="@PROP=@NAME=_HideUmlLinks@ENDNAME;@TYPE=string@ENDTYPE;@VALU=True@ENDVALU;@PRMT=@ENDPRMT;@ENDPROP;@PROP=@NAME=_defaultDiagramType@ENDNAME;@TYPE=string@ENDTYPE;@VALU=ArchiMate3::Application@ENDVALU;@PRMT=@ENDPRMT;@ENDPROP;"
            newxref1.Client=element.ea_guid
            newxref1.Supplier="<none>"
            self.session.add(newxref1)
            newxref2=Xref()
            newxref2.Name="Stereotypes"
            newxref2.Type="element property"
            newxref2.Description="@STEREO;Name=ArchiMate_ApplicationComponent;FQName=ArchiMate3::ArchiMate_ApplicationComponent;@ENDSTEREO;"
            newxref2.Client=element.ea_guid
            newxref2.Supplier="<none>"
            self.session.add(newxref2)
            print(newxref1)
            print(newxref2)

    def add(self,element):
        
        self.session.add(element)
        self._createStdXref(element)
        return self.session.commit()


class Object(Base):
    # Object(Name="Igen ny", Object_Type="Class", Package_ID=2)
    __tablename__ = "t_object"
    Object_ID = Column(Integer,primary_key=True)
    Object_Type = Column(String)
    Diagram_ID = Column(Integer,default=0)
    Name = Column(String)       
    Alias = Column(String)      
    Author = Column(String,default='python')     
    Version = Column(String,default='1.0')    
    Note = Column(String)       
    Package_ID = Column(Integer)
    Stereotype = Column(String) 
    NType = Column(Integer,default=0)     
    Complexity = Column(String,default=1) 
    Effort = Column(Integer,default=0)    
    Style = Column(String)
    Backcolor = Column(Integer,default=-1)
    BorderStyle = Column(Integer,default=0)
    BorderWidth = Column(Integer,default=-1)
    Fontcolor = Column(Integer,default=-1)
    Bordercolor = Column(Integer,default=-1)
    CreatedDate = Column(DateTime)
    ModifiedDate = Column(DateTime)
    Status = Column(String,default="Proposed")
    Abstract = Column(String,default=0)
    Tagged = Column(Integer,default=0)
    PDATA1 = Column(String)
    PDATA2 = Column(String)
    PDATA3 = Column(String)
    PDATA4 = Column(String)
    PDATA5 = Column(String) # Keywords
    Concurrency = Column(String)
    Visibility = Column(String)
    Persistence = Column(String)
    Cardinality = Column(String)
    GenType = Column(String,default="Java")
    GenFile = Column(String)
    Header1 = Column(String)
    Header2 = Column(String)
    Phase = Column(String)
    Scope = Column(String,default='Public')
    GenOption = Column(String)
    GenLinks = Column(String)
    Classifier = Column(Integer,default=0)
    ea_guid = Column(String)
    ParentID = Column(Integer,default=0)
    RunState = Column(String)
    Classifier_guid = Column(String)
    TPos = Column(Integer)
    IsRoot = Column(Integer,default=0)
    IsLeaf = Column(Integer,default=0)
    IsSpec = Column(Integer,default=0)
    IsActive = Column(Integer,default=0)
    StateFlags = Column(String)
    PackageFlags = Column(String)
    Multiplicity = Column(String)
    StyleEx = Column(String)
    ActionFlags = Column(String)
    EventFlags = Column(String)

    attributes = relationship("Attribute", cascade="all, delete")
    tags = relationship("ObjectTag",cascade="all, delete")
    xrefs = relationship("Xref",cascade="all, delete")

    def get_tag(self,tagname):
        #returns ObejctTag by name lookup
        for tag in self.tags:
            if tag.Property == tagname:
                return tag
                

    def tag_update(self,tagname,value):
        # Updates tag or add a new
        # Updates only first found
        tag=self.get_tag(tagname)
        if tag == None:
            tag=ObjectTag(tag=tagname,value=value)
            self.tags.append(tag)
        else:
            tag.Value=value
        return tag


    def __init__(self,Name,Object_Type,Package_ID):
        if Name is None or Object_Type is None or Package_ID is None :
            print("Mangler en parameter")
        self.Name =Name
        self.Object_Type = Object_Type
        self.Package_ID = Package_ID
        self.CreatedDate = datetime.now()
        self.ea_guid = '{'+str(uuid4())+'}'

    def __repr__(self):
        return f"{self.__tablename__} {self.Object_ID}:\t{self.Object_Type}: {self.Name}"
    
    


class Attribute(Base):
    __tablename__ = "t_attribute"
    ID = Column(Integer,primary_key=True)  
    Object_ID = Column(Integer,ForeignKey(Object.Object_ID))
    Name = Column(String)
    Scope = Column(String)
    Stereotype = Column(String)
    Containment = Column(String)
    IsStatic = Column(Integer)
    IsCollection = Column(Integer)
    IsOrdered = Column(Integer)
    AllowDuplicates = Column(Integer)
    LowerBound = Column(String)
    UpperBound = Column(String)
    Container = Column(String,default='Not Specified')
    Notes = Column(String)
    Derived = Column(String) # None,'0','1'
    Pos = Column(Integer)
    GenOption = Column(String)
    Length = Column(Integer)
    Precision = Column(Integer)
    Scale = Column(Integer)
    Const = Column(Integer)
    Style = Column(String)
    Classifier = Column(String,default=0)
    Default = Column(String)
    Type = Column(String)
    ea_guid = Column(String)
    StyleEx = Column(String,default='volatile=0')

    tags = relationship("AttributeTag", cascade="all, delete")

    def __init__(self):
        self.ea_guid='{'+str(uuid4())+'}'

    def __repr__(self):
        return f"{self.__tablename__} O:{self.Object_ID} {self.ID} : {self.Name}"

class ObjectTag(Base):
    __tablename__ = "t_objectproperties"
    PropertyID = Column(Integer,primary_key=True)  
    Object_ID = Column(Integer,ForeignKey(Object.Object_ID))
    ea_guid = Column(String)
    Property = Column(String)
    Value = Column(String)
    Notes = Column(String)

    def __init__(self,tag,value):
        self.Property=tag
        self.Value=value
        self.ea_guid='{'+str(uuid4())+'}'


    def __repr__(self):
        return f"{self.__tablename__} O:{self.Object_ID} {self.Property} : {self.Value}"

class AttributeTag(Base):
    __tablename__ = "t_attributetag"
    PropertyID = Column(Integer,primary_key=True)  
    ElementID = Column(Integer,ForeignKey(Attribute.ID))
    ea_guid = Column(String)
    Property = Column(String)
    Value = Column(String)
    Notes = Column(String)
    
    def __init__(self):
        self.ea_guid='{'+str(uuid4())+'}'

    def __repr__(self):
        return f"{self.__tablename__} A:{self.ElementID} {self.Property} : {self.Value}"

class Xref(Base):
    __tablename__ = "t_xref"
    XrefID = Column(String,primary_key=True)
    Name = Column(String)
    Type = Column(String)
    Visibility = Column(String,default='Public')
    Namespace = Column(String)
    Requirement = Column(String)
    Constraint = Column(String)
    Behavior = Column(String)
    Partition = Column(String,default='0')
    Description = Column(String)
    Client = Column(String,ForeignKey(Object.ea_guid))
    Supplier = Column(String)
    Link = Column(String)

    def __init__(self):
        self.XrefID='{'+str(uuid4())+'}'

    def __repr__(self):
        return f"{self.__tablename__} C:{self.Client} Id:{self.XrefID}  "

if __name__ == '__main__':
    pass