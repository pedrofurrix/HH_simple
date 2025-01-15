import numpy as np
import matplotlib.pyplot as plt
from .csv_max_minshift import get_folder,load_voltages_hdf5,load_params
from .low_pass import get_results


def load_vs(CF,E,cell_id,results=None,var="cfreq"):
    freq_dir, e_dir=get_folder(CF,E,cell_id,var)
    voltages=load_voltages_hdf5(e_dir)

    if results==None:
        results=get_results(freq_dir)
        maxpseg = results[results['EValue'] == E]['maxp_seg'].values[0]
        maxnseg = results[results['EValue'] == E]['maxn_seg'].values[0]
    else:
        maxpseg=results["maxp_seg"]
        maxnseg=results["maxn_seg"]

    print(f"maxpseg={maxpseg}")
    print(f"maxnseg={maxnseg}")
    t=np.array(voltages["t"].to_list())
    maxpvoltages = np.array(voltages[maxpseg].to_list())
    maxnvoltages = np.array(voltages[maxnseg].to_list())
    return t, maxpvoltages,maxnvoltages,e_dir

def sma(t,voltages,window_size=10):

    weights = np.ones(window_size) / window_size
    sma = np.convolve(voltages, weights, mode='valid')

    sma_time = t[window_size - 1:]  # Start from where the SMA calculation begins
    
    title=f"Simple MA with Window Size={window_size}"
    fig,ax=plt.subplots()
    # ax.plot(t,voltages,label=f"Original Data")
    ax.plot(sma_time,sma,label=f"Moving Average")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Membrane Potential (mV)")
    ax.legend()
    ax.set_title(title)
    plt.show()

def cma(t,voltages):
    cma = np.cumsum(voltages) / np.arange(1, len(voltages) + 1)
    title=f"Cummulative Moving Average"
    fig,ax=plt.subplots()
    # ax.plot(t,voltages,label=f"Original Data")
    ax.plot(t,cma,label=f"Moving Average")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Membrane Potential (mV)")
    ax.legend()
    ax.set_title(title)
    plt.show()