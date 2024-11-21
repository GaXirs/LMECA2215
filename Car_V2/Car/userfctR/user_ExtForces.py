# -*- coding: utf-8 -*-
"""Module for defining user function required to compute external forces."""
# Author: Robotran Team
# (c) Universite catholique de Louvain, 2019


import numpy as np
from tgc_car_kine_wheel import tgc_car_kine_wheel
from tgc_bakker_contact import tgc_bakker_contact

table_force = np.zeros(20)
table_anglis = np.zeros(8)

def user_ExtForces(PxF, RxF, VxF, OMxF, AxF, OMPxF, mbs_data, tsim, ixF):
    """Compute an user-specified external force.

    Parameters
    ----------
    PxF : numpy.ndarray
        Position vector (index starting at 1) of the force sensor expressed in
        the inertial frame: PxF[1:4] = [P_x, P_y, P_z]
    RxF : numpy.ndarray
        Rotation matrix (index starting at 1) from the inertial frame to the
        force sensor frame: Frame_sensor = RxF[1:4,1:4] * Frame_inertial
    VxF : numpy.ndarray
        Velocity vector (index starting at 1) of the force sensor expressed in
        the inertial frame: VxF[1:4] = [V_x, V_y, V_z]
    OMxF : numpy.ndarray
        Angular velocity vector (index starting at 1) of the force sensor
        expressed in the inertial frame: OMxF[1:4] = [OM_x, OM_y, OM_z]
    AxF : numpy.ndarray
        Acceleration vector (index starting at 1) of the force sensor expressed
        in the inertial frame: AxF[1:4] = [A_x, A_y, A_z]
    OMPxF : numpy.ndarray
        Angular acceleration vector (index starting at 1) of the force sensor
        expressed in the inertial frame: OMPxF[1:4] = [OMP_x, OMP_y, OMP_z]
    mbs_data : MBsysPy.MbsData
        The multibody system associated to this computation.
    tsim : float
        The current time of the simulation.
    ixF : int
        The ID identifying the computed force sensor.

    Notes
    -----
    For 1D numpy.ndarray with index starting at 1, the first index (array[0])
    must not be modified. The first index to be filled is array[1].

    For 2D numpy.ndarray with index starting at 1, the first row (mat[0, :]) and
    line (mat[:,0]) must not be modified. The subarray to be filled is mat[1:, 1:].

    Returns
    -------
    Swr : numpy.ndarray
        An array of length 10 equal to [0., Fx, Fy, Fz, Mx, My, Mz, dxF].
        F_# are the forces components expressed in inertial frame.
        M_# are the torques components expressed in inertial frame.
        dxF is an array of length 3 containing the component of the forces/torque
        application point expressed in the BODY-FIXED frame.
    """
    idpt = mbs_data.xfidpt[ixF]
    dxF = mbs_data.dpt[1:, idpt]

    wheels_ids = [mbs_data.extforce_id["F_av_g_1"], mbs_data.extforce_id["F_av_d_1"],
                  mbs_data.extforce_id["F_ar_g_1"], mbs_data.extforce_id["F_ar_d_1"]]

    if ixF in wheels_ids:
        # Wheel kinematics
        (pen, rz, anglis, ancamb, gliss, Pcontact, Vcontact, Rsol, dxF) =\
            tgc_car_kine_wheel(PxF, RxF, VxF, OMxF, mbs_data)
        # Wheel dynamics
        Fwhl_R = np.zeros(4)
        Mwhl_R = np.zeros(4)
        Flong = 0
        Flat = 0
        Mz = 0
        if mbs_data.process == 1:  # static equilibrium
            Fwhl_R[3] = pen * mbs_data.user_model["FrontTire"]["K"]
            Frad = Fwhl_R[3] # ajout 2024
        elif mbs_data.process == 2:  # dynamic
            if pen > 0:
                Fwhl_R[3] = pen * mbs_data.user_model["FrontTire"]["K"]
                Frad = Fwhl_R[3] # ajout 2024
                (Flong, Flat, Mz) = tgc_bakker_contact(Frad, anglis, ancamb, gliss, mbs_data)
        Fwhl_R[1] = Flong 	# ajout 2024
        Fwhl_R[2] = Flat 	# ajout 2024
        Mwhl_R[3] = Mz		# ajout 2024
        ind = 0
        for i in range(4):
            if ixF == wheels_ids[i]: ind = i
        table_force[ind*5+0] = ixF
        table_force[ind*5+1] = Flong
        table_force[ind*5+2] = Flat
        table_force[ind*5+3] = Frad
        table_force[ind*5+4] = Mz
        table_anglis[ind*2+0] = ixF
        table_anglis[ind*2+1] = anglis
        mbs_data.vector = table_force
        mbs_data.vector2 = table_anglis
        # expressed in inertial frame
        Fwhl_I = np.zeros(4)
        Mwhl_I = np.zeros(4)
        Rsol = Rsol.reshape((4, 4))[1:, 1:]


        Fwhl_I[1:] = np.matmul(Rsol.T, Fwhl_R[1:])[:]
        Mwhl_I[1:] = np.matmul(Rsol.T, Mwhl_R[1:])[:]

    Swr = np.zeros(10)
    Swr[1:4] = Fwhl_I[1:]
    Swr[4:7] = Mwhl_I[1:]
    Swr[7:] = dxF[0:]
    
    
    return Swr
