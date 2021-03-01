import csv
import re
csvfile = open('s&p500_new.csv', 'r')
string = csvfile.read()

new_text = re.sub("\".*\"", "words", string)

csvfile.close()

new_csvfile = open('s&p500_new_no_words.csv', 'w')
new_csvfile.write(new_text)
new_csvfile.close()
