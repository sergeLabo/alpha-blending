#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## always.py

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
Lancé à chaque frame durant tout le jeu.
'''


from time import sleep
from bge import logic as gl
from bge import events
from scripts.labtools import labgetobject as get_obj


def main():

    game = get_obj.get_scene_with_name("Game")
    if game:
        game_obj = game.objects
        keys()
        set_ball_visible(game_obj)


        # Rotation du Logo
        rotation(game_obj, "Plane.001", 0.02)

        # Scale des ondes
        gl.k_plage *= gl.k
        if gl.k_plage > 400:
            gl.k = 0.9
        if gl.k_plage < 0.1:
            gl.k = 1.1
        scale(game_obj, "Plane", gl.k_plage)

def rotation(game_obj, blend_o, beta):
    """Application d'une rotation sur y, en rad"""

    #
    b_obj = game_obj[blend_o]
    scene = gl.getCurrentScene()

    # set amount to rotate
    rotation = [0, beta, 0]
    b_obj.applyRotation(rotation, 0)

def scale(game_obj, blend_o, k):
    """Application d'un scale k sur l'objet"""

    #
    b_obj = game_obj[blend_o]
    scene = gl.getCurrentScene()
    b_obj.worldScale = (k, 0, k)

def keys():

    if gl.keyboard.events[events.VKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # V pour visible, invisible de la balle
        if gl.ball_visible == 0:
            gl.ball_visible = 1
        else:
            gl.ball_visible = 0
        sleep(0.1)

def set_ball_visible(game_obj):
    ball = game_obj["ball"]
    if gl.ball_visible == 0:
        ball.visible = 0
    else:
        ball.visible = 1
