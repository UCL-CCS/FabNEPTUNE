# FabNEPTUNE
<br>
 <img height="310" src="logo.png"/>
</br>

# How to run a Convection2D and Convection3D (test) Jobs

These examples assume that you have been able to run the basic FabSim examples described in the other documentation files, and that you have built and configured Nektar++ (https://www.nektar.info/) on the target machine.

Two minimal examples of  Convection2D and Convection3D simulation are provided in ``config_files/SCEMa_test1`` and  ``config_files/convection_2d_test`` and ``config_files/convection_3d_test`` to execute these examples type:

``fabsim localhost Convection2D_local:convection_2d_test``
``fabsim <remote machine name> Convection2D_remote:convection_2d_test``

``fabsim localhost Convection3D_local:convection_3d_test``
``fabsim <remote machine name> Convection3D_remote:convection_3d_test``

# Run Ensemble Examples

### Convection2D_ensemble

These examples assume that you have been able to run the basic FabSim examples described in the other documentation files, and that you have built and configured Nektar++ (https://www.nektar.info/) on the target machine.

To run type:
```
fabsim localhost Convection2D_ensemble_local:Convection2D_ensemble_example
fabsim <remote machine name> Convection2D_ensemble_remote:Convection2D_ensemble_example
```
This example runs 3 simulations with different input files, which vary the simulation timestep, using the same topology file.


### Convection3D_ensemble

This example runs 3 simulations with different input files, which vary the simulation timestep, using the same topology file.

To run type:
```
fabsim localhost  Convection3D_ensemble_local:Convection3D_ensemble_example
fabsim <remote machine name>  Convection3D_ensemble_remote:Convection3D_ensemble_example
```
## EasyVVUQ+FabNEPTUNE
After updating the following files with your credentials

```
  -FabSim3/deploy/machines_user.yml
  -FabSim3/deploy/machines.yml
  -FabSim3/plugins/FabNEPTUNE/machines_FabNEPTUNE_user.yml
  
```

run the following:

```
  -  fabsim   localhost   Convection2D_init_run_analyse_campaign_local:convection_2d_easyvvuq_InRuAn1_QCGPJ
  -  fabsim   <remote machine name>   Convection2D_init_run_analyse_campaign_remote:convection_2d_easyvvuq_InRuAn1_QCGPJ
  -  fabsim   localhost   Convection2D_init_run_analyse_campaign_local:convection_2d_easyvvuq_InRuAn2_QCGPJ
  -  fabsim   <remote machine name>   Convection2D_init_run_analyse_campaign_remote:convection_2d_easyvvuq_InRuAn2_QCGPJ

```

and copy the results back to your local machine with

```
 -  fabsim  localhost   fetch_results
 -  fabsim  <remote machine name>   fetch_results
```
## EasyVVUQ+EasySurrogate+FabNEPTUNE 
After updating the following files with your credentials

```
  -FabSim3/deploy/machines_user.yml
  -FabSim3/deploy/machines.yml
  -FabSim3/plugins/FabSCEMa/machines_FabNEPTUNE_user.yml
  
```

run the following:

```
  -  fabsim   localhost   Convection2D_init_run_analyse_campaign_local:convection_2d_easyvvuq_easysurrogate_InRuAn1_DAS_QCGPJ
  -  fabsim   <remote machine name>   Convection2D_init_run_analyse_campaign_remotel:convection_2d_easyvvuq_easysurrogate_InRuAn1_DAS_QCGPJ
  -  fabsim   localhost   Convection2D_init_run_analyse_campaign_local:convection_2d_easyvvuq_easysurrogate_InRuAn2_DAS_QCGPJ
  -  fabsim   <remote machine name>   Convection2D_init_run_analyse_campaign_remote:convection_2d_easyvvuq_easysurrogate_InRuAn2_DAS_QCGPJ

```

and as always copy the results back to your local machine with

```
 -  fabsim  localhost   fetch_results
 -  fabsim  <remote machine name>   fetch_results
