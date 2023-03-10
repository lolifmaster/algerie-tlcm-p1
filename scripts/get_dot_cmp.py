import openpyxl
import csv
from collections import defaultdict


def run(file):
    path = f'static/{file}'
    END_OF_FILE = 'Total Sans Region'
    wb_obj = openpyxl.load_workbook(path)
    sheet_obj = wb_obj.worksheets[1]

    DOT = defaultdict(list)

    for cell in sheet_obj.iter_rows(min_row=13, min_col=1, max_col=2):
        dot, cmd = tuple(map(lambda item: item.value, cell))
        if dot == END_OF_FILE:
            break
        if cmd:
            DOT[dot].append(cmd)
    wb_obj.close()

    with open('static/DOTS.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for dot in DOT:
            DOT[dot].insert(0, dot)
            writer.writerow(DOT[dot])
