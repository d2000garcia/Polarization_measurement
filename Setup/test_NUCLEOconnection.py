import serial
import time

# THIS IS BASICALLY TESTING CONNECTION TO NUCLEO BOARD

ser = serial.Serial(
    port="COM5",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=2,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False,
)


ser.reset_input_buffer()
ser.reset_output_buffer()

ser.write(b"0in\r\n")

time.sleep(0.5)

response = ser.read_until(b"\r\n")
print("Raw response:", repr(response))

ser.close()