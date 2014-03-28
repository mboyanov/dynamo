import random

words=['apple','trap','door','floor','desk','task','chair','hair','fair','appleton','maple','tone','complex','flex','computer','butter','utter','staple']


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
        if len(entry)>=5:
            if entry[4]=='addone':
                if 1 not in arrays[entry[0]]:
                    arrays[entry[0]].append(1)
            elif entry[4]=='characters':
                arrays[entry[0]]=[]
                wordindex=random.randint(0,len(words)-1)
                word=words[wordindex]
                for i in range(len(word)):
                    arrays[entry[0]].append(word[i])

    return arrays