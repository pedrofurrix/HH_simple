import numpy as np
import os
import gc
from neuron import h


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)

from functions.csv_max_minshift import get_folder
CF=2000
E=10
cell_id=1
var="cfreq"
data_dir=os.getcwd()
top_dir,bot_dir,param_dir=get_folder(CF,E,cell_id,var,data_dir=data_dir)

from init_ss import run_threshold
simtime=5000
dt=0.1
celsius=36
run_id=0
cell_id=1
v_plate=1
distance=1
field_orientation=[1,0,0]
ref_point=[0,0,0]
ton=0
amp=0
depth=1
dur=simtime
freq=0
modfreq=0

ramp=True
ramp_duration=400
tau=0


run_threshold(cell_id,v_plate,distance,field_orientation,ref_point,simtime,dt,ton,amp,depth,dur,freq,modfreq,top_dir,run_id,var,ramp,ramp_duration,tau,data_dir=data_dir)

