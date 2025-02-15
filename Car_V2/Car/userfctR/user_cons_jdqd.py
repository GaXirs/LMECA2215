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


def user_cons_jdqd(jdqd, mbs_data):
    """Compute the derivatives of the user constraints.

    Parameters
    ----------
    jdqd : numpy.ndaray
        The derivatives vector to be filled. The first index (jdqd[0]) must not
        be modified. The first index to be filled is jdqd[1].
    mbs_data : MBsysPy.MbsData
        The instance containing the multibody project.

    Returns
    -------
    None
    """
    return
