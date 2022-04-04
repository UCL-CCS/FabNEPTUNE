#!/usr/bin/env python3

import sys
import numpy as np
import json


import json
import numpy as np
import os
import sys
import signal
import subprocess
import time
import shlex
import platform
import xml.etree.ElementTree as ET
import pandas as pd

work_dirx = os.path.dirname(os.path.abspath(__file__))
# c_work_dir = os.path.join(work_dirx, 'in.lammps')
from pathlib import Path
curr_dir=Path(os.path.dirname(os.path.abspath(__file__)))
two_dir_up_=os.fspath(Path(curr_dir.parent.parent).resolve())
convection_2d_input = sys.argv[1]
c_path = sys.argv[2]

# $machine_name    '$run_command'   $convection_2d_exec

import shutil
import tempfile
from ruamel.yaml import YAML
from pathlib import Path

# with open(lmp_input, "r") as f:

if __name__ == '__main__':
    try:
        commandstring = ''

        for arg in sys.argv[3:]:  # skip sys.argv[0] since the question didn't ask for it
            if ' ' in arg:
                commandstring += '"{}"  '.format(arg)  # Put the quotes back in

            else:
                commandstring += "{}  ".format(arg)


        conv_exec = commandstring.split(sep=',').pop(2)
        conv_exec = conv_exec.replace("'", "").strip().replace("]", "")

        run_command = commandstring.split(sep=',').pop(1)
        run_command = run_command.replace("'", "").strip()
        run_command = run_command.split()

        string = conv_exec
        run_command.append(string)

        print("checking run_command", run_command)
    except:
        print("system error, terminating!")
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)

    return_code = -1
    try:
        print("Executing easyvvuq with FabNEPTUNE ...")
        # work_dirx = os.path.dirname(os.path.abspath(__file__))
        first = os.listdir('..')[0]
        sec = os.listdir('../..')[0]
        lm1 = c_path + '/' + str(sec) + '/' + str(first) + '/'
        px = os.listdir(two_dir_up_)
        pv = c_path + '/' + str(sec) + '/' + str(first) + '/output.csv'
        pep1x = work_dirx + '/convection_2d_mesh.xml'
        pep2x = c_path + '/' + str(sec) + '/' + str(first) + '/convection_2d_mesh.xml'
        # shutil.copy(os.path.join(pep1x), os.path.join(pep2x))

        c_work_dir = os.path.join(lm1, conv_exec)

        run_command.append(convection_2d_input)
        run_command.append(pep1x)
        print("run_command", run_command)
        process = subprocess.Popen(run_command,
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)

        while True:
            output = process.stdout.readline()
            print(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                print('RETURN CODE', return_code)
                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    print(output.strip())
                break
    except:
        print("system/file error, terminating!")
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)

    try:
        output_filename = 'out_file.csv'
        left_txt = pd.read_csv('NusseltTest1L.fce', skiprows=4)
        left_txt = np.array(left_txt)
        all = []
        for k in range(len(left_txt)):
            commandstring = ''
            for arg in left_txt[k]:
                if ' ' in arg:
                    commandstring += '"{}"  '.format(arg)

                else:
                    commandstring += "{}  ".format(arg)

            X = []
            X.append(k)
            for i in range(7):
                X.append(eval(commandstring.strip().split().pop(i + 1).strip().replace('"', "")))
            all.append(X)
        np.savetxt("output_NusseltL.csv", all, delimiter=",")
        columns_L = ['index', 'Time', 'F1-press_L', 'F1-visc_L', 'F1-total_L', 'F2-press_L', 'F2-visc_L', 'F2-total_L']
        CSV_Filex = pd.read_csv('output_NusseltL.csv', quotechar="'", names=columns_L)
        CSV_Filex.to_csv('output_NusseltL.csv',
                         index=None)
        print('output_NusseltL with header to csv ...')

        rt_txt = pd.read_csv('NusseltTest1R.fce', skiprows=4)
        rt_txt = np.array(rt_txt)
        all = []
        for k in range(len(rt_txt)):
            commandstring = ''
            for arg in rt_txt[k]:
                if ' ' in arg:
                    commandstring += '"{}"  '.format(arg)

                else:
                    commandstring += "{}  ".format(arg)

            X = []
            X.append(k)
            for i in range(7):
                X.append(eval(commandstring.strip().split().pop(i + 1).strip().replace('"', "")))
            all.append(X)

        np.savetxt("output_NusseltR.csv", all, delimiter=",")
        columns_R = ['index', 'Time', 'F1-pres_R', 'F1-visc_R', 'F1-total_R', 'F2-press_R', 'F2-visc_R', 'F2-total_R']
        CSV_Filex = pd.read_csv('output_NusseltR.csv', quotechar="'", names=columns_R)
        CSV_Filex.to_csv('output_NusseltR.csv',
                         index=None)
        print('output_NusseltR with header to csv ...')
        columns_to_be_removed1 = ['Time']
        # output1_path = c_path + '/' + str(sec) + '/' + str(first) + '/output1.csv'
        datax = pd.read_csv('output_NusseltR.csv').drop(columns_to_be_removed1, axis='columns')
        datax.to_csv('output_NusseltR.csv',
                     index=None)
    except:
        print("system/file error, terminating!")
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)

    try:
        print('combining NusseltR and NusseltL ...')
        data1 = pd.read_csv('output_NusseltL.csv').fillna(0.0)
        data2 = pd.read_csv('output_NusseltR.csv').fillna(0.0)
        columnsf = ['index', 'Time', 'F1-press_L', 'F1-visc_L', 'F1-total_L', 'F2-press_L', 'F2-visc_L', 'F2-total_L',
                    'F1-pres_R', 'F1-visc_R', 'F1-total_R', 'F2-press_R', 'F2-visc_R', 'F2-total_R']
        output3 = pd.merge(data1, data2, on='index', how='right')
        output3.to_csv('output.csv', index=False, header=False)
        # result_path = c_path + '/' + str(sec) + '/' + str(first) + '/result.csv'
        print('writing final results ...')
        my_File = pd.read_csv('output.csv', quotechar="'", names=columnsf)
        my_File.to_csv('output.csv',
                       index=None)

        # // all removed except one
        columnsfrem = ['index', 'Time']
        # output1_path = c_path + '/' + str(sec) + '/' + str(first) + '/output1.csv'
        datax = pd.read_csv('output.csv').drop(columnsfrem, axis='columns')
        datax.to_csv('output.csv',
                 index=None)


    except:
        print("system/file error, terminating!")
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)
