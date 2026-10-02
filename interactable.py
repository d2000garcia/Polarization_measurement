import os as os
import numpy as np
from numpy.polynomial import Polynomial as poly
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

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
        i=-1

        self.window_manager['Notes'] = ttk.Notebook(window)
        self.window_manager['Notes'].grid(column=0,row=0,columnspan=4, sticky="nsew")
        self.window_manager['dir'] = ''
        self.window_manager['Imgs'] = [{},{}]
        self.window_manager['entries'] = {'fit_rng':{'entry':[ttk.Entry(self.window,width=ent_wdth), ttk.Entry(self.window,width=ent_wdth)],'val':[tk.StringVar(value="0"), tk.StringVar(value="8000")]}}
        self.window_manager['entries']['fit_rng']['entry'][0].configure(textvariable=self.window_manager['entries']['fit_rng']['val'][0])
        self.window_manager['entries']['fit_rng']['entry'][0].grid(column=1,row=1)
        self.window_manager['entries']['fit_rng']['entry'][1].configure(textvariable=self.window_manager['entries']['fit_rng']['val'][1])
        self.window_manager['entries']['fit_rng']['entry'][1].grid(column=2,row=1)

        self.window_manager['entries']['beat_min']={'entry':[ttk.Entry(self.window,width=ent_wdth)],'val':[tk.StringVar(value="0")]}
        self.window_manager['entries']['beat_min']['entry'][0].configure(textvariable=self.window_manager['entries']['beat_min']['val'][0])
        self.window_manager['entries']['beat_min']['entry'][0].grid(column=7,row=1)

        self.window_manager['labels'] = [ttk.Label(self.window,text='Fit Range'),ttk.Label(self.window,text='Beat min')]
        self.window_manager['labels'][0].grid(column=0,row=1)

        for name in self.plotslabs:
            self.window_manager['Imgs'][name] = {}
            self.window_manager['Imgs'][name]['TkImg']=ImageTk.PhotoImage(resized_default.copy())
            self.window_manager['Imgs'][name]['Label']= tk.Label(self.window_manager['Notes'][-1],image=self.window_manager['Imgs'][name]['TkImg'])
            self.window_manager['Imgs'][name]['Label'].image = self.window_manager['Imgs'][name]['TkImg']
            self.window_manager['Imgs'][name]['Label'].pack()
            self.window_manager['Notes'][-1].add(self.window_manager['Imgs'][j][name]['Label'],text=scan+' '+name)

        self.window_manager['button']={'456':{'calcTFit':1,'calcBeatFit':1,'show':1},
                                          '894':{'calcTFit':1,'calcBeatFit':1,'show':1},
                                          'both':{'open_fold':1,'save':1,'exit':1}}
        i=-2
        for key1 in self.window_manager['button'].keys():
            for key2 in self.window_manager['button'][key1].keys():
                self.window_manager['button'][key1][key2] = ttk.Button(self.window,text=key2,command=lambda : print('Pick a data set for analysis!'))
                if key1 == 'both':
                    i+=2
                    self.window_manager['button'][key1][key2].grid(column=4,row=i)
                else:
                    self.window_manager['button'][key1][key2].configure(text=key1+' '+key2)
                    if key2 == 'show':
                        self.window_manager['button'][key1][key2].grid(row=1+2*int(key1=='894'),column=4)
                    else:
                        self.window_manager['button'][key1][key2].grid(row=1+2*int(key1=='894'),column=3+2*int(key2=='calcBeatFit'))

        self.window_manager['button']['both']['exit'].configure(command=exit)

        self.window_manager['work_dir'] = {'path':'Pick Directory','tk_var':tk.StringVar()}
        self.window_manager['work_dir']['tk_var'].set('Pick Directory')
        self.window_manager['work_dir']['lab'] = ttk.Label(self.window, textvariable=self.window_manager['work_dir']['tk_var'])
        self.window_manager['work_dir']['lab'].grid(column=3, row=11,columnspan=4, sticky="nsew")

    def update_work_dir(self,new_par_fold):
        self.window_manager['456']['dir']=new_par_fold+r'\Analysis\456\plots'
        self.window_manager['894']['dir']=new_par_fold+r'\Analysis\894\plots'
    
    def update_image(self,scan,name):
        if scan in self.scans:
            if name in self.plotslabs[0]:temp=1
            elif name in self.plotslabs[1]:temp=2
            else: temp=0
            if temp:
                plot_path = self.window_manager['dir'] + '\\' + name + '.png'
                temp2 = Image.open(plot_path)
                resized_temp2 = temp2.resize((self.plot_w, self.plot_h), Image.LANCZOS)
                self.window_manager['Imgs'][temp-1][name]['TkImg'] = ImageTk.PhotoImage(resized_temp2)
                self.window_manager['Imgs'][temp-1][name]['Label'].configure(image=self.window_manager['Imgs'][temp-1][name]['TkImg'])
                self.window_manager['Imgs'][temp-1][name]['Label'].image = self.window_manager['Imgs'][temp-1][name]['TkImg']
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
        self.wind.window_manager['button']['both']['open_fold'].configure(command=self.open_file_dialog)
        self.folderpath = ''
        self.fit_rng = [0,0]

        #make buttons
        self.wind.window_manager['button']['run'].configure(command=lambda:self.calculateTFit('456'))
        self.wind.window_manager['button']['Fit data'].configure(command=lambda:self.calculateBeatFit('456'))
        self.wind.window_manager['exit'][''].configure(command=lambda:self.show_plot('456'))

first = True
scale = 1.7
template_image = r".\Picture_template.png"
if __name__ == '__main__':
    if first:
        root = tk.Tk()
        first = False
        test = analysis(root,img_scale=scale)
    root.mainloop()