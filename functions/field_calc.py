from neuron import h

# Initialize variable to hold extracellularly recorded potential
vrec = [0]

def fieldrec():
    """
    Calculate the sum of er_xtra from all sections that have the 'xtra' mechanism.
    Avoids nodes at the ends (0 and 1 positions).
    """
    sum_val = 0
    for sec in h.allsec():
        if h.ismembrane("xtra"):  # Check if 'xtra' mechanism is present on this section
            for seg in sec:  # Iterate over all segments of the section
                sum_val += seg.er_xtra
    return sum_val

def init(initial_v):
    """
    Initialize the simulation by setting the initial membrane potential
    and calculating the initial extracellularly recorded potential.
    """
    global vrec
    
    h.v_init=initial_v
    h.finitialize(h.v_init)  # Set initial voltage
    h.fcurrent()  # Calculate currents
    vrec[0] = fieldrec()  # Get the initial extracellular potential

def advance():
    """
    Advance the simulation by one time step and update the extracellularly recorded potential.
    """
    global vrec
    h.fadvance()  # Advance the simulation one time step
    vrec.append(fieldrec())  # Update the extracellularly recorded potential