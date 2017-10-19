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
        keys(game_obj)
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

def keys(game_obj):

    if gl.keyboard.events[events.VKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        # V pour visible, invisible de la balle
        if gl.ball_visible == 0:
            gl.ball_visible = 1
        else:
            gl.ball_visible = 0
        sleep(0.1)

    if gl.keyboard.events[events.HKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        hide_all(game_obj)
        sleep(0.1)

    if gl.keyboard.events[events.PKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        coucher_action(game_obj)
        sleep(0.1)

    if gl.keyboard.events[events.MKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        reset_coucher_action(game_obj)
        sleep(0.1)

def hide_all(game_obj):
    print(game_obj)
    for o in game_obj:
        o.visible = 0
    game_obj["coucher"].visible = 1

def reset_coucher_action(game_obj):

    armature = game_obj["Armature"]
    armature.playAction('ArmatureAction.001',
                        25,
                        0,
                        speed=1,
                        play_mode=0)

def coucher_action(game_obj):
    """Scale du soleil avec ArmatureAction
    https://docs.blender.org/api/blender_python_api_2_69_1/bge.types.KX_GameObj\
    ect.html?highlight=playaction#bge.types.KX_GameObject.playAction
    own.playAction("Idle", 1, 61, blendin=5, speed=1, play_mode=1)
    own is the armature
    play_mode=1 is looping.
    play_mode=0 is play once.
    """

    print("Couche toi là")
    armature = game_obj["Armature"]
    armature.playAction('ArmatureAction.001',
                        0,
                        25,
                        blendin=5,
                        speed=1,
                        play_mode=0)


def set_ball_visible(game_obj):
    ball = game_obj["ball"]
    if gl.ball_visible == 0:
        ball.visible = 0
    else:
        ball.visible = 1
