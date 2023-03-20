import csv
from decimal import Decimal, getcontext

input_file = "final.txt"
output_file = "data.csv"
getcontext().prec = 10

with open(input_file, "r") as f_in, open(output_file, "w", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(["ch", "gOSNR", "OSNR"]) # write header row
    
    prev_ch = None # to keep track of previous channel value
    missing_channels = [] # to store missing channels
    
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
        
        if t == 't1':
            if prev_ch is not None and ch != prev_ch + 1:
                # add missing channels to list
                for i in range(prev_ch + 1, ch):
                    missing_channels.append(i)
            # write fields to CSV
            writer.writerow([ch, gOSNR, OSNR])
            prev_ch = ch # update previous channel value
            
            # check if last channel has been reached
            if ch == 90:
                # add missing channels from list with gOSNR and OSNR equal to 0
                for i in missing_channels:
                    writer.writerow([i, 0, 0])
                # clear missing_channels list for next iteration
                missing_channels = []
                # reset prev_ch to None to start over for next t = 't1' iteration
                prev_ch = None
        else:
            # write fields to CSV for t != 't1'
            writer.writerow([ch, gOSNR, OSNR])
            prev_ch = ch # update previous channel value
