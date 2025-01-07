import numpy as np
import os
import gc
from neuron import h
import pandas as pd
import matplotlib.pyplot as plt

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)

import functions.csv_max_minshift as csv_max_minshift
import functions.savedata as savedata

cell_id=1
freq=10000

print("wassup")


def get_voltages(cell_id,freq):
    folder=f"data\\{cell_id}\\threshold\\{freq}Hz"
    path=os.path.join(os.getcwd(),folder)
    file=os.path.join(path,"run_voltages.csv")
    print(file)
    voltages=pd.read_csv(file)
    return voltages,folder

def get_threshold(freq):
    folder=f"data\\{cell_id}\\threshold"
    path=os.path.join(os.getcwd(),folder)
    file=os.path.join(path,"thresholds.csv")
    thresholds=pd.read_csv(file)
    threshold=thresholds[thresholds["Carrier_Frequency"==int(freq)]]["Threshold"].to_list()
    return threshold

def get_maxv(cell_id,freq):
    voltages,folder=get_voltages(cell_id,freq)
    max_v = voltages.iloc[:, 1:].max().tolist()  # Returns a list of maximum values per segment
    threshold=get_threshold(freq)
    # threshold=1656.25
    print(max_v)

    headers=voltages.drop(columns=["t","is_xtra"]).columns.to_list()
    fig,ax=plt.subplots()

    time=voltages.iloc[:,0].to_list()
    is_xtra=voltages["is_xtra"].to_list()
    for val in headers:
        v=voltages[val].to_list()
        ax.plot(time,v,label=val)

    

    # ax.plot(time,is_xtra,label="is_xtra")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Membrane Potential (mV)")
    ax.legend()
    title=f"Membrane potential for E={threshold[-1]} V_m"
    ax.set_title(title)
    plt.show()

    savedata.saveplot(folder,title,fig)
    
    fig1,ax1=plt.subplots()
    ax1.plot(time,is_xtra)
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Stimulation (V/m)")
    title1="Stimulation_Vm"
    ax1.set_title(title1)
    plt.show()
    savedata.saveplot(folder,title1,fig1)


    return max_v

max_v=get_maxv(cell_id,freq)

