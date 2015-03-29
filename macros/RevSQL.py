"""
=========================================================
                       RevSQL.py
 Generate a UML specification from a XML of SQL package
=========================================================

FILL THIS SECTION AS SHOWN BELOW AND LINES STARTING WITH ###
@author Heda WANG <heda.wang@ujf-grenoble.fr>
@author Jennifer FRY <jennifer.fry@ujf-grenoble.fr>
@group  G250

Current state of the generator
----------------------------------
FILL THIS SECTION 
Explain which UML constructs are supported, which ones are not.
What is good in your generator?
    
What are the current limitations?
   

Current state of the tests
--------------------------
FILL THIS SECTION 
Explain how did you test this generator.
 - Tested by generating the ocl for Cyber Residence and running the tests UMLtest

Which test are working? 


Which are not?
    
Observations
------------
Additional observations could go there
The code could be better structured.
"""

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def sQLTable2UMLClass(table):
    trans = theSession().createTransaction("Class creation")
    try:
        fact= theUMLFactory()
        myp = instanceNamed(Package,"MyPackage")
        c1 = fact.createClass()
        c1.setOwner(myp)
        c1.setName(table.get('name'))
        #c2 = fact.createClass("Class4",myp)
        trans.commit()
    except:
        trans.rollback()
        raise
    #here or in clomuns?    
    for column in table.findall('column'):
        sQLColumn2UMLAttribute(table,column)

def sQLColumn2UMLAttribute(table,column):
    print "attrb name is : "+column.get('name')
    print "and the type for this attr is: "+column.get('type')
    trans = theSession().createTransaction("Attribute creation")
    try:
        fact= theUMLFactory()
        myp = instanceNamed(Class,table.get('name'))
        c1 = fact.createAttribute()
        c1.setOwner(myp)
        c1.setName(column.get('name'))
        c1.setType(sQLType2UMLType(column.get('type')))
        #c2 = fact.createClass("Class4",myp)
        #
        trans.commit()
    except:
        trans.rollback()
        raise



def sQLType2UMLType(type_):
    print "type is: "+type_
    basicType = theSession().getModel().getUmlTypes()
    print type_
    if type_ == "VARCHAR":
        return basicType.getSTRING()
    if type_ == "TEXT":
        return basicType.getSTRING()
    elif type_ == "INT":
        return basicType.getINTEGER()
    elif type_ == "BIGINT":
        return basicType.getLONG()
    elif type_ == "BOOL":
        return basicType.getBOOLEAN()
    elif type_ == "REAL":
        return basicType.getFLOAT()
    elif type_ == "DATE":
        return basicType.getDATE()
    else:
        return basicType.getUNDEFINED()
         
    

def sQLPrimaryKey2UML(pk):
    print pk

def sQLFK2UML(fk):
    print fk


tree = ET.parse('/home/jen/codeprojectsgit/dpmodels-m2sem2/Modelio3WorkspaceGenOCL-G99/library.xml')
root = tree.getroot()
print root
for children in root:
    for table in children.findall('table'):
        sQLTable2UMLClass(table)
        ttype = table.get('type')
        name = table.get('name')
        print(name, ttype)
print"++++++++++++++++++++"
#for elem in tree.iter():
 #   print elem.tag, elem.attrib
#print "================"
#for c_of_root in root:
#    for tables in c_of_root:
 #       print tables.tag, tables.attrib



trans = theSession().createTransaction("Class creation")
try:
    fact= theUMLFactory()
    myp = instanceNamed(Package,"MyPackage")
    c1 = fact.createClass()
    c1.setOwner(myp)
    c1.setName("Class3")
    c2 = fact.createClass("Class4",myp)
    trans.commit()
except:
    trans.rollback()
    raise
