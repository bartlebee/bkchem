#--------------------------------------------------------------------------
#     This file is part of BKchem - a chemical drawing program
#     Copyright (C) 2004 Beda Kosata <beda@zirael.org>

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


import config
import sys
import inspect


def log( *args, **kw):
  """it takes an optional keyword arguments 'output' (output file-like)
  and 'levels' (stack levels to report)"""
  if 'output' in kw:
    out = kw['output']
  else:
    out = None
  if 'levels' in kw:
    levels = kw['levels']
  else:
    levels = []
  if config.debug:
    frames = inspect.getouterframes( inspect.currentframe())
    for i in levels:
      if i < len( frames):
        print "  %s:%d -> %s()" % frames[i][1:4]
    for arg in args:
      print >> out, arg,
    print >> out


  
