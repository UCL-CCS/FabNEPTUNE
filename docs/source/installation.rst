.. _installation:

.. Installation
.. ============

Nektar++ configuration and build
===================

In the following we will provide an example on how to configure and build Nektar++ on a remote machine.

Nektar++ on ARCHER2
===================
.. image:: ../../logo.png
   :alt: some image
   :target: https://typo3.org
   :class: with-shadow
   :scale: 50


First load the following modules:

    .. code-block:: console
		
		export CRAY_ADD_RPATH=yes
                module swap PrgEnv-cray PrgEnv-gnu 
                module load cray-fftw
		module load cmake


Enter the work directory (/work) and clone the Nektar++ code into a folder, e.g. nektarpp

    .. code-block:: console
		
		cd /work/e01/e01/mlahooti
                git clone https://gitlab.nektar.info/nektar/nektar.git nektarpp 


After the code is cloned, enter the nektarpp folder, make a build directory and enter it
    .. code-block:: console
		
		cd nektarpp
                mkdir build
                cd build


From within the build directory, run the configure command. Note the use of CC and CXX to select the special ARCHER-specific compilers.
    .. code-block:: console
		
	CC=cc CXX=CC cmake -DNEKTAR_USE_SYSTEM_BLAS_LAPACK=OFF -DNEKTAR_USE_MPI=ON -DNEKTAR_USE_HDF5=ON -DNEKTAR_USE_FFTW=ON -DTHIRDPARTY_BUILD_BOOST=ON -DTHIRDPARTY_BUILD_HDF5=ON ..


cc and CC are the C and C++ wrappers for the Cray utilities and determined by the PrgEnv module.
SYSTEM_BLAS_LAPACK is disabled since, by default, we can use the libsci package which contains an optimized version of BLAS and LAPACK and not require any additional arguments to cc.
HDF5 is a better output option to use on ARCHER2 since often we run out of the number of files limit on the quota. Setting this option from within ccmake has led to problems however so make sure to specify it on the cmake command line as above. Further, the HDF5 version on the ARCHER2 is not supported at the moment, so here it is built as a third-party library.
They are currently not using the system boost since it does not appear to be using C++11 and so causing compilation errors.
At this point you can run ccmake .. to e.g. disable unnecessary solvers. Now run make as usual to compile the code

    .. code-block:: console
		
		make -j 4 install

For more detailed approach visit:
    .. code-block:: console
		
		https://www.nektar.info/nektar-on-archer2/
    

FabNEPTUNE Installation
==================

Before run NEPTUNE [assume that you have been able to run the basic FabSim examples described in the other documentation files, and that you have configured and built Nektar++ (https://www.nektar.info/) on the target machine, and  successfully tested the executable code!], you should install FabNEPTUNE which provides functionality to extend FabSim3's workflow and remote submission capabilities to NEPTUNE specific tasks. 

* To install FabSim3 tool, please follow the installation from https://fabsim3.readthedocs.io/en/latest/installation.html

* To install FabNEPTUNE plugin, simple type:

    .. code-block:: console
		
		fabsim localhost install_plugin:FabNEPTUNE	
