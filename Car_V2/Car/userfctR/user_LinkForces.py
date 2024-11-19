# -*- coding: utf-8 -*-
"""Module for the definition of user links forces."""
# Author: Robotran Team
# (c) Universite catholique de Louvain, 2020


def user_LinkForces(Z, Zd, mbs_data, tsim, identity):
    """Compute the force in the given link.

    Parameters
    ----------
    Z : float
        The distance between the two anchor points of the link.
    Zd : float
        The relative velocity between the two anchor points of the link.
    mbs_data : MBsysPy.MbsData
        The multibody system associated to this computation.
    tsim : float
        The current time of the simulation.
    identity : int
        The identity of the computed link.

    Returns
    -------
    Flink : float
        The force in the current link.

    """
    front_ids = [mbs_data.link_id["Amortisseur_av_g_1"], mbs_data.link_id["Amortisseur_av_d_1"]]
    rear_ids = [mbs_data.link_id["Amortisseur_ar_g_1"], mbs_data.link_id["Amortisseur_ar_d_1"]]

    if identity in front_ids:
        K = mbs_data.user_model["FrontSuspension"]["K"]
        D = mbs_data.user_model["FrontSuspension"]["D"]
        L0 = mbs_data.user_model["FrontSuspension"]["L0"]
        return K * (Z - L0) + D * Zd
    elif identity in rear_ids:
        K = mbs_data.user_model["RearSuspension"]["K"]
        D = mbs_data.user_model["RearSuspension"]["D"]
        L0 = mbs_data.user_model["RearSuspension"]["L0"]
        return K * (Z - L0) + D * Zd
