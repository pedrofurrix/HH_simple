from scipy.signal import butter, filtfilt,freqz,hilbert,lfilter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from .csv_max_minshift import get_folder,load_voltages_hdf5,load_params,load_voltages_csv
import os
from .savedata import saveplot
import json

# CF=100
# E=10
# cell_id=1



def get_results(freq_dir):
    path=os.path.join(freq_dir,"results_summary.csv")
    results=pd.read_csv(path)
    return results




def filter_data(CF,E,cell_id,cutoff=20,results=None,var="cfreq",order=2,save=True,plot=True,data_dir=os.getcwd()):
    freq_dir, e_dir,param_dir=get_folder(CF,E,cell_id,var,data_dir=data_dir)
    voltages=load_voltages_hdf5(e_dir)
    simparams, stimparams=load_params(param_dir)

    dt=simparams["dt"] # ms
    fs=1/(dt*1e-3) # Hz
    simtime=simparams["simtime"] # ms

    if results==None:
        results=get_results(freq_dir)
        maxpseg = results[results['EValue'] == E]['maxp_seg'].values[0]
        maxnseg = results[results['EValue'] == E]['maxn_seg'].values[0]
    else:
        maxpseg=results["maxp_seg"]
        maxnseg=results["maxn_seg"]

    print(f"maxpseg={maxpseg}")
    print(f"maxnseg={maxnseg}")
    t=voltages["t"].to_list()
    maxpvoltages = voltages[maxpseg].to_list()
    maxnvoltages = voltages[maxnseg].to_list()

    # print(f"Length of maxpvoltages: {len(maxpvoltages)}")
    # print(f"Length of maxnvoltages: {len(maxnvoltages)}")


    # print(f"Raw maxpvoltages: {maxpvoltages[:10]}")
    # Filtered hilbert
    analytic_p,envelope_p=hilbert_transform(maxpvoltages)
    filtered_maxp=butter_lowpass_filter(maxpvoltages, cutoff, fs, order)
    filtered_maxpenvelope=butter_lowpass_filter(envelope_p, cutoff, fs, order)

    print(f"Filtered maxpvoltages: {filtered_maxp[:10]}")
    analytic_n,envelope_n=hilbert_transform(maxnvoltages)
    filtered_maxn=butter_lowpass_filter(maxnvoltages, cutoff, fs,order)
    filtered_maxnenvelope=butter_lowpass_filter(envelope_n, cutoff, fs, order)

    filtered_file=os.path.join(e_dir,"filtered")
    if not os.path.exists(filtered_file):
        os.makedirs(filtered_file)

    if save:
        # Save the data
        data={
            "t":t,
            "maxpvoltages":maxpvoltages,
            "filtered_maxp":filtered_maxp,
            # Added these 3 after
            "analytic_p": analytic_p,
            "envelope_p":envelope_p,
            "filtered_maxpenvelope":filtered_maxpenvelope,
            "maxnvoltages":maxnvoltages,
            "filtered_maxn":filtered_maxn,
            # Added these 3 after
            "analytic_n": analytic_n,
            "envelope_n":envelope_n,
            "filtered_maxnenvelope":filtered_maxnenvelope,
        }
        out_file=os.path.join(filtered_file,f"filtered_data{order}.csv")
        data_pd=pd.DataFrame([data])
        data_pd.to_csv(out_file,index=False)
        print(f"Filtered data saved to {out_file}")

        # Save params
        params = {   
            "dt":dt,
            "simtime":simtime,
            "cutoff":cutoff,
            "fs":fs,
            "order":order
        }

        path=os.path.join(filtered_file,f"params{order}.json")
        with open(path, "w") as file:
            json.dump(params, file, indent=4)  # Use indent=4 for readability

        print(f"Parameters saved to {path}")

    if plot:
        plot_filtered(t,maxpseg,maxpvoltages,filtered_maxp,filtered_file,order,info="maxp",save=save)
        plot_filtered(t,maxnseg,maxnvoltages,filtered_maxn,filtered_file,order,info="maxn",save=save)
        plot_hilbert(t,maxpseg,maxpvoltages,envelope_p,filtered_maxpenvelope,filtered_file,order,info="maxp",save=save)
        plot_hilbert(t,maxnseg,maxnvoltages,envelope_n,filtered_maxnenvelope,filtered_file,order,info="maxn",save=save)
        plot_bode(cutoff, fs, order,filtered_file,save)
        plot_onlyfiltered(t,filtered_maxp,filtered_file,order,info="filter_maxp",save=save)

    return maxpvoltages,maxnvoltages,filtered_maxp,filtered_maxn,filtered_file,t


