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
#	==> Function: F7 - Link Forces (1D)
#
#	==> Git hash: c9679760b1e23dc6b2c784bde05d373c9aa55aef
#
#	==> Input XML
#

from math import sin, cos, sqrt

def link(frc, trq, Flink, Z, Zd, s, tsim):
    q = s.q
    qd = s.qd
 
# Trigonometric functions

    S18 = sin(q[18])
    C18 = cos(q[18])
    S19 = sin(q[19])
    C19 = cos(q[19])
    S20 = sin(q[20])
    C20 = cos(q[20])
    S21 = sin(q[21])
    C21 = cos(q[21])
 
# Augmented Joint Position Vectors

 
# Link anchor points Kinematics

    RLlnk2_22 = s.dpt[2,30]*C18
    RLlnk2_32 = s.dpt[2,30]*S18
    POlnk2_22 = RLlnk2_22+s.dpt[2,3]
    ORlnk2_22 = -qd[18]*RLlnk2_32
    ORlnk2_32 = qd[18]*RLlnk2_22
    Plnk21 = POlnk2_22-s.dpt[2,11]
    Plnk31 = RLlnk2_32-s.dpt[3,11]
    PPlnk1 = Plnk21*Plnk21+Plnk31*Plnk31
    Z1 = sqrt(PPlnk1)
    e21 = Plnk21/Z1
    e31 = Plnk31/Z1
    Zd1 = ORlnk2_22*e21+ORlnk2_32*e31
    RLlnk4_22 = s.dpt[2,32]*C19
    RLlnk4_32 = s.dpt[2,32]*S19
    POlnk4_22 = RLlnk4_22+s.dpt[2,4]
    ORlnk4_22 = -qd[19]*RLlnk4_32
    ORlnk4_32 = qd[19]*RLlnk4_22
    Plnk22 = POlnk4_22-s.dpt[2,14]
    Plnk32 = RLlnk4_32-s.dpt[3,14]
    PPlnk2 = Plnk22*Plnk22+Plnk32*Plnk32
    Z2 = sqrt(PPlnk2)
    e22 = Plnk22/Z2
    e32 = Plnk32/Z2
    Zd2 = ORlnk4_22*e22+ORlnk4_32*e32
    RLlnk6_22 = s.dpt[2,34]*C20
    RLlnk6_32 = s.dpt[2,34]*S20
    POlnk6_22 = RLlnk6_22+s.dpt[2,5]
    ORlnk6_22 = -qd[20]*RLlnk6_32
    ORlnk6_32 = qd[20]*RLlnk6_22
    Plnk13 = s.dpt[1,5]-s.dpt[1,6]
    Plnk23 = POlnk6_22-s.dpt[2,6]
    Plnk33 = RLlnk6_32-s.dpt[3,6]
    PPlnk3 = Plnk13*Plnk13+Plnk23*Plnk23+Plnk33*Plnk33
    Z3 = sqrt(PPlnk3)
    e13 = Plnk13/Z3
    e23 = Plnk23/Z3
    e33 = Plnk33/Z3
    Zd3 = ORlnk6_22*e23+ORlnk6_32*e33
    RLlnk7_22 = s.dpt[2,36]*C21
    RLlnk7_32 = s.dpt[2,36]*S21
    POlnk7_22 = RLlnk7_22+s.dpt[2,7]
    ORlnk7_22 = -qd[21]*RLlnk7_32
    ORlnk7_32 = qd[21]*RLlnk7_22
    Plnk14 = s.dpt[1,10]-s.dpt[1,7]
    Plnk24 = -POlnk7_22+s.dpt[2,10]
    Plnk34 = -RLlnk7_32+s.dpt[3,10]
    PPlnk4 = Plnk14*Plnk14+Plnk24*Plnk24+Plnk34*Plnk34
    Z4 = sqrt(PPlnk4)
    e14 = Plnk14/Z4
    e24 = Plnk24/Z4
    e34 = Plnk34/Z4
    Zd4 = -ORlnk7_22*e24-ORlnk7_32*e34

# Link Forces 

    Flink1 = s.user_LinkForces(Z1,Zd1,s,tsim,1)
    Flink2 = s.user_LinkForces(Z2,Zd2,s,tsim,2)
    Flink3 = s.user_LinkForces(Z3,Zd3,s,tsim,3)
    Flink4 = s.user_LinkForces(Z4,Zd4,s,tsim,4)
 
