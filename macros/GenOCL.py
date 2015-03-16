"""
=========================================================
                       GenOCL.py
 Generate a USE OCL specification from a UML package
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
	-package generation
	-class generation
	-enumeration generation
	-association generation
	-association class generation
	-composition generation
	-operation generation
	-cardinality generation (could be better)
What are the current limitations?
	-invariants
	-aggregation generation
	-attributes @derived comments
	-the order of the roles in the associations

Current state of the tests
--------------------------
FILL THIS SECTION 
Explain how did you test this generator.
 - Tested by generating the ocl for Cyber Residence and running the tests UMLtest

Which test are working? 
Cyber Residence test case
Uml Tests:
	classes
	Attribues Simple
	Attribues cardinality
	Attribues Enumeration
	operations
	Inheritence Single
	Inheritence multiples
	Associations Simple
	Associations composite
	Associations Class

Which are not?
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

def umlClass2OCL(umlclass):
    ""
    # The next statement run over multiples lines but \ are not necessary
    # because they are some ( ) [ ] { } or something that make obvious where it stop
    
    #doesnt work for class
    if isAssociationClass(umlclass):
    	print "associationClass "+ umlclass.name + " between"
    	for a in umlclass.linkToAssociation.associationPart.end:
    		umlRoles2OCL(a)
    elif umlclass.isAbstract:
    	print "Abstract Class "+ umlclass.name + umlHeritage2OCL(umlclass)
    else:
    	print "Class "+ umlclass.name + umlHeritage2OCL(umlclass)
    
    if len(umlclass.ownedAttribute)>0:
        umlAttributes2OCL(umlclass.ownedAttribute)
  
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

def umlAttributes2OCL(attributes):
    print "attributes"
    for a in attributes:
        print indent(4) + a.name + " : " + umlBasicType2OCL(a.type)+umlTypeCard2OCL(a)
    
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

    
 
#---------------------------------------------------------
#   Application dependent helpers on the source metamodel
#---------------------------------------------------------
# The functions below are defined on the UML metamodel
# but they are defined in the context of the transformation
# from UML Class diagramm to USE OCL. There are not
# intended to be reusable. 
#--------------------------------------------------------- 

# example
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
    	
    

    
#---------------------------------------------------------
#   Helpers for the target representation (text)
#---------------------------------------------------------
# The functions below aims to simplify the production of
# textual languages. They are independent from the 
# problem at hand and could be reused in other 
# transformation generating text as output.
#---------------------------------------------------------


# for instance a function to indent a multi line string if
# needed, or to wrap long lines after 80 characters, etc.

#---------------------------------------------------------
#           Transformation functions: UML2OCL
#---------------------------------------------------------
# The functions below transform each element of the
# UML metamodel into relevant elements in the OCL language.
# This is the core of the transformation. These functions
# are based on the helpers defined before. They can use
# print statement to produce the output sequentially.
# Another alternative is to produce the output in a
# string and output the result at the end.
#---------------------------------------------------------



# examples

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
    Generate a complete OCL specification for a given package.
    The inner package structure is ignored. That is, all
    elements useful for USE OCL (enumerations, classes, 
    associationClasses, associations and invariants) are looked
    recursively in the given package and output in the OCL
    specification. The possibly nested package structure that
    might exist is not reflected in the USE OCL specification
    as USE is not supporting the concept of package.
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
    		




#---------------------------------------------------------
#           User interface for the Transformation 
#---------------------------------------------------------
# The code below makes the link between the parameter(s)
# provided by the user or the environment and the 
# transformation functions above.
# It also produces the end result of the transformation.
# For instance the output can be written in a file or
# printed on the console.
#---------------------------------------------------------

# (1) computation of the 'package' parameter
# (2) call of package2OCL(package)
# (3) do something with the result


# This is a function with two parameters, one is optional
def indent(nb, character=' '):
    return character*nb
  
def plural(nb, word, plural=None):
    """ 
    This is the documentation of the function.
    This function returns a string that indicates how many
    'items' there are, 'nb' being the number of 'items'
    and 'word' the type of items. If they are more than
    two objects a 's' is added to the word unless the
    plural parameter is provided. In this case, the plural
    form is returned.
    """
    if nb == 0:
        return 'no '+word
    elif nb == 1:
        return 'one '+word
    else:
        if plural is None:
            return str(nb)+' '+word+'s'
        else:
            return str(nb)+' '+plural
#==========================Begin===================================
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
        	umlClass2OCL(c)
    if len(assocList) >0:
    	#print "assoc list ======="
    	#print assocList
    	assocList= list(set(assocList))
    	#print assocList
    	for allasoc in assocList:
    		umlAssocation2OCL(allasoc)
    