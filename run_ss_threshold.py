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

from init_steady import run_threshold
simtime=5000
dt=0.1
celsius=36
run_id=0
cell_id=1
theta=90
phi=0
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
ufield=True
coordinates=[0,0,0]
rho=100

threshold=1e-4
nc=True
record_all=False
time_before=1000
run_threshold(cell_id,theta,phi,ref_point,simtime,dt,ton,amp,depth,dur,freq,modfreq,
              top_dir,run_id,var,ramp,ramp_duration,tau,
              data_dir=data_dir,threshold=threshold,nc=nc,record_all=record_all,ufield=ufield,coordinates=coordinates,rho=rho,time_before=time_before)

