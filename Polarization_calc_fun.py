from matplotlib import pyplot as plt
import numpy as np
# from matplotlib import pyplot as plt
# import scipy as sci
from scipy.signal import find_peaks
import os as os

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
        if i < 20:
            if angles_deg[i] >270:
                angles_deg[i]-=360
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
def E2_max_inv(scale,maxi):
    #fit phi for max values
    return np.arccos(2*maxi/scale-1)/2
def E2_min_inv(scale,mini):
    #fit phi for min values
    return np.arccos(1-2*mini/scale)/2

def use_extrema(angles_deg, angles_rad, data):
    #might be best to do estimate in phi then refit with actual fitting of the data
    #reason is actual data will likely miss max/min due to being discrete
    avg = np.mean(data)
    temp = np.abs(data - avg)
    extrema_ind = find_peaks(temp)[0]
    extrema = [[],[]]
    for i in extrema_ind:
        if data[i] < avg:
            #mins
            extrema[0].append(data[i])
        else:
            #maxs
            extrema[1].append(data[i])
    avgs = [np.mean(extrema[0]),np.mean(extrema[1])]
    scale_est = avgs[0]+avgs[1]
    phis = []
    for i in [0,1]:
        for val in extrema[i]:
            if i==0:
                if val/scale_est>0:
                    phis.append(E2_min_inv(scale_est,val))
                else:
                    #Then min is negative so assume scale/measurment err
                    phis.append(0)
                
            else:
                if val/scale_est<1:
                    phis.append(E2_max_inv(scale_est,val))
                else:
                    #Then max is larger than 1 so assume scale/measurment err
                    phis.append(0)
    phi_est = np.mean(phis)
    print('Mean_phi_peak_fit =',phi_est)
    print('Std_phi_peak_fit =',np.std(phis))
    step_size = np.mean(list(map(lambda x,y:x-y,angles_rad[1:],angles_rad[:-1])))
    convolv_input = np.arange(angles_rad[0]-np.pi/2,angles_rad[-1]+np.pi/2,step_size)
    convolv_dat = list(map(lambda x:scale_est*E2(x,phi_est),convolv_input.tolist()))
    result = np.convolve(np.array(data),np.array(convolv_dat),mode='valid')
    x = np.arange(0,result.shape[0],1)
    phase_shift = convolv_input[np.argmax(result)]
    continuous_angles = np.linspace(angles_rad[0],angles_rad[-1],1000)
    est_init = list(map(lambda x:scale_est*E2(x,phi_est),continuous_angles.tolist()))
    est_v2 = list(map(lambda x:scale_est*E2(x+phase_shift,phi_est),continuous_angles.tolist()))
    plt.plot(angles_deg,data,'.')
    plt.plot(continuous_angles*180/np.pi,est_init,'--')
    plt.plot(continuous_angles*180/np.pi,est_v2,'-')
    plt.show()
    return phi_est , phase_shift



def fit_phi(dat_file,bkg_file,fit_type='extrema'):
    bkg = np.mean(pull_T_data(bkg_file)[2])
    angles_deg,angles_rad,data,std_dev = pull_T_data(dat_file)
    data = np.array(data) - bkg
    if fit_type == 'extrema':
        fitted_phi = use_extrema(angles_deg, angles_rad, data)

cwd = os.getcwd()
if __name__ == '__main__':
    file_bkg = cwd+r"\Data\Test_Data_9-22-26\sample_data_background.csv"
    file_dat = cwd+r"\Data\Test_Data_9-22-26\sample_data.csv"
    fit_phi(file_dat,file_bkg)