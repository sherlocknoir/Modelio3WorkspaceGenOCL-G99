print "Hello Heda!"

# This is a comment
print '\n'*3
print '-'*80  # isn't that nice?
print "I'm a macro. I'm in the file sandbox.py located in the directory"
print '"macros" of the current workspace. You can edit me with a'
print "regular text editor (e.g. Notepad++ on windows)."
print "I will be happy if you change me and execute me again (and again...)."
print
print "By the way you have selected the following elements in modelio:"

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

if len(selectedElements)==0:   
    # indentation is important since they are no { }
    print indent(4)+"Ah no, sorry. You have no selected elements."
    print indent(8,'*')+'Play again.'
    print indent(8,character='')+'Please!'
    
else:
    print 'they are {nb} elements'.format(nb=len(selectedElements)) 
    print selectedElements
    print
    print "Look, I'm smart: I can count the selected classes:"
    classes = []   # this is a list
    for element in selectedElements:
        if isinstance(element, Class):
            classes.append(element)
    # Statements can run over multiple lines if a \ is put at the end of a lines
    # like in the next line. 
    print 'I figured out that  you have selected ' \
            + plural(len(classes),'class','classes')
    
    if len(classes) >=0:
        class_pattern = \
          'class {className} has {attributes} and {operations}' 
        for c in classes:
            # The next statement run over multiples lines but \ are not necessary
            # because they are some ( ) [ ] { } or something that make obvious where it stop
            print indent(5)+class_pattern.format(
                    className = c.name,
                    attributes = plural(len(c.ownedAttribute),'attribute'),
                    operations = plural(len(c.ownedOperation),'operation') )
    else:
        print 'Well, select some classes if you want to see what happen...'
    