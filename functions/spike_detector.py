import os
import pandas as pd
import h5py
import pickle
from .csv_max_minshift import load_voltages_hdf5,load_params,get_folder
import json



def spike_detector(bot_dir,param_dir,filtered=False,threshold=0):
    '''
    Voltages is a pd dataframe with the columns as the membrane potential for each segment and the rows being this potential over time
    '''
    voltages=load_voltages_hdf5(bot_dir,filtered)
    simparams, stimparams=load_params(param_dir)

    columns=list(voltages) # List of dataframe columns
    time=voltages[columns[0]].to_list() # Time values
    timesteps=len(time)
    spikedata={seg: [] for seg in columns[1:]}  

    for seg in columns[1:]: # Loop through timesteps
        v_values=voltages[seg].to_list()
        for i in range(timesteps-1):
            # Detect threshold crossing: voltage crosses the threshold upwards
            if v_values[i+1]>=threshold and v_values[i]<=threshold:
                spikedata[seg].append(time[i+1])


    total_spikes = sum(len(spike_times) for spike_times in spikedata.values())
    most_spikes_segment = max(spikedata, key=lambda k: len(spikedata[k]))
    most_spikes_count = len(spikedata[most_spikes_segment])
    freqspikes=most_spikes_count/simparams["simtime"]*1000 #simtime in ms

    any_spikes = total_spikes > 0
    spikefolder=os.path.join(bot_dir,"spike_data")
    if not os.path.exists(spikefolder):
        os.makedirs(spikefolder)

    if most_spikes_count>1:
        spikes=spikedata[most_spikes_segment]
        isi=[spikes[i+1]-spikes[i] for i in range(most_spikes_count-1)]
        avg_isi=sum(isi)/len(isi)
    else:
        avg_isi=None
        isi=None


    if any_spikes==False:
        summary = {
        "any_spikes": any_spikes,
    }
    else:
        summary = {
        "any_spikes": any_spikes,
        "total_spikes": total_spikes,
        "most_spikes_segment": most_spikes_segment,
        "most_spikes_count": most_spikes_count,
        "spikes_per_segment": {seg: len(spike_times) for seg, spike_times in spikedata.items()},
        "Average_ISI_maxseg":avg_isi,
        "spikefreq":freqspikes
         }
        
        '''
        Choose one file format...
        '''
        # Save the spikedata dictionary to a Pickle file
        spikefile = os.path.join(spikefolder, "spiketimes.pkl")
        with open(spikefile, "wb") as f:
            pickle.dump(spikedata, f)
        print(f"Spike times saved to {spikefile}")

        # Save the spikedata dictionary to a JSON file
        spikefile = os.path.join(spikefolder, "spiketimes.json")
        with open(spikefile, "w") as f:
            json.dump(spikedata, f, indent=4)
        print(f"Spike times saved to {spikefile}")

    json_file=os.path.join(spikefolder,"spike_summary.json")
    with open(json_file, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"Spike summary saved to {json_file}")    
    return any_spikes


# freq_dir,e_dir=get_folder(100,10,1)
# spike_detector(e_dir)