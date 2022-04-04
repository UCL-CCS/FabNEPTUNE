# -*- coding: utf-8 -*-
#
# This source file is part of the FabSim software toolkit, which is
# distributed under the BSD 3-Clause license.
# Please refer to LICENSE for detailed information regarding the licensing.
#
# This file contains FabSim definitions specific to FabNEPTUNE.
# authors:
#           Kevin Bronik, Derek Groen, Ed Threlfall

try:
    from fabsim.base.fab import *
except ImportError:
    from fabsim.base import *

from pprint import pprint
import os
import yaml
import ruamel.yaml

# Add local script, blackbox and template path.
add_local_paths("FabNEPTUNE")

FabNEPTUNE_path = get_plugin_path('FabNEPTUNE')


@task
@load_plugin_env_vars("FabNEPTUNE")
def Convection2D_local(config, **args):
    """
    fabsim localhost Convection2D_local:convection_2d_test
    """
    env.update(env.FabNEPTUNE_params)
    return NEPTUNE_job(config, 'Convection2D_local', **args)

@task
@load_plugin_env_vars("FabNEPTUNE")
def Convection3D_local(config, **args):
    """
    fabsim localhost Convection3D_local:convection_3d_test
    """
    env.update(env.FabNEPTUNE_params)
    return NEPTUNE_job(config, 'Convection3D_local', **args)

@task
@load_plugin_env_vars("FabNEPTUNE")
def Convection2D_remote(config, **args):
    """
    fabsim remotemachine Convection2D_remote:convection_2d_test
    """
    env.update(env.FabNEPTUNE_params)
    return NEPTUNE_job(config, 'Convection2D_remote', **args)

@task
@load_plugin_env_vars("FabNEPTUNE")
def Convection3D_remote(config, **args):
    """
    fabsim remotemachine Convection3D_remote:convection_3d_test
    """
    env.update(env.FabNEPTUNE_params)
    return NEPTUNE_job(config, 'Convection3D_remote', **args)


def NEPTUNE_job(config, script, **args):
    """
    Submit an NEPTUNE job
    input args

        script:
            input script for job execution,
            available scripts : NEPTUNE
        config:
            config directory to use to define geometry
            please look at /FabNEPTUNE/config_files to see the available configs
    """
    update_environment(args)
    with_config(config)
    execute(put_configs, config)
    return job(dict(script=script,
                    memory='4G'),
               args)


@task
@load_plugin_env_vars("FabNEPTUNE")
def Convection2D_ensemble_local(config, sweep_dir=False, **kwargs):
    '''
        fabsim localhost Convection2D_ensemble_local:Convection2D_ensemble_example

    '''
    env.update(env.FabNEPTUNE_params)
    Convection2D_ensemble_run(config, 'Convection2D_local', sweep_dir, **kwargs)


@task
@load_plugin_env_vars("FabNEPTUNE")
def Convection2D_ensemble_remote(config, sweep_dir=False, **kwargs):
    '''
        fabsim remotemachine Convection2D_ensemble_remote:Convection2D_ensemble_example

    '''
    env.update(env.FabNEPTUNE_params)
    Convection2D_ensemble_run(config, 'Convection2D_remote', sweep_dir, **kwargs)


def Convection2D_ensemble_run(config, script, sweep_dir, **kwargs):

    # If sweep_dir not set assume it is a directory in config with default name
    if sweep_dir is False:
        path_to_config = find_config_file_path(config)
        sweep_dir = os.path.join(path_to_config, env.sweep_dir_name)

    env.script = script
    with_config(config)
    run_ensemble(config, sweep_dir, **kwargs)

@task
@load_plugin_env_vars("FabNEPTUNE")
def Convection3D_ensemble_local(config, sweep_dir=False, **kwargs):
    '''
        fabsim localhost Convection3D_ensemble_local:Convection3D_ensemble_example

    '''
    env.update(env.FabNEPTUNE_params)
    Convection3D_ensemble_run(config, 'Convection3D_local', sweep_dir, **kwargs)

@task
@load_plugin_env_vars("FabNEPTUNE")
def Convection3D_ensemble_remote(config, sweep_dir=False, **kwargs):
    '''
        fabsim remotemachine Convection3D_ensemble_remote:Convection3D_ensemble_example

    '''
    env.update(env.FabNEPTUNE_params)
    Convection3D_ensemble_run(config, 'Convection3D_remote', sweep_dir, **kwargs)


def Convection3D_ensemble_run(config, script, sweep_dir, **kwargs):

    # If sweep_dir not set assume it is a directory in config with default name
    if sweep_dir is False:
        path_to_config = find_config_file_path(config)
        sweep_dir = os.path.join(path_to_config, env.sweep_dir_name)

    env.script = script
    with_config(config)
    run_ensemble(config, sweep_dir, **kwargs)



@task
@load_plugin_env_vars("FabNEPTUNE")
def Convection2D_init_run_analyse_campaign_remote(config, **args):

    update_environment(args)
    with_config(config)
    # to prevent mixing with previous campaign runs
    env.prevent_results_overwrite = "delete"
    execute(put_configs, config)

    # adds a label to the generated job folder
    job_lable = 'init_run_analyse_campaign_remote'
    # job_name_template: ${config}_${machine_name}_${cores}
    env.job_name_template += '_{}'.format(job_lable)

    env.script = 'Convection2D_init_run_analyse_campaign_remote'
    job(args)

@task
@load_plugin_env_vars("FabNEPTUNE")
def Convection2D_init_run_analyse_campaign_local(config, **args):

    update_environment(args)
    with_config(config)
    # to prevent mixing with previous campaign runs
    env.prevent_results_overwrite = "delete"
    execute(put_configs, config)

    # adds a label to the generated job folder
    job_lable = 'init_run_analyse_campaign_local'
    # job_name_template: ${config}_${machine_name}_${cores}
    env.job_name_template += '_{}'.format(job_lable)

    env.script = 'Convection2D_init_run_analyse_campaign_local'
    job(args)

def get_FabNEPTUNE_tmp_path():
    """ Creates a directory within FabNEPTUNE for file manipulation
    Once simulations are completed, its contents can be removed"""
    tmp_path = FabNEPTUNE_path + "/tmp"
    if not os.path.isdir(tmp_path):
        os.mkdir(tmp_path)
    return tmp_path
