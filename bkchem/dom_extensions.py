#--------------------------------------------------------------------------
#     This file is part of BKChem - a chemical drawing program
#     Copyright (C) 2002-2009 Beda Kosata <beda@zirael.org>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file gpl.txt in the
#     main directory of the program

#--------------------------------------------------------------------------
#
#
#
#--------------------------------------------------------------------------

"""some extensions to DOM for more convenient work"""

from __future__ import absolute_import
import re
import xml.dom.minidom as dom
import operator
from six.moves import filter
from six.moves import map
from functools import reduce
#from __future__ import division


def safe_indent( element, level=0, step=2, dont_indent=("ftext","text")):
  """indents DOM tree. Does not add any extra whitespaces to text elements."""
  if not element.childNodes:
    pass
  elif reduce( operator.add, [isinstance( child, dom.Text) for child in element.childNodes], 0):
    pass
  elif element.nodeName in dont_indent:
    pass
  else:
    for child in element.childNodes[:]:
      element.insertBefore( element.ownerDocument.createTextNode("\n"+(level+step)*" "), child)
      safe_indent( child, level=level+step, step=step, dont_indent=dont_indent)
    element.appendChild(  element.ownerDocument.createTextNode("\n"+level*" "))


def elementUnder( parent, name, attributes=()):
  """creates element inside of parent and returns it,
  attributes are as sequence of (name,value) sequences"""
  if parent.DOCUMENT_NODE == parent.nodeType:
    a = parent.createElement( name)
  else:
    a = parent.ownerDocument.createElement( name)
  parent.appendChild( a)
  if attributes:
    for i in attributes:
      a.setAttribute( i[0], i[1])
  return a

def textOnlyElementUnder( parent, name, text, attributes=()):
  a = elementUnder( parent, name, attributes=attributes)
  if attributes:
    for i in attributes:
      a.setAttribute( i[0], i[1])
  a.appendChild( parent.ownerDocument.createTextNode( text))
  return a
  
def getTextFromElement( element):
  text = ''
  for child in element.childNodes:
    if child.nodeValue:
      text += child.nodeValue
  return text

def childNodesWithoutEmptySpaces( node):
  return list(filter( isNotEmptyText, node.childNodes))

def isNotEmptyText( element):
  empty = re.compile('^\s*$')
  if element.nodeValue and empty.match( element.nodeValue): #(element.nodeValue == '\n') or (element.nodeValue == '\t'):
    return 0
  else:
    return 1

def getAllTextFromElement( element):
  """like getTextFromElement but mines text also from child nodes"""
  text = ''
  for child in element.childNodes:
    if child.nodeValue:
      text += child.nodeValue
    else:
      text += getAllTextFromElement( child)
  return text

def setAttributes( element, attributes):
  for a in attributes:
    element.setAttribute( a[0], a[1])
  
def getAttributes( element, names):
  """returns a list of attribute values from a list of attr names"""
  return [element.getAttribute( n) for n in names]

def getParentNameList( element):
  """returns a list of parent names (from father to grandfather...)"""
  par = element.parentNode
  if par != None:
    return [par.nodeName] + getParentNameList( par)
  else:
    return []

def getFirstChildNamed( element, name):
  l = getChildrenNamed( element, name)
  if l:
    return l[0]
  else:
    return None


def getChildrenNamed( element, name):
  return [o for o in element.childNodes if (not o.nodeValue) and (o.localName == name)]  



def isOnlyTags( text):
  """this function takes a !string! as an argument and returns true if text is only tags"""
  try:
    doc = dom.parseString( '<a>%s</a>' % text)
  except:
    return not len( text)
  if getAllTextFromElement( doc):
    return 0
  return 1
  

def simpleXPathSearch( element, path):
  atomic_paths = path.split( "/")
  out = [element]
  for atomic_path in atomic_paths:
    search_with_path = lambda x: _atomicXPathSearch( x, atomic_path)
    out =  reduce( operator.add, list(map( search_with_path, out)), [])
  return out



def _atomicXPathSearch( element, path):
  if path == "":
    if element.DOCUMENT_NODE == element.nodeType:
      return [element]
    else:
      return [element.ownerDocument]
  if path == "*":
    return element.childNodes
  else:
    return getChildrenNamed( element, path) #element.getElementsByTagName( path)


