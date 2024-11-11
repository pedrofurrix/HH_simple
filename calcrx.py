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

def setrx1(xe,ye,ze): #x,y,z are the electrode coordinates #it's wrong, see the representation
     #include more than one electrode
     #doesn't hold up if the waveforms are different - will have to see how I can do that
     #x,y and z in um and rt in MOhm (rho in ohm cm)
        for sec in h.allsec():
            if h.ismembrane("xtra"):
                for seg in sec:
                    rt=0
                    for (x,y,z) in zip(xe,ye,ze):
                        r = h.sqrt((seg.x_xtra - x)**2 + (seg.y_xtra - y)**2 + (seg.z_xtra - z)**2)
        # 0.01 converts rho's cm to um and ohm to megohm
        # if electrode is exactly at a node, r will be 0
        # this would be meaningless since the location would be inside the cell
        # so force r to be at least as big as local radius
                      #  r = h.diam(seg)/2 if r==0 else r=r
                        rt+=(rho / 4 / h.PI)*(1/r)*0.01
                    if rt==0:
                        rt=seg.diam/2
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

def setelec(xe,ye,ze):
    setrx1(xe,ye,ze)
    show_position(xe,ye,ze)
    return 1

def homogenous(rho,factor):
    for sec in h.allsec():
        for seg in sec:
            seg.rx_xtra=rho*factor*1e-6 



#Uniform E-field - based on ChatGPT


def set_uniform_field_between_plates(v_plate,distance,field_orientation,ref_point):
    # Reference position for zero potential, here it is at soma(0)
    '''ref_x = soma.x3d(0)
    ref_y = soma.y3d(0)
    ref_z = soma.z3d(0)'''
    #V_plate in mV - potential difference between the 2 plates
    #distance between the 2 plates in um
    #e_field_strength - mV/um #to convert to V/m, multiply by 1e3 


    e_field_strength=v_plate/distance*1e-3 #if V and d are in V/m #convert to mV/um

    # Set the zero potential reference at the 0 end of the soma
    #soma(0).e_extracellular = 0 
    #i removed his part cause it's already defined to be like that when one 
    ref_x,ref_y,ref_z=ref_point
    
    # Loop over all segments to apply the extracellular field
    for sec in h.allsec():
        if h.ismembrane("xtra"):
            for seg in sec:

                # Calculate displacement from the zero potential reference
                displacement = np.array([seg.x_xtra - ref_x, seg.y_xtra - ref_y, seg.z_xtra - ref_z]) #um  

                # Calculate the component of displacement in the direction of the field
                field_component = np.dot(displacement, field_orientation)
                
                # Set the transfer resistance using the constant field, using a i amplitude of 1 mA
                #look at the explanation for the negative sign in the notes (25/10)
                seg.rx_xtra = -e_field_strength * field_component*1e-6 #kV, 1e-6 is there for the conversion 
                #use minus sign - look at explanation - because the electric field is positive from + to -
                # a dislocation in the direction of the electric field means the potential is reduced
                #Should I include a rho factor??? 
                #(supposedly, basically, as it is, a current of 1mA will make it so that V has the nominal value of rx_xtra always)
                #1e-6 is just to neutralize the other conversion factor
