from neuron import h
import numpy as np
import matplotlib.pyplot as plt


#gvec.play(h._ref_is_xtra, tvec, 1) # interpolated play #basically, the is_xtra variable will get the gvec(index) value at tvec(index)

#ton is starting point
#dur is the duration of the stimulus
#amp is the amplitude
  
def stimplay(ton,dur,amp,simtime):
  gvec = h.Vector(6) # gradient--0 when field off, nonzero when on
  tvec = h.Vector(6)
  #Based on stimsphere and ec_stim_and_rec
  tvec.from_python([0, ton, ton,      ton+dur,  ton+dur, ton+dur+1])
  gvec.from_python([0, 0,   amp, amp, 0,       0])
  gvec.play(h._ref_is_xtra, tvec, 1)
  # plotvector(gvec,tvec,simtime,amp)
  return tvec, gvec

def stimplay2(ton,dur,amp): #two-part stimulation, with part positive and part negative
  gvec = h.Vector(6) # gradient--0 when field off, nonzero when on
  tvec = h.Vector(6)
  gvec.resize(8)
  tvec.resize(8)
  tvec.from_python([0, ton, ton, ton+dur/2, ton+dur/2, ton+dur, ton+dur, ton+dur+1])
  gvec.from_python([0, 0,   amp, amp,-amp,-amp, 0,       0])
  gvec.play(h._ref_is_xtra, tvec, 1)
  return tvec,gvec

'''
def setupstims(cell):
  fsquare=h.Fsquare(cell.soma(0.5))
  fzap=h.Fzap(cell.soma(0.5))
  fsquare._ref_x= h._ref_is_xtra
  fzap._ref_x= dummy
  '''



def squarestim(cell,ton,freq,num,amp1,amp2):
  fsquare=h.Fsquare(cell.soma(0.5))
  #set is to point to x
  fsquare._ref_x=h._ref_is_xtra 
  # h.setpointer(h._ref_is_xtra, 'x',fsquare)

  # # # Parameters
  #ton  time at which first cycle starts
  #dp   duration of a phase (duration of a half cycle)
  #num  number of cycles
  #amp1 level for first half cycle
  #amp2 level for second half cycle
  dp=1/(freq/1000)
  fsquare.ton=ton
  fsquare.dp=dp
  fsquare.num=num
  fsquare.amp1=amp1
  fsquare.amp2=amp2
  return fsquare

def sinstim(cell,ton,nc,f0,amp):
  fzap=h.Fzap(cell.soma(0.5))
  # Set pointer
  fzap._ref_x=h._ref_is_xtra #this is the syntax they use in tstpnt1.py
  # h.setpointer(h._ref_is_xtra, 'x',fzap)

  # # Parameters
  #tp 	period
  #nc 	number of full cycles of sine wave
  #f0   initial frequency
  #f1   final frequencys
  #amp  amplitude
  tp=1/(f0/1000)#f0 is in Hz and tp in ms
  fzap.ton = ton #1
  fzap.dur = tp*nc #TP*2*NC
  fzap.f0 = f0  #1000/2/TP
  fzap.f1 = fzap.f0
  fzap.amp=amp
  return fzap

#amp in mA, dt,dur and simtime in ms, freq in Hz
#similar to the method that we see in Mirzakhalili-et-al--CellSystems-2020
#Variable start and end time for stimulation, defined by ton and dur
def playsin(ton,amp,dt,dur,simtime,freq):
  times=np.arange(0,simtime+dt,dt)
  # 1000 is a factor because dt is in ms and freq in Hz
  stim=amp*np.sin(2*np.pi*freq/1000*times)
  #Making it so that while time<ton and time>ton+dur, stim value=0
  stim[times < ton] = 0
  stim[times > (ton + dur)] = 0

  t=h.Vector(times)
  stim1=h.Vector(stim)
  stim1.play(h._ref_is_xtra,t,0)
  return t,stim1

#amp in mA, dt and tstop in ms, freq in Hz
#similar to the method that we see in Mirzakhalili-et-al--CellSystems-2020
def simpleplaysin(amp,dt,tstop,freq):
  times=np.arange(0,tstop+dt,dt)
  stim=amp*np.sin(2*np.pi*freq/1000*times)
  t=h.Vector(times)
  stim1=h.Vector(stim)
  stim1.play(h._ref_is_xtra,t,0)
  return t,stim1


  
