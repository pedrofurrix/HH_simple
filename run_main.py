import numpy as np
import os
import gc
from neuron import h
import time

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)
import init_stim

start=time.time()

var="test_space"
simtime=1500
dt=0.001
celsius=36
run_id=0
cell_id=1
theta=90
phi=0
ref_point=[0,0,0]
ton=0
amp=15
depth=1
dur=simtime
freq=8000
modfreq=10
ramp=True
ramp_duration=400
tau=0
data_dir=os.getcwd()
ufield=True
coordinates=[0,0,0]
rho=100
try:
    print(f"Running simulation for freq={freq}, v_plate={amp}")
    e_dir, t, is_xtra, vrec, soma_v, dend_v, cell = init_stim.run_sim(
        simtime, dt, celsius, run_id, cell_id, theta,phi, ref_point, 
        ton, amp, depth, dur, freq, modfreq,var,ramp,ramp_duration,tau,data_dir=data_dir,ufield=ufield,coordinates=coordinates,rho=rho)
    print(f"Simulation completed for freq={freq}, v_plate={amp}")
    init_stim.save_plots(e_dir, t, is_xtra, vrec, soma_v, dend_v)
except Exception as e:
    print(f"Error during simulation for freq={freq}, v_plate={amp}: {e}")
finally:
    # Cleanup to free resources
    h("forall delete_section()")  # Delete all sections
    gc.collect()  # Force garbage collection

    
end=time.time()
print(f"The time of execution of above program is : {end-start} s")
print(f"The time of execution of above program is : {(end-start)/60} mins")