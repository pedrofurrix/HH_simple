import numpy as np
import os
import gc
from neuron import h
import sys




# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)


# Redirect stdout and stderr to a log file


# Load Mechanisms
currdir=os.getcwd()
path = os.path.join(currdir, "mechanisms", "nrnmech.dll")
print(path)
h.nrn_load_dll(path)

from functions.csv_max_minshift import get_folder
save_out=sys.stdout

def run_threshold(cell_id,freq,var):
    E=100
    
    top_dir,bot_dir=get_folder(freq,E,cell_id,var)
    path=os.path.join(os.getcwd(),"data",str(cell_id),str(var),"threshold",f"{freq}Hz",'output.log')
    log_file = open(path, 'a')  # Use 'w' to overwrite or 'a' to append
    sys.stdout = log_file
    sys.stderr = log_file

    from init_threshold import threshold,initialize,threshsearch

    simtime=1000
    dt=0.001
    celsius=36
    run_id=0
    cell_id=1
    v_plate=1
    distance=1
    field_orientation=[1,0,0]
    ref_point=[0,0,0]
    ton=0
    amp=100
    depth=1
    dur=simtime
    modfreq=10
    thresh=0
    cb=False

    ramp=False
    ramp_duration=0
    tau=0

    threshold(cell_id, simtime,v_plate,distance,field_orientation,ref_point, dt, amp, depth, freq, modfreq,ton,dur,run_id,top_dir,thresh,cb,var,ramp,ramp_duration,tau)
    sys.stdout=save_out

# Test run
# APCounters,cell=initialize(run_id,cell_id,v_plate,distance,field_orientation,ref_point,top_dir)
# apcs=threshsearch(cell_id,cell, simtime,dt,ton,amp,depth,dur,freq,modfreq,APCounters,thresh)
# print(apcs)

cell_id=1
run_threshold(cell_id,5000,"cfreq")

