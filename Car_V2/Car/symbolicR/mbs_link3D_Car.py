#
#	MBsysTran - Release 8.1
#
#	Copyright 
#	Universite catholique de Louvain (UCLouvain) 
#	Mechatronic, Electrical Energy, and Dynamic systems (MEED Division) 
#	2, Place du Levant
#	1348 Louvain-la-Neuve 
#	Belgium 
#
#	http://www.robotran.be 
#
#	==> Generation Date: Mon Nov  4 15:48:11 2024
#	==> using automatic loading with extension .mbs 
#
#	==> Project name: Car
#
#	==> Number of joints: 44
#
#	==> Function: F27 - Link Forces (3D)
#
#	==> Git hash: c9679760b1e23dc6b2c784bde05d373c9aa55aef
#
#	==> Input XML
#

from math import sin, cos, sqrt

def link3D(frc, trq, s, tsim):
    q = s.q
    qd = s.qd
    qdd = s.qd

# Number of continuation lines = 0

    print("ERROR : This symbolic file should not be called.")
    print("        Please regenerate your symbolic files. ")
    print("        Error raised in mbs_link3D.")
    s.flag_stop = 1