def plot_filtered(t,maxseg,maxvoltage,filteredv,file,order,info=None,save=False):
    fig,ax=plt.subplots()
    ax.plot(t,maxvoltage,label=f"Unfiltered")
    ax.plot(t,filteredv,label=f"Filtered")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Membrane Potential (mV)")
    ax.legend()
    title=f"Filtered response_{order}_{info}"
    ax.set_title(title)
    if not save:
        plt.show()
    else:
        saveplot(file,title,fig)    

def plot_hilbert(t,maxseg,maxvoltage,envelope,filtered_envelope,file,order,info=None,save=False):
    fig,ax=plt.subplots()
    ax.plot(t,maxvoltage,label=f"Unfiltered")
    ax.plot(t,envelope,label=f"Envelope")
    ax.plot(t,filtered_envelope,label=f"Filtered Envelope")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Membrane Potential (mV)")
    ax.legend()
    title=f"Hilbert Filtered response_{order}_{info}"
    ax.set_title(title)
    if not save:
        plt.show()
    else:
        saveplot(file,title,fig)    


def butter_lowpass_filter(data, cutoff, fs,order):
    """
    Applies a low-pass Butterworth filter.

    Parameters:
        data (array): The input signal.
        cutoff (float): The cutoff frequency of the filter (Hz).
        fs (float): The sampling frequency (Hz).
        order (int): The order of the filter.

    Returns:
        filtered_data (array): The filtered signal.
    """
    nyquist = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyquist  # Normalized cutoff frequency
    # Design the Butterworth filter
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    # Apply the filter using filtfilt (zero-phase filtering)
    filtered_data = filtfilt(b, a, data)
    print(f"Low pass filter of order:{order*2} and with a cutoff:{cutoff} applied to the data successfully")
    return filtered_data


def plot_bode(cutoff, fs, order,save_dir=None,save=False):
    """
    Plots the Bode magnitude and phase response of a Butterworth filter.

    Parameters:
        cutoff (float): The cutoff frequency of the filter (Hz).
        fs (float): The sampling frequency (Hz).
        order (int): The order of the filter.
    """
    nyquist = 0.5 * fs  # Nyquist frequency
    normal_cutoff = cutoff / nyquist  # Normalized cutoff frequency

    # Design the Butterworth filter
    b, a = butter(order, normal_cutoff, btype='low', analog=False)

    # Compute the frequency response
    w, h = freqz(b, a, worN=8000)  # `w` is frequency, `h` is the response

    # Convert from rad/sample to Hz
    freqs = w * fs / (2 * np.pi)

    # Magnitude plot
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].semilogx(freqs, 20 * np.log10(abs(h)), label=f"Cutoff: {cutoff} Hz")
    ax[0].set_title('Bode Plot')
    ax[0].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel('Magnitude (dB)')
    ax[0].grid(which='both', linestyle='--', linewidth=0.5)
    ax[0].legend()

    # Phase plot
    ax[1].semilogx(freqs, np.angle(h, deg=True), label=f"Order: {order}")
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Phase (Degrees)')
    ax[1].grid(which='both', linestyle='--', linewidth=0.5)
    ax[1].legend()

    plt.tight_layout()

    # Save the plot if a directory is provided
    if save_dir:
        if save:
            title = f"Bode_Plot_Cutoff_{cutoff}_Order_{order}"
            saveplot(save_dir, title, fig)
        else:
            plt.show() 

      
    print(f"Bode plot created for a {order}-order Butterworth filter with cutoff frequency {cutoff} Hz.")


