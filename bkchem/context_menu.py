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


import Tkinter
import misc


class context_menu( Tkinter.Menu):

  def __init__( self, app, selected, **kw):
    Tkinter.Menu.__init__( self, app, tearoff=0, **kw)
    self.app = app
    self.selected = selected
    self.changes_made = 0
    already_there = []

    obj_types = misc.filter_unique( [o.object_type for o in selected])
    obj_types.sort()
  
    for obj_type in obj_types:
      if obj_type not in configurable:
        continue
      for attr in configurable[ obj_type]:
        vals = config_values[ attr]
        if vals and attr not in already_there:
          casc = Tkinter.Menu( self, tearoff=0)
          self.add_cascade( label=vals[ I18N_NAME], menu=casc)
          for v in vals[ VALUES]:
            casc.add_command( label=v, command=misc.lazy_apply( self.callback, (attr,v)))
          # to know what is already there
          already_there.append( attr)

  def callback( self, command, value):
    for o in self.selected:
      if o.object_type not in configurable:
        continue
      if command in configurable[ o.object_type]:
        for c in o.__class__.mro():
          if command in c.__dict__:
            c.__dict__[ command].fset( o, value)
            o.redraw()
            self.changes_made = 1
            break
    if self.changes_made:
      self.app.paper.start_new_undo_record()
      self.app.paper.add_bindings()



  def close( self, event):
    self.unpost()



  def post( self, x, y):
    Tkinter.Menu.post( self, x, y)
    self.grab_set()



config_values = { 'show':             ( _("show"),             ('yes','no')),
                  'show_hydrogens':   ( _("hydrogens"),        ('on','off')),
                  'font_size':        ( _("font size"),        (8,10,12,14,16,18)),
                  'line_width':       ( _("line width"),       (1.0,1.5,2.0,2.5,3.0))
                  }


configurable = {'atom':    ('show', 'font_size', 'show_hydrogens'),
                'text':    ('font_size',),
                'bond':    ('line_width',),
                'plus':    ('font_size',),
                'arrow':   ('line_width',)

                }


I18N_NAME = 0
VALUES = 1
