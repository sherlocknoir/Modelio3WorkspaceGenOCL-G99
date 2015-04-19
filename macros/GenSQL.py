"""
CREATE TABLE Persons
(
PersonID int,
LastName varchar(255),
FirstName varchar(255),
Address varchar(255),
City varchar(255)
); 
=========================================================
                       GenSQL.py
 Generate a XML specification from a UML package
=========================================================

FILL THIS SECTION AS SHOWN BELOW AND LINES STARTING WITH ###
@author Heda WANG <heda.wang@ujf-grenoble.fr>
@author Jennifer FRY <jennifer.fry@ujf-grenoble.fr>
@group  G250

Current state of the generator
----------------------------------
The prupose of this generator is to create xml that can be then used in another 
script that can write the data to a specified database type like Mysql, mongo, google spreadsheet..
Explain which UML constructs are supported, which ones are not.
What is good in your generator?
	-xml generation
	-class to table generation
    -attributes to coloumns generation
	-enumeration type generation
	
What are the current limitations?
    -association generation
    -association class generation
    -composition generation
    -operation generation
    -cardinality generation (could be better)
	-invariants
	-aggregation generation
	-attributes @derived comments
	-the order of the roles in the associations

Current state of the tests
--------------------------
FILL THIS SECTION 
Explain how did you test this generator.
 - Tested by generating the xml from library uml model to see how close it matches original xlm file.

Which test are working? 
Library xml test case
Xml Tests:
	classes to tables
	Attribues Simple to columns

Which are not?

    Associations Class
    Attribues cardinality
    Attribues Enumeration
    operations
    Inheritence Single
    Inheritence multiples
    Associations Simple
    Associations composi
	Attribues Visibility
	Associations Unspecified
	Associations Ordered
	Associations aggregation
	Associations Qualified
	Associations Nary
	Notes
	Invarients
Observations
------------
Additional observations could go there
The code could be better structured.
"""
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#from ElementTree_pretty import prettify

def umlClass2XmlTable(umlclass):
    ""
    tbname = umlclass.name
    tbtype = "TABLE"
    
    if isAssociationClass(umlclass):
    	print "associationClass "+ umlclass.name + " between"
    	for a in umlclass.linkToAssociation.associationPart.end:
    		umlRoles2OCL(a)
    elif umlclass.isAbstract:
    	print "Abstract Class "+ umlclass.name + umlHeritage2OCL(umlclass)
    else:
    	classTable = ET.SubElement(tables, "table", name=tbname,type=tbtype)

    
    if len(umlclass.ownedAttribute)>0:
        umlAttributes2OXmlColumn(umlclass.ownedAttribute,classTable)
  
    if len(umlclass.ownedOperation)>0:
        umlMethod2OCL(umlclass.ownedOperation)
    print "end"
    print '\n'

def umlHeritage2OCL(umlclass):
	x=[]

	for p in umlclass.parent:
		x.append(p.superType.name)
	if len(x)>0:	
		return " < "+ ", ".join(x)
	else:
		return ""

def umlMethod2OCL(operations):
    ""
    print "operations"

    for o in operations:
    	print indent(4) + o.name +\
        	"("+umlParams2OCL(o)+")"+ umlReturnVal2OCL(o)+" = expression"

def umlParams2OCL(operation):
	x=[]
	for o in operation.IO:
		x.append(o.name +" : "+ umlBasicType2OCL(o.type))
	return ", ".join(x)	
	

#needs to works for sets
def umlReturnVal2OCL(operation):
	if operation.return:
		if operation.return.multiplicityMax == "*":
			return " : set("+ umlBasicType2OCL(operation.return.type)+")"
		return " : "+ umlBasicType2OCL(operation.return.type)
	else:
		return ""

def umlAttributes2OXmlColumn(attributes, classTable):
    print "attributes"
    for a in attributes:
        ET.SubElement(classTable, "column", name=a.name,type=umlBasicType2OCL(a.type))
        if(a.isStereotyped("LocalModule", "PK")):
            umlPKStereoType2OXmlColumn(a.name,classTable)

def umlPKStereoType2OXmlColumn(name, classTable):
    ET.SubElement(classTable, "primaryKey", column=name)
        
    
def umlAssocation2OCL(association):
	kind ="association "
	for assokind in association.end:
		if (assokind.aggregation.name == "KindIsComposition"):
			kind = "composition "
		
	print kind+ association.name +" between"
	for a in association.end:
		umlRoles2OCL(a)

	print "end"
	print '\n'


