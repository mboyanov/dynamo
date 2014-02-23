import re
from ParserException import ParserException
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

def splitFunction(function):
  b,c=(function.find('('),function.rfind(')'))
  value=function[b+1:c]
  function=function[:b]

 # print value
  return function,value


def removeWhiteSpace(t):
  t=re.sub(' +',' ',t)
  t=re.sub('\[ ','[',t)
  t=re.sub('\s?\]',']',t)
  t=re.sub('\s?\(\s?','(',t)
  t=re.sub('\s*\)',')',t)
  t=re.sub('\s?\+\s?','+',t)
  t=re.sub('\s?-\s?','-',t)
  t=re.sub('\s?\*\s?','*',t)
  return t

def massSplit2(t,arrays,constants,twod):
  t=removeWhiteSpace(t)
  for i in arrays.keys():
    t=t.replace(i,'arrays[\''+i+'\']')
  if twod:
    return massSplitTwoD(t,constants,arrays)
  else:
    return massSplitOneD(t,constants,arrays)
  
def massSplitOneD(command,constants,arrays):
    
    equalsignindex=re.search('=',command)
    if equalsignindex is None:
        raise ParserException("Improper syntax : no '=' sign detected in line "+command)
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


def checkParameter(parameter,constants=[],arrays={}):
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
                raise ParserException('Missing [ or ]')
            parameter=parameter[parameterindex.start()+1:parameterindex.end()-1]
            found=False
            for name in arrays.keys(): #Find the array in question
                if name in parameter:
                    found=True
                    parameterindex=re.search('\[.*\]',parameter)
                    if parameterindex is None:
                        raise ParserException('Missing [ or ]')
                    parameter=parameter[parameterindex.start()+1:parameterindex.end()-1]
                    try:
                        if int(parameter) is not None:
                            return -1  #example : T[arrays[values[3]]]
                    except ValueError:
                        for c in constants:
                            if parameter==c:
                                return -1 #example: T[arrays[values[N]]]
            if not found:
                raise ParserException("Unknown array "+parameter)
    return parameter


def extractLeftParameter(left,constants=[],arrays={}):
    parameterindex=re.search('\[.*\]',left)
    if parameterindex is None:
      if 'answer' in left or 'default' in left:
          return -1 #no parameter=>this is an answer line or a default line
      else:
          raise ParserException("Missing [ or ] in "+left)

    parameter=left[parameterindex.start()+1:parameterindex.end()-1]
    parameter=checkParameter(parameter,constants,arrays)
    return parameter


def massSplitOneDFor(command,left,constants=[],arrays={}):
  forindex=re.search("for",command)
  forclause=command[forindex.start():]
  function=command[:forindex.start()-1]
  param=extractLeftParameter(left,constants,arrays)
  if param!=-1:
    paramindex=re.search('\s'+param+'\s',forclause)
    # if paramindex is None:
    #   raise ParserException('undefined loop parameter '+param+" in "+left+"="+command)
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
    # if paramindex is None:
    #   raise ParserException('undefined loop parameter '+param)
  forclause=re.sub(':',',',forclause)
  rangeindex=re.search('\s+[^\s]+,[^\s]+\s*',forclause)
  forclause=forclause[:rangeindex.start()]+' range('+forclause[rangeindex.start()+1:rangeindex.end()]+'):'
  (function,argument)=extractFunctionAndArgument(function)
  bp=left.replace("T","backpointers")
  forclause=forclause+'\n\targuments=[]\n\tfor item in range(n):\n\t\tif '+whereclause+":"
  forclause+="\n\t\t\targuments.append((item,"+argument+"))"
  forclause+="\n\t\ttry:"
  forclause+="\n\t\t\t"+bp+","+left+"="+function+"(arguments, key=operator.itemgetter(1))"
  forclause+="\n\t\texcept(ValueError):"
  forclause+="\n\t\t\t"+left+"="+"default"
  forclause+="\n\t\t\t"+bp+"="+"-1"
  return forclause

def extractFunctionAndArgument(function):
  argumentindex=re.search('\(.*\)',function)
  if argumentindex is None:
    raise ParserException("Missing ( or ) in " + function)
  effectivefunction = function[:argumentindex.start()]
  if 'min' not in effectivefunction and 'max' not in effectivefunction:
    raise ParserException("Outside function needs to be min or max")
  argument=function[argumentindex.start()+1:argumentindex.end()-1]
  return (effectivefunction,argument)

def extractLeftParameterTwoD(left,constants=[],arrays={}):
  parameterindex=re.search('\[.*\]\[.*\]',left)
  if parameterindex is None:
      if 'answer' in left or 'default' in left:
          return (-1,-1) #no parameter=>this is an answer line or a default line
      else:
          raise ParserException("Missing [ or ] in "+left)

  parameter1index=re.search('\[.*\]\[',left)
  parameter1=left[parameter1index.start()+1:parameter1index.end()-2]
  parameter2index=re.search('\]\[.*\]',left)
  parameter2=left[parameter2index.start()+2:parameter2index.end()-1]
  parameter1=checkParameter(parameter1,constants,arrays)
  parameter2=checkParameter(parameter2,constants,arrays)
  return (parameter1,parameter2)