def test_fake_data(dt=0.001, simtime=1000, noise_level=0.5,cfreq=100,modfreq=10,order=2,cutoff=20):
        
    """
    Generate fake membrane potential data for debugging.

    Parameters:
        dt (float): Time step in milliseconds.
        simtime (float): Total simulation time in milliseconds.
        noise_level (float): Amplitude of random noise to add to the signal.

    Returns:
        voltages (pd.DataFrame): Time and fake voltage data.
    """
    fs=1/(dt*1e-3) # Hz


    # Time vector: start=0, stop=simtime, step=dt
    t = np.arange(0, simtime, dt)
    
    # Simulated signal: a combination of sine waves + noise
    f1 = modfreq # Frequency of the main signal (Hz)
    f2 = cfreq  # Secondary frequency
    signal = -65 + 5 * np.sin(2 * np.pi * f1 * t / 1000) + 2 * np.sin(2 * np.pi * f2 * t / 1000)
    
    # Add random noise
    noise = np.random.normal(0, noise_level, size=len(t))
    voltages = signal + noise          

    filtered_data=butter_lowpass_filter(voltages, cutoff,fs,order)

    plt.plot()
    # Plot the original and filtered data
    plt.figure(figsize=(10, 6))
    plt.plot(t, voltages, label='Original Signal')
    plt.plot(t, filtered_data, label='Filtered Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Low-Pass Filtering Example')
    plt.legend()
    plt.grid(True)
    plt.show()


def hilbert_transform(signal):
    signal=np.array(signal)
    average=np.mean(signal)
    analytic_signal = hilbert(signal-average)
    envelope = np.abs(analytic_signal)+average
    return analytic_signal,envelope

def plot_onlyfiltered(t,filteredv,title=None,file=None,order=2,info=None,save=False,bp=False):
    fig,ax=plt.subplots()
    ax.plot(t,filteredv,label=f"Filtered")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Membrane Potential (mV)")
    ax.legend()
    if title is None:
        if not bp:
            title=f"Filtered response_{order*2}_{info}"
        else:
            title=f"BP Filtered_{order*2}_{info}"
    ax.set_title(title)
    if not save:
        plt.show()
    else:
        saveplot(file,title,fig)

def filter_data_threshold(voltages,dt,order,cell_id,var,freq,cutoff,amp,threshold=15,data_dir=os.getcwd()):

    folder=os.path.join(data_dir,"data",str(cell_id),str(var),"threshold",f"{freq}Hz")
    # voltages=load_voltages_csv(folder)
    fig,ax=plt.subplots()
    v=np.array(voltages)
    num_segments=np.len(v)
    spike_count=np.zeros(num_segments)
    for seg in range(num_segments):
        v=v[seg,:]-np.mean(v[seg])

        fs=1/(dt*1e-3) # Hz
        filtered=butter_lowpass_filter(v, cutoff, fs, order)

        t=np.linspace(0,1000,dt)
        title=f"Filtered response_{order}_{amp}Vm"
          
        for i in range(len(v)-1):
            if v[i-1]<=threshold and v[i]>threshold:
                spike_count[seg]+=1

        ax.plot(t,filtered,label=f"Filtered_{seg}")

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Membrane Potential (mV)")
    ax.legend()
    if title is None:
        title=f"Filtered response_{order}"

        ax.set_title(title)

    saveplot(folder,title,fig)



    return spike_count



def butter_bandpass(lowcut, highcut, fs, order=3):
    nyquist=0.5*fs
    low = lowcut / nyquist
    high = highcut / nyquist
    # Ensure frequencies are valid
    if not (0 < low < 1 and 0 < high < 1):
        raise ValueError(f"Cutoff frequencies must be within (0, Nyquist). Got low={lowcut}, high={highcut}, fs={fs}.")
    
    b,a=butter(order, [low, high], btype='band', analog=False)
    return b,a
    
