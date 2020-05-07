

from sys import argv
import csv


class Table(object):

    def __init__(self, input_file_name, output_file_name):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.chromosome_dictionary = {}

    def read_result(self):
      
        with open(self.input_file_name, 'r') as in_file:
            num_of_chromosomes= in_file.readline()
            for i in range(int(num_of_chromosomes)):
               tempList = in_file.readline().split(';')
               self.chromosome_dictionary[tempList[0]] =int(tempList[1]) 
            global fields
            fieldnames = ["qseqid","sseqid","header","pident" ,"qlen"," mismatch","qstart", "qend","sstart", "sstop","evalue","bitscore"]

            blast_reader = csv.DictReader(in_file, delimiter='\t', fieldnames=fieldnames)
            file_contents = [] 
            for i in blast_reader:
                file_contents.append(i)
            fields = len(file_contents[0])
            return file_contents

    def write_gff(self):

        with open(self.output_file_name, 'w+') as gff_out:
            fieldnames = ["header", "blastresult", "hit", "start", "stop", "score", "orientation", "period", "ID"]
            read_results = self.read_result()
            gff_writer = csv.DictWriter(gff_out, delimiter='\t', fieldnames=fieldnames)
            iterator = 1
            for i in read_results:
                start = i["sstart"]
                stop = i["sstop"]
                tempArray = i['qseqid'].split(':')
                header = tempArray[0]
                numReads = int(tempArray[1])
                color = self.getColor(numReads)
                gff_writer.writerow({"header":i["sseqid"],
                                    "blastresult": "blast_result",
                                    "hit": "hit",
                                    "start": min(int(i["sstart"]),int( i["sstop"])),
                                    "stop": max(int(i["sstart"]),int( i["sstop"])),
                                    "score": ".",
                                    "orientation": self.orientation(start,stop),
                                    "period": ".",
                                    "ID": self.number_of_fields(fields, i, iterator,color,numReads,i['sseqid'],start)})


    def orientation(self, start, end):
        if int(start) < int(end):
            return "+"
        return "-"


    def number_of_fields(self, amount, i, iterator,color,numReads,header,start):
        color
        if amount < 4:
            return "ID=%s;Parent=%s" % (i["header"] + "_%s" % iterator, i["header"])
        elif amount < 6:
            return "ID=%s;Parent=%s;QueryStart=%s;QueryStop=%s" % (i["header"] + "_%s" % iterator, i["header"],
                                                                   i["qstart"], i["qstop"])
        return "ID=%s;Parent=%s;QueryLength=%s;QueryStart=%s;QueryStop=%s;Bitscore=%s;NumberOfReads=%s;color=%s;distanceToNearestEnd=%s" % \
                   (i["qseqid"] + "_%s" % iterator, i["sseqid"], i["qlen"], i["qstart"], i["qend"],
                     i["bitscore"],numReads,color,self.getDistance(int(start),header))

    def getDistance(self,sstart,chromosome):
        return min(sstart-1,self.chromosome_dictionary[chromosome]-sstart)

    def getColor(self,numReads):
        colors = {
            1:"#0000FF",
            2:"#1C00E2",
            3:"#3800C6",
            4:"#5500AA",
            5:"#71008D",
            6:"#8D0071",
            7:"#AA0055",
            8:"#C60038",
            9:"#E2001C",
            10:"#FF0000"
        }
        if(numReads <=10):
            return colors[numReads]
        else:
            return "#FF0000"
if __name__ == "__main__":
    infile = argv[1]
    outfile = argv[2]
    listprint = Table(infile, outfile)
    listprint.write_gff()