def umlRoles2OCL(role):
	card = ""
	if (role.multiplicityMax == role.multiplicityMin or
		role.multiplicityMax == "*"):
		card = card+ "["+ role.multiplicityMax +"]"
	else:
		 card = card +  "["+ role.multiplicityMin + ".."+role.multiplicityMax +"]"
	if role.target is not None:
		print indent(4)+role.target.name+card+ " role "+role.name
#---------------------------------------------------------
#   Helpers on the source metamodel (UML metamodel)
#---------------------------------------------------------
# The functions below can be seen as extensions of the
# modelio metamodel. They define useful elements that 
# are missing in the current metamodel but that allow to
# explorer the UML metamodel with ease.
# These functions are independent from the particular 
# problem at hand and could be reused in other 
# transformations taken UML models as input.
#---------------------------------------------------------

# example
def isAssociationClass(element):
    """ 
    Return True if and only if the element is an association 
    that have an associated class, or if this is a class that
    has a associated association. (see the Modelio metamodel
    for details)
    """
    if isinstance(element,Class):
        return element.getLinkToAssociation()!=None
    return False


def associationsInPackage(package):
    """
    Return the list of all associations that start or
    arrive to a class which is recursively contained in
    a package.
    """
    for element in package.ownedElement:
    	if isinstance(element, Package):
    		associationsInPackage(element)
    	elif isinstance(element, Class):
    		for assoc in element.ownedEnd:
    			if assoc.association is not None:
    				if assoc.association.linkToClass==None:
    				#print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
    					assocList.append(assoc.association)
    	
    

def umlEnumeration2OCL(enumeration):
    """
    Generate USE OCL code for the enumeration
    """
    l = []
    for e in enumeration.value:
    	l.append(e.name)
    
    print "enum "+enumeration.name+"{"
    print indent(2)+(", \n"+indent(2)).join(l)
    print  "}"
    print '\n'

def umlBasicType2OCL(basicType):
    """
    Generate USE OCL basic type. Note that
    type conversions are required.
    """
    if basicType.name == "string":
    	return "String"
    elif basicType.name == "integer":
    	return "Integer"
    elif basicType.name == "boolean":
    	return "Boolean"
    elif basicType.name == "float":
    	return "Real"
    else:
    	return basicType.name
    	 
def umlTypeCard2OCL(attributes):
	if (attributes.multiplicityMax != "1" or attributes.multiplicityMin !="1"):
		return "["+ attributes.multiplicityMin + ".."+attributes.multiplicityMax +"]"
	else:
		return ""   


def package2OCL(package):
    """
    
    """
    associationsInPackage(package)
    for element in package.ownedElement:
    	if isinstance(element, Package):
    		package2OCL(element)

    	elif isinstance(element, Class):
    		classesList.append(element)
    	elif isinstance(element,Enumeration):
    		enumList.append(element)
    	else:
    		myhash["allclasses"].append(element)
    		





# This is a function with two parameters, one is optional
def indent(nb, character=' '):
    return character*nb
  

#==========================Begin===================================
dbname = "library2"
dbtype = "MySql "
filename = dbname+'.xml'
root = ET.Element("database", name=dbname, type=dbtype)
tables = ET.SubElement(root, "tables")


if len(selectedElements)==0:   
    # indentation is important since they are no { }
    print indent(4)+"Ah no, sorry. You have no selected package."
else:
    #print 'they are {nb} elements'.format(nb=len(selectedElements)) 
    #print selectedElements
   
    classesList = [] 
    assocList = []
    enumList = []  # this is a list
   
    myhash= {}
    
    
    for element in selectedElements:
        if isinstance(element, Package):
        	print "Model "+element.name
        	print '\n' 
        	package2OCL(element)
    
    if len(enumList)>0:
    	#print "enum list======"
    	#print enumList
    	for e in enumList:
    		umlEnumeration2OCL(e)
    if len(classesList) >0:
    	#print "class list======="
    	#print classesList
        for c in classesList:
        	umlClass2XmlTable(c)
    if len(assocList) >0:
    	#print "assoc list ======="
    	#print assocList
    	assocList= list(set(assocList))
    	#print assocList
    	for allasoc in assocList:
    		umlAssocation2OCL(allasoc)
tree = ET.ElementTree(root)
tree.write(filename)
    