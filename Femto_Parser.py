# Small script to parse and graph the FemtoSat data

import numpy as np 
import matplotlib.pyplot as plt
from tqdm import tqdm #used for progress bar

filename_list = ["FTSatNoGPS.log","FTSat.log","FTSat2.log"] # List of filenames
fig, [ax1, ax2] = plt.subplots(2,1,sharex = True)
ax1.title.set_text("FemtoSat Launch Data")

FACTOR = 0.125 # Conversion factor for 8Hz transmission

# Data is structured in the following way
# Temp (C), Pressure (hPa), Alt (m), AccX (m/s^2), AccY (m/s^2), AccZ (m/s^2)
# From the code it says the the sample rate is 50 Hz

# Read the number of lines in the file
def line_number(filename):
    count = 0
    with open(filename, "r") as fp:
        for count, line in enumerate(fp):
            pass
    total_lines = count + 1

    return total_lines

# Generates the graph from the file
def generate_graph(filename):
    ### Convert between file to list
    temp    = 0
    pres    = 0
    alt     = 0
    accx    = 0
    accy    = 0
    accz    = 0

    #set up the data matrix
    lines = open(filename, "r").readlines()
    first_line = lines[0]
    file_len = line_number(filename)

    comma = ","
    #Get the locations of the data breaks
    subs = [i for i in range(len(first_line)) if first_line.startswith(comma,i)]
    # matrix to hold the variables, variables x line number
    data = np.zeros(shape=(file_len,len(subs)-1))

    #Run through the length of the file and append the data to the datapoint structure
    for x in range(file_len):
        line = lines[x]
        #Get the locations of the data breaks
        subs = [i for i in range(len(line)) if line.startswith(comma,i)]
        #Assign data to variables
        temp  = float(line[subs[0]+1:subs[1]])
        pres  = float(line[subs[1]+1:subs[2]])
        alt   = float(line[subs[2]+1:subs[3]])
        accx  = float(line[subs[3]+1:subs[4]])
        accy  = float(line[subs[4]+1:subs[5]])
        accz  = float(line[subs[5]+1:subs[6]])
        newdata = [temp,pres,alt,accx,accy,accz]
        # add data to the matrix
        data[x] = newdata

    # Create a vector of the dot product of the accelerations
    acc_vector = []
    for x in range(file_len):
        acc_vector.append(np.sqrt(data[x][3]**2+data[x][4]**2+data[x][5]**2))

    # Vector of altitude
    alt_vector = data[:,2]

    # Create x vector for graph and convert to seconds
    x1 = np.linspace(0,file_len,file_len)
    x1 = [i * FACTOR for i in x1]

    #Build the figure
    ax1.plot(x1,alt_vector,label=filename)
    ax1.set_ylabel("Height above Sea Level (m)")
    ax2.plot(x1,acc_vector,label=filename)
    ax2.set_ylabel("Acceleration (m/s^2)")
    ax2.set_xlabel("Data Points")
    ax1.legend()
    ax2.legend()

    # Transmit the interesting characteristics
    generate_statement(filename, np.max(acc_vector),np.max(alt_vector))

# Generates final statement for launch statistics
def generate_statement(filename,max_g,max_h):
    print("===\nStatistics about launch from ", filename, "file.\n===")
    print("Total Data Points", line_number(filename))
    print("Max Acceleration",max_g, "m/s^2")
    print("Max Height", max_h, "m")
    print("===")
    open(filename, "r").close()

def main():
    # generate_graph("FTSatNoGPS.log")
    for filename in filename_list:
        generate_graph(filename)
    plt.show()

if __name__ == "__main__":
    main()
