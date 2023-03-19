import csv

input_file = "final.txt"
output_file = "output2.csv"

with open(input_file, "r") as f_in, open(output_file, "w", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(["t", "ch", "freq", "gOSNR", "OSNR"]) # write header row
    
    for line in f_in:
        # extract fields from line
        fields = line.strip().split()
        t = fields[0]
        try:
        	ch = int(fields[2][3:5]) # extract number from ch field
        except:
        	ch = int(fields[2][3:4])
        try:
        	freq = float(fields[2][5:-4]) # extract frequency from ch field

        except:
        	freq = float(fields[2][6:-4]) # extract frequency from ch field
        #freq = float(fields[2][5:-4]) # extract frequency from ch field
        gOSNR = float(fields[8])
        OSNR = float(fields[11])
        
        # write fields to CSV
        writer.writerow([t, ch, freq, gOSNR, OSNR])
