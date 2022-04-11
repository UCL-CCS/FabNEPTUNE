.. _workflow:


FabNEPTUNE Workflow
==============

Introduction
------------
FabNEPTUNE is a tool that allows for the easy execution of NEPTUNE project simulations(especially convection2d and convection3d) in remote machines. This section of the documentation will cover an example of how one would go about configuring FabNEPTUNE and running a simulation using any NEPTUNE project code.


Example of workflow for FabNEPTUNE
-----------------------------

Before submitting the simulation to a remote machine, two YAML files must be edited. First we modify the file ``FabSim3/deploy/machines_user.yml`` and add our login credentials in the template so that FabNEPTUNE knows where to run the simulation. In this example we will use the PSNC HPC system called Eagle, so the only parameter we need to add is the ``username`` we use for that computer. Other computers may have have more parameters that need to be added, such as for example, the UK National Supercomputer ARCHER2, which also requires a password to be entered. 

The next file that needs to be updated is ``FabSim3/plugins/FabNEPTUNE/machines_FabNEPTUNE project_user.yml``. In this file you can set the path to the LAMMPS executable on the remote machine. However, most HPC clusters have Nektar++ (https://www.nektar.info/) available as a module and this can be added in the loaded modules section of the file. This means that the ``convection2d_exec`` parameter can be set to the convection command rather than the path of the compiled executable. For example, an arbitrary remote machine might look like:

	.. code-block:: yaml

		remote-machine-name:
		   convection2d_exec: "lmp"
		   ...
		   ...
		   ...
		   modules:
		      loaded: ["python"]

After all this configuration, we can submit a simulation to a remote machine using the command:

    .. code-block:: console
		
		fabsim archer2 Convection2D_local:convection_2d_test	


