from multiprocessing import Process
import os
from neuron import h
import gc

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)
import init_stim


def run_single_simulation(freq, amp):
    # Your simulation logic here
    # Replace the following with the actual simulation function call
    print(f"Running simulation for freq={freq}, amp={amp}")
    simtime = 1000
    dt = 0.001
    celsius = 36
    run_id = 0
    cell_id = 1
    v_plate = 1
    distance = 1
    field_orientation = [1, 0, 0]
    ref_point = [0, 0, 0]
    ton = 0
    depth = 1
    dur = simtime
    modfreq = 10
    try:
        e_dir, t, is_xtra, vrec, soma_v, dend_v, cell = init_stim.run_sim(
            simtime, dt, celsius, run_id, cell_id, v_plate, distance,
            field_orientation, ref_point, ton, amp, depth, dur, freq, modfreq)
        init_stim.save_plots(e_dir, t, is_xtra, vrec, soma_v, dend_v)
    except Exception as e:
        print(f"Error during simulation for freq={freq}, v_plate={amp}: {e}")
    finally:
        # Cleanup
        h("forall delete_section()")
        gc.collect()

if __name__ == '__main__':
    

    v_values = [10, 20, 30, 50, 100, 150, 200, 300, 400, 500, 700, 1000]
    CFreqs = [100, 500, 1000, 2000, 3000, 5000, 10000, 20000, 30000, 40000, 50000]

    processes = []

    for freq in CFreqs:
        for amp in v_values:
            p = Process(target=run_single_simulation, args=(freq, amp))
            p.start()
            processes.append(p)

    for p in processes:
        p.join()