# Link Dynamics: forces projection on body-fixed frames

    fPlnk21 = Flink1*e21
    fPlnk31 = Flink1*e31
    trqlnk6_1_1 = -fPlnk21*(s.dpt[3,11]-s.l[3,6])+fPlnk31*s.dpt[2,11]
    trqlnk6_1_2 = fPlnk31*s.l[1,6]
    trqlnk6_1_3 = -fPlnk21*s.l[1,6]
    fSlnk21 = Flink1*(e21*C18+e31*S18)
    fSlnk31 = Flink1*(-e21*S18+e31*C18)
    trqlnk18_1_1 = -fSlnk31*s.dpt[2,30]
    fPlnk22 = Flink2*e22
    fPlnk32 = Flink2*e32
    frclnk6_2_2 = fPlnk21+fPlnk22
    frclnk6_2_3 = fPlnk31+fPlnk32
    trqlnk6_2_1 = trqlnk6_1_1-fPlnk22*(s.dpt[3,14]-s.l[3,6])+fPlnk32*s.dpt[2,14]
    trqlnk6_2_2 = trqlnk6_1_2+fPlnk32*s.l[1,6]
    trqlnk6_2_3 = trqlnk6_1_3-fPlnk22*s.l[1,6]
    fSlnk22 = Flink2*(e22*C19+e32*S19)
    fSlnk32 = Flink2*(-e22*S19+e32*C19)
    trqlnk19_2_1 = -fSlnk32*s.dpt[2,32]
    fPlnk13 = Flink3*e13
    fPlnk23 = Flink3*e23
    fPlnk33 = Flink3*e33
    frclnk6_3_2 = fPlnk23+frclnk6_2_2
    frclnk6_3_3 = fPlnk33+frclnk6_2_3
    trqlnk6_3_1 = trqlnk6_2_1-fPlnk23*(s.dpt[3,6]-s.l[3,6])+fPlnk33*s.dpt[2,6]
    trqlnk6_3_2 = trqlnk6_2_2+fPlnk13*(s.dpt[3,6]-s.l[3,6])-fPlnk33*(s.dpt[1,6]-s.l[1,6])
    trqlnk6_3_3 = trqlnk6_2_3-fPlnk13*s.dpt[2,6]+fPlnk23*(s.dpt[1,6]-s.l[1,6])
    fSlnk13 = Flink3*e13
    fSlnk23 = Flink3*(e23*C20+e33*S20)
    fSlnk33 = Flink3*(-e23*S20+e33*C20)
    trqlnk20_3_1 = -fSlnk33*s.dpt[2,34]
    trqlnk20_3_3 = fSlnk13*s.dpt[2,34]
    fPlnk14 = Flink4*e14
    fPlnk24 = Flink4*(e24*C21+e34*S21)
    fPlnk34 = Flink4*(-e24*S21+e34*C21)
    trqlnk21_4_1 = fPlnk34*s.dpt[2,36]
    trqlnk21_4_3 = -fPlnk14*s.dpt[2,36]
    fSlnk14 = Flink4*e14
    fSlnk24 = Flink4*e24
    fSlnk34 = Flink4*e34
    frclnk6_4_1 = fPlnk13-fSlnk14
    frclnk6_4_2 = -fSlnk24+frclnk6_3_2
    frclnk6_4_3 = -fSlnk34+frclnk6_3_3
    trqlnk6_4_1 = trqlnk6_3_1+fSlnk24*(s.dpt[3,10]-s.l[3,6])-fSlnk34*s.dpt[2,10]
    trqlnk6_4_2 = trqlnk6_3_2-fSlnk14*(s.dpt[3,10]-s.l[3,6])+fSlnk34*(s.dpt[1,10]-s.l[1,6])
    trqlnk6_4_3 = trqlnk6_3_3+fSlnk14*s.dpt[2,10]-fSlnk24*(s.dpt[1,10]-s.l[1,6])
 
# Symbolic model output

    frc[1,6] = s.frc[1,6]+frclnk6_4_1
    frc[2,6] = s.frc[2,6]+frclnk6_4_2
    frc[3,6] = s.frc[3,6]+frclnk6_4_3
    trq[1,6] = s.trq[1,6]+trqlnk6_4_1
    trq[2,6] = s.trq[2,6]+trqlnk6_4_2
    trq[3,6] = s.trq[3,6]+trqlnk6_4_3
    frc[2,18] = s.frc[2,18]-fSlnk21
    frc[3,18] = s.frc[3,18]-fSlnk31
    trq[1,18] = s.trq[1,18]+trqlnk18_1_1
    frc[2,19] = s.frc[2,19]-fSlnk22
    frc[3,19] = s.frc[3,19]-fSlnk32
    trq[1,19] = s.trq[1,19]+trqlnk19_2_1
    frc[1,20] = s.frc[1,20]-fSlnk13
    frc[2,20] = s.frc[2,20]-fSlnk23
    frc[3,20] = s.frc[3,20]-fSlnk33
    trq[1,20] = s.trq[1,20]+trqlnk20_3_1
    trq[3,20] = s.trq[3,20]+trqlnk20_3_3
    frc[1,21] = s.frc[1,21]+fPlnk14
    frc[2,21] = s.frc[2,21]+fPlnk24
    frc[3,21] = s.frc[3,21]+fPlnk34
    trq[1,21] = s.trq[1,21]+trqlnk21_4_1
    trq[3,21] = s.trq[3,21]+trqlnk21_4_3
 
# Symbolic model output

    Z[1] = Z1
    Zd[1] = Zd1
    Flink[1] = Flink1
    Z[2] = Z2
    Zd[2] = Zd2
    Flink[2] = Flink2
    Z[3] = Z3
    Zd[3] = Zd3
    Flink[3] = Flink3
    Z[4] = Z4
    Zd[4] = Zd4
    Flink[4] = Flink4

# Number of continuation lines = 0


