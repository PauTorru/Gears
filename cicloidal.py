import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def parallel(x,y,d):

    '''returns a curve paralel to y(x), separated by distance d'''

    p=np.vstack([x,y])

    dif=p[:,:-1]-p[:,1:]
    dif/=np.linalg.norm(dif,axis=0)

    para_xy=np.dot([[0,1],[-1,0]],dif)*d+p[:,1:]
    return para_xy[0],para_xy[1]

def draw_cicloidal_gear(ratio=8,pin_radius=10,gear_radius=100,input_radius=20,eccentricity=5,
    ring_pad=0,output_scale=1,n_points=10000):

    "Draws a cycloidal gear with the desired geometry and gear ratio"

    n_pins=ratio+1
    r2=gear_radius/(ratio+1)
    r1=ratio*r2
    r_pins_arrange=r1+r2

    #cicloidal calculation
    th=np.linspace(0,2*np.pi,n_points)
    x=(r1+r2)*np.cos(th)-eccentricity*np.cos((1+r1/r2)*th)
    y=(r1+r2)*np.sin(th)-eccentricity*np.sin((1+r1/r2)*th)

    yd=(y[1:]-y[:-1])/(x[1:]-x[:-1])
    x2,y2=parallel(x,y,pin_radius)
    x2=np.array(list(x2)+[x2[0]])
    y2=np.array(list(y2)+[y2[0]])

    #Input parts
    center=plt.Circle((0,0),pin_radius/2,facecolor="None",edgecolor="k")
    drive=plt.Circle((eccentricity,0),input_radius,facecolor="None",edgecolor="k")

    #output parts
    cicloidal_holes=[]
    output_pins=[]

    for k in range(6):
        alpha=k*np.pi/3.
        cicloidal_holes.append(plt.Circle((gear_radius*np.cos(alpha)/2+eccentricity,
                        gear_radius*np.sin(alpha)/2),
                        output_scale*pin_radius+eccentricity,facecolor="None",edgecolor="k"))
        output_pins.append(plt.Circle((gear_radius*np.cos(alpha)/2,
                            gear_radius*np.sin(alpha)/2),
                            output_scale*pin_radius,facecolor="None",edgecolor="k"))

    #outer ring parts
    sectors=[]
    pins=[]

    pin_angle=np.arccos(((r_pins_arrange+ring_pad)**2+r_pins_arrange**2-pin_radius**2)\
    /(2*(r_pins_arrange+ring_pad)*r_pins_arrange))
    pin_angle*=180/np.pi

    sector_angle=360/n_pins

    wedge_angle=np.arccos((pin_radius**2+r_pins_arrange**2-(r_pins_arrange+ring_pad)**2)\
    /(2*pin_radius*r_pins_arrange))-np.pi/2
    wedge_angle*=180/np.pi

    for j in range(n_pins):
        current_angle=(2*np.pi*j/(ratio+1))
        current_angle_deg=current_angle*180/np.pi

        sectors.append(mpatches.Wedge((0,0),r_pins_arrange+ring_pad,
                     current_angle_deg+pin_angle,
                     current_angle_deg+sector_angle-pin_angle,
                     facecolor="None",edgecolor="k",width=0))

        pin_center=(gear_radius*np.cos(current_angle),gear_radius*np.sin(current_angle))

        pins.append(mpatches.Wedge(pin_center,pin_radius,
                current_angle_deg+90-wedge_angle,current_angle_deg+270+wedge_angle,
                facecolor="None",edgecolor="k",width=0))

    # Put all the parts together

    fig=plt.gcf()
    plt.clf()
    ax=plt.gca()

    #Add cicloidal gear
    plt.plot(x2+eccentricity,y2,"k-")

    #Add inputs
    ax.add_artist(center)
    ax.add_artist(drive)

    #Add outputs
    for j in range(6):
        ax.add_artist(cicloidal_holes[j])
        ax.add_artist(output_pins[j])

    #Add ring
    for j in range(n_pins):
        ax.add_artist(sectors[j])
        ax.add_artist(pins[j])

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-(gear_radius+2*pin_radius),gear_radius+2*pin_radius)
    ax.set_ylim(-(gear_radius+2*pin_radius),gear_radius+2*pin_radius)
    plt.show()

    return fig
