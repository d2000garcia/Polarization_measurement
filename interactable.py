import os as os
import numpy as np
from numpy.polynomial import Polynomial as poly
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import Polarization_calc as Pc
import run_rotation as rot

class window:
    def __init__(self,window,default_path = r".\Picture_template.png", plot_w = 500, plot_h = 300):
        default_img = Image.open(default_path)
        ent_wdth = 20
        resized_default = default_img.resize((plot_w, plot_h), Image.LANCZOS)
        #Save variables for reference
        self.window = window
        self.plot_w = plot_w
        self.plot_h = plot_h
        #labels to ref plot indices
        self.plotslabs = ['OgScan','Fitted','Resid']
        self.day_fold = ''
        self.window_manager={}
        self.window_manager['separator'] = ttk.Separator(window, orient='vertical')
        self.window_manager['separator'].grid(column=4,row=0,rowspan=4,sticky='ns')
        # self.window_manager['separator'].place(relx=0.5, rely=0, relwidth=2, relheight=1)

        self.window_manager['Notes'] = ttk.Notebook(window)
        self.window_manager['Notes'].grid(column=0,row=0,columnspan=4, sticky="nsew")
        self.window_manager['dir'] = ''
        self.window_manager['Imgs'] = {}

        self.window_manager['labels'] = [ttk.Label(self.window,text='Start'),ttk.Label(self.window,text='End'),ttk.Label(self.window,text='Fit range (deg)')]
        self.window_manager['labels'][0].grid(column=1,row=1)
        self.window_manager['labels'][1].grid(column=2,row=1)
        self.window_manager['labels'][2].grid(column=0,row=2)
        self.window_manager['laser_on'] = tk.IntVar()
        # tk.Checkbutton(self.window,text="Laser On for Background?",variable=self.window_manager['laser_on']).grid(column=3,row=2)

        self.window_manager['labels'].append(ttk.Label(self.window,text='Run Measurement [deg]'))
        self.window_manager['labels'].append(ttk.Label(self.window,text='Start Angle'))
        self.window_manager['labels'].append(ttk.Label(self.window,text='End Angle'))
        self.window_manager['labels'].append(ttk.Label(self.window,text='Step Size'))
        self.window_manager['labels'].append(ttk.Label(self.window,text='# Samples per step'))
        self.window_manager['labels'][3].grid(column=6,row=1,columnspan=2)
        self.window_manager['labels'][4].grid(column=5,row=2)
        self.window_manager['labels'][5].grid(column=8,row=2)
        self.window_manager['labels'][6].grid(column=5,row=3)
        self.window_manager['labels'][7].grid(column=8,row=3)



        for name in self.plotslabs:
            self.window_manager['Imgs'][name] = {}
            self.window_manager['Imgs'][name]['TkImg']=ImageTk.PhotoImage(resized_default.copy())
            self.window_manager['Imgs'][name]['Label']= tk.Label(self.window_manager['Notes'],image=self.window_manager['Imgs'][name]['TkImg'])
            self.window_manager['Imgs'][name]['Label'].image = self.window_manager['Imgs'][name]['TkImg']
            self.window_manager['Imgs'][name]['Label'].pack()
            self.window_manager['Notes'].add(self.window_manager['Imgs'][name]['Label'],text=name)

        self.window_manager['entries'] = {'fit_rng':{'entry':[ttk.Entry(self.window,width=ent_wdth), ttk.Entry(self.window,width=ent_wdth)],'val':[tk.StringVar(value="0"), tk.StringVar(value="0")]}}
        self.window_manager['entries']['rot_ent']={'entry':[ttk.Entry(self.window,width=ent_wdth), ttk.Entry(self.window,width=ent_wdth), ttk.Entry(self.window,width=ent_wdth),ttk.Entry(self.window,width=ent_wdth)],'val':[tk.StringVar(value="0"), tk.StringVar(value="360"), tk.StringVar(value="5"), tk.StringVar(value="0")]}
        self.window_manager['button']={'Folder':1,'Show':1,'Set Fit Rng':1,'Fit':1,'Get Background':1,'Get Normal Measurement':1}
        functs = list(self.window_manager['button'].keys())
        for i in [0,1,2,3]:
            self.window_manager['entries']['rot_ent']['entry'][i].configure(textvariable=self.window_manager['entries']['rot_ent']['val'][i])
            self.window_manager['entries']['rot_ent']['entry'][i].grid(column=6+i%2,row=2+round(i/3))
            self.window_manager['button'][functs[i]] = ttk.Button(self.window,text=functs[i],command=lambda : print('Pick a data set for analysis!'))
            self.window_manager['button'][functs[i]].grid(column=i,row=4)
            if i%2:
                self.window_manager['entries']['fit_rng']['entry'][round(i/3)].configure(textvariable=self.window_manager['entries']['fit_rng']['val'][round(i/3)])
                self.window_manager['entries']['fit_rng']['entry'][round(i/3)].grid(column=1+round(i/3),row=2)
                self.window_manager['button'][functs[round(i/3)+4]] = ttk.Button(self.window,text=functs[round(i/3)+4],command=lambda : print('Pick a data set for analysis!'))
                self.window_manager['button'][functs[round(i/3)+4]].grid(column=5+round(i/3)*2,columnspan=2,row=4)
        self.window_manager['button']['exit'] = ttk.Button(self.window,text='Close',command=exit)
        self.window_manager['button']['exit'].grid(column=4,row=5)


        # self.window_manager['button']['both']['exit'].configure(command=exit)

        # self.window_manager['work_dir'] = {'path':'Pick Directory','tk_var':tk.StringVar()}
        # self.window_manager['work_dir']['tk_var'].set('Pick Directory')
        # self.window_manager['work_dir']['lab'] = ttk.Label(self.window, textvariable=self.window_manager['work_dir']['tk_var'])
        # self.window_manager['work_dir']['lab'].grid(column=3, row=11,columnspan=4, sticky="nsew")

    # def update_work_dir(self,new_par_fold):
    #     self.window_manager['dir']=new_par_fold

    def update_image(self,name):
        """
        name : str
            name of plot
        """
        if name in self.plotslabs:
            plot_path = self.window_manager['dir'] + '\\' + name + '.png'
            temp2 = Image.open(plot_path)
            resized_temp2 = temp2.resize((self.plot_w, self.plot_h), Image.LANCZOS)
            self.window_manager['Imgs'][name]['TkImg'] = ImageTk.PhotoImage(resized_temp2)
            self.window_manager['Imgs'][name]['Label'].configure(image=self.window_manager['Imgs'][name]['TkImg'])
            self.window_manager['Imgs'][name]['Label'].image = self.window_manager['Imgs'][name]['TkImg']

    # def change_Label_image(self,new,oldlabel):
    # #oldlabel is the label you want to change and
    # #new is new Tkimage to exchange
    #     oldlabel.configure(image=new)
    #     oldlabel.image = new
    
    # def update_all_imgs(self):
    #     for scan in self.scan:
    #         for name in self.plotslabs:
    #             if name != 'TBD':
    #                 plot_path = self.fold + '\\' + scan +name + '.png'
    #                 temp = Image.open(plot_path)
    #                 resized_temp = temp.resize((self.plot_w, self.plot_h), Image.LANCZOS)
    #                 self.window_manager['Imgs'][name]['TkImg'] = ImageTk.PhotoImage(resized_temp)
    #                 self.change_Label_image(self.window_manager['Imgs'][name]['TkImg'],self.window_manager['Imgs'][name]['Label'])

