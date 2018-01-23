#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# once.py

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
Ce script est appelé par main_init.main dans blender
Il ne tourne qu'une seule fois pour initier les variables
qui seront toutes des attributs du bge.logic (gl)
Seuls les attributs de logic sont stockés en permanence.

Envoi en multicast de l'IP de ce PC
Réception en TCP du smartphone.
"""


import os
import ast
import json
import threading
from time import sleep, time

from twisted.internet.protocol import DatagramProtocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

from mylabotools.labconfig import MyConfig
from mylabotools.labsometools import get_my_ip

from bge import logic as gl


# Variable globale
ini_file = "scripts/alpha-blending.ini"


class MyMulticast(DatagramProtocol):
    """Envoi en continu de ip  de ce PC toutes les secondes."""

    def __init__(self, multicast_ip, multicast_port):

        self.tempo = time()
        self.multicast_ip = multicast_ip
        self.multicast_port = multicast_port
        self.ip_server = get_my_ip()

        print("Envoi en multicast sur", self.multicast_ip,
                                        self.multicast_port, "\n")

    def startProtocol(self):
        """Called after protocol has started listening."""

        # Set the TTL>1 so multicast will cross router hops:
        # https://www.rap.prd.fr/pdf/technologie_multicast.pdf

        # préconise TTL = 1
        self.transport.setTTL(1)

        # Join a specific multicast group:
        self.transport.joinGroup(self.multicast_ip)

        # Boucle infinie pour envoi continu à tous les joueurs
        self.send_loop_thread()

    def create_multi_msg(self):

        ip_msg = {"svr_msg": {"ip": self.ip_server}}
        ip_msg_enc = json.dumps(ip_msg).encode("utf-8")

        return ip_msg_enc

    def send_loop(self):

        addr = self.multicast_ip, self.multicast_port
        ip_msg_enc = self.create_multi_msg()
        while 1:
            sleep(1)
            try:
                self.transport.write(ip_msg_enc, addr)
            except OSError as e:
                if e.errno == 101:
                    print("Network is unreachable")

    def send_loop_thread(self):
        thread_s = threading.Thread(target=self.send_loop)
        thread_s.start()

    def datagramReceived(self, datagram, address):
        """Je reçois ce que j'envoie"""

        if datagram:
            data = datagram_decode(datagram)
            if 'svr_msg' in data:
                if not "ip" in data['svr_msg']:
                    print(data)


class MyTcpServer(Protocol):
    """Reception du smartphone en TCP."""

    def __init__(self, factory):
        self.factory = factory

        self.tempo = time()

    def connectionMade(self):
        self.addr = self.transport.client
        print("Une connexion établie par le client {}".format(self.addr))

    def connectionLost(self, reason):
        print("Connection lost, reason:", reason)
        print("Connexion fermée avec le client {}".format(self.addr))

    def dataReceived(self, data):

        # Retourne un dict ou None
        data = datagram_decode(data)

        if data:
            # {'screen 2': {'slider': {'/2/s3': 0.86}}}
            apply_data_from_blendcontrol(data)


class MyTcpServerFactory(Factory):
    """self ici sera self.factory dans les objets MyTcpServer."""

    def __init__(self):

        self.numProtocols = 1
        print("Serveur twisted réception TCP sur {}\n"\
                                                .format(gl.tcp_port))

    def buildProtocol(self, addr):
        print("Nombre de protocol dans factory", self.numProtocols)

        # le self permet l'accès à self.factory dans MyTcpServer
        return MyTcpServer(self)