#amp in mA, dt,dur and simtime in ms, freq in Hz
#Amplitude modulation function, with variable depth and modulation frequency
#Variable start and end time for stimulation, defined by ton and dur
#depth is between 0 and 1, with 1 being 100% mod depth
#modfreq is in Hz
def ampmodulation(ton,amp,depth,dt,dur,simtime,freq,modfreq,ramp=False,ramp_duration=0,tau=None):
  times=np.arange(0,simtime+dt,dt)
  # 1000 is a factor because dt is in ms and freq in Hz
  #added -ton so that it starts at 0
  if modfreq!=0:
    mod=1/2*(np.sin(2*np.pi*modfreq/1000*(times-ton-1/(4*modfreq/1000)))+1)*depth+(1-depth)
  else:
    mod=1
    
  stim=amp*mod*np.sin(2*np.pi*freq/1000*(times-ton))
  #Making it so that while time<ton and time>ton+dur, stim value=0
  stim[times < ton] = 0
  stim[times > (ton + dur)] = 0
  if ramp:
    if tau is None:
      current=generate_ramp_current(times, ramp_duration,dt)
    elif tau == 0:
      tau=ramp_duration/3
      current=generate_exponential_ramp_current(times, ramp_duration, tau,dt)
    else:
      current=generate_exponential_ramp_current(times, ramp_duration, tau,dt)
    stim=stim*current

  t=h.Vector(times)
  stim1=h.Vector(stim)
  stim1.play(h._ref_is_xtra,t,0)
  return t,stim1

#amp in mA, dt,dur and simtime in ms, freq in Hz
#Amplitude modulation function, with variable depth and modulation frequency
#Variable start and end time for stimulation, defined by ton and dur
#depth is between 0 and 1, with 1 being 100% mod depth
#modfreq is in Hz
#varies between 1+depth and 1-depth
#Based on wikipedia definition of modulation index
def ampmodulation_wiki(ton,amp,depth,dt,dur,simtime,freq,modfreq):
  times=np.arange(0,simtime+dt,dt)
  # 1000 is a factor because dt is in ms and freq in Hz
  #added -ton so that it starts at 0
  mod=depth*(np.sin(2*np.pi*modfreq/1000*(times-ton-1/(4*modfreq/1000))))+1

  stim=amp*mod*np.sin(2*np.pi*freq/1000*(times-ton))
  #Making it so that while time<ton and time>ton+dur, stim value=0
  stim[times < ton] = 0
  stim[times > (ton + dur)] = 0

  t=h.Vector(times)
  stim1=h.Vector(stim)
  stim1.play(h._ref_is_xtra,t,0)
  return t,stim1

def generate_ramp_current(times, ramp_duration,dt):
    """
    Generate a stimulation current that ramps up and holds steady.

    Parameters:
        duration (float): Total duration of the simulation in ms.
        dt (float): Time step in ms.
        ramp_duration (float): Duration of the ramp-up phase in ms.
        max_current (float): Maximum current value (nA).

    Returns:
        np.array: Array of stimulation current values.
    """
    
    current = np.zeros_like(times)     # Initialize current array

    # Ramp phase
    current[times<=ramp_duration] = np.linspace(0, 1, int(ramp_duration/dt)+1)
    
    # Steady phase
    current[times>ramp_duration] = 1

    return current


def generate_exponential_ramp_current(times, ramp_duration, tau,dt):
    """
    Generate an exponentially ramping stimulation current that stabilizes at a maximum value.

    Parameters:
        duration (float): Total duration of the simulation in ms.
        dt (float): Time step in ms.
        ramp_duration (float): Duration of the ramp-up phase in ms.
        max_current (float): Maximum current value (nA).
        tau (float): Time constant for the exponential ramp (ms).

    Returns:
        np.array: Array of stimulation current values.
    """

    current = np.zeros_like(times)     # Initialize current array
    
    # Exponential ramp phase
    # ramp_end_index = int(ramp_duration / dt)
    # ramp_time = times[:ramp_end_index]  # Time points during ramp
    ramp_time = times[times <= ramp_duration]
    current[times <= ramp_duration] = (1 - np.exp(-ramp_time / tau))    
    # Steady phase
    current[times>ramp_duration] = 1  # Maintain max current after ramp duration
    
    return current