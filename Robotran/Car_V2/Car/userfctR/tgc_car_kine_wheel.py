# Author: Robotran Team
# (c) Universite catholique de Louvain, 2024

import numpy as np
from math import sin, cos, asin, atan  
import sys 

def tgc_car_kine_wheel(PxF, RxF, VxF, OMxF, mbs_data):	  
    """Compute the wheel-tire kinematics.

    Parameters
    ----------
	pen	     : tire/ground penetration in I" direction (positive if tire in the ground)
    rz       : instantaneous radius (in the wheel plane)
    ancamb   : camber angle [rad], positibve clockwise along x-direction
    anglis   : slip angle [rad], positive for a right turn
    gliss    : longitudinal slip ratio [.]
    Pcontact : contact point position in the inertial frame
    Vcontact : contact point velocity in the inertial frame
    Rt_ground: rotation matrix between the inertial frame and the
              wheel/ground contact frame, R: [R]=Rt_ground*[I]
    dxF      : contact point vector in the fixed-material wheel frame (from the previous joint)

    Input:
    -----   
    PxF       : absolute position vector of the center of the wheel (Inertial frame)
    RxF       : absolute rotation matrix of the wheel:  [Xwheel]=RxF*[I]
    VxF       : absolute velocity vector of the center of the wheel (Inertial frame)
    OMxF      : absolute angular velocity vector of the wheel(Inertial frame) 
    mbs_data : the mbs_data structure
             
    Hypotheses de base
      > le sol est plan et horizontal
      > roulis (ancamb) de maximum pi/4 (sinon modele faux)
 
 	Conventions : l'axe de la roue doit etre un axe Y (R2)	
   
 """
 
	# on repasse avec des variables locales a 3 dimensions et pas 4 

 
    Pw = PxF.reshape((4, 1))[1:]		 
    Rw = RxF.reshape((4, 4))[1:, 1:]	 
    Vw = VxF.reshape((4, 1))[1:]		 
    OMw = OMxF.reshape((4, 1))[1:]		 

	## Definition des reperes

	# ey = axe de la roue dans In
    ey = np.copy(Rw[1,:])
	# eyP = axe de la roue projete dans In
    eyP = np.copy(ey)
    eyP[2] = 0
    eyP = eyP/np.linalg.norm(eyP)
	# ex = vecteur tg a la roue dans le plan dans In
    ex = np.cross(eyP,np.array([0, 0, 1]))

	# [Rsol]=Rsol*[I]  Repère de contact tangent au sol
    Rsol = np.array([np.copy(ex), np.copy(eyP), np.array([0,0,1])])
	# [Rtg]=Rtg*[I]    Repère de contact tangent à la roue
    crossxy = np.cross(ex, ey)
    Rtg = np.array([np.copy(ex), np.copy(ey), np.copy(crossxy)])


	## 	ANGLE DE CAMBRURE (f)
	# 	Calcul de l'angle (f) d'inclinaison de la roue (ancamb) par rapport a la normale au sol
	#

    sinf = Rw[1,2]       #	! ok sur sol horizontal !
    ancamb = asin(sinf)

	## 	POINT DE CONTACT + VITESSE
	# 	Calcul du rayon de percee (rz) de la roue dans le sol et
	# 	de la position et vitesse du point de contact 
	# 	de la roue avec le sol
	# 	

	# Position
	# Hauteur du sol sous le centre de la roue
    Zgnd = 0 # version avec sol plat et horizontal (plan I1, I2)

	# Rayon de percee et penetration
    rz = (Pw[2]-Zgnd)/cos(ancamb) # dans le plan de la roue
    pen = cos(ancamb)*(mbs_data.user_model["FrontTire"]["R"]-rz)	  # suivant I3

	# vecteur rayon dans le repere [Rtg]
    vrz = np.array([0,0,-rz[0]])	

	# vecteur rayon dans le repere [I]
    vrz_I = np.dot(Rtg.T, vrz)
	# position du point de contact (dans [I])
    Pc = Pw.T + vrz_I
    Pcontact = Pc[0] 

	# Vitesse: 
	# vitesse d'entrainememt du point materiel au contact
    vx1 = np.cross(OMw.T[0],vrz_I)

	# vitesse du point materiel situe au contact (dans [I])
    Vct = Vw.T[0] + vx1	
    Vcontact = Vct

	# vitesse du point materiel situe au contact (dans [Rsol])
    Vcts = np.dot(Rsol,Vct) 
	# Point d'application de la force dans [Rw]
    dxF = np.dot(Rw, vrz_I) 
	## GLISSEMENT LATERAL (angliss)
	# 	Calcul de l'angle de glissement lateral
	#   angle entre la vitesse du point geometrique et le plan de la roue

	# Calcul dans le repere [Rsol] avec la vitesse du point geometrique
	# Vitesse du centre de la roue dans le repere [Rsol]
    Vws = np.dot(Rsol, Vw.T[0])

	# Vitesse point geometrique: 
	# vecteur vitesse angulaire roue gelee
    OMw_w = np.dot(Rw, OMw.T[0])
    OMwf_w = np.array([OMw_w[0],0,OMw_w[2]])
    OMwf = np.dot(Rw.T, OMwf_w)
	# vitesse d'entrainememt du point geometrique au contact
    vx1 = np.cross(OMwf,vrz_I)	
	# vitesse du point geometrique situe au contact (dans [I])
    Vct_geo = Vw.T[0] + vx1		

	# vitesse du point geometrique situe au contact (dans [Rsol])
    Vct_geo_s = np.dot(Rsol,Vct_geo)       
    
    if abs(Vct_geo_s[0]) >= 1e-3:
        tg_anglis = Vct_geo_s[1]/Vct_geo_s[0]
    else:
        tg_anglis = 0

    anglis = atan(tg_anglis)

	## GLISSEMENT
	# 	Calcul du glissement longitudinal
	# 	
	# 	rapport de la vitesse du point de contact a la vitesse du centre de la
	# 	roue suivant l'axe de la roue
	#

	# vitesse du point de contact: Vcts(1)
	# vitesse du centre de la roue: Vws(1)
    
    if abs(Vws[0]) >= 1e-3:
        gliss = -Vcts[0]/abs(Vws[0])   # Signe négatif pour compatibilité avec le modèle Bakker Pacejka
    else:
        gliss = 0
		
    # Cohérence des dimensions des vecteurs et matrices (de dim 3 vers dim 4 pour le respect des indices)
    np.insert(Pcontact, 0, 0)
    np.insert(Vcontact, 0, 0)
    np.insert(dxF, 0, 0)
    row_zeros = np.zeros((1, 1))
    col_zeros = np.zeros((1, 1))
    Rsol = np.insert(np.insert(Rtg,0,row_zeros,0),0,col_zeros,1)


    return (pen, rz, anglis, ancamb, gliss, Pcontact, Vcontact, Rsol, dxF)