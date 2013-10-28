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
  value=t[b+1:]
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


def massSplit(t,arrays):
  for i in arrays.keys():
    t=t.replace(i,'arrays[\''+i+'\']')
  forclause=None
  whereclause=None
  
  if hasForClause(t):
    index=re.search('for',t)
    forclause=t[index.start():]
    
    function=t[:index.start()]
    if hasWhereClause(forclause):
	index=re.search('where',t)
	whereclause=t[index.start():]
	print whereclause
    rangeindex=re.search( '[a-zA-Z0-9]+:[a-zA-Z0-9]+',forclause)
    forclause=forclause.replace(':',',')
    forclause=forclause[:rangeindex.start()]+'range('+forclause[rangeindex.start():rangeindex.end()]+'):\n\t'
    if whereclause is None:
      t=forclause+function
    else:
      t=forclause
      whereclause=whereclause[5:]
      (item,function,args)=splitFunction(function)
      where="arguments=[]\n\tfor j in range(n):\n\t\tif "+whereclause+":\n\t\t\targuments.append("+args+" \n\tprint arguments\n\ttry:\n\t\t"+item+"="+function+"(arguments)\n\texcept(ValueError):\n\t\t"+item+"=default"
      t+=where
      print t
  return t



#exec( massSplit(lis0))	       
#exec( massSplit(lis1))
#exec( massSplit(lis2))

#exec(massSplit(makingchange1))
#exec(massSplit(makingchange2))