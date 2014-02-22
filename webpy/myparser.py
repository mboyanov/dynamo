import re
cs1="T[0]=values[0]"
cs2="T[i]=max(T[i-1]+values[i],values[i]) for i in 1:n"


fibonnaci1="T[0]=1"
fibonnaci2="T[1]=1"
fibonnaci3="T[i]=T[i-1]+T[i-2] for i in 2:n"

makingchange1="T[0]=0"
makingchange2="T[i]= min(T[i-values[j]]+1) for i in 1:C where values[j]<=i"

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
  t=re.sub('\s?\]\s?',']',t)
  t=re.sub('\s?\(\s?','(',t)
  t=re.sub('\s?\)\s?',')',t)
  t=re.sub('\s?\+\s?','+',t)
  t=re.sub('\s?-\s?','-',t)
  t=re.sub('\s?\*\s?','*',t)
  return t

def massSplit2(t,arrays):
  t=removeWhiteSpace(t)
  for i in arrays.keys():
    t=t.replace(i,'arrays[\''+i+'\']')
  if 'answer' in t:
    return answerLine(t)
  forclause=None
  whereclause=None
  function=None
  if hasWhereClause(t):
    index=re.search('where',t)
    whereclause=t[index.start():]
    t=t[:index.start()]
  if hasForClause(t):
    index=re.search('for',t)
    forclause=t[index.start():]
    function=t[:index.start()]
  if forclause is None:
    return t
  a=forclause.count('for')
  if a==1:
    rangeindex=re.search( '[a-zA-Z0-9+-]+:[a-z()\[\]\'\'A-Z0-9+-]+',forclause)
    forclause=forclause.replace(':',',')
    forclause=forclause[:rangeindex.start()]+'range('+forclause[rangeindex.start():rangeindex.end()]+'):\n\t'

    if whereclause is None:
      t=forclause+function
    else:
      t=forclause
      whereclause=whereclause[5:]
      (item,function,args)=splitFunction(function)
      bp=item.replace('T','backpointers')
      where="arguments=[]\n\tfor j in range(n):\n\t\tif "+whereclause+":\n\t\t\targuments.append((j,("+args+"))) \n\t\n\ttry:\n\t\t"+bp+","+item+"="+function+"(arguments, key=operator.itemgetter(1))\n\texcept(ValueError):\n\t\t"+item+"=default"
      t+=where
      
  elif a==2:
    rangeindex=re.search( '[a-zA-Z0-9+-]+:[a-z()\[\]\'\'A-Z0-9+-]+',forclause)
    secondfor=forclause[rangeindex.end():]
    forclause=forclause[:rangeindex.start()]+'range('+forclause[rangeindex.start():rangeindex.end()]+')'
    rangeindex=re.search( '[a-zA-Z0-9+-]+:[a-z()\[\]\'\'A-Z0-9+-]+',secondfor)
    secondfor=secondfor[:rangeindex.start()]+'range('+secondfor[rangeindex.start():rangeindex.end()]+')'
    t=forclause.replace(':',',')+':\n\t'+secondfor.replace(':',',')+':\n\t\t'
    
    if whereclause is None:
      (item,function,args)=splitFunction(function)
      if function=='min' or function=='max':
	args=args.split(',')
	where="arguments=[]\n\t\ttry:\n\t\t\t"
	for j in args:
	  where+="arguments.append("+j+")\n\t\t\t"
	where=where[:-1]+'\n\t\texcept:\n\t\t\tprint arguments\n\t\t'
	t+=where
	t+=item+'='+function+'(arguments)'
      else:
	t+=item+'='+function
    else:
      (item,function,args)=splitFunction(function)
      where="arguments=[]\n\t\tfor j in range(n):\n\t\t\tif "+whereclause+":\n\t\t\t\targuments.append("+args+"\n\t\tprint arguments\n\t\ttry:\n\t\t\t"+item+"="+function+"(arguments)\n\t\texcept(ValueError):\n\t\t\t"+item+"=default"
      t+=where
  #print t
  return t


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




print massSplit2('T[0]=1   +   2',{})

print massSplit2('T[   0   ]=1   +   2',{})
print massSplit2('T[   0   ] =1   +   2',{})
print massSplit2('T[   0   ] =1   *   2',{})

s="T[i]=T[i-1]+1 for i in 1:N"
s1="T[0]=1"
massSplit2(lis2,arrays)
s2="T[i]= min(T[i-values[j]]+1) for i in 1:C where values[j]<=i"
#T[i][j]=min(T[i-1][j]+1,T[i][j-1]+1,T[i-1][j-1]+(word1[i-1]!=word2[j-1])) for i in 1:n+1 for j in 1:n+1
import operator
n=len(arrays['values'])
T=[0]*100
backpointers=[0]*100
exec( massSplit2(lis0,arrays))	       
exec( massSplit2(lis1,arrays))
exec( massSplit2(lis2,arrays))

#exec(massSplit(makingchange1))
#exec(massSplit(makingchange2))