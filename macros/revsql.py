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
    print column.get('name')
    trans = theSession().createTransaction("Attribute creation")
    try:
        fact= theUMLFactory()
        myp = instanceNamed(Class,table.get('name'))
        c1 = fact.createAttribute()
        c1.setOwner(myp)
        c1.setName(column.get('name'))
        #c2 = fact.createClass("Class4",myp)
        #
        trans.commit()
    except:
        trans.rollback()
        raise



def sQLType2UMLType(type_):
    print type_

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
