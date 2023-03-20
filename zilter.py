import csv
from decimal import Decimal, getcontext
input_file = "final.txt"
output_file = "output.csv"
getcontext().prec = 10
with open(input_file, "r") as f_in, open(output_file, "w", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(["ch", "gOSNR", "OSNR"]) # write header row
    
    prev_ch = None # to keep track of previous channel value
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
        
        # check if current ch is missing and add with gOSNR and OSNR as 0
        if prev_ch is not None and ch != prev_ch + 1:
            for i in range(prev_ch + 1, ch):
                writer.writerow([i, 0, 0])
                
        # write fields to CSV
        writer.writerow([ch, gOSNR, OSNR])
        prev_ch = ch # update previous channel value
       
        # add missing channels after the last one up to 90
        if ch == 90:
            break
        if prev_ch is None:
            for i in range(1, ch):
                writer.writerow([i, 0, 0])
            prev_ch = ch
