# How to run a Convection2D and Convection3D (test) Jobs

These examples assume that you have been able to run the basic FabSim examples described in the other documentation files, and that you have built and configured Nektar++ (https://www.nektar.info/) on the target machine.

Two minimal examples of  Convection2D and Convection3D simulation are provided in ``config_files/SCEMa_test1`` and  ``config_files/convection_2d_test`` and ``config_files/convection_3d_test`` to execute these examples type:

``fabsim localhost Convection2D_local:convection_2d_test``

``fabsim localhost Convection3D_local:convection_3d_test``