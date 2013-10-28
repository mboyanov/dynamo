import random
def getRandomConstants(t):
  if t is None:
    return {}
  text="t="+t;
  exec(text)
  constants={}
  for a in t:
    print a
    constants[a[0]]=random.randint(1,a[1])
  return constants
  
def getRandomArrays(t):
  if t is None:
    return {}
  text="t="+t;
  exec(text)
  arrays={}
  for entry in t:
    arrays[entry[0]]=[]
    for n in range(entry[1]):
      arrays[entry[0]].append(random.randint(1,entry[2]))
  print arrays
  return arrays