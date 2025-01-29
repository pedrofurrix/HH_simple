import os
import h5py
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import json
from low_pass import butter_lowpass_filter,butter_bandpass_filter

def filter_and_save_voltages(bot_dir, highcut=100,order=4,lowcut=None,bp=False,modfreq=10):
    """
    Apply a low-pass filter to the voltages in an HDF5 file and save the filtered data to a new file.
    
    Args:
        input_dir (str): Directory containing the input HDF5 file.
        output_dir (str): Directory to save the filtered HDF5 file.
        cutoff_freq (float): Cutoff frequency for the low-pass filter (Hz).
        sampling_rate (float): Sampling frequency of the data (Hz).
    """
    # Load the input HDF5 file
    input_file = os.path.join(bot_dir, "run_voltages.h5")
    output_path = os.path.join(bot_dir,"filtered")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_file = os.path.join(output_path, f"filtered_voltages.h5")
    
    with h5py.File(input_file, "r") as infile, h5py.File(output_file, "w") as outfile:
        # Read time and voltages
        time = infile["time"][:]
        voltages = infile["voltages"][:]
        segment_names = infile["voltages"].attrs["segment_names"]
        dt=time[1]-time[0] #dt ms
        fs=1/(dt/1000) # Hz
        
        # Create datasets for filtered data
        num_timesteps, num_segments = voltages.shape
        filtered_voltages = outfile.create_dataset(
            "filtered_voltages",
            shape=(num_timesteps, num_segments),
            dtype="f",
            compression="gzip",
        )
        outfile.create_dataset("time", data=time, dtype="f")
        filtered_voltages.attrs["segment_names"] = segment_names
        
        # Apply the low-pass filter to each segment
        for i, segment_name in enumerate(segment_names):
            print(f"Filtering segment {segment_name} ({i+1}/{num_segments})...")
            if bp:
                v=voltages[:,i]-voltages[0,i]
                filtered_data=butter_bandpass_filter(v,fs,modfreq=modfreq,lowcut=lowcut,highcut=highcut,order=order)
            else:
                v=voltages[:,i]-voltages[0,i]
                filtered_data = butter_lowpass_filter(v, highcut, fs,order)
            filtered_voltages[:, i] = filtered_data
        
        print(f"Filtered data saved to {output_file}")
    save_filterparams(output_path,highcut,lowcut,order,bp)

def save_filterparams(output_dir,highcut,lowcut,order,bp):
    """
        Save filter parameters to a JSON file.
    
         rgs:
        output_dir (str): Directory to save the parameters file.
        filter_order (int): The order of the filter.
        cutoff_freq (float): The cutoff frequency of the filter.
    """
    # Define the file path for the parameters file
    params_file = os.path.join(output_dir, "filter_parameters.json")
    
    # Create a dictionary of parameters
    parameters = {
        "filter_order": order,
        "High Cut": highcut,
        "Low Cut": lowcut,
        "BandPass": bp,
          }
    
     # Save the dictionary to a JSON file
    with open(params_file, "w") as file:
        json.dump(parameters, file, indent=4)
    print(f"Filter parameters saved to {params_file}")

