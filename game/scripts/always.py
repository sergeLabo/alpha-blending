#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# # always.py

# #####################################################################
# Copyright (C) Labomedia November 2017
#
# This file is part of alpha-blending.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# #####################################################################


"""
Lancé à chaque frame durant tout le jeu.

https://docs.blender.org/api/blender_python_api_current/bge.types.BL_ActionActuator.html

playAction( name, start_frame, end_frame, layer=0, priority=0, blendin=0,
            play_mode=KX_ACTION_MODE_PLAY, layer_weight=0.0, ipo_flags=0,
            speed=1.0,  blend_mode=KX_ACTION_BLEND_BLEND)

Plays an action.
Parameters:

    name (string) – the name of the action
    start (float) – the start frame of the action
    end (float) – the end frame of the action
    layer (integer) – the layer the action will play in (actions in
    different layers are added/blended together)
    priority (integer) – only play this action if there isn’t an action
    currently playing in this layer with a higher (lower number) priority
    blendin (float) – the amount of blending between this animation and
    the previous one on this layer
    play_mode (one of these constants) – the play mode
    layer_weight (float) – how much of the previous layer to use for blending
    ipo_flags (int bitfield) – flags for the old IPO behaviors (force, etc)
    speed (float) – the playback speed of the action as a factor
                        (1.0 = normal speed, 2.0 = 2x speed, etc)
    blend_mode (one of these constants) – how to blend this layer with
                                            previous layers
"""

from time import sleep
from bge import logic as gl
from bge import events
from mylabotools import labgetobject as get_obj


def main():
    # En cours de test
    #print("Tous les objets:\n", get_obj.get_all_objects())

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

        # Action avec send_json
        set_action_position(game_obj)

def set_action_position(game_obj):

    val = int(250 * gl.orders[2]['slider'][7])

    armature = game_obj["Armature"]
    armature.playAction('ArmatureAction.001',
                        val,
                        val,
                        speed=5,
                        play_mode=0)



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
