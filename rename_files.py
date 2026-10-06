import os as os
import shutil as shut
def check_for_analysis(folder):
    dir_lst = os.listdir(folder)
    x = list(os.scandir(folder))
    temp = list(map(lambda y:'PD_scan+' in y,dir_lst))
    if True in temp:
        for i, truth in enumerate(temp):
            if truth:
                # name = dir_lst[i].replace('_0924_','+09_24_26+')
                # swap = dir_lst[i].split('+')[2]
                # new = swap[0:2] +'_'+swap[2:4] +'_'+swap[4:]
                # name = dir_lst[i].replace(swap,new)
                # os.rename(folder+'\\'+dir_lst[i],folder+'\\'+name)
                dir = dir_lst[i].split('PD_scan+')[1].split('.csv')[0]
                new_dir = folder+'\\'+dir
                os.mkdir(new_dir)
                shut.copyfile(folder+'\\'+dir_lst[i], folder+'\\'+dir+'\\'+dir_lst[i])

    else:
        for val in x:
            if val.is_dir():
                check_for_analysis(val.path)
if __name__ == '__main__':
    base_dir = os.getcwd()
    start_folder = base_dir+r'\Data'
    check_for_analysis(start_folder)