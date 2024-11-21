# -*- coding: utf-8 -*-
"""Module for the definition of driven joints."""
# Author: Robotran Team
# (c) Universite catholique de Louvain, 2020


def user_DrivenJoints(mbs_data, tsim):
    """Set the values of the driven joints directly in the MbsData structure.

    The position, velocity and acceleration of the driven joints must be set in
    the attributes mbs_data.q, mbs_data.qd and mbs_data.qdd .

    Parameters
    ----------
    mbs_data : MBsysPy.MbsData
        The multibody system associated to this computation.
    tsim : float
        The current time of the simulation.

    Returns
    -------
    None
    """
    
    if mbs_data.process == 2:  # dynamics 
        rack_disp = 0.012 #0.009 # Rack lateral displacement parameter
        tstart = 1.2 # 1.2
        tstop = 2.2 # 2.2

        if (tsim<tstart):
            mbs_data.q[mbs_data.joint_id["T2_rack"]] = 0
            mbs_data.qd[mbs_data.joint_id["T2_rack"]] = 0
            # mbs_data.qdd[mbs_data.joint_id["T2_rack"]] = 0   Steering acceleration is neglected
        elif (tsim>= tstart and tsim<tstop):
            mbs_data.q[mbs_data.joint_id["T2_rack"]] = rack_disp * (tsim-tstart)
            mbs_data.qd[mbs_data.joint_id["T2_rack"]] = rack_disp
            # mbs_data.qdd[mbs_data.joint_id["T2_rack"]] = 0   Steering acceleration is neglected
        elif (tsim >= tstop):
            mbs_data.q[mbs_data.joint_id["T2_rack"]] = (tstop-tstart) * rack_disp
            mbs_data.qd[mbs_data.joint_id["T2_rack"]] = 0
            # mbs_data.qdd[mbs_data.joint_id["T2_rack"]] = 0   Steering acceleration is neglected

    return
