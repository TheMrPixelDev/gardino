import csv
from csv import writer
import datetime

class log:

    def __init__(self, file):
        self.file = file

    def append(self, daten):
        elems = ["[{time}] {data}".format(time=datetime.datetime.now(), data=daten)]
        with open(self.file, "a", newline='') as f:
            csv_writer = writer(f, delimiter=";")
            csv_writer.writerow(elems)
            f.close()

    def read_everything(self):
        with open(self.file, "r") as f:
            reader = csv.reader(f, delimiter=";")
            liste = []
            for row in reader:
                liste.append(row)
            f.close()
        return liste

    def read_limited(self, count):
        logs = self.read_everything()
        logs.sort(reverse=True)
        liste = []
        counter = 0
        for row in logs:
            if counter < count:
                liste.append(row)
                counter = counter + 1
            else:
                break
        return liste