import os
from neuron import h
from neuron.units import mV,V,m,um,ms
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
h.load_file("stdrun.hoc")

currdir=os.getcwd()
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

    v_plate=v_plate*V #- potential difference between the plates
    distance=distance*m #distance
    field_orientation=np.array(field_orientation) 
    ref_point=ref_point #reference point with a 0 e_extracellular
    calcrx.set_uniform_field_between_plates(v_plate,distance,field_orientation,ref_point)

    return cell, cell_name

def setstim(simtime,dt,ton,amp,depth,dur,freq,modfreq,ramp,ramp_duration,tau):
    time,stim1=stim.ampmodulation(ton,amp,depth,dt,dur,simtime,freq,modfreq,ramp,ramp_duration,tau)
    return time,stim1

def get_steady_state(simtime,dt,celsius,run_id,cell_id,v_plate,distance,field_orientation,ref_point,ton,amp,depth,dur,freq,modfreq,ramp=False,ramp_duration=None,tau=None):
    cell, cell_name=init_cell(run_id,cell_id,v_plate,distance,field_orientation,ref_point)
    time,stim1=setstim(simtime,dt,ton,amp,depth,dur,freq,modfreq,ramp,ramp_duration,tau)

    t=h.Vector().record(h._ref_t)
    is_xtra=h.Vector().record(h._ref_is_xtra)
    soma_v=h.Vector().record(cell.soma(0.5)._ref_v)
    dend_v=h.Vector().record(cell.dend(0.5)._ref_v)
    vrec = h.Vector().record(h._ref_vrec)  # records vrec at each timestep

    h.celsius=celsius
    h.tstop=simtime
    h.dt=dt
    h.v_init=cell.v_init
    h.finitialize()

    # simparams=[dt,simtime,cell_id,cell_name]
    # stimparams=[v_plate,ton,dur,freq,depth,modfreq,field_orientation,amp,distance,ref_point]
    # freq_dir, e_dir = savedata.saveparams(run_id, simparams, stimparams)
    # savedata.save_es(freq_dir, amp, cell)

    # Check voltage at 1 point...
    
    def record_voltages():
        global voltages
        voltages=[seg.v for sec in cell.all for seg in sec]

    h.cvode.event(simtime-20, record_voltages)

    h.continuerun(simtime)

    final_v=[seg.v for sec in cell.all for seg in sec]
    seg=[seg for sec in cell.all for seg in sec]
    print(final_v)
    print(voltages)

    delta = [final-v for final,v in zip(final_v, voltages)]
    # Check steady_state one time point
    def steady_state_reached(threshold=1e-3):
        if abs(max(delta,key=abs)) >= threshold:
            return False
        return True
    
    threshold=1e-3
    steady_state=steady_state_reached(threshold)

    max_dif=max(delta,key=abs)

    #plot intracellular voltage over time
    fig,ax=plt.subplots()
    ax.plot(t,soma_v,label="soma")
    #ax.plot(t,dend_v,label="dend")
    #ax.plot(t,axon_v,label="axon")
    ax.set_xlabel("time(ms)")
    ax.set_ylabel("Membrane Voltage (mV)") #vint-vext~
    ax.legend()
    title1="Membrane Potential"

    plt.show()
    def saveparams(cell_id,simtime):
        #Create folder for run
        current_directory = os.getcwd()
        print(current_directory)

        folder_name=f"data\\{cell_id}\\steady_state"
        ssfolder = os.path.join(current_directory, folder_name,f"{simtime}")
        if not os.path.exists(ssfolder):
            os.makedirs(ssfolder)

        filename="params.json"
        path=os.path.join(ssfolder,filename)

        params = {"temperature" : h.celsius,
                    "dt": h.dt,  # in ms
                    "simtime": h.tstop,  # in ms
                    "v_init": h.v_init,  # in ms
                    "max_dif": max_dif,
                    "threshold" : threshold,
                    "reached_ss": steady_state
                }
        
        with open(path, "w") as file:
            json.dump(params, file, indent=4)  # Use indent=4 for readability
        print(f"Parameters saved to {path}")
    
        filev="voltages.csv"
        pathv=os.path.join(ssfolder,filev)
        data=pd.DataFrame({"seg_info":seg,"v_final":final_v,"v_20":voltages,"difference":delta})
        data.to_csv(pathv)
        print(f"Voltages saved to {pathv}")
        
        return ssfolder,folder_name

    ssfolder,folder_name=saveparams(cell_id,simtime)

    from functions.savedata import saveplot
    saveplot(ssfolder,title1,fig)

    def save_steady_state(folder_name,steady_state):
        savestate=h.SaveState()
        steady_state_file = "steady_state.bin" 
        path=os.path.join(folder_name,steady_state_file)

        if steady_state:
            savestate.save()
            h_file = h.File(path)  # Create an h.File object
            savestate.fwrite(h_file)           # Use fwrite with the h.File object
            h_file.close()                     # Close the file
            print(f"Steady state saved to {path}")

            filev="steady_voltages.csv"
            pathv=os.path.join(folder_name,filev)
            data=pd.DataFrame({"seg_info":seg,"v_init":final_v})
            data.to_csv(pathv)
            print(f"Voltages saved to {pathv}")


    save_steady_state(folder_name,steady_state)

    folder=f"data\\{cell_id}"
    savedata.savelocations_xtra(folder,cell)
    savedata.save_locations(folder,cell)



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
            print(seg)

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
        ap_counter = h.APCount(segment) 
        APCounters.append(ap_counter)
    print(APCounters)

    recordings=[]
    # t=h.Vector().record(h._ref_t)
    # is_xtra=h.Vector().record(h._ref_is_xtra)
    # recordings.extend([t,is_xtra])
    # for segment in segments:
    #     rec=h.Vector().record(segment._ref_v)
    #     recordings.append(rec)
    return segments,APCounters,recordings


