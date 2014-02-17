import myparser
from customlist import *
def solve(arrays,constants,commands,x,y):
    for key in constants:
      exec(key+"="+str(constants[key]))
    if x==1:
      T=[None]*y
      P=[None]*y
    else:
      T=CustomList2D([])
      for i in range(x):
	T.append([None]*y)
    print arrays=={}
    default=0
    if (arrays=={})==False:
      n=len(arrays[arrays.keys()[0]])
    for command in commands:
      command=myparser.massSplit2(command,arrays)
      print command
      
      
      exec(command)
      
    
    return T


