import myparser
from customlist import *
import operator
def solve(arrays,constants,commands,x,y):
    answer=None
    for key in constants:
      exec(key+"="+str(constants[key]))
    if x==1:
      T=[None]*y
      P=[None]*y
    else:
      T=CustomList2D([])
      P=CustomList2D([])
      for i in range(x):
	T.append([None]*y)
	P.append([None]*y)
    backpointers=[None]*100
    default=0
    if (arrays=={})==False:
      n=len(arrays[arrays.keys()[0]])
    for command in commands:
      if 'import' in command or 'exec' in command:
	return None
      #print command
      parsedcommand=myparser.massSplit2(command,arrays)
      print parsedcommand
      print "before",T
      
      exec(parsedcommand)
      print "after",T
      if x==1:
	for j in range(y):
	  if P[j] is None and T[j] is not None:
	    P[j]=myparser.extract(j,command,arrays,T[j])
	    if backpointers[j]:
	      P[j]+= "and correct item is item number "+str(backpointers[j])
      else:
	for i in range(x):
	  for j in range(y):
	    if P[i][j] is None and T[i][j] is not None:
	      P[i][j]=myparser.extract2d(i,j,command,arrays)
	      
    #print T
    #print P
    return T,P,answer

T=[[0]*5]*5
ed1="for i in range(0,n):\n\tT[0][i]=i" 
