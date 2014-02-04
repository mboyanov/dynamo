import random
def getRandomConstants(t):
  if t is None:
    return {}
  text="t="+t;
  exec(text)
  constants={}
  for a in t:
    print a
    constants[a[0]]=random.randint(a[1],a[2])
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
      arrays[entry[0]].append(random.randint(entry[2],entry[3]))
  print arrays
  return arrays