import os
import numpy as np

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)

import init_steady as init_steady
simtime=1000
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
data_dir=os.getcwd()
ufield=True
coordinates=[0,0,0]
rho=100
time_before=1000
threshold=1e-4

init_steady.get_steady_state(simtime,dt,celsius,run_id,cell_id,theta,phi,ref_point,ton,amp,depth,dur,freq,modfreq,ramp,ramp_duration,tau,data_dir,ufield,coordinates,rho,threshold,time_before)
