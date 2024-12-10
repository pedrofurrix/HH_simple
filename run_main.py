import numpy as np
import os
import gc
from neuron import h

from argparse import ArgumentParser


# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)
import init_stim

# v_values=[10,20,30,50,100,150,200,300,400,500,700,1000]
# CFreqs=[100,500,1000,2000,3000,5000,10000,20000,30000,40000,50000]

parser = ArgumentParser(description="Run a NEURON simulation with specified parameters.")
parser.add_argument("-f", "--freq", type=float, required=True, help="Frequency (Hz) for the simulation")
parser.add_argument("-v", "--voltage", type=float, required=True, help="Voltage (mV) for the simulation")

args = parser.parse_args()


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
# amp=1
depth=1
dur=simtime
# freq=500
modfreq=10

# Get command-line arguments
freq = args.freq
amp = args.voltage

# for freq in CFreqs:
#     for amp in v_values:

try:
    print(f"Running simulation for freq={freq}, v_plate={amp}")
    e_dir, t, is_xtra, vrec, soma_v, dend_v, cell = init_stim.run_sim(
        simtime, dt, celsius, run_id, cell_id, v_plate, distance,
        field_orientation, ref_point, ton, amp, depth, dur, freq, modfreq)
    print(f"Simulation completed for freq={freq}, v_plate={amp}")
    init_stim.save_plots(e_dir, t, is_xtra, vrec, soma_v, dend_v)
except Exception as e:
    print(f"Error during simulation for freq={freq}, v_plate={amp}: {e}")
finally:
    # Cleanup to free resources
    h("forall delete_section()")  # Delete all sections
    gc.collect()  # Force garbage collection
    
    