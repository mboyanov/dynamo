__author__ = 'marty'
import myparser2
import random
import re

commands=["T[0]=0","T[i]=T[i-1]+1 for i in 1:n"]

class splitter:
    def __init__(self,istwod):
        self.forclauses=set()
        self.functions=set()
        self.whereclauses=set()
        if (istwod):
            self.lefts=set(["T[0][0]","T[i][j]","T[j][i]"])
        else:
            self.lefts=set(["T[0]","T[i]"])

    def split(self,commands):
        for command in commands:
            left,right=myparser2.getLeftRight(command)
            function,forclause,whereclause=myparser2.getClauses(right)
            if whereclause is not None:
                whereclause="where "+whereclause
            self.lefts.add(left)
            self.functions.add(function)
            self.whereclauses.add(whereclause)
            self.forclauses.add(forclause)
            for i in range(3):
                iterator=re.finditer("\d+",left)
                try:
                    iteration=iterator.next()
                    number=int(left[iteration.start():iteration.end()])
                    newnumber=random.randint(0,(number+2)*2)
                    self.lefts.add(left[:iteration.start()]+str(newnumber)+left[iteration.end():])
                except:
                    continue
            for i in range(3):
                iterator=re.finditer("\d+",function)
                try:
                    iteration=iterator.next()
                    number=int(function[iteration.start():iteration.end()])
                    newnumber=random.randint(0,(number+2)*2)
                    self.functions.add(function[:iteration.start()]+str(newnumber)+function[iteration.end():])
                except:
                    pass
            if forclause is not None:
                for i in range(3):
                    iterator=re.finditer("\d+",forclause)
                    try:
                        iteration=iterator.next()
                        number=int(forclause[iteration.start():iteration.end()])
                        newnumber=random.randint(0,(number+2)*2)
                        self.forclauses.add(forclause[:iteration.start()]+str(newnumber)+forclause[iteration.end():])
                    except:
                        pass
            if whereclause is not None:
                for i in range(3):
                    iterator=re.finditer("\d+",forclause)
                    try:
                        iteration=iterator.next()
                        number=int(whereclause[iteration.start():iteration.end()])
                        newnumber=random.randint(0,(number+2)*2)
                        self.whereclauses.add(whereclause[:iteration.start()]+str(newnumber)+whereclause[iteration.end():])
                    except:
                        pass
        return self.lefts,self.functions,self.forclauses,self.whereclauses

#msplitter=splitter(False)
#print msplitter.split(commands)