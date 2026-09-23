import numpy as np
import scipy as sci

def pull_T_data(filename):
    #Give file_path and will returns 3 lists: angles_deg,angles_rad,data
    angles_deg=[]
    angles_rad=[]
    data=[]
    file = open(filename,'r')
    file.readline()
    full_rot = 0
    i = -1
    for line in file:
        i+=1
        line = list(map(float,line.strip().split(',')))
        angles_deg.append(line[0]+full_rot*360)
        data.append(np.mean(line[1:-1]))
        if i!=0:
            if angles_deg[-1]<angles_deg[-2]:
                full_rot =1
    angles_rad = list(map(lambda x: x*np.pi/180,angles_deg))
    return angles_deg, angles_rad, data