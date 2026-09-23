import numpy as np
import scipy as sci

def pull_T_data(filename):
    #Give file_path and will returns 4 lists: angles_deg,angles_rad,data,std_dev
    angles_deg=[]
    angles_rad=[]
    data=[]
    std_dev=[]
    file = open(filename,'r')
    file.readline()
    full_rot = 0
    i = -1
    for line in file:
        i+=1
        line = list(map(float,line.strip().split(',')))
        angles_deg.append(line[0]+full_rot*360)
        data.append(np.mean(line[1:-1]))
        std_dev.append(np.std(line[1:-1]))
        if i < 10:
            if angles_deg[i] >180:
                angles_deg[i]
        if i!=0:
            if angles_deg[i]<angles_deg[i-1]:
                full_rot +=1
                angles_deg[i] += 360
    angles_rad = list(map(lambda x: x*np.pi/180,angles_deg))
    return angles_deg, angles_rad, data, std_dev

def E2(theta,phi):
    #In radians angle theta of polarizer to x-axis and radians phi of quarter wave to x-axis 
    return 0.5+0.5*np.cos(2*theta-2*phi)*np.cos(2*phi)
def E2_min(phi):
    return 0.5-0.5*np.cos(2*phi)

def E2_max(phi):
    return 0.5+0.5*np.cos(2*phi)

def use_extrema(angles_deg, angles_rad, data):
    mean = np.mean()
    #might be best to do estimate in phi then refit with actual fitting of the data
    #reason is actual data will likely miss max/min due to being discrete

def fit_phi(dat_file,bkg_file,fit_type='extrema'):
    bkg = np.mean(pull_T_data(bkg_file)[2])
    angles_deg,angles_rad,data,std_dev = pull_T_data(dat_file)
    data = np.array(data) - bkg
    if fit_type == 'extrema':
        fitted_phi = use_extrema(angles_deg, angles_rad, data)