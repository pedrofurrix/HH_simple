import numpy as np
import os
import gc
from neuron import h
from itertools import product
from multiprocessing import Pool, cpu_count



from argparse import ArgumentParser

parser = ArgumentParser(description="Run NEURON simulations with specified parameters.")
parser.add_argument("-f", "--freq", type=float, nargs="*", required=True, help="Frequencies (Hz) for the simulations")
parser.add_argument("-v", "--voltage", type=float, nargs="*", required=True, help="Voltages (mV) for the simulations")
parser.add_argument("-d", "--depth", type=float, nargs="*", required=False,  default=1.0, help="Modulation depth (0-1)")
parser.add_argument("-m", "--modfreq", type=float, nargs="*", required=False,  default=10, help="Modulation Frequency (Hz)")
parser.add_argument("-b","--batch", action="store_true", help="Enable batch processing mode")



# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)
import init_stim

var="cfreq"
simtime=1500
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
# modfreq=10
ramp=True
ramp_duration=400
tau=0
data_dir=os.getcwd()

def run_simulation(params):
    freq, amp, modfreq, depth = params
    try:
        print(f"Running simulation for freq={freq}, amp={amp}, modfreq={modfreq}, depth={depth}")
        e_dir, t, is_xtra, vrec, soma_v, dend_v, cell = init_stim.run_sim(
            simtime, dt, celsius, run_id, cell_id, v_plate, distance,
            field_orientation, ref_point, ton, amp, depth, dur, freq, modfreq, var, ramp, ramp_duration, tau,data_dir
        )
        print(f"Simulation completed for freq={freq}, amp={amp}")
        init_stim.save_plots(e_dir, t, is_xtra, vrec, soma_v, dend_v)
    except Exception as e:
        print(f"Error during simulation for freq={freq}, amp={amp}: {e}")
    finally:
        h("forall delete_section()")  # Cleanup NEURON sections
        gc.collect()  # Force garbage collection
    

if __name__ == "__main__":
    # Parse arguments
    args = parser.parse_args()

    # Get values
    freqs = args.freq
    amps = args.voltage
    modfreq = args.modfreq
    depth = args.depth

    if args.batch:
        # Generate all combinations of (freq, amp)
        param_combinations = list(product(freqs, amps,modfreq,depth))

        # Add modfreq and depth to each combination
        # params = [(freq, amp, modfreq, depth) for freq, amp in param_combinations]
        params=param_combinations
        # Use multiprocessing
        maxnum_processes = cpu_count()  # Use all available cores
        num_processes=len(param_combinations)
        if num_processes>maxnum_processes:
            raise ValueError("Trying to run too many processes at once")

        with Pool(processes=num_processes) as pool:
            pool.map(run_simulation, params)

    else:
        # Run a single simulation
        if len(freqs) > 1 or len(amps) > 1:
            raise ValueError("Batch mode (--batch) must be enabled for multiple frequencies/voltages.")

        # Extract single values for freq and amp
        freq = freqs[0]
        amp = amps[0]

        run_simulation((freq, amp, modfreq, depth))