def butter_bandpass_filter(signal, dt, modfreq=10,lowcut=None, highcut=None,order=3):
    fs=1/(dt/1000) #Hz
    if lowcut is None:
        lowcut=0.7*modfreq
    if highcut is None:
        highcut = 1.3 * modfreq
    
    b, a = butter_bandpass(lowcut, highcut, fs, order)

    #Add Padding
    pad_len = max(len(b), len(a)) * 3  # Safe padding
    padded_signal = np.pad(signal, (pad_len, pad_len), mode="reflect")
    filtered = filtfilt(b, a, padded_signal)[pad_len:-pad_len]
    # filtered = filtfilt(b, a, signal)
    # filtered = filtfilt(b, a, signal)
    return filtered

def plot_bode_bandpass(lowcut,highcut, fs, order=5,save_dir=None,save=False):
    """
    Plots the Bode magnitude and phase response of a Butterworth filter.

    Parameters:
        cutoff (float): The cutoff frequency of the filter (Hz).
        fs (float): The sampling frequency (Hz).
        order (int): The order of the filter.
    """
    order*=2
    nyquist = 0.5 * fs  # Nyquist frequency
    normal_cutoff = highcut / nyquist  # Normalized cutoff frequency

    # Design the Butterworth filter
    b, a = butter_bandpass(lowcut,highcut,fs,order)

    # Compute the frequency response
    w, h = freqz(b, a, worN=8000)  # `w` is frequency, `h` is the response

    # Convert from rad/sample to Hz
    freqs = w * fs / (2 * np.pi)

    # Magnitude plot
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    ax[0].semilogx(freqs, 20 * np.log10(abs(h)), label=f"Cutoff Hz")
    ax[0].set_title('Bode Plot')
    ax[0].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel('Magnitude (dB)')
    ax[0].grid(which='both', linestyle='--', linewidth=0.5)
    ax[0].legend()

    # Phase plot
    ax[1].semilogx(freqs, np.angle(h, deg=True), label=f"Order: {order}")
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Phase (Degrees)')
    ax[1].grid(which='both', linestyle='--', linewidth=0.5)
    ax[1].legend()

    plt.tight_layout()

    # Save the plot if a directory is provided
    if save_dir is not None:
        if save:
            title = f"Bode_Plot_Bandpass_{lowcut}_{highcut}_Order_{order}"
            saveplot(save_dir, title, fig)
        else:
            plt.show() 

      
    print(f"Bode plot created for a {order}-order Band-Pass Butterworth filter with HF {highcut} Hz and LF {lowcut} Hz.")

def simple_plot_bode_bp(fs,lowcut,highcut,freqlim=None,save_dir=None,save=False,order=None):
     # Sample rate and desired cutoff frequencies (in Hz).
    # fs = 1/(0.001/1000)

    fig, ax = plt.subplots()  # Create figure and axis objects
    
    # Loop through filter orders
    if order is None:
        for order in [3, 6, 9]:
            b, a = butter_bandpass(lowcut, highcut, fs, order=order)
            w, h = freqz(b, a, worN=2000)
            # Convert from rad/sample to Hz
            freqs = w * fs / (2 * np.pi)
            gain_db = 20 * np.log10(np.maximum(abs(h), 1e-10))  # Convert gain to dB
            # Plot the magnitude response
            ax.plot(freqs, gain_db, label=f"order = {order}")
    else:
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        w, h = freqz(b, a, worN=2000)
        # Convert from rad/sample to Hz
        freqs = w * fs / (2 * np.pi)
        gain_db = 20 * np.log10(np.maximum(abs(h), 1e-10))  # Convert gain to dB
        # Plot the magnitude response
        ax.plot(freqs, gain_db, label=f"order = {order}")

     # Set x-axis to logarithmic scale
    ax.set_xscale('log')
    if freqlim is not None:
        ax.set_xlim(10 ** int(np.log10(lowcut)), freqlim)
    else:
        ax.set_xlim(10 ** int(np.log10(lowcut)), fs / 2)
    
    ax.set_ylim(-80, 5)  # Gain in dB (reasonable range)    ax.set_xlabel('Frequency (Hz)')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Gain')
    ax.grid(True)
    
    # Plot sqrt(0.5) line
    ax.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)], '--', label='sqrt(0.5)')
    
    # Add legend and title
    ax.legend(loc='best')
    if save_dir is not None:
            title = f"Bode_Plot_Bandpass_{lowcut}_{highcut}"
            saveplot(save_dir, title, fig)
    else:
            plt.show() 


