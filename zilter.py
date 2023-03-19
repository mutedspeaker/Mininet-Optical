import csv

input_file = "final.txt"
output_file = "output.csv"

with open(input_file, "r") as f_in, open(output_file, "w", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(["t", "ch", "freq", "gOSNR", "OSNR"]) # write header row
    
    for line in f_in:
        # extract fields from line
        fields = line.strip().split()
        t = fields[0]
        ch = int(fields[2][3:]) # extract number from ch field
        freq = float(fields[2][4:-3]) # extract frequency from ch field
        gOSNR = float(fields[7])
        OSNR = float(fields[9])
        
        # write fields to CSV
        writer.writerow([t, ch, freq, gOSNR, OSNR])
