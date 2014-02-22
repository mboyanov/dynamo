import re
cs1="T[0]=values[0]"
cs2="T[i]=max(T[i-1]+values[i],values[i]) for i in 1:n"


fibonnaci1="T[0]=1"
fibonnaci2="T[1]=1"
fibonnaci3="T[i]=T[i-1]+T[i-2] for i in 2:n"

makingchange1="T[0]=0"
makingchange2="T[i]= min(T[i-values[item]]+1) for i in 1:C where values[item]<=i"

lis0="default=1"
lis1="T[0]=1"
lis2="T[i]=max(T[j]+1) for i in 1:n where j<i and values[j]<values[i]"

try2d="T[i][j]=1 for i in 1:n for j in  1:n"

values=[1,2]
arrays={}
size=2
arrays['values']=[1,2,-4,5,-3,10]
C=10
n=len(arrays['values'])

T=[0]*len(arrays['values'])

def splitFunction(t):
  a,b,c=(t.find('='),t.find('('),t.rfind(')'))
  item=t[:a]
  function=t[a+1:b]
  value=t[b+1:c]
 # print value
  return item,function,value
  


def hasForClause(t):
  t=re.search("for",t)
  if t is None:
    return False
  return True

def hasWhereClause(t):
  t=re.search("where",t)
  if t is None:
    return False
  return True



def removeWhiteSpace(t):
  t=re.sub(' +',' ',t)
  t=re.sub('\[ ','[',t)
  t=re.sub('\s?\]',']',t)
  t=re.sub('\s?\(\s?','(',t)
  t=re.sub('\s?\)',')',t)
  t=re.sub('\s?\+\s?','+',t)
  t=re.sub('\s?-\s?','-',t)
  t=re.sub('\s?\*\s?','*',t)
  return t

def massSplit2(t,arrays,constants,twod):
  t=removeWhiteSpace(t)
  for i in arrays.keys():
    t=t.replace(i,'arrays[\''+i+'\']')
  if twod:
    return massSplitTwoD(t)
  else:
    return massSplitOneD(t,constants,arrays)
  
def massSplitOneD(command,constants,arrays):
    
    equalsignindex=re.search('=',command)
    print command
    left=command[:equalsignindex.start()]
    right=command[equalsignindex.end():]
    if 'where' in command.lower():
      right= massSplitOneDWhere(right,left,constants,arrays)
      return right
    elif 'for' in command.lower():
      return massSplitOneDFor(right,left,constants,arrays)
    else:
      #TODO: more checking
      return command

def extractLeftParameter(left,constants=[],arrays={}):
  parameterindex=re.search('\[.*\]',left) 
  
  if parameterindex is None:
    if 'answer' in left or 'default' in left:
      return -1 #no parameter=>this is an answer line or a default line
    else:
      raise Exception("Missing [ or ] in "+left)
  else:
    parameter=left[parameterindex.start()+1:parameterindex.end()-1]
    try:
      if int(parameter) is not None:
	return -1 #parameter is integer for example T[0] has parameter 0
    except ValueError:
      for c in constants:
	if parameter==c:
	  return -1 #parameter is a defined constant for the problem.
      if 'arrays' in parameter:
	parameterindex=re.search('\[.*\]',parameter)
	if parameterindex is None:
	  raise Exception('Missing [ or ]')
	parameter=parameter[parameterindex.start()+1:parameterindex.end()-1]
	found=False
	for name in arrays.keys(): #Find the array in question
	  if name in parameter:
	    found=True
	    parameterindex=re.search('\[.*\]',parameter)
	    if parameterindex is None:
	      raise Exception('Missing [ or ]')
	    parameter=parameter[parameterindex.start()+1:parameterindex.end()-1]
	    try:
	      if int(parameter) is not None:
		return -1  #example : T[arrays[values[3]]]
	    except ValueError:
	      for c in constants:
		if parameter==c:
		  return -1 #example: T[arrays[values[N]]]
	if not found:
	  raise Exception("Unknown array "+parameter)
      return parameter
    
    



def massSplitOneDFor(command,left,constants=[],arrays={}):
  forindex=re.search("for",command)
  forclause=command[forindex.start():]
  function=command[:forindex.start()-1]
  param=extractLeftParameter(left,constants,arrays)
  if param!=-1:
    paramindex=re.search('\s'+param+'\s',forclause)
    if paramindex is None:
      raise Exception('undefined loop parameter '+param+" in "+left+"="+command)
  forclause=re.sub(':',',',forclause)
  rangeindex=re.search('\s+[^\s]+,[^\s]+\s*',forclause)
  forclause=forclause[:rangeindex.start()]+' range('+forclause[rangeindex.start()+1:rangeindex.end()]+'):'
  forclause+="\n\t"+left+"="+function
  return forclause
 
 
 
