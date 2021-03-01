import csv
headers = []
with open('s&p500_new_no_words.csv', 'r', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i = 0
    for row in reader:
        if i == 0:
            headers = row
            with open('s&p500_new_fixed_row.csv', 'w', newline="\n") as csvfile2:
                writer = csv.writer(csvfile2, delimiter=',')
                writer.writerow(headers)
            i+=1
            continue
        if row[2] == 'words':
            row.insert(2, 'unknown')
        with open('s&p500_new_fixed_row.csv', 'a', newline="\n") as csvfile2:
            writer = csv.writer(csvfile2, delimiter=',')
            writer.writerow(row)
