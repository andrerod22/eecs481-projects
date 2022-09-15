import sys
import math
import operator

class Ochiai:
    def __init__(self):
        self.num_failures = 0
        self.lines = list()
        self.passes = {}
        self.failures = {}
        self.results = {}
        self.extract_file()
        print(self.inspect_file())

    def extract_file(self):
        for f in sys.argv[1:]:
            # breakpoint()
            extracted_lines = None
            with open(f) as gcov_file:
                extracted_lines = gcov_file.read().split('\n')
                    
            for l in extracted_lines:
                if l == None: continue
                try: is_num = int(l.split(':')[0].split(' ')[-1])
                except (TypeError, ValueError): continue
                loc = int(l.split(':')[1].split(' ')[-1])
                #if loc == 100: 
                    #breakpoint()
                    #print("hey")
                if loc not in self.lines:
                    self.lines.append(loc)
                
                if 'pass' in f: 
                    if self.passes.get(loc) != None:
                        self.passes[loc] += 1
                    else:
                        self.passes[loc] = 1
                elif 'fail' in f:
                    if self.failures.get(loc) != None:
                        self.failures[loc] += 1
                    else:
                        self.failures[loc] = 1
            self.num_failures = self.num_failures + 1 if 'fail' in f else self.num_failures
    
    def inspect_file(self):
        #Calculate suspicion based on the lines we parsed:
        for l in self.lines:
            #Undefined
            denominator = 0
            try: math.sqrt(self.num_failures * (self.failures[l] + self.passes[l]))
            except(KeyError): 
                if self.failures.get(l) == None:
                    self.failures[l] = 0
                else:
                    self.passes[l] = 0
            denominator = math.sqrt( self.num_failures * (self.failures[l] + self.passes[l]))
            if(denominator == 0): continue
            self.results[l] = self.failures[l] / math.sqrt(self.num_failures * (self.failures[l] + self.passes[l]))

        descending_order = sorted(self.results.items(), key=operator.itemgetter(0), reverse=False)
        descending_order = sorted(descending_order, key=operator.itemgetter(1), reverse=True)
        #descending_order = sorted(self.results.items(), key=lambda kv: -kv[1])
        return descending_order[:100]


def main():
    Ochiai()
if __name__ == '__main__':
    main()