def massSplitOneDWhere(command,left,constants=[],arrays={}):
  whereindex=re.search("where",command)
  whereclause=command[whereindex.end():]
  command = command[:whereindex.start()-1]
  forindex=re.search("for",command)
  forclause=command[forindex.start():]
  function=command[:forindex.start()-1]
  param=extractLeftParameter(left,constants,arrays)
  if param!=-1:
    paramindex=re.search('\s'+param+'\s',forclause)
    if paramindex is None:
      raise Exception('undefined loop parameter '+param) 
  forclause=re.sub(':',',',forclause)
  rangeindex=re.search('\s+[^\s]+,[^\s]+\s*',forclause)
  forclause=forclause[:rangeindex.start()]+' range('+forclause[rangeindex.start()+1:rangeindex.end()]+'):'
  (function,argument)=extractFunctionAndArgument(function)
  forclause=forclause+'\n\targuments=[]\n\tfor item in range(n):\n\t\tif '+whereclause+":"
  forclause+="\n\t\t\targuments.append("+argument+")"
  forclause+="\n\t\ttry:"
  forclause+="\n\t\t\t"+left+"="+function+"(arguments)"
  forclause+="\n\t\texcept(ValueError):"
  forclause+="\n\t\t\t"+left+"="+"default"
  return forclause


def extractFunctionAndArgument(function):
  argumentindex=re.search('\(.*\)',function)
  if argumentindex is None:
    raise Exception("Missing ( or ) in " + function)
  effectivefunction = function[:argumentindex.start()]
  if 'min' not in effectivefunction and 'max' not in effectivefunction:
    raise Exception("Outside function needs to be min or max")
  argument=function[argumentindex.start()+1:argumentindex.end()-1]
  return (effectivefunction,argument)
  
def massSplitTwoD(command):
  
  return None

def extractArgument(forclause):
  forindex=re.search('for',forclause)
  withoutfor=forclause[forindex.end():]
  argindex=re.search('\s[^\s]*\s',withoutfor)
  arg=withoutfor[argindex.start()+1:argindex.end()-1]
  return arg


def extract(value,string,arrays,cellvalue):
  forindex=re.search('for',string)
  if not forindex:
    return string
  forclause=string[forindex.start():]
  function=string[string.find('=')+1:forindex.start()]
  #print function
  string=string[:forindex.start()]
  arg=extractArgument(forclause)
  t=re.finditer('\W'+arg+'\W',string)
  newstring=""
  start=0
  while True:
    try:
      match=t.next()
      newstring+=string[start:match.start()+1]+str(value)
      start=match.end()-1
    except:
      newstring+=string[match.end()-1:]
      break;
    
  return newstring

def extract2d(value,value2,string,arrays):
  forindex=re.search('for',string)
  if not forindex:
    return string
  forclause=string[forindex.start():]
  string=string[:forindex.start()]
  arg=extractArgument(forclause)
  t=re.finditer('\W'+arg+'\W',string)
  newstring=""
  start=0
  while True:
    try:
      match=t.next()
      newstring+=string[start:match.start()+1]+str(value)
      start=match.end()-1
    except:
      newstring+=string[match.end()-1:]
      break;
      
  return newstring


def answerLine(command):
  return command




#print massSplit2('T[0]=1   +   2',{})

#print massSplit2('T[   0   ]=1   +   2',{})
#print massSplit2('T[   0   ] =1   +   2',{})
#print massSplit2('T[   0   ] =1   *   2',{})
print(extractLeftParameter('T[0]'))
arrays={'values':5}
constants=['C']
assert(extractLeftParameter('T[arrays[values[2]]]',arrays=arrays)==-1)
assert(extractLeftParameter('T[arrays[values[C]]]',arrays=arrays,constants=constants)==-1)

assert(extractLeftParameter('T[0]')==-1)
assert(extractLeftParameter('T[i]')=='i')
assert(extractLeftParameter('T[C]',constants=constants)==-1)
assert(extractLeftParameter('answer')==-1)


assert(extractFunctionAndArgument('min(T[j]+1)')==('min','T[j]+1'))
assert(massSplitOneDFor('T[i-1]+1 for i in 1:N','T[i]')=='for i in range(1,N):\n\tT[i]=T[i-1]+1')
print massSplitOneD(makingchange2,[],{})
print massSplitOneD(lis2,[],{})

#s="T[i]=T[i-1]+1 for i in 1:N"
#s1="T[0]=1"
#massSplit2(lis2,arrays)
#s2="T[i]= min(T[i-values[j]]+1) for i in 1:C where values[j]<=i"
##T[i][j]=min(T[i-1][j]+1,T[i][j-1]+1,T[i-1][j-1]+(word1[i-1]!=word2[j-1])) for i in 1:n+1 for j in 1:n+1
#import operator
#n=len(arrays['values'])
#T=[0]*100
#backpointers=[0]*100
#exec( massSplit2(lis0,arrays))	       
#exec( massSplit2(lis1,arrays))
#exec( massSplit2(lis2,arrays))

#exec(massSplit(makingchange1))
#exec(massSplit(makingchange2))