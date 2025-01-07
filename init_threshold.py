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
run = 0

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
    print(f"Getting steady state from {path}")
    savestate.fread(h_file)
    savestate.restore(1)
    h.fcurrent()  # Synchronize restored state
    h.t = 0               # Reset simulation time to 0
    h.tstop = 0.1         # Run a very brief simulation
    h.continuerun(h.tstop)  # Allow NEURON to stabilize
    h.t = 0
    print(f"Steady state restored from {path}, and time reset to {h.t} ms")


def add_callback(cell,cell_id,freq,segments):
    from functions.all_voltages import custom_threshold
    file,callback=custom_threshold(cell,cell_id,freq,segments)
    return file, callback


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
                # print (sec.name())
                if sec.name() == section_name:
                    # Access the segment
                    segment=sec(segment_loc)    
                    segments.append(segment)
                    # print(segment)
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

    recordings=[]
    # t=h.Vector().record(h._ref_t)
    # is_xtra=h.Vector().record(h._ref_is_xtra)
    # recordings.extend([t,is_xtra])
    # for segment in segments:
    #     rec=h.Vector().record(segment._ref_v)
    #     recordings.append(rec)

    return segments,APCounters, recordings


def initialize(run_id,cell_id,v_plate,distance,field_orientation,ref_point,top_dir,thresh,freq):
    print("Init cell")
    cell, cell_name=init_cell(run_id,cell_id,v_plate,distance,field_orientation,ref_point)
    print("Init APCs")
    segments,APCounters, recordings = setup_apcs(top_dir,cell)
    # recorders=[]
    for apc in APCounters:
        apc.thresh=thresh
        # rec=apc.record(h.Vector())
        # recorders.append(rec)

    # folder=f"data\\{cell_id}\\threshold\\{freq}Hz\\run_threshold.csv"
    # path=os.path.join(currdir,folder)
    # file1= open(path,'w',newline='')
    # writer2 = csv.writer(file1)
    # header= ["Run"] + [seg for seg in segments]
    # writer2.writerow(header)

    print("Simulation Initialized")
    return APCounters,cell,recordings,segments

def threshsearch(cell_id,cell,simtime,dt,ton,amp,depth,dur,freq,modfreq,APCounters,recordings,segments,cb):
    time,stim1= setstim(simtime,dt,ton,amp,depth,dur,freq,modfreq)

    print(f"Set stim with amplitude: {amp} V/m")
    h.finitialize(cell.v_init)
    restore_steady_state(cell_id)

    print("Before Stim")
    print(any(apc.n>0 for apc in APCounters))

    h.frecord_init()  
    h.dt = dt
    h.tstop = simtime
    h.celsius = 36
   
    if cb:
        print("Adding Callback")
        file,callback=add_callback(cell,cell_id,freq,segments)

    print(f"Continue Run {simtime}")
    h.continuerun(simtime)
    if cb:
        file.close()
        # get_maxv(cell_id,freq,segments,writer2)

    print([apc.n for apc in APCounters])
    any1=any(apc.n>0 for apc in APCounters)
    print(any1)
    print([apc.time for apc in APCounters])

    # ax,fig,title=plot_v(recordings,segments,freq,amp)
    return any1

def threshold(cell_id, simtime, v_plate, distance, field_orientation, ref_point, dt, amp, depth, freq, modfreq, ton, dur, run_id, top_dir, thresh=0,cb=False):
    low = 0
    high = 1e6
    APCounters, cell,recordings,segments = initialize(run_id, cell_id, v_plate, distance, field_orientation, ref_point, top_dir,thresh,freq)
    
    # Set a reasonable starting amplitude if none provided
    if amp == 0: 
        amp = 50

    # Phase 1: Find an upper bound (high) and lower bound (low) where spiking behavior changes
    while low == 0 or high == 1e6:
        print(f"Searching bounds: low={low}, high={high}, amp={amp}")

        if threshsearch(cell_id, cell, simtime, dt, ton, amp, depth, dur, freq, modfreq, APCounters,recordings,segments,cb):
            high = amp
            amp /= 2  # Reduce amplitude
        else:
            low = amp
            amp *= 2  # Increase amplitude
        
        # ax,fig,title=plot_v(recordings,segments,freq,amp)

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

        if threshsearch(cell_id, cell, simtime, dt, ton, amp, depth, dur, freq, modfreq, APCounters,recordings,segments,cb):
            high = amp
        else:
            low = amp
        
        # ax,fig,title=plot_v(recordings,segments,freq,amp)

        amp = (high + low) / 2
        epsilon=amp*1e-2

        # Stop the loop if stoprun_flag is True
        if h.stoprun == 1: 
            break
    
    cb=True
    threshsearch(cell_id, cell, simtime, dt, ton, amp, depth, dur, freq, modfreq, APCounters,recordings,segments,cb)
    # saveplot(title,fig,cell_id)
    savethresh(amp, freq, cell_id)
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
    

def plot_v(recordings,segments,freq,amp):
    fig,ax=plt.subplots()
    for i in range(len(segments)):
        ax.plot(recordings[0],recordings[i+2],label=segments[i])
    ax.set_xlabel("time(ms)")
    ax.set_ylabel("Membrane Potential")
    ax.legend()
    title1=f"Membrane Potential for CFreq= {freq} and Amp={amp}"
    ax.set_title(title1)
    plt.show()

    return ax,fig,title1

def saveplot(title,fig_or_ax,cell_id):
    filename=f"{title}.png"
    if isinstance(fig_or_ax, plt.Axes):
        # If it's an Axes object, get the Figure from the Axes
        fig = fig_or_ax.get_figure()
    elif isinstance(fig_or_ax, plt.Figure):
        # If it's already a Figure, use it as is
        fig = fig_or_ax
    else:
        raise TypeError("Input must be a matplotlib Figure or Axes object.")
    
    path=os.path.join(f"data\\{cell_id}\\threshold",filename)

    fig.savefig(path, dpi=300, bbox_inches='tight')
    print(f"Successfully saved as {filename}")

# def get_maxv(cell_id,freq,segments,writer2):
#     folder=f"data\\{cell_id}\\threshold\\{freq}Hz\\run_voltages.csv"
#     path=os.path.join(os.getcwd(),folder)
#     voltages=pd.read_csv(path)
#     max=[]
#     for seg in segments:
#        max_v=voltages[f"{seg}"].max
#        max.append(max_v)
#     print (f"Max values={max}")
#     global run
#     row=[run]+[max]
#     writer2.writerow(row)
#     run+=1
