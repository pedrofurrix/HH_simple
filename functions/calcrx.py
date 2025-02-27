#Based on calcrxc.hoc
# V=RxI - if we know the V and the I is constant, the R associated with each segment is given by V/I
# Look at the papers to see how to implement the different waveforms xD
from neuron import h
import numpy as np

rho = 100 #35.4  # ohm cm, squid axon cytoplasm
	   # for squid axon, change this to seawater's value
	   # for mammalian cells, change to brain tissue or Ringer's value
b = 400  # um between electrodes
c = 100  # um between electrodes and axon

def setrx2(rho,b,c):
    for sec in h.allsec():
        if h.ismembrane("xtra"):
             for seg in sec:
                x = seg.x
                L = sec.L  # Length of the section #não acho que seja isto...

                # Calculate r1 and r2 #rever o que é o L e o x para perceber como calcular
                r1 = h.sqrt(((x - 0.5) * L + 0.5 * b)**2 + c**2)
                r2 = h.sqrt(((x - 0.5) * L - 0.5 * b)**2 + c**2)

                # Assign the calculated rx_xtra value for the segment 
                seg.rx_xtra = (rho / 4 / h.PI) * ((1 / r1) - (1 / r2)) * 0.01

def setrx1(xe,ye,ze,rho=100): #x,y,z are the electrode coordinates #it's wrong, see the representation
     #include more than one electrode
     #works only for the case where the waveform is the same for multiple electrodes
     #for different waveforms, see multiplesources
     #doesn't hold up if the waveforms are different - will have to see how I can do that
     #x,y and z in um and rt in Ohm (rho in S/um)
        for sec in h.allsec():
            if h.ismembrane("xtra"):
                for seg in sec:
                    rt=0
                    # for (x,y,z) in zip(xe,ye,ze):
                    r = h.sqrt((seg.x_xtra - xe)**2 + (seg.y_xtra - ye)**2 + (seg.z_xtra - ze)**2)
        # 0.01 converts rho's cm to um and ohm to megohm
        # if electrode is exactly at a node, r will be 0
        # this would be meaningless since the location would be inside the cell
        # so force r to be at least as big as local radius
                      #  r = h.diam(seg)/2 if r==0 else r=r
                    if r==0:
                        r=seg.diam/2
                    rt+=1e-3/(4*h.PI*rho*r) 
                seg.rx_xtra = rt


def show_position(xe,ye,ze):
    gElec = h.Shape(False)  # The 'False' argument ensures it's not immediately displayed
    # Set the view for the Shape object #The gElec.view() method sets the view parameters for the Shape. The arguments are:
    #The x and y coordinates of the bottom-left corner.
    #Width and height.
    #Position of the window on the screen (x and y).
    #Width and height of the window.
    gElec.view(-245.413, -250, 520.827, 520, 629, 104, 201.6, 201.28)
    markers=[h.Section() for i in xe]
    pointprocess=[]
    for i,(x,y,z) in enumerate(zip(xe,ye,ze)):
        markers[i].pt3dclear()
        markers[i].pt3dadd(x-0.5, y, z, 1)
        markers[i].pt3dadd(x+0.5, y, z, 1)
        pointprocess.append(h.PointProcessMark(markers[i](0.5)))
        gElec.point_mark(pointprocess[i], 2)

def setelec(xe,ye,ze,rho):
    setrx1(xe,ye,ze,rho)
    # show_position(xe,ye,ze)
    

def homogenous(rho,factor):
    for sec in h.allsec():
        for seg in sec:
            seg.rx_xtra=rho*factor*1e-6 



#Uniform E-field approximation

# input theta, and phi angles of E-field, assigns rx to all compartments (es_xtra(x)) for unit E-field (1 V/m)
def set_uniform_field_between_plates(theta=90,phi=0,ref_point=[0,0,0]):
    # Reference position for zero potential, here it is at soma(0)
    
    '''
    ref_x = soma.x3d(0)
    ref_y = soma.y3d(0)
    ref_z = soma.z3d(0)
    theta - polar angle between the radial line (z axis) and a given polar axis - 0° ≤ θ ≤ 180°
    phi - azimuthal angle - angle of rotation of the radial line around the polar axis - 0° ≤ φ < 360°
    '''

    theta = theta*np.pi/180
    phi = phi*np.pi/180
    Ex = np.sin(theta)*np.cos(phi)
    Ey = np.sin(theta)*np.sin(phi)
    Ez = np.cos(theta) 

    # Set the reference point (0 potential point)
    ref_x,ref_y,ref_z=ref_point
    
    # Loop over all segments to apply the extracellular field
    for sec in h.allsec():
        if h.ismembrane("xtra"):
            for seg in sec:
                # Set the transfer resistance using the constant field, using a i amplitude of 1 mA
                #// rx in [mV] for E of 1 [V/m] <= µm*1e-3 = mm * 1mV/mm = mV
                # ex = is*rx # ex should be in mV # rx is in mV as well and is acts only as a multiplier.
                seg.rx_xtra = -(Ex*(seg.x_xtra - ref_x) + Ey*(seg.y_xtra - ref_y) + Ez*(seg.z_xtra - ref_z))*1e-3