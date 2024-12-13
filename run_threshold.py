import numpy as np
import os
import gc
from neuron import h


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)
from functions.csv_max_minshift import get_folder
freq=100
E=10
cell_id=1
top_dir,bot_dir=get_folder(freq,E,cell_id)

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
amp=63
depth=1
dur=simtime
modfreq=10
thresh=0
threshold(cell_id, simtime,v_plate,distance,field_orientation,ref_point, dt, amp, depth, freq, modfreq,ton,dur,run_id,top_dir,thresh)

# Test run
# APCounters,cell=initialize(run_id,cell_id,v_plate,distance,field_orientation,ref_point,top_dir)
# apcs=threshsearch(cell_id,cell, simtime,dt,ton,amp,depth,dur,freq,modfreq,APCounters,thresh)
# print(apcs)