# -*- coding: utf-8 -*-
"""Module for the definition of joint forces."""
# Author: Robotran Team
# (c) Universite catholique de Louvain, 2020


def user_JointForces(mbs_data, tsim):
    """Compute the force and torques in the joint.

    It fills the MBsysPy.MbsData.Qq array.

    Parameters
    ----------
    mbs_data : MBsysPy.MbsData
        The multibody system associated to this computation.
    tsim : float
        The current time of the simulation.

    Notes
    -----
    The numpy.ndarray MBsysPy.MbsData.Qq is 1D array with index starting at 1.
    The first index (array[0]) must not be modified. The first index to be
    filled is array[1].

    Returns
    -------
    None
    """
    # Example with propulsion torque on both rear wheels (the rotation of the wheel must be an independant variable)
    # 4x4
    mbs_data.Qq[mbs_data.joint_id["R2_wheel_rr_lt"]] = mbs_data.user_model["EquilQuantities"]["Qpropulsion"]
    mbs_data.Qq[mbs_data.joint_id["R2_wheel_rr_rt"]] = mbs_data.user_model["EquilQuantities"]["Qpropulsion"]
    mbs_data.Qq[mbs_data.joint_id["R2_wheel_ft_lt"]] = mbs_data.user_model["EquilQuantities"]["Qpropulsion"]
    mbs_data.Qq[mbs_data.joint_id["R2_wheel_ft_rt"]] = mbs_data.user_model["EquilQuantities"]["Qpropulsion"]

    # # Force on the direction rack
    # mbs_data.Qq[mbs_data.joint_id["T2_rack"]] = mbs_data.user_model["EquilQuantities"]["Qrack"]

    # anti-roll bar
    mbs_data.Qq[mbs_data.joint_id["R2_def_bar_ft"]] = -mbs_data.user_model["FrontSuspension"]["C_bar"] * mbs_data.q[mbs_data.joint_id["R2_def_bar_ft"]]
    mbs_data.Qq[mbs_data.joint_id["R2_def_bar_rr"]] = -mbs_data.user_model["RearSuspension"]["C_bar"] * mbs_data.q[mbs_data.joint_id["R2_def_bar_rr"]]
