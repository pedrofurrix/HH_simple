import numpy as np
import os
import gc
from neuron import h
import sys
import time


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

nc=True
if not nc:
    from init_threshold import threshold
else:
    from init_threshold_ncs import threshold


from functions.csv_max_minshift import get_folder
save_out=sys.stdout

cell_id=1
var="cfreq"

start=time.time()


pathf=os.path.join(os.getcwd(),"data",str(cell_id),str(var),"threshold")
if not os.path.exists(pathf):
    os.makedirs(pathf)
path=os.path.join(pathf,'output.log')
log_file = open(path, 'a')  # Use 'w' to overwrite or 'a' to append
sys.stdout = log_file
sys.stderr = log_file


amp=100
freq=1000
simtime=1000
dt=0.01
celsius=36


cell_id=1
theta=90
phi=0
ref_point=[0,0,0]
ton=0

depth=1
dur=simtime
modfreq=10
ramp=True
ramp_duration=400
tau=0
thresh=20
data_dir=os.getcwd()
record_all=False
ufield=True
coordinates=[0,0,0]
rho=100
cb=False

threshold(cell_id, simtime,theta, phi,ref_point, dt, amp, depth, freq, modfreq,ton,dur,
              thresh=thresh,cb=cb,var=var,ramp=ramp,ramp_duration=ramp_duration,tau=tau,data_dir=data_dir,ufield=ufield,coordinates=coordinates,rho=rho,record_all=record_all)
end=time.time()
print(f"The time of execution of above program is : {end-start} s")
print(f"The time of execution of above program is : {(end-start)/60} mins")

sys.stdout=save_out




