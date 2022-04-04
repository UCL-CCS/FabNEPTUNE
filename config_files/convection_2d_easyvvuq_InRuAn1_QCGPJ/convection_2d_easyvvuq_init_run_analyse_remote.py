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
import yaml
# import ruamel.yaml
# from pprint import pprint
from shutil import rmtree
# import json
import chaospy as cp
import numpy as np
# import tempfile
import easyvvuq as uq
import time
import pickle
import matplotlib
if not os.getenv("DISPLAY"):
    matplotlib.use("Agg")
import matplotlib.pylab as plt
# import execute_qcgpj
from easyvvuq.actions import QCGPJPool
from easyvvuq.actions import CreateRunDirectory, Encode, Decode, ExecuteLocal, Actions

import sys


def init_run_analyse_campaign(work_dir=None, sampler_inputs_dir=None , inpt=None):

    print('inpt', inpt)
    # from shlex import quote
    # # $machine_name    '$run_command'   $convection_2d_exec
    machine_name = inpt[0]
    run_command = inpt[1]
    convection_2d_exec = inpt[2]


    campaign_params = load_campaign_params(sampler_inputs_dir=sampler_inputs_dir, machine=machine_name)
    keys = list(campaign_params.keys())
    CRED = '\33[31m'
    CEND = '\33[0m'
    print('Campaign parameters <---------->')
    for key in keys:
        print(CRED + key, ':' + CEND, campaign_params[key])
    print('\x1b[6;30;45m' + '                   ' + '\x1b[0m')
    campaign_work_dir = os.path.join(
        work_dir,
        'CONVECTION_easyvvuq_%s' % (campaign_params['sampler_name'])
    )
    if os.path.exists(campaign_work_dir):
        rmtree(campaign_work_dir)
    os.mkdir(campaign_work_dir)

    print(CRED + 'campaign_work_dir -> ', campaign_work_dir + CEND)
    db_location = "sqlite:///" + campaign_work_dir + "/campaign.db"
    print(CRED + 'db_location -> ', db_location + CEND)

    campaign = uq.Campaign(name=campaign_params['campaign_name'], db_location=db_location,
                           work_dir=campaign_work_dir)

    # Create an encoder and decoder
    encoder = uq.encoders.GenericEncoder(
        template_fname=os.path.join(sampler_inputs_dir, campaign_params[
                                    'encoder_template_fname']),
        delimiter=campaign_params['encoder_delimiter'],
        target_filename=campaign_params['encoder_target_filename']
    )

    decoder = uq.decoders.SimpleCSV(
        target_filename=campaign_params['decoder_target_filename'],
        output_columns=campaign_params['decoder_output_columns']
    )
    host = 'localhost'

    this_path = campaign._campaign_dir
    # machine_name = inpt[0]
    # convection_2d_exec = inpt[1]
    # convection_2d_input = inpt[2]
    # convection_2d_mesh = inpt[3]
    # run_command = inpt[4]
    print('machine name:', CRED + str(machine_name) + CEND)
    print('run command:', CRED + str(run_command) + CEND)
    print('convection_2d_exec:', CRED + str(convection_2d_exec) + CEND)
    print('work_dir:', CRED + str(os.getcwd()) + CEND)


    if str(machine_name) == 'localhost':
        print('\x1b[6;30;45m' + '.........................' + '\x1b[0m')
        print('\x1b[6;30;45m' + 'running on local machine!' + '\x1b[0m')
        print('\x1b[6;30;45m' + '.........................' + '\x1b[0m')
        execute = uq.actions.ExecuteLocal(
            'python3 {}/easyvvuq_convection_2d_RUN_localhost.py {} {} {}'.format(os.getcwd(),
            campaign_params['encoder_target_filename'], this_path, inpt))

    else:
        print('\x1b[6;30;45m' + '..........................' + '\x1b[0m')
        print('\x1b[6;30;45m' + 'running on remote machine!' + '\x1b[0m')
        print('\x1b[6;30;45m' + '..........................' + '\x1b[0m')
        execute = uq.actions.ExecuteLocal(
            'python3 {}/easyvvuq_convection_2d_RUN_remote.py {} {} {}'.format(os.getcwd(),
            campaign_params['encoder_target_filename'], this_path, inpt))

    actions = uq.actions.Actions(
        uq.actions.CreateRunDirectory(root=campaign_work_dir, flatten=True),
        uq.actions.Encode(encoder),
        execute,
        uq.actions.Decode(decoder))


    print('campaign_params[params]', campaign_params['params'])
    campaign.add_app(
        name=campaign_params['campaign_name'],
        params=campaign_params['params'],
        actions=actions
    )

    vary = {}
    for param in campaign_params['selected_parameters']:
        lower_value = campaign_params['parameters'][param]['uniform_range'][0]
        upper_value = campaign_params['parameters'][param]['uniform_range'][1]
        if campaign_params['distribution_type'] == 'DiscreteUniform':
            vary.update({param: cp.DiscreteUniform(lower_value, upper_value)})
        elif campaign_params['distribution_type'] == 'Uniform':
            vary.update({param: cp.Uniform(lower_value, upper_value)})

    print('vary', vary)
    if campaign_params['sampler_name'] == 'SCSampler':
        sampler = uq.sampling.SCSampler(
            vary=vary,
            polynomial_order=campaign_params['polynomial_order'],
            quadrature_rule=campaign_params['quadrature_rule'],
            growth=campaign_params['growth'],
            sparse=campaign_params['sparse'],
            midpoint_level1=campaign_params['midpoint_level1'],
            dimension_adaptive=campaign_params['dimension_adaptive']
        )
    elif campaign_params['sampler_name'] == 'PCESampler':
        sampler = uq.sampling.PCESampler(
            vary=vary,
            polynomial_order=campaign_params['polynomial_order'],
            rule=campaign_params['quadrature_rule'],
            sparse=campaign_params['sparse'],
            growth=campaign_params['growth']
        )
    elif campaign_params['sampler_name'] == 'QMCSampler':
        sampler = uq.sampling.QMCSampler(
            vary=vary,
            n_mc_samples=32,
            count=2
        )
    elif campaign_params['sampler_name'] == 'RandomSampler':
        sampler = uq.sampling.RandomSampler(
            vary=vary
        )
    #
    # if str(machine_name) == 'localhost':
    #     print("Running locally")
    #     from dask.distributed import Client
    #     client = Client(processes=True, threads_per_worker=1)
    #
    # else:
    #     print("Running remotely-SLURM")
    #     from dask.distributed import Client
    #     from dask_jobqueue import SLURMCluster
    #     cluster = SLURMCluster(cores=128,
    #                            processes=16,
    #                            memory='256GB',
    #                            queue='standard',
    #                            header_skip=['--mem'],
    #                            job_extra=['--qos="standard"'],
    #                            # python='srun python',
    #                            project='e723-kevinb',
    #                            walltime="24:00:00",
    #                            shebang="#!/bin/bash --login",
    #                            local_directory='$PWD',
    #                            env_extra=['export PYTHONUSERBASE=/mnt/lustre/a2fs-work2/work/e723/e723/kevinb/miniconda3/envs/py38',
    #                                      'export PATH=$PYTHONUSERBASE/bin:$PATH',
    #                                      'export PYTHONPATH=$PYTHONUSERBASE/lib/python3.8/site-packages:$PYTHONPATH'])
    #     cluster.scale(10)
    #     print(cluster)
    #     print(cluster.job_script())
    #     client = Client(cluster)
    # print(client)


    # Associate the sampler with the campaign
    # sampler=uq.sampling.MCSampler(vary=vary, n_mc_samples=16)
    campaign.set_sampler(sampler)
    time_start = time.time()
    campaign.draw_samples()
    print("Number of samples = %s" % campaign.get_active_sampler().count)
    #
    time_end = time.time()
    # from dask.distributed import Client
    # client = Client(processes=True, threads_per_worker=1)
    print("Time for phase 2 = %.3f" % (time_end - time_start))
    time_start = time.time()
    # campaign.execute(pool=client).collate()
    with QCGPJPool(template_params={'venv': '/mnt/lustre/a2fs-work2/work/e723/e723/kevinb/venv_kevin'}) as qcgpj:
        campaign.execute(pool=qcgpj).collate(progress_bar=True)


    time_end = time.time()
    print("Time for phase 3 = %.3f" % (time_end - time_start))
    time_start = time.time()
    time_end = time.time()
    print("Time for phase 4 = %.3f" % (time_end - time_start))
    time_start = time.time()
    output_column = campaign_params['decoder_output_columns']
    if campaign_params['sampler_name'] == 'SCSampler':
        analysis = uq.analysis.SCAnalysis(
            sampler=campaign._active_sampler,
            qoi_cols=["F1-press_L"]
        )
    elif campaign_params['sampler_name'] == 'PCESampler':
        analysis = uq.analysis.PCEAnalysis(
            sampler=campaign._active_sampler,
            qoi_cols=["F1-press_L"]
        )
    elif campaign_params['sampler_name'] == 'QMCSampler':
        analysis = uq.analysis.QMCAnalysis(
            sampler=campaign._active_sampler,
            qoi_cols=["F1-press_L"]
        )

    else:
        print("uq.analysis for sampler_name = %s is not specified! " %
              (campaign_params['sampler_name']))
        exit(1)
    time_end = time.time()
    print("Time for phase 5 = %.3f" % (time_end - time_start))

    campaign.apply_analysis(analysis)
    time_end = time.time()
    print("Time for phase 6 = %.3f" % (time_end - time_start))
    time_start = time.time()

    # Get Descriptive Statistics
    results_df = campaign.get_collation_result()
    results = campaign.get_last_analysis()


    print("descriptive statistics :")
    print(results.describe("F1-press_L"))
    print("the first order sobol index :")
    print(results.sobols_first()['F1-press_L'])

    mean = results.describe("F1-press_L", "mean")
    var = results.describe("F1-press_L", "var")

    t = np.linspace(0, 200, 150)
    results.plot_moments(qoi="F1-press_L", ylabel="F1-press_L", xlabel="Time", alpha=0.2,
                         filename=os.path.join(campaign_work_dir, 'F1-press_L_moments.png'))
    results.plot_sobols_first(
        qoi="F1-press_L", xlabel="Time",
        filename=os.path.join(campaign_work_dir, 'F1-press_L_sobols_first.png')
    )

    plt.figure()
    rho00 = results.describe('F1-press_L', 'mean')
    for k in results.sobols_total()['F1-press_L'].keys():
        plt.plot(rho00, results.sobols_total()['F1-press_L'][k], label=k)
    plt.legend(loc=0)
    plt.xlabel('F1-press_L [N/A]')
    plt.ylabel('sobols_total')
    plt.title('F1-press_L')
    plt.savefig(os.path.join(campaign_work_dir, 'F1-press_L_sobols_total.png'))
    print("saving F1-press_L_sobols_total.png -->", os.path.join(campaign_work_dir, 'F1-press_L_sobols_total.png'))
    plt.close()
    plt.figure()
    rho02 = results.describe('F1-press_L', 'mean')
    for k1 in results.sobols_second()['F1-press_L'].keys():
        for k2 in results.sobols_second()['F1-press_L'][k1].keys():
            plt.plot(rho02, results.sobols_second()['F1-press_L'][k1][k2], label=k1 + '/' + k2)
    plt.legend(loc=0, ncol=2)
    plt.xlabel('F1-press_L [N/A]')
    plt.ylabel('sobols_second')
    plt.title('F1-press_L')
    plt.savefig(os.path.join(campaign_work_dir, 'F1-press_L_sobols_second.png'))
    print("saving F1-press_L_sobols_second.png -->",
          os.path.join(campaign_work_dir, 'F1-press_L_sobols_second.png'))
    plt.close()

    time_end = time.time()
    print("Time for phase 7 = %.3f" % (time_end - time_start))
    time_start = time.time()

    pickle_file = os.path.join(campaign_work_dir, "convection_2d.pickle")
    with open(pickle_file, "bw") as f_pickle:
        pickle.dump(results, f_pickle)

    time_end = time.time()
    print("Time for phase 8 = %.3f" % (time_end - time_start))


