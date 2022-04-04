#!/usr/bin/env python3


import json
import numpy as np
import os
import sys
import signal
import subprocess
import time
import platform
import xml.etree.ElementTree as ET
import pandas as pd

work_dirx = os.path.dirname(os.path.abspath(__file__))

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
                        X.append(eval(commandstring.strip().split().pop(i+1).strip().replace('"', "")))
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
                        X.append(eval(commandstring.strip().split().pop(i+1).strip().replace('"', "")))
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
        # columnsr = ['index', 'stress_01_macro', 'stress_02_macro', 'stress_11_macro', 'stress_12_macro',
        #             'stress_22_macro', 'stress_01_nano', 'stress_02_nano', 'stress_11_nano',
        #             'stress_12_nano',
        #             'stress_22_nano']
        # columnsr = ['index']
        output3 = pd.merge(data1, data2, on='index', how='right')
        output3.to_csv('output.csv', index=False, header=False)
        # result_path = c_path + '/' + str(sec) + '/' + str(first) + '/result.csv'
        print('writing final results ...')
        my_File = pd.read_csv('output.csv', quotechar="'", names=columnsf)
        my_File.to_csv('output.csv',
                       index=None)
        # data_macrox = pd.read_csv('output.csv').drop(columnsr, axis='columns')
        # data_macrox.to_csv('output.csv',
        #                    index=None, header=False)
        # cols = ['stress_00_macro', 'stress_01_macro', 'stress_02_macro', 'stress_11_macro', 'stress_12_macro',
        #         'stress_22_macro', 'stress_00_nano', 'stress_01_nano', 'stress_02_nano', 'stress_11_nano',
        #         'stress_12_nano', 'stress_22_nano']
        # CSV_Fileyy = pd.read_csv('output.csv', quotechar="'", names=cols).fillna(0.0)
        # CSV_Fileyy.to_csv('output.csv',
        #                   index=None)

except:
        print("system/file error, terminating!")
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)