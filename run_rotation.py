from thorlabs_elliptec import ELLx
from datetime import datetime
import numpy as np
import serial
import time
import csv


def main():
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

    # Filename
    filename = datetime.now().strftime("photodiode_scan_%Y%m%d_%H%M%S.csv")

    # User input
    acquisition_count = int(input("Enter sampling averaging count: "))
    start_pos = float(input("Enter a starting position in degrees: "))
    end_pos = float(input("Enter an ending position in degrees: "))
    step_size = float(input("Enter a step size in degrees: "))
    
    angles = np.arange(start_pos, end_pos + step_size, step_size).tolist() # generates list of angles that work with step size floats

    '''MOVEMENT + MEASUREMENT CODE'''

    # READING BUFFER - ignore 
    test_list = []
    for i in range(0, 25):
        voltage = get_photodiode_measurement(nucleo, 3.3)
        test_list.append(voltage)


    # ACTUAL MEASUREMENTS
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Angle (degrees)", "Voltage (V)"]) # headings

        for angle in angles:

            measured_voltages = []
            start_time = time.perf_counter() # index to start timing for loop iterations

            stage.move_absolute(angle%360, blocking=True)
            time.sleep(0.1) # waiting to make sure everythings all synced up

            print(f"Reached {stage.get_position()} degrees")

            for i in range(0, acquisition_count):
                             
                voltage = get_photodiode_measurement(nucleo, ref_voltage)
                measured_voltages.append(float(voltage))
                                
            # write to csv
            elapsed_time = time.perf_counter() - start_time
            measured_voltages.append(elapsed_time)
            writer.writerow([stage.get_position(), *measured_voltages])

        
    stage.home(blocking=True)

    '''CLOSE CONNECTION'''
    stage.close()

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

if __name__ == "__main__":
    main()