def load_campaign_params(sampler_inputs_dir=None, machine=None):
    if str(machine) == 'localhost':
        print('\x1b[6;30;45m' + '..............................................' + '\x1b[0m')
        print('\x1b[6;30;45m' + 'loading campaign parameters for local machine!' + '\x1b[0m')
        print('\x1b[6;30;45m' + '..............................................' + '\x1b[0m')
        user_campaign_params_yaml_file = os.path.join('campaign_params_local.yml')
        campaign_params = yaml.load(open(user_campaign_params_yaml_file),
                                    Loader=yaml.SafeLoader
                                    )
        campaign_params['campaign_name'] += '-' + campaign_params['sampler_name']

    else:
        print('\x1b[6;30;45m' + '...............................................' + '\x1b[0m')
        print('\x1b[6;30;45m' + 'loading campaign parameters for remote machine!' + '\x1b[0m')
        print('\x1b[6;30;45m' + '...............................................' + '\x1b[0m')
        user_campaign_params_yaml_file = os.path.join('campaign_params_remote.yml')
        campaign_params = yaml.load(open(user_campaign_params_yaml_file),
                                    Loader=yaml.SafeLoader
                                    )
        campaign_params['campaign_name'] += '-' + campaign_params['sampler_name']


    # save campaign parameters in to a log file
    with open('campaign_params.log', 'w') as param_log:
        param_log.write('-' * 45 + '\n')
        param_log.write(" The used parameters for easyvvuq campaign\n")
        param_log.write('-' * 45 + '\n')
        yaml.dump(campaign_params, param_log, default_flow_style=False,
                  indent=4)
        param_log.write('-' * 45 + '\n\n')

    # print to campaign_params.log
    print("\ncampaign_params.log :")
    with open('campaign_params.log', 'r') as param_log:
        lines = param_log.readlines()
        print('\n'.join([line.rstrip() for line in lines]))
        return campaign_params


if __name__ == "__main__":
    # CRED = '\33[31m'
    # CEND = '\33[0m'
    # # $machine_name    '$run_command'   $convection_2d_exec

    inpt = []
    inpt.append(sys.argv[1])
    inpt.append(sys.argv[2])
    inpt.append(sys.argv[3])

    # work_dir1 = os.path.join(os.path.dirname(__file__))
    work_dir1 = os.getcwd()

    sampler_inputs_dir = os.path.join(work_dir1)
    init_run_analyse_campaign(work_dir=work_dir1, sampler_inputs_dir=sampler_inputs_dir, inpt=inpt)
