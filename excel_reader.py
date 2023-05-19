import csv
import datetime

with open('excel/tool_csv.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        old_date = row[1].split("/")
        new_date = (".").join(old_date)
        row[1] = new_date