def butter_highpass_filter(data,lowcut,fs,order):
    """
    Applies a high-pass Butterworth filter.

    Parameters:
        data (array): The input signal.
        cutoff (float): The cutoff frequency of the filter (Hz).
        fs (float): The sampling frequency (Hz).
        order (int): The order of the filter.

    Returns:
        filtered_data (array): The filtered signal.
    """
    nyquist = 0.5 * fs  # Nyquist frequency
    normal_cutoff = lowcut / nyquist  # Normalized cutoff frequency
    # Design the Butterworth filter
    b, a = butter(order, normal_cutoff, btype='highpass', analog=False)
    # Apply the filter using filtfilt (zero-phase filtering)
    filtered_data = filtfilt(b, a, data)
    print(f"Highpass filter of order:{order*2} and with a cutoff:{lowcut} applied to the data successfully")
    return filtered_data

def plot_bode_both(fs,lowcut,highcut,freqlim=None,save_dir=None,save=False,order_high=None,order_low=None):
    fig, ax = plt.subplots()  # Create figure and axis objects
    # Normalize cutoff frequencies (relative to Nyquist frequency)
    nyquist = fs / 2
    low = lowcut / nyquist
    high = highcut / nyquist
   
      # Loop through filter orders
    if order_high and order_low is None:
        for order in [3, 6, 9]:
            # High-pass filter design
            b_high, a_high = butter(order, low, btype='highpass')
            w_high, h_high = freqz(b_high, a_high, worN=2000)
            freqs_high = w_high * fs / (2 * np.pi)

            gain_db_h = 20 * np.log10(np.maximum(abs(h_high), 1e-10))  # Convert gain to dB
            # Plot the magnitude response
            ax.plot(freqs_high, gain_db_h, label=f"High-pass (order = {order})")
            # ax.plot(freqs_high, abs(h_high), label=f"High-pass (order = {order})")
            
            # Low-pass filter design
            b_low, a_low = butter(order, high, btype='low')
            w_low, h_low = freqz(b_low, a_low, worN=2000)
            freqs_low = w_low * fs / (2 * np.pi)
            gain_db_l = 20 * np.log10(np.maximum(abs(h_low), 1e-10))  # Convert gain to dB
            ax.plot(freqs_low, gain_db_l, label=f"Low-pass (order = {order})")
            # ax.plot(freqs_low, abs(h_low), linestyle='--', label=f"Low-pass (order = {order})")
    else:
        # High-pass filter design
        order_high*=2
        order_low*=2
        b_high, a_high = butter(order_high, low, btype='highpass')
        w_high, h_high = freqz(b_high, a_high, worN=2000)
        freqs_high = w_high * fs / (2 * np.pi)

        gain_db_h = 20 * np.log10(np.maximum(abs(h_high), 1e-10))  # Convert gain to dB
        # Plot the magnitude response
        ax.plot(freqs_high, gain_db_h, label=f"High-pass (order = {order_high})")
        # ax.plot(freqs_high, abs(h_high), label=f"High-pass (order = {order})")
        
        # Low-pass filter design
        b_low, a_low = butter(order_low, high, btype='low')
        w_low, h_low = freqz(b_low, a_low, worN=2000)
        freqs_low = w_low * fs / (2 * np.pi)
        gain_db_l = 20 * np.log10(np.maximum(abs(h_low), 1e-10))  # Convert gain to dB
        ax.plot(freqs_low, gain_db_l, label=f"Low-pass (order = {order_low})")
        # ax.plot(freqs_low, abs(h_low), linestyle='--', label=f"Low-pass (order = {order})")


    ax.set_xscale('log')
    if freqlim is not None:
        ax.set_xlim(10 ** int(np.log10(lowcut)), freqlim)
    else:
        ax.set_xlim(10 ** int(np.log10(lowcut)), fs / 2)

    ax.set_ylim(-80, 5)  # Gain in dB (reasonable range)    
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Gain')
    ax.grid(True)
    
    # Plot reference line for sqrt(0.5)
    ax.axhline(-3, color='gray', linestyle='--', label='-3 dB cutoff')
    
    # Add legend and title
    ax.legend(loc='best')
    ax.set_title(f'High-pass and Low-pass Filter Frequency Response\nLowcut = {lowcut} Hz, Highcut = {highcut} Hz')
    
    if save_dir is not None:
            title = f"Bode_Plot_Bandpass_{lowcut}_{highcut}"
            saveplot(save_dir, title, fig)
    else:
            plt.show() 