def massSplitTwoDOneFor(left,right,constants=[],arrays={}):
  forindex=re.search("for",right)
  forclause=right[forindex.start():]
  function=right[:forindex.start()-1]
  parameter1,parameter2=extractLeftParameterTwoD(left,constants,arrays)
  if parameter1!=-1:
    paramindex=re.search('\s'+parameter1+'\s',forclause)
    # if paramindex is None:
    #   raise ParserException('undefined loop parameter '+parameter1+" in "+left+"="+right)
  if parameter2!=-1:
    paramindex=re.search('\s'+parameter2+'\s',forclause)
  #   if paramindex is None:
  #     raise ParserException('undefined loop parameter '+parameter2+" in "+left+"="+right)
  forclause=convertForClause(forclause)
  forclause+="\n\t"+left+"="+function
  return forclause


def convertForClause(forclause):
    forclause=re.sub(':',',',forclause)
    rangeindex=re.search('\s+[^\s]+,[^\s]+\s*',forclause)
    forclause=forclause[:rangeindex.start()]+' range('+forclause[rangeindex.start()+1:rangeindex.end()]+'):'
    return forclause


def massSplitTwoDZeroFor(left,right,constants=[],arrays={}):
    parameter1,parameter2 = extractLeftParameterTwoD(left,constants,arrays);
    if parameter1!=-1:
        raise ParserException("Undefined parameter: "+parameter1 )
    if parameter2!=-1:
        raise ParserException("Undefined parameter: "+parameter2 )
    return left+"="+right

def massSplitTwoDTwoFor(left,right,constants=[],arrays={}):
    parameter1,parameter2 = extractLeftParameterTwoD(left,constants,arrays)
    if parameter1==-1 or parameter2==-1:
        raise ParserException("Illegal parameter name in "+left)
    forindex=re.finditer("for",right)
    firstindex=forindex.next()
    secondindex=forindex.next()
    function=right[:firstindex.start()-1]
    forclauses=right[firstindex.start():]
    forclause1=right[firstindex.start():secondindex.start()-1]
    forclause2=right[secondindex.start():]
    paramindex=re.search('\s'+parameter1+'\s',forclauses)
    # if paramindex is None:
    #   raise ParserException('undefined loop parameter '+parameter1+" in "+left+"="+right)
    # paramindex=re.search('\s'+parameter2+'\s',forclauses)
    # if paramindex is None:
    #   raise ParserException('undefined loop parameter '+parameter2+" in "+left+"="+right)
    forclause1=convertForClause(forclause1)
    forclause2=convertForClause(forclause2)
    result=forclause1+"\n\t"+forclause2
    if "min" in function or "max" in function:
        result+="\n\t\targuments=[]"
        function,args=splitFunction(function)
        args=args.split(',')
        result+="\n\t\ttry:"
        for arg in args:
            result+="\n\t\t\targuments.append("+arg+")"
        result+="\n\t\t\t"+left+"="+function+"(arguments)"
        result+="\n\t\texcept:"
        result+="\n\t\t\t"+left+"=default"
    else:
        result+="\n\t\t"+left+"="+function
    return result



def massSplitTwoD(command,constants=[],arrays={}):
  equalsignindex=re.search('=',command)
  if equalsignindex is None:
        raise ParserException("Improper syntax : no '=' sign detected in line "+command)
  left=command[:equalsignindex.start()]
  right=command[equalsignindex.end():]
  result=re.findall("for",right)
  if len(result)==0:
      return massSplitTwoDZeroFor(left,right,constants,arrays)
  elif len(result)==1:
      return massSplitTwoDOneFor(left,right,constants,arrays)
  elif len(result)==2:
      return massSplitTwoDTwoFor(left,right,constants,arrays)
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

def extract2d(values,string,arrays):
    newstring=""
    firstindex=re.search("for",string)
    if not firstindex:
        return string
    newstring=string[:firstindex.start()]
    forindex=re.finditer("for",string)
    if not forindex:
        return string
    iterations=string.count("for")
    for iteration in range(iterations):
        index=forindex.next()
        forclause=string[index.start():]
        arg=extractArgument(forclause)
        print arg
        argiterator=re.finditer('\W'+arg+'\W',newstring)
        while True:
            try:
                arg_index=argiterator.next()
                newstring=newstring[:arg_index.start()+1]+str(values[iteration])+newstring[arg_index.end()-1:]
            except StopIteration:
                break

        print newstring
    return newstring
        # temp=list(t)
        # lent=len(temp)
        # if lent==0:
        #     raise ParserException("Argument "+arg+" never used")
        # t=iter(temp)
        # start=0
        # while True:
        #    try:
        #         match=t.next()
        #         newstring+=string[start:match.start()+1]+str(value)
        #         start=match.end()-1
        #    except:
        #       if match:
        #         newstring+=string[match.end()-1:]
        #       break



    return newstring


def answerLine(command):
  return command




print massSplit2("T[0][i]=0 for i in 1:N",{},[],True)
# print massSplit2("T[i][0]]=0 for i in 1:N",{},[],True)
print massSplit2("T[a][b]=1 for a in 1:N for b in 1:N",{},[],True)

print massSplit2("T[i][j]=min(T[i-1][j]+1,T[i][j-1]+1,T[i-1][j-1]+(word1[i-1]!=word2[j-1])) for i in 1:n+1 for j in 1:n+1",{'word1':[],'word2':[]},[],True)