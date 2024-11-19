# -*- coding: utf-8 -*-
"""
Module for the definition of user constraints.

Summary
-------
The user constraints enable to impose constraints that can not be resolved using
classical Robotran cuts.
"""
# Author: Robotran Team
# (c) Universite catholique de Louvain, 2020


def user_cons_hJ(h, Jac, mbs_data, tsim):
    """Compute the Jacobian and the constraints vector for the user constraints.

    Parameters
    ----------
    h : numpy.ndarray
        The constraint vector to be filled. The first index (h[0]) must not be
        modified. The first index to be filled is h[1].
    Jac : numpy.ndarray
        The jacobian matrix to be filled. The first row (Jac[0,:]) and line (Jac[:,0])
        must not be modified. The subarray to be filled is Jac[1:, 1:].
    mbs_data : MBsysPy.MbsData
        The instance containing the multibody project.
    tsim : float
        The current time of the simulation.

    Returns
    -------
    None
    """
    return
