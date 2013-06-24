import csv

'''
open the hand-cleaned csv file and pluck out just the columns we need
for an FFS schema, mostly ignoring the ID field
'''

csvfile = open("nbi.csv", "r")
reader=csv.reader(csvfile)

outfile = open("nbi_record_format.csv", "w")
writer = csv.writer(outfile)

writer.writerow(['column','start','length'])

for row in reader:
    column = row[1]
    start = row[2]
    length = row[3]
    line = column, start, length
    writer.writerow(line)

csvfile.close()
outfile.close()    