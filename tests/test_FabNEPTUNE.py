# -*- coding: utf-8 -*-
#
# This source file is part of the FabSim software toolkit, which is
# distributed under the BSD 3-Clause license.
# Please refer to LICENSE for detailed information regarding the licensing.
#
# This file contains FabSim definitions specific to FabNEPTUNE.
# authors:
#           Kevin Bronik, Derek Groen, Ed Threlfall

import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '../')


def test_SCEMa():
    assert(subprocess.call(["fabsim", "localhost", "Convection2D_local:convection_2d_test"]) == 0)
    assert (subprocess.call(["fabsim", "localhost", "Convection3D_local:convection_3d_test"]) == 0)
  
def test_SCEMa_ensemble1():
    assert(subprocess.call(["fabsim", "localhost", "Convection2D_ensemble_local:Convection2D_ensemble_example"]) == 0)
    assert (subprocess.call(["fabsim", "localhost", "Convection3D_ensemble_local:Convection3D_ensemble_example"]) == 0)
