import myparser
def solve(arrays,constants,commands,x,y):
    for key in constants:
      exec(key+"="+str(constants[key]))
    T=[0]*20
    print arrays=={}
    default=0
    if (arrays=={})==False:
      n=len(arrays[arrays.keys()[0]])
    for command in commands:
      command=myparser.massSplit(command,arrays)
      print command
      exec(command)
    print T
    return T
