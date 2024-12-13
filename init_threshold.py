import os
from neuron import h
from neuron.units import mV,V,m,um,ms
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import csv

h.load_file("stdrun.hoc")# Get the directory of the current script
currdir = os.getcwd()

# Load Mechanisms
path = os.path.join(currdir, "mechanisms", "nrnmech.dll")
print(path)
h.nrn_load_dll(path)

# Import functions
import functions.stim as stim
import functions.calcrx as calcrx
import functions.savedata as savedata
import functions.all_voltages as all_voltages
import functions.record_voltages_gpt as record_voltages_gpt
import functions.HH_minimal_cells as HHcells
import functions.savedata as savedata

#Local Field Potential calculation
h.load_file("./functions/field.hoc")

def init_cell(run_id,cell_id,v_plate,distance,field_orientation,ref_point):
    if cell_id==1:
        cell=HHcells.Fast_Spiking(0,0,0,0,0,0)
    elif cell_id==2:
        cell=HHcells.Intrinsic_Bursting(0,0,0,0,0,0)
    elif cell_id==3:
        cell=HHcells.Repetitive_Bursting(0,0,0,0,0,0)
    elif cell_id==4:
        cell=HHcells.Low_Threshold(0,0,0,0,0,0)
    elif cell_id==5:
        cell=HHcells.Regular_Spiking(0,0,0,0,0,0)
    
    cell_name=cell.name

    # After Cell is created
    h.load_file("./functions/interpxyz.hoc")
    h.load_file("./functions/setpointers.hoc")
    field_orientation=np.array(field_orientation)
    calcrx.set_uniform_field_between_plates(v_plate,distance,field_orientation,ref_point)

    return cell, cell_name

def setstim(simtime,dt,ton,amp,depth,dur,freq,modfreq):
    time,stim1=stim.ampmodulation(ton,amp,depth,dt,dur,simtime,freq,modfreq)
    return time,stim1

def restore_steady_state(cell_id):
    currdir=os.getcwd()
    path = os.path.join(currdir, f"data\\{cell_id}\\threshold\\steady_state\\steady_state.bin")
    savestate = h.SaveState()
    h_file = h.File(path)
    print(f"{path}")
    savestate.fread(h_file)
    savestate.restore(1)
    h.fcurrent()  # Synchronize restored state
    h.t = 0               # Reset simulation time to 0
    h.tstop = 0.1         # Run a very brief simulation
    h.continuerun(h.tstop)  # Allow NEURON to stabilize
    h.t = 0
    print(f"Steady state restored from {path}, and time reset to {h.t} ms")

def get_results(top_dir):
    top_file=os.path.join(top_dir, "results_summary.csv")
    results_df=pd.read_csv(top_file)
    return results_df

def get_max_segs(top_dir,cell):
    results_df=get_results(top_dir)
    maxp_seg=results_df["maxp_seg"].to_list()
    segslist=[]
    for seg in maxp_seg:
        if seg not in segslist:
            segslist.append(seg)

    def get_segments(segslist):
        segments=[]
        for seg in segslist:
            # Parse the string
            section_name = seg.split('(')[0]  # Extract "Fast Spiking[0].dend"             
            segment_loc = float(seg.split('(')[1].split(')')[0])  # Example: 0.5
            # Loop through all sections in the cell
            for sec in cell.all:  # Assuming `cell.all` is a list of all sections
                print (sec.name())
                if sec.name() == section_name:
                    # Access the segment
                    segment=sec(segment_loc)    
                    segments.append(segment)
                    print(segment)
        print(segments)
        return segments
    
    segments=get_segments(segslist)
    return segments

def setup_apcs(top_dir,cell):
    segments=get_max_segs(top_dir,cell)
    APCounters=[]
    for segment in segments:
        ap_counter = h.APCount(segment)  # Use parentheses, not square brackets
        APCounters.append(ap_counter)
    
    print(APCounters)
    return segments,APCounters


def initialize(run_id,cell_id,v_plate,distance,field_orientation,ref_point,top_dir):
    print("Init cell")
    cell, cell_name=init_cell(run_id,cell_id,v_plate,distance,field_orientation,ref_point)
    print("Init APCs")
    segments,APCounters=setup_apcs(top_dir,cell)
    print("Simulation Initialized")
    return APCounters,cell

def threshsearch(cell_id,cell,simtime,dt,ton,amp,depth,dur,freq,modfreq,APCounters,thresh=0):
    time,stim1= setstim(simtime,dt,ton,amp,depth,dur,freq,modfreq)

    print(f"Set stim with amplitude: {amp} V/m")
    h.finitialize(cell.v_init)
    restore_steady_state(cell_id)

    h.dt = dt
    h.tstop = simtime
    h.celsius = 36


    for apc in APCounters:
        apc.thresh=thresh

    print(f"Continue Run {simtime}")
    h.continuerun(simtime)
     
    print([apc.n for apc in APCounters])
    any1=any(apc.n>0 for apc in APCounters)
    print(any1)
    return any1

def threshold(cell_id, simtime, v_plate, distance, field_orientation, ref_point, dt, amp, depth, freq, modfreq, ton, dur, run_id, top_dir, thresh=0):
    low = 0
    high = 1e6
    APCounters, cell = initialize(run_id, cell_id, v_plate, distance, field_orientation, ref_point, top_dir)

    # Set a reasonable starting amplitude if none provided
    if amp == 0: 
        amp = 50

    # Phase 1: Find an upper bound (high) and lower bound (low) where spiking behavior changes
    while low == 0 or high == 1e6:
        print(f"Searching bounds: low={low}, high={high}, amp={amp}")

        if threshsearch(cell_id, cell, simtime, dt, ton, amp, depth, dur, freq, modfreq, APCounters, thresh):
            high = amp
            amp /= 2  # Reduce amplitude
        else:
            low = amp
            amp *= 2  # Increase amplitude

        # Stop the loop if stoprun_flag is True
        if h.stoprun == 1: 
            return amp
        
        # Prevent `amp` from exceeding a maximum reasonable value
        if amp > 1e7:
            print("Amplitude exceeded maximum allowable value. Exiting.")
            amp = None
            savethresh(amp, freq, cell_id)
            return amp

    # Phase 2: Perform binary search to refine the threshold
    epsilon = high * 1e-2  # Define acceptable resolution for the threshold
    amp = (high + low) / 2

    while (high - low) > epsilon:
        print(f"Binary search: low={low}, high={high}, amp={amp}")

        if threshsearch(cell_id, cell, simtime, dt, ton, amp, depth, dur, freq, modfreq, APCounters, thresh):
            high = amp
        else:
            low = amp

        amp = (high + low) / 2
        epsilon=amp*1e-2

        # Stop the loop if stoprun_flag is True
        if h.stoprun == 1: 
            break

    savethresh(high, freq, cell_id)
    print([apc.n for apc in APCounters])
    return high

def savethresh(amp,freq,cell_id):
    currdir=os.getcwd()
    path = os.path.join(currdir, f"data\\{cell_id}\\threshold\\thresholds.csv")
    file_exists = os.path.exists(path)
     # Open the file in append mode
    with open(path, mode="a", newline="") as file:
        writer = csv.writer(file)
        # Write the header only if the file is new
        if not file_exists:
            writer.writerow(["Carrier_Frequency", "Threshold"])
        # Append the new data
        writer.writerow([freq, amp])
    print(amp)
    print(f"Threshold for frequency {freq} saved to {path}")