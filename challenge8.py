"""https://adventofcode.com/2018"""
from time import time
from numpy import matrix

import sys

class Day8:
    """https://adventofcode.com/2018/day/8"""
    def __init__(self, filename="input/2018_8.txt", run=False):
        self.filename = filename

        if run:
            self.time = time()
            res = self.total_metadata()
            print("CHALLENGE 2018.8.1: "+str(res))

            #res = self.ex_2()
            #print("CHALLENGE 2018.8.2: "+str(res))

            time_taken = time()-self.time
            print("TIME TAKEN %s sec" % time_taken)

    def extract_metadata(self, nodes, brothers=[], extra_entries=[], metadata=[]):
        """Auxiliar function to extract metadata from file"""
        print(nodes, brothers, extra_entries, metadata)
        if not nodes or len(nodes) == sum(extra_entries):
            return metadata + nodes

        childs = int(nodes[0])
        entries = int(nodes[1])

        if childs > 0:
            if brothers:
                brothers = brothers[:-1] if brothers[-1]==0 else brothers
            print('ONE')
            return self.extract_metadata(nodes[2:], brothers+[childs-1], extra_entries+[entries], metadata)

        if brothers:
            if brothers[-1]>0:
                metadata += nodes[2:2+entries]
                brothers[-1] = brothers[-1]-1
                print('TWO')
                return self.extract_metadata(nodes[2+entries:], brothers, extra_entries, metadata)
            brothers = brothers[:-1]

        if extra_entries:
            metadata += nodes[2:2+entries+extra_entries[-1]]
            print('THREE')
            return self.extract_metadata(nodes[2+entries+extra_entries[-1]:], brothers, extra_entries[:-1], metadata)

        metadata += nodes[2:2+entries]
        print('FOUR')
        return self.extract_metadata(nodes[2+entries:], brothers, extra_entries, metadata)

    @staticmethod
    def parse_data(filename):
        """Auxiliar function to parse data file into dict and array"""
        data = sorted(open(filename, "r"))
        for line in data:
            return line.split()

    def total_metadata(self):
        """CHALLENGE 8.1 - xx"""
        nodes = self.parse_data(self.filename)
        metadata = self.extract_metadata(nodes)

        print(metadata)
        total = 0
        for data in metadata:
            total += int(data)

        return total

    def ex_2(self):
        """CHALLENGE 8.2 - xx"""
        return self.parse_data(self.filename)

if __name__ == "__main__":
    pass
#    Day8(run=True, filename='test.txt')
#    Day8(run=True, filename='test2.txt')
#    Day8(run=True, filename='test3.txt')
#    sys.setrecursionlimit(4200)
#    Day8(run=True)