class analysis:
    #V2 includes the plots from simultaneous hot cell meas
    def __init__(self,root,img_scale):
        self.root =  root
        self.wind = window(root, plot_w=int(500*img_scale),plot_h=int(300*img_scale))
        self.wind.window_manager['button']['Folder'].configure(command=self.open_file_dialog)
        self.pol_calc = Pc.pol_analysis()
        self.file_loaded= False
        self.folderpath = ''
        # self.fit_rng = [0,0]
        #make buttons
        self.wind.window_manager['button']['Show'].configure(command=self.show_plot)
        self.wind.window_manager['button']['Set Fit Rng'].configure(command=self.set_rng)
        self.wind.window_manager['button']['Fit'].configure(command=self.do_fit)
        self.wind.window_manager['button']['Get Background'].configure(command=lambda : self.run_rot(True))
        self.wind.window_manager['button']['Get Normal Measurement'].configure(command=lambda : self.run_rot(False))

    def open_file_dialog(self):
        temporary = filedialog.askdirectory(
            initialdir="/",  # Optional: set initial directory
            title="Select a folder"
            # filetypes=(("Text files", "*.txt"), ("All files", "*.*")) # Optional: filter file types
        )
        if temporary:
            self.folderpath = temporary
            date_time = self.folderpath[self.folderpath.rfind('/')+1:]
            self.root.title(date_time + ' Fiting Analysis')
            print(f"Selected folder: {self.folderpath}")
            self.checkforanalysis()

    def checkforanalysis(self):
        contents = os.listdir(self.folderpath)
        check = list(map(lambda x:'PD_scan' in x,contents))
        if True in check:
            par_fold = self.folderpath[:self.folderpath.rfind('/')]
            contents2 = os.listdir(par_fold)
            check2 = list(map(lambda x:'background' in x,contents2))
            if True in check2:
                self.file_loaded = True
                bkg_file = par_fold + '\\'+ contents2[check2.index(True)]
                self.pol_calc.grab_background(bkg_file)
                file = self.folderpath + '\\'+ contents[check.index(True)]
                self.pol_calc.grab_data(self.folderpath,file)
                self.wind.window_manager['dir'] = self.folderpath
                self.wind.update_image('OgScan')
            else:
                print('Need to run background scan first!')

        else:
            print('Not a valid folder picked!')

    def set_rng(self):
        if self.file_loaded:
            self.pol_calc.set_rng(int(self.window_manager['entries']['fit_rng']['val'][0].get()),int(self.window_manager['entries']['fit_rng']['val'][1].get()))
            self.wind.update_image('OgScan')
        else:
            print('Pick file to analyze first!')

    def show_plot(self):
        if self.file_loaded:
            self.pol_calc.show_plot()
        else:
            print('Pick file to analyze first!')

    def do_fit(self):
        if self.file_loaded:
            self.pol_calc.fit_phi()
        else:
            print('Pick file to analyze first!')

    def run_rot(self,background_meas=False):
        good = False
        temp = []
        try:
            temp =  list(map(lambda x: int(self.wind.window_manager['entries']['rot_ent']['val'][x].get()),[0,1,2,3]))   
            if temp[0] < temp[1]:
                if temp[2] > 0:
                    if temp[3] > 0:
                        rot.main(temp[0],temp[1],temp[2],temp[3],background_meas)
                    else:
                        print('Number of samples per step needs to be greater than 0!')
                else:
                    print('Step size needs to be greater than 0!')
            else:
                print('Min angle needs to be less than max angle!')     
        except Exception as e:
            print(f'Not valid entries into rotation values! : {e}')

first = True
scale = 1
# template_image = r".\Picture_template.png"
if __name__ == '__main__':
    if first:
        root = tk.Tk()
        first = False
        test = analysis(root,img_scale=scale)
    root.mainloop()