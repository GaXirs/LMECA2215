# Author: Robotran Team
# (c) Universite catholique de Louvain, 2024

import numpy as np
from math import sin, tan, atan   # ajout 2024

def tgc_bakker_contact(Frad, anglis, ancamb, gliss, mbs_data):		
    """Compute the Bakker-Pacejka model from:
		Pacejka, H. B., & Bakker, E. (1992). 
		THE MAGIC FORMULA TYRE MODEL. 
		Vehicle System Dynamics, 21(sup001), 1–18. 
	
    Input Parameters
    ----------------
    Frad : float 
        The normal ground_on_tire force in [N] (> 0)
    anglis : float
        The slip angle in [rad] (positive for a right turn (i.e. micro-slip to the left direction (y))
    ancamb : float
        The camber angle in [rad] (positive for clockwise rotation of the wheel around the longitudinal axis)
    gliss : float
        The longitudnial slip ratio [.] (NB: gliss = 1 means 100%) (along the x-longitudinal axis)
		
    Returns
    -------
    Flong : float 
        The longitudinal tangent force in [N] expressed in the {R} snake contact plane (along Rx)
    Flat : float 
        The lateral tangent force in [N] expressed in the {R} snake contact plane (along Ry)
    Mz : float 
        The spin pure torque in [Nm] expressed in the {R} snake contact plane (along Rz = Iz)
 
 """

	# Parameters
	# ----------

    anglisdeg = anglis*180.0/np.pi 
    ancambdeg = ancamb*180.0/np.pi 

	# Normal force in kN
	# ------------------

    FradkN = Frad/1000.0

	# Longitudinal force
	# ------------------

    k = gliss*100.0

    C	= 1.65
    D	= -21.3*FradkN**2+1144*FradkN
    B	= (49.6*FradkN**2+226*FradkN)/(C*D*np.exp(0.069*FradkN))
    E	= -0.006*FradkN**2+0.056*FradkN+0.486
    phi = (1.0-E)*k+(E/B)*atan(B*k) 
    Flong = D*sin(C*atan(B*phi))

	# Lateral force
	# -------------

    C	= 1.3
    D	= -22.1*FradkN**2+1011*FradkN
    B	= (1078*sin(1.82*atan(0.208*FradkN))*(1.0-0.022*abs(ancambdeg)))/(C*D)
    E	= -0.354*FradkN+0.707
    deltaSh = 0.028*ancambdeg
    deltaSv = (14.8*FradkN)*ancambdeg
    phi = (1.0-E)*(anglisdeg+deltaSh)+(E/B)*atan(B*(anglisdeg+deltaSh))
    Flat = -(D*sin(C*atan(B*phi))+deltaSv)

	# Combined Flong and Flat 
	# -----------------------

    k = k/100.0

    if (k == 0 and anglis == 0):
        sxs = 1
        sys = 1
    else:
        sxs = abs(k/(np.sqrt(k**2+tan(anglis)**2)))
        sys = abs(tan(anglis)/(np.sqrt(k**2+tan(anglis)**2)))

    Flong = sxs*Flong
    Flat = sys*Flat

	# Spin pure torque
	# ----------------

    C = 2.4
    D = -2.72*FradkN**2-2.28*FradkN
    B=(-1.86*FradkN**2-2.73*FradkN)/(C*D*np.exp(0.11*FradkN))*(1.0-0.03*abs(ancambdeg))
    E=(-0.07*FradkN**2+0.643*FradkN-4.04)*(1.0-0.07*np.abs(ancambdeg))
    deltaSh = 0.015*ancambdeg
    deltaSv = (-0.066*FradkN**2+0.945*FradkN)*ancambdeg
    phi = (1-E)*(anglisdeg+deltaSh)+(E/B)*atan(B*(anglisdeg+deltaSh))

    Mz = D*sin(C*atan(B*phi))+deltaSv 	

    return (Flong, Flat, Mz)
