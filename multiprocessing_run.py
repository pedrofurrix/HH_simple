from multiprocessing import Process,Pool, cpu_count
import os
from neuron import h
import gc
import time 
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)
import init_stim

start=time.time()

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
    var="test_multiprocessing"
    ramp=True
    ramp=True
    ramp_duration=400
    tau=0
    data_dir=os.getcwd()
    try:
        e_dir, t, is_xtra, vrec, soma_v, dend_v, cell = init_stim.run_sim(
        simtime, dt, celsius, run_id, cell_id, v_plate, distance,
        field_orientation, ref_point, ton, amp, depth, dur, freq, modfreq,var,ramp,ramp_duration,tau,data_dir)
        init_stim.save_plots(e_dir, t, is_xtra, vrec, soma_v, dend_v)
    except Exception as e:
        print(f"Error during simulation for freq={freq}, v_plate={amp}: {e}")
    finally:
        # Cleanup
        h("forall delete_section()")
        gc.collect()


if __name__ == '__main__':
    
    num_processes = cpu_count()

    v_values = [10, 20, 30, 50,100,200,300,500]
    CFreqs = [100]
    inputs = [(freq, amp) for freq in CFreqs for amp in v_values]
    # processes = []

    # for freq in CFreqs:
    #     for amp in v_values:
    #         p = Process(target=run_single_simulation, args=(freq, amp))
    #         p.start()
    #         processes.append(p)

    # for p in processes:
    #     p.join()
    # Use a Pool to parallelize simulations

    with Pool(processes=num_processes) as pool:
        # Run simulations in parallel
        pool.starmap(run_single_simulation, inputs)

end=time.time()
print(f"The time of execution of above program is : {end-start} s")
print(f"The time of execution of above program is : {(end-start)/60} mins")

