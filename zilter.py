import csv
from decimal import Decimal, getcontext
input_file = "final.txt"
output_file = "output.csv"
getcontext().prec = 10
with open(input_file, "r") as f_in, open(output_file, "w", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(["t", "ch", "freq", "gOSNR", "OSNR"]) # write header row
    
    for line in f_in:
        # extract fields from line
        fields = line.strip().split()
        t = fields[0]
        try:
        	ch = int(fields[2][3:5])
        except:
        	ch = int(fields[2][3:4])
        gOSNR = Decimal(fields[8])
        OSNR = Decimal(fields[11])
        
        # write fields to CSV
        writer.writerow([ch, gOSNR, OSNR])