def plot_bode_together(fs,lowcut,highcut,freqlim=None,save_dir=None,save=False,order_high=None,order_low=None):
    fig, ax = plt.subplots()  # Create figure and axis objects
    # Normalize cutoff frequencies (relative to Nyquist frequency)
    nyquist = fs / 2
    low = lowcut / nyquist
    high = highcut / nyquist
      # Loop through filter orders
    order_high*=2
    order_low*=2

    # High-pass filter design
    b_high, a_high = butter(order_high, low, btype='highpass')
    w_high, h_high = freqz(b_high, a_high, worN=2000)
    # freqs_high = w_high * fs / (2 * np.pi)

    # gain_db_h = 20 * np.log10(np.maximum(abs(h_high), 1e-10))  # Convert gain to dB
    # Plot the magnitude response
    # ax.plot(freqs_high, gain_db_h, label=f"order = {order}")
    # ax.plot(freqs_high, abs(h_high), label=f"High-pass (order = {order})")
    
    # Low-pass filter design
    b_low, a_low = butter(order_low, high, btype='low')
    w_low, h_low = freqz(b_low, a_low, worN=2000)
    # freqs_low = w_low * fs / (2 * np.pi)
    # gain_db_l = 20 * np.log10(np.maximum(abs(h_low), 1e-10))  # Convert gain to dB
    # Ensure both frequency axes (`w_high` and `w_low`) are the same
    
    assert np.allclose(w_high, w_low), "Frequency axes for high-pass and low-pass filters must match"

    # Combine high-pass and low-pass responses (overall bandpass response)
    h_total = h_high * h_low
    freqs = w_high * fs / (2 * np.pi)  # Convert from rad/sample to Hz

    # Convert combined gain to decibels
    gain_db_total = 20 * np.log10(np.maximum(abs(h_total), 1e-10))

    ax.plot(freqs, gain_db_total, label=f"Bandpass:  Low order = {order_low}, High_order={order_high}")
    # ax.plot(freqs_low, abs(h_low), linestyle='--', label=f"Low-pass (order = {order})")
    
    ax.set_xscale('log')
    if freqlim is not None:
        ax.set_xlim(10 ** int(np.log10(lowcut)), freqlim)
    else:
        ax.set_xlim(10 ** int(np.log10(lowcut)), fs / 2)

    ax.set_ylim(-80, 5)  # Gain in dB (reasonable range)    
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Gain (dB)')
    ax.grid(True)
    
    # Plot reference line for sqrt(0.5)
    ax.axhline(-3, color='gray', linestyle='--', label='-3 dB cutoff')
    
    # Add legend and title
    ax.legend(loc='best')
    ax.set_title(f'High-pass and Low-pass Filter Frequency Response\nLowcut = {lowcut} Hz, Highcut = {highcut} Hz')
    
    if save_dir is not None:
            title = f"Bode_Plot_Bandpass_{lowcut}_{highcut}"
            saveplot(save_dir, title, fig)
    else:
            plt.show() 

def low_and_high_pass(signal,dt,lowcut,highcut,order_low=2,order_high=2):
    fs=1/(dt/1000)
    lpfiltered=butter_lowpass_filter(signal, highcut, fs,order_low)
    hpfiltered=butter_highpass_filter(lpfiltered,lowcut,fs,order_high)
    return lpfiltered,hpfiltered
    