def apply_data_from_blendcontrol(data):
    """
    {'screen 1': {'xy': [0.413, 0.511]}}

    {'screen 2': {'slider': {'/2/s1': 0.5625}}}
    {'screen 2': {'slider': {'/2/s8': 0.7470334047904392}}}
    {'screen 2': {'button': {'/2/b8': 0}}}
    {'screen 2': {'button': {'/2/b8': 1}}}

    {'screen 3': {'xy': [0.75, 0.738]}}
    {'screen 3': {'slider': {'/3/s1': 0.520}}}
    {'screen 3': {'slider': {'/3/s8': 0.763}}}
    """

    # 3 écrans
    if 'screen 1' in data:
        if 'xy' in data['screen 1']:
            xy = data['screen 1']['xy']
            gl.orders[1]['xy'] = xy
            print("Ordres reçus:", xy)

    if 'screen 2' in data:
        # data['screen 2'] = {'slider': {'/2/s6': 0.861}}

        if 'slider' in data['screen 2']:
            sl = data['screen 2']['slider']
            for i in range(8):
                if "/2/s" + str(i) in sl:
                    a = sl["/2/s" + str(i)]
                    gl.orders[2]['slider'][i] = a
                    print("Ordres reçus:", a)

        if 'button' in data['screen 2']:
            bt = data['screen 2']['button']
            for i in range(8):
                if "/2/b" + str(i) in bt:
                    b =  bt["/2/b" + str(i)]
                    gl.orders[2]['button'][i] = b
                    print("Ordres reçus:", b)

    if 'screen 3' in data:
        if 'xy' in data['screen 3']:
            xy = data['screen 3']['xy']
            gl.orders[3]['xy'] = xy
            print("Ordres reçus:", xy)

        if 'slider' in data['screen 3']:
            sl = data['screen 3']['slider']
            for i in range(8):
                if "/3/s" + str(i) in sl:
                    c = sl["/3/s" + str(i)]
                    gl.orders[2]['slider'][i] = c
                    print("Ordres reçus:", c)

def run_reactor():
    """
    Je reçois aussi ce que j'envoie
    Je reçois de blendcontrol du smartphone en TCP
    """

    endpoint = TCP4ServerEndpoint(reactor, 8000)  # gl.tcp_port)
    endpoint.listen(MyTcpServerFactory())

    reactor.listenMulticast(gl.multi_port,
                            MyMulticast(gl.multi_ip,gl.multi_port),
                            listenMultiple=True)

    reactor.run(installSignalHandlers=0)

def datagram_decode(datagram):
    """
    Decode la réception qui est des bytes, pour obtenir un dict.
    Ne fonctionne qu'avec un msg contenant un dict.
    """

    try:
        dec = datagram.decode("utf-8")
    except:
        print("Décodage UTF-8 inutile !")
        dec = datagram

    try:
        msg_dict = ast.literal_eval(dec)
    except:
        print("ast.literal_eval raté")
        msg_dict = None

    if isinstance(msg_dict, dict):
        return msg_dict
    else:
        print("Mauvais message reçu")
        return None

def get_conf():
    """Récupère la configuration depuis le fichier *.ini."""

    # Le dossier courrant est le dossier dans lequel est le *.blend
    current_dir = gl.expandPath("//")
    print("Dossier courant depuis once.py {}".format(current_dir))
    gl.once = 0

    gl.ma_conf = MyConfig(current_dir + ini_file)
    gl.conf = gl.ma_conf.conf

    print("\nConfiguration du jeu multipong:")
    print(gl.conf, "\n")

def get_network_conf():
    """Valeurs par défaut de tous les attributs du bge.logic"""

    gl.ip_server = None
    gl.multi_ip = gl.conf["multicast"]["ip"]
    gl.multi_port = gl.conf["multicast"]["port"]
    gl.multi_addr = gl.multi_ip, gl.multi_port
    gl.tcp_port = gl.conf["tcp"]["port"]

def set_variable():
    # bordel
    gl.ball_visible = 0
    gl.k_plage = 1
    gl.k = 1.1

def create_or_reset_orders():
    """
    {1: {'xy': [0, 0]},
     2: {'slider': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0},
         'button': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}},
     3: {'xy': [0, 0],
         'slider': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}}}

    """

    gl.orders = {1: {}, 2: {}, 3: {}}

    # screen 1
    gl.orders[1] = {'xy': [0, 0]}

    # screen 2
    gl.orders[2]['slider'] = {}
    gl.orders[2]['button'] = {}

    for i in range(8):
        gl.orders[2]['slider'][i] = 0
        gl.orders[2]['button'][i] = 0

    # screen 3
    gl.orders[3] = {'xy': [0, 0]}

    gl.orders[3]['slider'] = {}

    for i in range(8):
        gl.orders[3]['slider'][i] = 0

    print("Dict des ordres créés:", gl.orders)

def main():

    print("\nInitialisation lancée un seule fois par labomedia_once.")

    get_conf()
    get_network_conf()
    set_variable()
    create_or_reset_orders()

    thread_twisted = threading.Thread(target=run_reactor)
    thread_twisted.start()

    # Pour les mondoshawan
    print("Fin de once.py")
