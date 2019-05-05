#!/usr/bin/env python3.7
#----------------------------------------------------------------------------------
# minirdapc
#
# (c) carlos@xt6.us
# 
# Changed: 2019-03-14
#----------------------------------------------------------------------------------

import click
import csv
import ipaddr

from minirdapc import *

if __name__ == "__main__":
    print("Enriching CSV file")

    csvfile = open("input.csv", "r")
    outfile = open("output.csv", "w")

    csvin = csv.reader(csvfile, dialect="excel", delimiter="|")
    csvout = csv.writer(outfile, dialect='excel', delimiter='|')

    rdapc = rdap_client("https://rdap.lacnic.net/rdapt2/", \
            w_apikey="1d72e332-ed44-4234-bc45-6bde980d2705-a09732ff-0746-4d95-986a-a5111890c6ba"
            )

    header = next(csvin, None)
    # csvout.writerow(header)
    for line in csvin:
        # print(line)
        newline = []
        for field in line:
            try:
                n4 = ipaddr.IPv4Network(field)
                orgid = rdapc.prefixToOrgid(field)
                newline.append(field)
                newline.append(orgid)
            except:
                # raise
                newline.append(field)
                next
        ## end for
        print(newline)
        csvout.writerow(newline)
    ## end for

    csvfile.close()
    outfile.close()

# END SCRIPT ######################################################################