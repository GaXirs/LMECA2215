# coding _*_ utf-8 _*
"""Example of a car using the Bakker Pacejka model.

Universite catholique de Louvain
MEED : Mechatronic, electrical energy, and dynamic systems
http://www.robotran.eu

Example of a car
----------------
This script gives an example of a car simulation:
  - Pre-process: check of the coordinate partitioning
  - Straight track equilibrium at constant speed (V)
  - Time simulation: car cornering (to the right)

(c) Universite catholique de Louvain
"""
# %% Packages loading
import MBsysPy as robotran
import sys
sys.path.insert(1, "../userfctR")
import numpy as np

# %% Project loading
# Before executing : verify if your terminal is in the folder workR
mbs_data = robotran.MbsData("../dataR/Car.mbs",
                            user_path="userfctR",
                            symbolic_path="symbolicR"
                            )
print(mbs_data.m)


# %% Coordinate partitioning

mbs_data.set_qdriven(mbs_data.joint_id["T2_rack"])

mbs_data.process = 0
mbs_part = robotran.MbsPart(mbs_data)
mbs_part.set_options(rowperm=1)
mbs_part.run()
del mbs_part


# %% STRAIGHT LINE EQUILIBRIUM
print('\n\nComputing STRAIGHT LINE EQUILIBRIUM')
print('--------------------------------------------------------------------------------\n')

# Set to driven all the ignorable variables
mbs_data.set_qdriven(mbs_data.joint_id["T1_chassis"])
mbs_data.set_qdriven(mbs_data.joint_id["T2_chassis"])
mbs_data.set_qdriven(mbs_data.joint_id["R3_chassis"])
mbs_data.set_qdriven(mbs_data.joint_id["R2_wheel_ft_rt"])
mbs_data.set_qdriven(mbs_data.joint_id["R2_wheel_ft_lt"])
mbs_data.set_qdriven(mbs_data.joint_id["R2_wheel_rr_rt"])
mbs_data.set_qdriven(mbs_data.joint_id["R2_wheel_rr_lt"])


# Velocity in m/s
V = 5.0

# Equilibrium module
mbs_data.process = 1 # Equilibrium or modal analysis
mbs_equil = robotran.MbsEquil(mbs_data)
mbs_equil.set_options(senstol=1e-2,  # Default : 1e-6
                      devjac=1e-2,  # Default : 1e-6
                      equitol=1e-8,  # Default : 1e-6
                      itermax=50,   # Default : 30
                      mode=2,  # Default : 1 (documentation is wrong)
                      resfilename="python_sl"
                      )

# Set the velocity in all required joints
mbs_data.qd[mbs_data.joint_id["T1_chassis"]] = V

front_wheels_height = 0.27792681  # True height of the center of the front wheel at equilibrium
rear_wheels_height = 0.28167976   # True height of the center of the rear wheel at equilibrium
mbs_data.qd[mbs_data.joint_id["R2_wheel_ft_rt"]] = V / front_wheels_height   # Wheel angular velocity
mbs_data.qd[mbs_data.joint_id["R2_wheel_ft_lt"]] = V / front_wheels_height
mbs_data.qd[mbs_data.joint_id["R2_wheel_rr_rt"]] = V / rear_wheels_height
mbs_data.qd[mbs_data.joint_id["R2_wheel_rr_lt"]] = V / rear_wheels_height



# Equilibrium procedure
mbs_equil.run()
mbs_equil.print_equil()


# Deleting the equilibrium
del mbs_equil

# %% MODAL ANALYSIS around the straight line
print('\n\nComputing MODAL ANALYSIS around the straight line')
print('----------------------------------------------------------\n')

mbs_data.process = 1

# Setting modal module (see Robotran webpage for more options)
mbs_modal = robotran.MbsModal(mbs_data)
mbs_modal.set_options(save_mat=1,  # Default : 0
                      save_eval=1,  # Default : 0
                      save_evec=1,  # Default : 0
                      save_anim=1,  # Default : 0
                      lpk_itermax=100,  # Default : 10
                      resfilename="python_modal"
                      )

# Modal procedure
mbs_modal.run()

# Deleting the modal
del mbs_modal


# %% CORNERING DIRECT DYNANMICS
# Compute the direct dynamics for car cornering.
print('\n\nComputing CORNERING DIRECT DYNANMICS')
print('--------------------------------------------------------------------------------\n')

mbs_data.process = 2

# Set all variables to independant
mbs_data.set_qu(mbs_data.joint_id["T1_chassis"])
mbs_data.set_qu(mbs_data.joint_id["T2_chassis"])
mbs_data.set_qu(mbs_data.joint_id["R3_chassis"])
mbs_data.set_qu(mbs_data.joint_id["R2_wheel_ft_rt"])
mbs_data.set_qu(mbs_data.joint_id["R2_wheel_ft_lt"])
mbs_data.set_qu(mbs_data.joint_id["R2_wheel_rr_rt"])
mbs_data.set_qu(mbs_data.joint_id["R2_wheel_rr_lt"])

# Car initial conditions (car centred on the road, non-zero forward velocity and wheel angular velocities)
mbs_data.qd[mbs_data.joint_id["T1_chassis"]] = V
mbs_data.q[mbs_data.joint_id["T2_chassis"]] = 0.0
mbs_data.q[mbs_data.joint_id["R3_chassis"]] = 0.0
mbs_data.qd[mbs_data.joint_id["R2_wheel_ft_rt"]] = V / front_wheels_height
mbs_data.qd[mbs_data.joint_id["R2_wheel_ft_lt"]] = V / front_wheels_height
mbs_data.qd[mbs_data.joint_id["R2_wheel_rr_rt"]] = V / rear_wheels_height
mbs_data.qd[mbs_data.joint_id["R2_wheel_rr_lt"]] = V / rear_wheels_height

# Set the rack displacement as driven variable to turn the car (time history to be implemented in user_DrivenJoints.py)
mbs_data.set_qdriven(mbs_data.joint_id["T2_rack"])

# Setting Dirdyn module (see Robotran webpage for more options)
mbs_dirdyn = robotran.MbsDirdyn(mbs_data)
mbs_dirdyn.set_options(tf=10,  # Default : 5.0
                       resfilename="python_dirdyn",
                       save2file=1,
                       integrator="RK4", # Other integrator: "RK4", "Dopri5"
                       flag_oneshot = 0 # Put flag to 1 to observe initial configuration with no integration
                       )

# Direct Dynamics procedure
mbs_dirdyn.run()

# Deleting the direct dynamics
del mbs_dirdyn

# %% CLOSING OPERATIONS                      *
# Free mbs_data
del mbs_data
