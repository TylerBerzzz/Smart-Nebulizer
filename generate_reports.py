import serial
import time
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")


plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.grid'] = False

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

# COLLECT ANALYTICS
raw_fig = df['meters'].iloc[::8].plot()
plt.title("Air Velocity", fontsize=20)
plt.xlabel('seconds', fontsize=16)
plt.ylabel('meters', fontsize=16)
plt.savefig('results/air_flow.pdf')
plt.cla()

# Lung Capacity
Q = df['meters'] * 125/1000 * 1000 * 1.57 * 1e-4 * 100
l_per_sec_fig = Q.plot()
# plt.title("Litres per second" + '\n' + 'Peak L/s {}'.format(np.round(np.max(Q), 4)), fontsize=20)
plt.title("Litres per second", fontsize=20)
plt.xlabel('seconds', fontsize=16)
plt.ylabel('litres', fontsize=16)
plt.savefig('results/lung_capacity.pdf')
plt.cla()

# Breath intervals
a = np.nonzero(df['meters'].values)[0]
lengths = []
cur_st, cur_end = a[0], 0
for i, val in enumerate(a[:-1]):
    if a[i] + 1 != a[i + 1]:
        if a[i] - 1 == a[i - 1]:
            lengths.append(cur_end - cur_st)  # [cur_st, cur_end]
        cur_st = a[i + 1]
    elif a[i] + 1 == a[i + 1]:
        cur_end = a[i + 1]

s = 'Average breath length: {} seconds'.format(np.round(np.mean(lengths), 4)) + '\n' + 'Breath length  Peak: {} sec'\
                                                                                       ''.format(
    np.round(np.max(lengths), 4)) + '  Lowest: {} sec'.format(np.round(np.min(lengths), 4))

lengths = np.array(lengths) * 125 / 1000
intervals_fig = pd.Series(lengths).plot()
plt.title(s, fontsize=20)
intervals_fig.set_xlabel("breath #", fontsize=16)
intervals_fig.set_ylabel("seconds", fontsize=16)
plt.savefig('results/breathing.pdf')
plt.cla()

pdf.close()
