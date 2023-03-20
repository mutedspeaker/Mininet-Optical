import csv
from decimal import Decimal, getcontext

input_file = "final.txt"
output_file = "output.csv"
getcontext().prec = 10

with open(input_file, "r") as f_in, open(output_file, "a", newline="") as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    
    # check if any channel is missing from 1 to 90
    existing_ch = set()
    for row in reader:
        ch = int(row[2][3:5] if len(row[2]) == 5 else row[2][3:4])
        existing_ch.add(ch)
    missing_ch = sorted(set(range(1, 91)).difference(existing_ch))
    
    # append missing channels to the output file with gOSNR and OSNR as 0
    for ch in missing_ch:
        writer.writerow([ch, Decimal(0), Decimal(0)])
    
    # write existing fields to CSV
    f_in.seek(0)  # reset file pointer to beginning
    next(reader)  # skip header row
    for row in reader:
        ch = int(row[2][3:5] if len(row[2]) == 5 else row[2][3:4])
        gOSNR = Decimal(row[8])
        OSNR = Decimal(row[11])
        writer.writerow([ch, gOSNR, OSNR])
