from thorlabs_elliptec import ELLx
from datetime import datetime
import numpy as np
import serial
import time
import csv
import os as os


# def main():
#     '''CONNECTION CHECKS:'''

#     # Connection management + variable definition
#     stage = ELLx(serial_port="COM5", x=16)
#     nucleo = serial.Serial("COM6", 115200, timeout=1)
#     time.sleep(1) # make sure all connections are set 
#     ref_voltage = 3.3  # (V)
    
#     # Check ELL16 connection and status
#     print(f"{stage.model_number} on {stage.port_name},"
#         f"serial number {stage.serial_number}, "
#         f"status {stage.status.description}")

#     '''SETUP CODE:'''

#     # Set ELL16 home
#     stage.home(blocking=True)
#     time.sleep(1)
#     print(f"Setting home position to: {stage.get_position()} degrees")

#     # Filename
#     filename = datetime.now().strftime("photodiode_scan_%Y%m%d_%H%M%S.csv")

#     # User input
#     acquisition_count = int(input("Enter sampling averaging count: "))
#     start_pos = float(input("Enter a starting position in degrees: "))
#     end_pos = float(input("Enter an ending position in degrees: "))
#     step_size = float(input("Enter a step size in degrees: "))
    
#     angles = np.arange(start_pos, end_pos + step_size, step_size).tolist() # generates list of angles that work with step size floats

#     '''MOVEMENT + MEASUREMENT CODE'''

#     # READING BUFFER - ignore 
#     test_list = []
#     for i in range(0, 25):
#         voltage = get_photodiode_measurement(nucleo, 3.3)
#         test_list.append(voltage)


#     # ACTUAL MEASUREMENTS
#     with open(filename, "w", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["Angle (degrees)", "Voltage (V)"]) # headings

#         for angle in angles:

#             measured_voltages = []
#             start_time = time.perf_counter() # index to start timing for loop iterations

#             stage.move_absolute(angle%360, blocking=True)
#             time.sleep(0.1) # waiting to make sure everythings all synced up

#             print(f"Reached {stage.get_position()} degrees")

#             for i in range(0, acquisition_count):
                             
#                 voltage = get_photodiode_measurement(nucleo, ref_voltage)
#                 measured_voltages.append(float(voltage))
                                
#             # write to csv
#             elapsed_time = time.perf_counter() - start_time
#             measured_voltages.append(elapsed_time)
#             writer.writerow([stage.get_position(), *measured_voltages])

        
#     stage.home(blocking=True)

#     '''CLOSE CONNECTION'''
#     stage.close()

#     # 
#     # \print(measured_angles, measured_voltages)

def main(start_pos,end_pos,acquisition_count,step_size,background=False):
    """
    Main function to run scan and save the file.

    Parameters
    ----------
    start_pos : int
        Integer for starting position in degrees, can be below 0.
    end_pos : int
        Integer for ending position in degrees, can be beyond 360.
    step_size : int
        Step size in degrees for rotation mount to rotate.
    acquisition_count : int
        Number of samples to take per step.
    background : bool
        Bool that informs program whether this is a background measurement or instead a normal measurement.

    Returns
    -------
    data : list of lists
        Data from measurement
    filename : str
        Path to last taken file
    """
    '''CONNECTION CHECKS:'''

    # Connection management + variable definition
    stage = ELLx(serial_port="COM5", x=16)
    nucleo = serial.Serial("COM6", 115200, timeout=1)
    time.sleep(1) # make sure all connections are set 
    ref_voltage = 3.3  # (V)
    
    # Check ELL16 connection and status
    print(f"{stage.model_number} on {stage.port_name},"
        f"serial number {stage.serial_number}, "
        f"status {stage.status.description}")

    '''SETUP CODE:'''

    # Set ELL16 home
    stage.home(blocking=True)
    time.sleep(1)
    print(f"Setting home position to: {stage.get_position()} degrees")

    cwd = os.getcwd()
    # Filename
    day_folder = time.strftime(cwd+"\\Measurements\\%m_%d_%y")
    meas_time = time.strftime("%m_%d_%y+%H_%M_%S")
    # file = time.strftime("\\photodiode_scan_%m_%d_%y+%H_%M_%S.csv")
    if not os.path.exists(day_folder):
        os.mkdir(day_folder)
    if background == False:
        os.mkdir(day_folder+'\\'+meas_time)
        filename = day_folder+'\\'+meas_time+'\\PD_scan_'+meas_time+'.csv'
    else:
        filename = day_folder+'\\PD_background_scan_'+meas_time+'.csv'

    # # User input
    # acquisition_count = int(input("Enter sampling averaging count: "))
    # start_pos = float(input("Enter a starting position in degrees: "))
    # end_pos = float(input("Enter an ending position in degrees: "))
    # step_size = float(input("Enter a step size in degrees: "))
    
    angles = np.arange(start_pos, end_pos + step_size, step_size).tolist() # generates list of angles that work with step size floats

    '''MOVEMENT + MEASUREMENT CODE'''

    # READING BUFFER - ignore 
    test_list = []
    for i in range(0, 25):
        voltage = get_photodiode_measurement(nucleo, 3.3)
        test_list.append(voltage)

    # # ACTUAL MEASUREMENTS
    # with open(filename, "w", newline="") as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(["Angle (degrees)", "Voltage (V)"]) # headings

    #     for angle in angles:

    #         measured_voltages = []
    #         start_time = time.perf_counter() # index to start timing for loop iterations

    #         stage.move_absolute(angle%360, blocking=True)
    #         time.sleep(0.1) # waiting to make sure everythings all synced up

    #         print(f"Reached {stage.get_position()} degrees")

    #         for i in range(0, acquisition_count):
                             
    #             voltage = get_photodiode_measurement(nucleo, ref_voltage)
    #             measured_voltages.append(float(voltage))
                                
    #         # write to csv
    #         elapsed_time = time.perf_counter() - start_time
    #         measured_voltages.append(elapsed_time)
    #         writer.writerow([stage.get_position(), *measured_voltages])

    data = []
    for angle in angles:
        start_time = time.perf_counter() # index to start timing for loop iterations

        stage.move_absolute(angle%360, blocking=True)
        data.append([stage.get_position()])
        time.sleep(0.1) # waiting to make sure everythings all synced up

        print(f"Reached {stage.get_position()} degrees")

        for i in range(0, acquisition_count): 
            voltage = get_photodiode_measurement(nucleo, ref_voltage)
            data[-1].append(float(voltage))       
        # write to csv
        elapsed_time = time.perf_counter() - start_time
        data.append(elapsed_time)
    i = True
    title = ['angle']
    title.extend(map(lambda x: 'V%i'%x,range(acquisition_count)))
    title.append('loop_time')
    file = open(filename,'w')
    file.write(','.join(title))
    for dat in data:
        file.write('\n')
        file.write(','.join(map(str,dat)))
    file.close()

    stage.home(blocking=True)

    '''CLOSE CONNECTION'''
    stage.close()
    return data, filename
    # 
    # \print(measured_angles, measured_voltages)


def get_photodiode_measurement(nucleo, ref_voltage):
    # Read one measurement from the NUCLEO
    response = nucleo.readline().decode().strip()

    # Extract the ADC number
    adc_value = int(response)

    # Convert to Voltage
    voltage = (adc_value * ref_voltage) / 4095

    return voltage

# if __name__ == "__main__":
#     main()