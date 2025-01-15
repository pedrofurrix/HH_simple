import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.fft import fft, rfft
from scipy.fft import fftfreq, rfftfreq

from .moving_average import load_vs
from .savedata import saveplot
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def fft(CF,E,cell_id,results=None,voltages=None,e_dir=None,t=None,var="cfreq",plot=False,save=False):
   
    if voltages is not None and t is not None and e_dir is not None:
        maxpvoltages=voltages
    else:
        t, maxpvoltages,maxnvoltages,e_dir= load_vs(CF,E,cell_id,results,var)
   
    # # Apply windowing function
    # windowed_signal = maxpvoltages * np.hanning(len(maxpvoltages))

    # Remove DC offset
    windowed_signal=maxpvoltages-np.mean(maxpvoltages)


    fft_values = np.fft.fft(windowed_signal)
    freqs = np.fft.fftfreq(len(t), d=(t[1] - t[0])/1000)
    freqs = freqs[:len(freqs)//2]  # Keep only positive frequencies

    # Power Spectrum (normalized)
    power = np.abs(fft_values[:len(fft_values)//2])**2 / len(t)  # Normalize power
    
    # Plot
    if plot:
        plot_fft(power,freqs,e_dir,save)
    return power,freqs

def welch_analysis(CF,E,cell_id,results=None,voltages=None,t=None,var="cfreq",plot=False,save=False):
    t, maxpvoltages,maxnvoltages,e_dir= load_vs(CF,E,cell_id,results,var)

    # Calculate sampling frequency in Hz
    dt = (t[1] - t[0]) / 1000  # Convert ms to seconds
    sf = 1 / dt  # Sampling frequency in Hz
    
    maxpvoltages-=np.mean(maxpvoltages)
    f, Pxx = welch(maxpvoltages, fs=sf, nperseg=1024)
    if plot:
        fig,ax=plt.subplots()
        ax.semilogy(f,Pxx)
        title=f"Power Spectrum - Welch"
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Power Spectral Density")
        ax.set_title(title)
        fig.show()
        if save:
            saveplot(e_dir,title,fig)

def plot_fft(power,freqs,e_dir=None,save=False):
    fig,ax=plt.subplots()
    
    title=f"Power Spectrum - FFT"
    # ax.plot(t,voltages,label=f"Original Data")
    ax.plot(freqs[:len(freqs)//200],power[:len(power)//200],label=f"Power for each Frequency")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power")
    ax.legend()
    ax.set_title(title)
    fig.show()
    if save:
        saveplot(e_dir,title,fig)

# Building a class Fourier for better use of Fourier Analysis.
class Fourier:
    """
    Apply the Discrete Fourier Transform (DFT) on the signal using the Fast Fourier 
    Transform (FFT) from the scipy package.

    Example:
        fourier = Fourier(signal, sampling_rate=2000.0)
    """
  
    def __init__(self, signal,dt=0.001):
        """
        Initialize the Fourier class.

        Args:
            signal (np.ndarray): The samples of the signal
            sampling_rate (float): The sampling per second of the signal

        Additional parameters,which are required to generate Fourier calculations, are
        calculated and defined to be initialized here too:
            time_step (float): 1.0/sampling_rate
            time_axis (np.ndarray): Generate the time axis from the duration and
                                the time_step of the signal. The time axis is
                                for better representation of the signal.
            duration (float): The duration of the signal in seconds.
            frequencies (numpy.ndarray): The frequency axis to generate the spectrum.
            fourier (numpy.ndarray): The DFT using rfft from the scipy package.
        """
        self.signal = signal
        self.ac=self.signal-np.mean(self.signal)
        self.sampling_rate = 1/(dt/1000) #Hz
        self.time_step = dt/1000
        self.duration = len(self.signal)/self.sampling_rate
        self.time_axis = np.arange(0, self.duration, self.time_step)
        self.frequencies = rfftfreq(len(self.signal), d = self.time_step)
        self.fourier = rfft(self.ac)
  # Generate the actual amplitudes of the spectrum
    def amplitude(self):
        """
        Method of Fourier

        Returns:
            numpy.ndarray of the actual amplitudes of the sinusoids.
        """
        return 2*np.abs(self.fourier)/len(self.signal)

    # Generate the phase information from the output of rfft  
    def phase(self, degree = False):
        """
        Method of Fourier

        Args:
            degree: To choose the type of phase representation (Radian, Degree).
                    By default, it's in radian. 

        Returns:
            numpy.ndarray of the phase information of the Fourier output.
        """
        return np.angle(self.fourier, deg = degree)

    def plot_spectrum(self, interactive=False, max_freq=None, line_color='blue', line_width=2):
        """
        Plot the spectrum (Frequency Domain) of the signal.

        Args:
            interactive (bool): If True, creates an interactive plot using Plotly.
            max_freq (float): Maximum frequency to display in the spectrum. If None, displays all.
            line_color (str): Color of the spectrum line.
            line_width (float): Width of the spectrum line.

        Returns:
            None
        """
        if max_freq is not None:
            freq_mask = self.frequencies <= max_freq
            freqs_to_plot = self.frequencies[freq_mask]
            amps_to_plot = self.amplitude()[freq_mask]
        else:
            freqs_to_plot = self.frequencies
            amps_to_plot = self.amplitude()


        if interactive:
            trace = go.Scatter(
                x=freqs_to_plot,
                y=amps_to_plot,
                mode='lines',
                line=dict(color=line_color, width=line_width),
                name="Spectrum"
            )
            layout = go.Layout(
                title=dict(
                    text='Spectrum',
                    x=0.5,
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=25, family='Arial, bold')
                ),
                xaxis=dict(title='Frequency [Hz]'),
                yaxis=dict(title='Amplitude')
            )
            fig = go.Figure(data=[trace], layout=layout)
            fig.show()
        else:
            fig, ax = plt.subplots(figsize=(10, 6))            
            ax.plot(freqs_to_plot, amps_to_plot, color=line_color, linewidth=line_width)
            # Set titles and labels
            ax.set_title('Spectrum', fontsize=16)
            ax.set_xlabel('Frequency [Hz]', fontsize=14)
            ax.set_ylabel('Amplitude', fontsize=14)
            # Customize ticks
            ax.tick_params(axis='both', which='major', labelsize=12)
            # Add grid for better readability
            ax.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            return fig
        return fig
  
    def plot_time_frequency(self, max_freq=None, t_ylabel="Amplitude", f_ylabel="Amplitude",
                            t_title="Signal (Time Domain)", f_title="Spectrum (Frequency Domain)",
                            line_color='blue', line_width=2):
        """
        Plot the signal in both time domain and frequency domain.

        Args:
            max_freq (float): Maximum frequency to display in the spectrum. If None, displays all.
            t_ylabel (str): Y-axis label for the time-domain plot.
            f_ylabel (str): Y-axis label for the frequency-domain plot.
            t_title (str): Title for the time-domain plot.
            f_title (str): Title for the frequency-domain plot.
            line_color (str): Color of the spectrum line.
            line_width (float): Width of the spectrum line.

        Returns:
            None
        """

        if max_freq is not None:
            freq_mask = self.frequencies <= max_freq
            freqs_to_plot = self.frequencies[freq_mask]
            amps_to_plot = self.amplitude()[freq_mask]
        else:
            freqs_to_plot = self.frequencies
            amps_to_plot = self.amplitude()


        # Time-domain plot
        time_trace = go.Scatter(
            x=self.time_axis,
            y=self.signal,
            mode='lines',
            line=dict(color='red', width=line_width),
            name="Time Domain"
        )

        time_layout = go.Layout(
            title=dict(
                text=t_title,
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=25, family='Arial, bold')
            ),
            xaxis=dict(title='Time [sec]'),
            yaxis=dict(title=t_ylabel),
            width=1000,
            height=400
        )
        time_fig = go.Figure(data=[time_trace], layout=time_layout)
        time_fig.show()

        # Frequency-domain plot
        freq_trace = go.Scatter(
            x=freqs_to_plot,
            y=amps_to_plot,
            mode='lines',
            line=dict(color=line_color, width=line_width),
            name="Frequency Domain"
        )
        freq_layout = go.Layout(
            title=dict(
                text=f_title,
                x=0.5,
                xanchor='center',
                yanchor='top',
                font=dict(size=25, family='Arial, bold')
            ),
            xaxis=dict(title='Frequency [Hz]'),
            yaxis=dict(title=f_ylabel),
            width=1000,
            height=400
        )
        freq_fig = go.Figure(data=[freq_trace], layout=freq_layout)
        freq_fig.show()
        return time_fig,freq_fig
  
    def plot_save(self,fig,title,e_dir):
        saveplot(e_dir,title,fig)