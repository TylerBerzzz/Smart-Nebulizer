import serial
import time
import pandas as pd

# set up the serial line
ser = serial.Serial('/dev/cu.usbmodem14101', 115200, timeout=1)

# Read and record the data
data = []  # empty list to store the data
for i in range(200):
    b = ser.readline()  # read a byte string
    string_n = b.decode()  # decode byte string into Unicode
    string = string_n.rstrip()  # remove \n and \r
    flt = float(string)  # convert string to float
    print(flt, i)
    data.append(flt)  # add to the end of data list
    time.sleep(0.01)  # wait (sleep) 0.1 seconds

ser.close()
# save data to csv
data_raw = [x for i, x in enumerate(data) if i % 2 == 0]
data_meters = [x for i, x in enumerate(data) if i % 2 != 0]
data_dict = {
    'raw': data_raw,
    'meters': data_meters
}
df = pd.DataFrame.from_dict(data_dict)
df.to_csv('data/airvelocity_sensor.csv', index=False)
