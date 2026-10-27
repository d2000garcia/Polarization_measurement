from matplotlib import pyplot as plt
import numpy as np
# from matplotlib import pyplot as plt
# import scipy as sci
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import os as os

#File structure should look like
#Day folder "10_02_26" -> time folder "10_02_26+13_45_25" -> "measurement_dat.csv" 
#interactable will add so that time folder "10_02_26+13_45_25" -> "measurement_dat.csv" & "Analysis" -> 'param_fit.csv" & "Og_plot.png" & "fitted.png" & "resid.png"
def pull_T_data(filename):
    """
    Pull transmission data generated from run_rotation

    Parameters
    ----------
    filename : str
        filepath to pull data from

    Returns
    ------- All lists same length
    angles_deg : list
        Returned angles from thorlabs mount in degrees.
    angles_rad : list
        Converted angles from angles_deg to radians.
    data : list
        Averaged measurements for each step in the rotation measurement.
    std_dev :  list
        Standard deviation of the averaged measurements for each step in the rotation measurement.
    """
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

def E2_fit(theta,phi,shift,scale):
    #In radians angle theta of polarizer to x-axis and radians phi of quarter wave to x-axis 
    return scale*(0.5+0.5*np.cos(2*(theta-shift)-2*phi)*np.cos(2*phi))

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

class pol_analysis:
    def __init__(self):
        self.folderpath = ''
        self.fit_rng = [0,0]
        self.background = 0
        self.angles_deg = []
        self.angles_rad = []
        self.data = []
        self.std_dev = []

    def grab_background(self,bkg_file):
        temp = pull_T_data(bkg_file)
        #Check for if laser is on
        if np.std(temp[2])/np.mean(temp[3])>15:
            #Then assume laser is on
            #Assume phi=0 so that min = background
            self.background = min(temp[2])+np.mean(temp[3])
        else:
            #Background measurement present so use that
            leng = len(temp[2])
            #Pulling data from inner range just to make sure no bugs of wrong measurements
            self.background = np.mean(temp[2][int(leng*0.25):int(leng*0.75)])

    def grab_data(self,folderpath,file_path):
        self.folderpath = folderpath
        self.angles_deg,self.angles_rad,data,self.std_dev = pull_T_data(file_path)
        self.data =list(map(lambda x: x-self.background,data))
        self.fit_rng_ind = [0,len(self.angles_deg)]
        self.fit_angles_deg = self.angles_deg[self.fit_rng_ind[0]:self.fit_rng_ind[1]]
        self.fit_angles_rad = self.angles_rad[self.fit_rng_ind[0]:self.fit_rng_ind[1]]
        self.fit_data = self.data[self.fit_rng_ind[0]:self.fit_rng_ind[1]]
        if not os.path.exists(self.folderpath+r'\OgScan.png'):
            plt.plot(self.fit_angles_deg,self.fit_data,'--',marker='o')
            plt.xlim(min(self.angles_deg),max(self.angles_deg))
            plt.title('Original Data in fitting range')
            plt.savefig(self.folderpath+r'\OgScan.png')
            # plt.show()
            plt.clf()

    def set_rng(self,ang_min,ang_max):
        #in degrees
        self.fit_rng = [ang_min,ang_max]
        self.fit_rng_ind = [0,len(self.angles_deg)]
        if ang_min!=ang_max:
            for i,angle in enumerate(self.angles_deg):
                if self.angles_deg[i-1] < ang_min and ang_min < angle:
                    self.fit_rng_ind[0] = i
                elif self.angles_deg[i-1] < ang_max and ang_max < angle:
                    self.fit_rng_ind[1] = i
        self.fit_angles_deg = self.angles_deg[self.fit_rng_ind[0]:self.fit_rng_ind[1]]
        self.fit_angles_rad = self.angles_rad[self.fit_rng_ind[0]:self.fit_rng_ind[1]]
        self.fit_data = self.data[self.fit_rng_ind[0]:self.fit_rng_ind[1]]

        plt.plot(self.angles_deg,self.data,'--',marker='o')
        plt.xlim(min(self.angles_deg),max(self.angles_deg))
        plt.title('Original Data in fitting range')
        if ang_min!=ang_max:
            plt.axvspan(self.angles_deg[0],self.fit_angles_deg[0],alpha=0.2,color='grey')
            plt.axvspan(self.fit_angles_deg[-1],self.angles_deg[-1],alpha=0.2,color='grey')
        plt.savefig(self.folderpath+r'\OgScan.png')
        # plt.show()
        plt.clf()

    def show_plot(self):
        plt.plot(self.angles_deg,self.data)
        plt.xlim(min(self.angles_deg),max(self.angles_deg))
        plt.title('Original Data in fitting range')
        plt.show()

    def use_extrema(self):
        #might be best to do estimate in phi then refit with actual fitting of the data
        #reason is actual data will likely miss max/min due to being discrete
        avg = np.mean(self.fit_data)
        temp = np.abs(self.fit_data - avg)
        extrema_ind = find_peaks(temp)[0]
        extrema = [[],[]]
        for i in extrema_ind:
            if self.fit_data[i] < avg:
                #mins
                extrema[0].append(self.fit_data[i])
            else:
                #maxs
                extrema[1].append(self.fit_data[i])
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
        # continuous_angles = np.linspace(angles_rad[0],angles_rad[-1],1000)
        # est_init = list(map(lambda x:scale_est*E2(x,phi_est),continuous_angles.tolist()))
        # plt.plot(angles_deg,self.fit_data,'.')
        # plt.plot(continuous_angles*180/np.pi,est_init,'--')
        # plt.ylim(0,scale_est)
        # plt.show()
        self.phi_est = phi_est
        self.scale_est = scale_est

    def fit_phi(self):
        bound = ([self.phi_est-5*np.pi/180, -np.pi/2 , self.scale_est*0.8],[self.phi_est+5*np.pi/180, np.pi/2, self.scale_est*1.2])
        self.param, self.param_cov = curve_fit(E2_fit,self.fit_angles_rad,self.fit_data,[self.phi_est , 0 , self.scale_est],bounds=bound)
        np.savetxt(self.folderpath+'\\fit_param.csv',self.param)
        continuous_angles = np.linspace(self.fit_angles_rad[0],self.fit_angles_rad[-1],1000)
        fit = list(map(lambda x:E2_fit(x,*self.param),continuous_angles.tolist()))
        ellip = np.sqrt(1-np.tan(self.param[0])**2)
        plt.plot(self.fit_angles_deg,self.fit_data,'.')
        plt.plot(continuous_angles*180/np.pi,fit)
        plt.ylim(0,self.scale_est)
        plt.xlabel('Angle [deg]')
        plt.title(r'Fitted Curve, $\phi=%.4f^\circ,e=%.4f$'%(self.param[0]*180/np.pi,ellip))
        plt.savefig(self.folderpath+r'\Fitted.png')
        # plt.show()
        plt.clf()

        resid = np.array(self.fit_data)-np.array(list(map(lambda x:E2_fit(x,*self.param),self.fit_angles_rad)))
        plt.plot(self.fit_angles_deg,resid)
        plt.title(r'Residuals, $\phi=%.4f^\circ,e=%.4f$'%(self.param[0]*180/np.pi,ellip))
        plt.xlabel('Angle [deg]')
        plt.savefig(self.folderpath+r'\Resid.png')
        # plt.show()
        plt.clf()