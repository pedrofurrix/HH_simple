import os
import numpy as np

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)

import ss_runfile
simtime=100
dt=0.1
celsius=36
run_id=0
cell_id=1
v_plate=40
distance=1
field_orientation=np.array([1,1,0])
ref_point=[0,0,0]
ton=0
amp=0
depth=1
dur=simtime
freq=0
modfreq=0


ss_runfile.get_steady_state(simtime,dt,celsius,run_id,cell_id,v_plate,distance,field_orientation,ref_point,ton,amp,depth,dur,freq,modfreq)