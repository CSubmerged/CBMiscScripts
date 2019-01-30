import csv
import os
import re

def listOfLists2Csv(list):
    with open("output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(list)

def csvFiller():
    with open("editedOutput.csv", "w", newline="") as mainf:
        with open("output.csv", "r") as file:
            start = True
            previous = ""
            for line in file:
                if start:
                    start = False
                    previous = line
                else:
                    a = previous.split(',')
                    z = line.split(',')
                    between = int(z[0]) - int(a[0])
                    increase_per_sec = (int(z[1]) - int(a[1])) / between
                    index = 0
                    for sec in range(int(a[0]), int(z[0])):
                        val = str(int(round(int(a[1]) + (index * increase_per_sec))))
                        mainf.write(str(sec) + ',' + val + '\n')
                        index += 1
                    previous = line

def main():
    # list = [[time, value],[time, value],...]
    # listOfLists2Csv(list)
    csvFiller()
    return

main()