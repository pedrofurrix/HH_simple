import os
from neuron import h
from neuron.units import mV,V,m,um,ms
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import csv
import sys
from functions.low_pass import filter_data_threshold

h.load_file("stdrun.hoc")# Get the directory of the current script
currdir = os.getcwd()

# # Load Mechanisms
# path = os.path.join(currdir, "mechanisms", "nrnmech.dll")
# print(path)
# h.nrn_load_dll(path)

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

def init_cell(cell_id,theta,phi,ref_point,ufield=True,coordinates=None,rho=100):
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
    if ufield==True:
        calcrx.set_uniform_field_between_plates(theta,phi,ref_point)
    else:
        xe, ye, ze = coordinates
        calcrx.setelec(xe,ye,ze,rho)

    return cell, cell_name

def setstim(simtime,dt,ton,amp,depth,dur,freq,modfreq,ramp,ramp_duration,tau):
    time,stim1=stim.ampmodulation(ton,amp,depth,dt,dur,simtime,freq,modfreq,ramp,ramp_duration,tau)
    return time,stim1

def restore_steady_state(cell_id,var,data_dir):
    path = os.path.join(data_dir, "data",str(cell_id),str(var),"threshold","steady_state","steady_state.bin")
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


def add_callback(cell,cell_id,freq,modfreq,depth,theta,phi,segments,var,data_dir,save):
    from functions.all_voltages import custom_threshold
    folder,file,callback,voltages,finalize=custom_threshold(cell,cell_id,freq,modfreq,depth,theta,phi, segments,var,buffer_size=1000000,data_dir=data_dir,save=save,max_timesteps=1000000)
    return folder, file, callback,voltages, finalize




def setup_netcons(cell,record_all=False):
    if record_all:
        segments=[seg for sec in cell.all for seg in sec]
    else:
        segments=[cell.soma(0.5)]
    NCs=[]
    Recorders=[h.Vector() for seg in segments]
    for i,segment in enumerate(segments):
        netcon = h.NetCon(segment._ref_v,None)  # Use parentheses, not square brackets
        NCs.append(netcon)
        netcon.record(Recorders[i])
    return segments,NCs,Recorders

def threshsearch(cell_id,cell,simtime,theta,phi,dt,ton,amp,depth,dur,freq,modfreq,NCs,Recorders,segments,var,ramp,ramp_duration,tau,thresh=0,cb=False,save=True,data_dir=os.getcwd()):
    time,stim1= setstim(simtime,dt,ton,amp,depth,dur,freq,modfreq,ramp,ramp_duration,tau)

    print(f"Set stim with amplitude: {amp} V/m")
    h.finitialize(cell.v_init)
    restore_steady_state(cell_id,var,data_dir)
    h.celsius=36

    for nc in NCs:
        nc.threshold=thresh


    h.frecord_init()  
    h.dt = dt
    h.tstop = simtime
    h.celsius = 36
   
    if cb:
        print("Adding Callback")
        folder,file,callback,voltages,finalize=add_callback(cell,cell_id,freq,modfreq,depth,theta,phi,segments,var,data_dir,save)

    print(f"Continue Run {simtime}")
    h.continuerun(simtime)
    
    if cb:  
        file.close()

    if cb and save:
        finalize()

    minspikes=(simtime-(ramp_duration))/1000*modfreq
    num_spikes=[]

    for recorder in Recorders:
        spike_count=0
        spikes=recorder.to_python()
        if len(spikes) > 0:
            spike_count += 1  # Always count the first spike
            for i in range(1, len(spikes)):
                if spikes[i] - spikes[i-1] > 5:
                    spike_count += 1  # Count as new spike if time gap is large enough
        num_spikes.append(spike_count)

    if save:
        save_spiketimes(folder,Recorders,num_spikes,segments)

    any1=any(num>=minspikes for num in num_spikes)
    return any1
        
                    
