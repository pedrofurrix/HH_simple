import os
from neuron import h
from neuron.units import mV,V,m,um,ms
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import gc
h.load_file("stdrun.hoc")

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)

currdir = os.getcwd()# Get the directory of the current script

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

def setstim(simtime,dt,ton,amp,depth,dur,freq,modfreq,ramp,ramp_duration,tau):
    time,stim1=stim.ampmodulation(ton,amp,depth,dt,dur,simtime,freq,modfreq,ramp,ramp_duration,tau)
    return time,stim1

def restore_steady_state(cell_id):
    currdir=os.getcwd()
    path = os.path.join(currdir, f"data\\{cell_id}\\steady_state\\steady_state.bin")
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

def run_sim(simtime,dt,celsius,run_id,cell_id,v_plate,distance,field_orientation,ref_point,ton,amp,depth,dur,freq,modfreq,var,ramp=False,ramp_duration=None,tau=None):
    
    print("Init cell")
    cell, cell_name=init_cell(run_id,cell_id,v_plate,distance,field_orientation,ref_point)

    print("Init setting stim")
    time,stim1=setstim(simtime,dt,ton,amp,depth,dur,freq,modfreq,ramp,ramp_duration,tau)

    t=h.Vector().record(h._ref_t)
    is_xtra=h.Vector().record(h._ref_is_xtra)
    soma_v=h.Vector().record(cell.soma(0.5)._ref_v)
    dend_v=h.Vector().record(cell.dend(0.5)._ref_v)
    vrec = h.Vector().record(h._ref_vrec)  # records vrec at each timestep
    
    print("Finitialize")
    h.finitialize(cell.v_init)

    # print("Restore steady state")
    restore_steady_state(cell_id)

    h.frecord_init()
    h.dt = dt
    h.tstop = simtime
    h.celsius = 36

    simparams=[dt,simtime,cell_id,cell_name]
    stimparams=[v_plate,ton,dur,freq,depth,modfreq,field_orientation,amp,distance,ref_point]

    freq_dir, e_dir = savedata.saveparams(run_id, simparams, stimparams,var)
    savedata.save_rx(freq_dir, v_plate,amp, cell)
    # file, callback = all_voltages.record_voltages(cell, e_dir)
    # file,callback=record_voltages_gpt.record_voltages_hdf5(cell,e_dir)

    max_timesteps=int(simtime/dt)
    buffer_size=10000
    file, callback, finalize=record_voltages_gpt.record_voltages_hdf5(cell, e_dir,max_timesteps, buffer_size)
    # save_data,callback= record_voltages_gpt.record_voltages_numpy(cell, e_dir)

    print("Continuerun")
    h.continuerun(simtime)
    print(f"Voltages saved to {file}")
    finalize()
    # save_data()
    print(f"Simulation Finished\n")
    

    savedata.savedata(e_dir, t, is_xtra, vrec)
    print("Finished with success")

    return e_dir,t,is_xtra,vrec,soma_v,dend_v,cell


def save_plots(e_dir,t,is_xtra,vrec,soma_v,dend_v):
    fig1,ax1=plt.subplots()
    ax1.plot(t,soma_v,label="soma")
    ax1.plot(t,dend_v,label="dend")
    ax1.set_xlabel("time(ms)")
    ax1.set_ylabel("Membrane Voltage (mV)") #vint-vext~
    ax1.legend()
    title1="Membrane_Potential"
    ax1.set_title(title1)
    savedata.saveplot(e_dir,title1,fig1)

    fig2,ax2=plt.subplots()
    ax2.plot(t,is_xtra)
    ax2.set_xlabel("time(ms)")
    ax2.set_ylabel("IS_xtra")
    title2="Stimulation_current"
    ax2.set_title(title2)
    savedata.saveplot(e_dir,title2,fig2)

    fig3,ax3=plt.subplots()
    ax3.plot(t,vrec)
    ax3.set_xlabel("time(ms)")
    ax3.set_ylabel("vrec(uV)")
    title3="Recorded_Potential"
    ax3.set_title(title3)
    savedata.saveplot(e_dir,title3,fig3)





var="test_ramping"
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
amp=100
depth=1
dur=simtime
freq=100
modfreq=10
ramp=True
ramp_duration=50
tau=None




try:
    print(f"Running simulation for freq={freq}, v_plate={amp}")
    e_dir, t, is_xtra, vrec, soma_v, dend_v, cell = run_sim(
        simtime, dt, celsius, run_id, cell_id, v_plate, distance,
        field_orientation, ref_point, ton, amp, depth, dur, freq, modfreq,var,ramp,ramp_duration,tau)
    print(f"Simulation completed for freq={freq}, v_plate={amp}")
    save_plots(e_dir, t, is_xtra, vrec, soma_v, dend_v)
except Exception as e:
    print(f"Error during simulation for freq={freq}, v_plate={amp}: {e}")
finally:
    # Cleanup to free resources
    h("forall delete_section()")  # Delete all sections
    gc.collect()  # Force garbage collection