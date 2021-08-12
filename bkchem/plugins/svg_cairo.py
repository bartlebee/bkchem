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


from __future__ import absolute_import
from .cairo_lowlevel import cairo_exporter
from .tk2cairo import tk2cairo
import cairo
import sys
from six.moves import map
# try if there is SVGSurface in cairo
_x = cairo.SVGSurface


class svg_cairo_exporter( cairo_exporter):
  """Exports SVG via the Cairo (pycairo) library. This SVG does not embed BKChem data and is simpler
  than the default one used by BKChem."""

  doc_string = _("Exports SVG via the Cairo (pycairo) library. This SVG does not embed BKChem data and is simpler than the default one used by BKChem.")

  def __init__( self, paper):
    cairo_exporter.__init__( self, paper, converter_class=tk2cairo)

  def init_surface( self):
    w, h = list(map( int, list(map( round, self.pagesize))))
    return cairo.SVGSurface(self.filename.encode(sys.getfilesystemencoding()), w, h)

  def get_scaling( self, x, y):
    sc = self._get_scaling_ratio()
    return sc, sc

  def _get_scaling_ratio( self):
    from singleton_store import Screen
    return 72.0/Screen.dpi

  def save( self):
    self.surface.finish()


# PLUGIN INTERFACE SPECIFICATION
name = "SVG_Cairo"
extensions = [".svg"]
exporter = svg_cairo_exporter
local_name = _("SVG (Cairo)")
