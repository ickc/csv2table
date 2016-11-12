#!/usr/bin/env python3
import csv
import sys
from terminaltables import AsciiTable

if __name__ == "__main__":
    with open(sys.argv[1], 'r', newline='') as f:
        data = list(csv.reader(f))
    table = AsciiTable(data)
    table.inner_row_border = True
    table.CHAR_H_INNER_HORIZONTAL = '='
    print(table.table)
