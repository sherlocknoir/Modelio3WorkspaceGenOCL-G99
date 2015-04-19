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
This generator reads an xml file that represents a database schema, and translates it
into a modelio rational model.
Explain which UML constructs are supported, which ones are not.
What is good in your generator?
Tables are translated into classes.
Coloumns are translated into attributes.
Foreign keys are tranlsated into associations.
    
What are the current limitations?
Curently unable to add stereo types to associations, and attributes.
Currently only works for packages names mypackage.
Currently uses fixed path to read the xml file.
   

Current state of the tests
--------------------------
FILL THIS SECTION 
Explain how did you test this generator.
 - Tested by generating the rational model from library.xml example

Which test are working? 
Everything wrks with the exception of primary keys and foreignKeys.
    
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
    for parent in column.findall('parent'):
        print "fk for the col is: "+parent.get('foreignKey')
        addAssocToList(table,column, parent)
   
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

    print "i am here"


def sQLType2UMLType(type_):
    #add stereo type fk or pk
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

def addAssocToList(table,column,association):
     #add stero type fk to name
    print "association: source is: "+table.get('name')
    print "association cont: the dest is: "+ association.get('table')
    
    assocInfo = {
        "from":    table.get('name'),
        "to": association.get('table'),
        "name":  association.get('table')+'s',
    }
    listOfAssocs.append(assocInfo)
    return

def createUmlAssociation(source,dest,name):
    trans = theSession().createTransaction('Create association')
    try:
        fact= theUMLFactory()
        s = instanceNamed(Class,source)
        d = instanceNamed(Class, dest)
        asso = fact.createAssociation(s,d,dest)
        asso.addStereotype("LocalModule", "fk")
        trans.commit()
    except:
        trans.rollback()
        raise


def removeAll():
    transaction = theSession().createTransaction('Remove all')
    try:
        packageTarget = instanceNamed(Package, "MyPackage")
        elements = list(packageTarget.getOwnedElement())

        for element in elements:
            element.delete()
            
        transaction.commit()
    except:
        transaction.rollback()
        raise
   
tree = ET.parse('/home/jen/codeprojectsgit/dpmodels-m2sem2/Modelio3WorkspaceGenOCL-G99/library.xml')
root = tree.getroot()

listOfAssocs =[]
print root
cleanPackage()
for children in root:
    for table in children.findall('table'):
        sQLTable2UMLClass(table)
        ttype = table.get('type')
        name = table.get('name')
        print(name, ttype)
print"++++++++++++++++++++"
print (listOfAssocs)
for item in listOfAssocs:
    print item['from'], item['to'],item['name']
    source = item['from']
    dest = item['to']
    name = item['name']
    createUmlAssociation(source,dest,name)

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