def run_threshold(cell_id,v_plate,distance,field_orientation,ref_point,simtime,dt,ton,amp,depth,dur,freq,modfreq,top_dir,run_id,var="cfreq",ramp=False,ramp_duration=0,tau=None):
    cell,cell_name=init_cell(run_id,cell_id,v_plate,distance,field_orientation,ref_point)
    time,stim1=setstim(simtime,dt,ton,amp,depth,dur,freq,modfreq,ramp,ramp_duration,tau)
    segments,APCounters,recordings=setup_apcs(top_dir,cell)

    h.dt = dt
    h.tstop = simtime
    h.celsius = 37
    h.v_init=cell.v_init

    h.finitialize()
    
    def record_voltages():
        global voltages
        voltages=[seg.v for sec in cell.all for seg in sec]

    h.cvode.event(simtime-20, record_voltages)

    h.continuerun(simtime)

    final_v=[seg.v for sec in cell.all for seg in sec]
    seg=[seg for sec in cell.all for seg in sec]

    delta = [final-v for final,v in zip(final_v, voltages)]
    # Check steady_state one time point
    def steady_state_reached(threshold=1e-3):
        if abs(max(delta,key=abs)) >= threshold:
            return False
        return True
    
    threshold=1e-3
    steady_state=steady_state_reached(threshold)

    max_dif=max(delta,key=abs)




    def saveparams(cell_id,simtime):
        #Create folder for run
        current_directory = os.getcwd()
        print(current_directory)

        folder_name=f"data\\{cell_id}\\{var}\\threshold\\steady_state"
        ssfolder = os.path.join(current_directory, folder_name,f"{simtime}")
        if not os.path.exists(ssfolder):
            os.makedirs(ssfolder)

        filename="params.json"
        path=os.path.join(ssfolder,filename)

        params = {"temperature" : h.celsius,
                    "dt": h.dt,  # in ms
                    "simtime": h.tstop,  # in ms
                    "v_init": h.v_init,  # in ms
                    "max_dif": max_dif,
                    "threshold" : threshold,
                    "reached_ss": steady_state
                }
        
        with open(path, "w") as file:
            json.dump(params, file, indent=4)  # Use indent=4 for readability
        print(f"Parameters saved to {path}")
    
        filev="voltages.csv"
        pathv=os.path.join(ssfolder,filev)
        data=pd.DataFrame({"seg_info":seg,"v_final":final_v,"v_20":voltages,"difference":delta})
        data.to_csv(pathv)
        print(f"Voltages saved to {pathv}")
        
        return ssfolder,folder_name
    def save_steady_state(folder_name,steady_state):
        savestate=h.SaveState()
        steady_state_file = "steady_state.bin" 
        path=os.path.join(folder_name,steady_state_file)

        if steady_state:
            savestate.save()
            h_file = h.File(path)  # Create an h.File object
            savestate.fwrite(h_file)           # Use fwrite with the h.File object
            h_file.close()                     # Close the file
            print(f"Steady state saved to {path}")

            filev="steady_voltages.csv"
            pathv=os.path.join(folder_name,filev)
            data=pd.DataFrame({"seg_info":seg,"v_init":final_v})
            data.to_csv(pathv)
            print(f"Voltages saved to {pathv}")

    ssfolder,folder_name=saveparams(cell_id,simtime)

    save_steady_state(folder_name,steady_state)



    
            