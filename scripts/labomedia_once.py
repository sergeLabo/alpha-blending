#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## main_once.py

#############################################################################
# Copyright (C) Labomedia 2017
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franproplin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################

'''
Ne jamais modifier ce script.

Les scripts:
- labomedia_once.py
- labomedia_always.py
sont les seuls scripts importer directement dans Blender.
Les autres scripts sont importés en temps que modules.

Il est alors possible de les modifier dans un éditeur externe
sans avoir à les recharger dans Blender.
'''

# imports locaux
from scripts import once


def main():
    '''Fonction lancée à chaque frame dans blender en temps que module.'''

    once.main()
