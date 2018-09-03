import serial
import time


def serial_setup(com_port="COM6", baudrates=57600):
    serial_port = serial.Serial()
    serial_port.baudrate = baudrates
    serial_port.port = com_port
    print(serial_port.is_open)
    try:
        serial_port.open()
    except serial.SerialException:
        serial_port.close()
        time.sleep(4)
        serial_port.open()
    return serial_port

def read_serial(serial_port):
    print ("Reading for 5 iterations")
    for i in range(5):
        time.sleep(1)
        line = str(serial_port.read(90))
        print( line)

def write_serial(serial_port, text):
    print(text)
    serial_port.write(str.encode(text))

srial = serial_setup()
read_serial(srial)
write_serial(srial, "This sucks")
read_serial(srial)
srial.close()
