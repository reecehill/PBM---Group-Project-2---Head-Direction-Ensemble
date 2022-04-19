import automatedParameters
import numpy as np


numberOfUnits = 360

f_max = 40 #Hz

# Taken from Section 3, Basic Dynamic Model, in-text.
tau = 10 #msec


# ----------START------------
# (INV) SIGMOID FUNCTION PARAMETERS
# ---------------------------

# Taken from Figure 4.
# "Determined by scaling condition: sigma(1-c) = f_max = 40Hz"
# NOTE: Is referenced in paper as both alpha and a?!
alpha = 6.34

# Taken from Figure 4.
beta = 0.8

# Taken from Figure 4.
b = 10

# Taken from Figure 4.
c = 0.5

# ---------------------------
# (INV) SIGMOID FUNCTION PARAMETERS
# -----------END-------------


# //////////////////////////////////


# ----------START------------
# TUNING CURVE PARAMETERS
# ---------------------------

# TODO: Taken from ?
K = 8

# TODO: Taken from ?
# To produce Figure 2...
# A = 2.53
A = 1

# TODO: Taken from ?
# To produce Figure 2...
# B = 34.8/np.exp(K)
# To produce Figure ?...
B = (f_max - A)/np.exp(K)


# TODO: Taken from ?
theta_0 = 0


# ---------------------------
# TUNING CURVE PARAMETERS
# -----------END-------------


# //////////////////////////////////

# ----------START------------
# WEIGHT DISTRIBUTION PARAMETERS
# ---------------------------

# NOTE: penaltyForMagnitude = lambda in paper, but the word is reserved in Python.
penaltyForMagnitude_0 = 10**(-2)

# Taken from Figure 5
epsilon = 0.1

# ---------------------------
# WEIGHT DISTRIBUTION PARAMETERS
# -----------END-------------


# //////////////////////////////////

# Do not edit below this line
outputDirectory, cwd, randomGenerator, theta = automatedParameters.generate()
