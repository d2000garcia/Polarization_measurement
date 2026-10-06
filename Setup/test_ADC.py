import serial

# CONTINUOUS READ-OUTS OF NUCLEO ADC READINGS

# ser = serial.Serial(
#     port="COM6",
#     baudrate=115200,
#     bytesize=serial.EIGHTBITS,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     timeout=1,
# )

nucleo = serial.Serial("COM6", 115200, timeout=1)


print("Connected to COM6. Waiting for ADC readings...")

try:
    while True:
        line = nucleo.readline().decode("utf-8", errors="replace").strip()

        # Ignore empty lines
        if not line:
            continue

        # Convert to Voltage
        try:
            adc_value = int(line)
        except ValueError:
            print(f"Ignoring invalid data: {line!r}")
            continue

        adj_value = (adc_value * 3.3) / 4095

        print(f"ADC: {adc_value:4d}    Voltage: {adj_value:.6f} V")

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    nucleo.close()