def threshold(cell_id, simtime,theta,phi,
              ref_point, dt, amp, depth, freq, modfreq, ton, dur, 
                thresh=0,cb=False,var="cfreq",ramp=False,ramp_duration=0,tau=None,save=False,data_dir=os.getcwd(),record_all=False,ufield=True,coordinates=[0,0,0],rho=100):
    cell,cell_name=init_cell(cell_id,theta,phi,ref_point,ufield,coordinates,rho)
    low = 0
    high = 1e6
    segments,NCs,Recorders=setup_netcons(cell,record_all)

    # Set a reasonable starting amplitude if none provided
    if amp == 0: 
        amp = 50

    # Phase 1: Find an upper bound (high) and lower bound (low) where spiking behavior changes
    while low == 0 or high == 1e6:
        print(f"Searching bounds: low={low}, high={high}, amp={amp}")

        if threshsearch(cell_id, cell, theta,phi,simtime, dt, ton, amp, depth, dur, freq, modfreq, NCs,Recorders,segments,var,ramp,ramp_duration,tau,thresh=thresh,data_dir=data_dir):
        
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
    amp=(high+low)/2
    epsilon = amp*1e-2

    while (high - low) > epsilon:
        amp = (high + low)/2
        epsilon = amp*1e-2
        print(f"Binary search: low={low}, high={high}, amp={amp}")

        if threshsearch(cell_id, cell, simtime,theta,phi, dt, ton, amp, depth, dur, freq, modfreq, NCs,Recorders,segments,var,ramp,ramp_duration,tau,thresh=thresh,data_dir=data_dir):
            high = amp
        else:
            low = amp
        
        # ax,fig,title=plot_v(recordings,segments,freq,amp)


        # Stop the loop if stoprun_flag is True
        if h.stoprun == 1: 
            break
    
    final_amp=(high+low)/2
    cb=True
    save=True

    threshsearch(cell_id, cell, simtime, theta,phi,dt, ton, final_amp, depth, dur, freq, modfreq, NCs,Recorders,segments, var,ramp,ramp_duration,tau,cb=cb,save=save,thresh=thresh,data_dir=data_dir)
    # saveplot(title,fig,cell_id,var)
    savethresh(amp,freq,modfreq,depth,theta,phi,cell_id,var,data_dir)
    return amp

def savethresh(amp,freq,modfreq,depth,theta,phi,cell_id,var,data_dir):
    path = os.path.join(data_dir, "data",str(cell_id),str(var),"threshold","thresholds.csv")
    file_exists = os.path.exists(path)
    # Initialize a list to store the updated data
    updated_data = []
    condition_exists = False  # Flag to check if the frequency exists in the file
    mapping = {
    "cfreq": freq,
    "modfreq": modfreq,
    "theta": theta,
    "phi": phi,
    "depth": depth
    }
    condition = mapping.get(var)  # Returns None if var is not in the dictionary
    # Check if the file exists
    if file_exists:
        # Read the existing file
        with open(path, mode="r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Read the header (if it exists)
            
            # Add the header to updated_data
            if header:
                updated_data.append(header)

            # Iterate through the rows and update the amp value if the freq matches
            for row in reader:
                if len(row) >= 2 and row[0] == str(condition):  # Match the frequency
                    updated_data.append([condition, amp])  # Replace the amp value
                    condition_exists = True
                else:
                    updated_data.append(row)  # Keep the row unchanged
    # If the file doesn't exist, create it and add headers
    else:
        updated_data.append([var, "Threshold"])  # Add header to new file

     # If the frequency doesn't exist, add it as a new row
    if not condition_exists:
        if not updated_data: # If the file was empty, add the header
            updated_data.append([var, "Threshold"])
        updated_data.append([condition, amp])
    
    # Write the updated data back to the file
    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_data)  # Write all rows back to the file
    print(amp)
    print(f"Threshold for var:{var}={condition} saved to {path}")
    

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

def saveplot(title,fig_or_ax,cell_id,var,data_dir):
    filename=f"{title}.png"
    if isinstance(fig_or_ax, plt.Axes):
        # If it's an Axes object, get the Figure from the Axes
        fig = fig_or_ax.get_figure()
    elif isinstance(fig_or_ax, plt.Figure):
        # If it's already a Figure, use it as is
        fig = fig_or_ax
    else:
        raise TypeError("Input must be a matplotlib Figure or Axes object.")
    
    path=os.path.join(data_dir,"data",str(cell_id),str(var),"threshold",filename)

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

def save_apcs(folder,APCounters,segments):
    """
    Saves the APCounters and segments data into a JSON file.

    Parameters:
    - APCounters: A list or array of spike counts (number of spikes per segment).
    - segments: A list or array of segment identifiers (e.g., segment names or indices).
    - filename: The name of the file to save the data in (default is "spikes_data.json").
    """
    file=os.path.join(folder,"spikes_data.json")
     # Create a dictionary to store the data
    data = {}
    
    # Assuming APCounters and segments have the same length, pair them together
    for i in range(len(segments)):
        data[str(segments[i])] = APCounters[i].n
     # Save the data to a JSON file~

    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {file}")     

def save_spiketimes(folder,Recorders,num_spikes,segments):
    """
    Saves the APCounters and segments data into a JSON file.

    Parameters:
    - APCounters: A list or array of spike counts (number of spikes per segment).
    - segments: A list or array of segment identifiers (e.g., segment names or indices).
    - filename: The name of the file to save the data in (default is "spikes_data.json").
    """
    file=os.path.join(folder,"spike_times.json")
    file_number=os.path.join(folder,"spike_number.json")
     # Create a dictionary to store the data
    data = {}
    num={}
    # Assuming APCounters and segments have the same length, pair them together
    for i in range(len(segments)):
        times=Recorders[i].to_python()
        data[str(segments[i])] = times
        num[str(segments[i])]=num_spikes[i]
     # Save the data to a JSON file

    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    with open(file_number, 'w') as json_file:
        json.dump(num, json_file, indent=4)
    print(f"Data saved to {file}")     
