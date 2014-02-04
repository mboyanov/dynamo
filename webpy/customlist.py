class CustomList(list):
    
    def __getitem__(self,i):
      if i<0:
	return None
      else:
	return list.__getitem__(self,i)
   
      

class CustomList2D():
  def __init__(self,list):
    self.array=[]
    for t in list:
      self.array.append(CustomList(t))
    
  def append(self,a):
    self.array.append(CustomList(a))
  def __getitem__(self,i):
    if i<0:
	return None
    return self.array[i]
      
  def __str__(self):
    return str(self.array)
  
  def __len__(self):
    return len(self.array)
  
  def __cmp__(self,other):
    for i in range(len(self.array)):
      if self.array[i]!=other.array[i]:
	return -1
    return 0
#a=CustomList2D([[0, 1, 2, 3, 4, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [1, 1, 2, 3, 4, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [2, 2, 2, 3, 4, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [3, 3, 3, 3, 4, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [4, 4, 4, 4, 4, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [5, 5, 5, 5, 5, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]])
#b=CustomList2D([[0, 1, 2, 3, 4, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [1, 1, 2, 3, 4, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [2, 2, 2, 3, 4, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [3, 3, 3, 3, 4, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [4, 4, 4, 4, 4, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [5, 5, 5, 5, 5, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]])
#print a==b