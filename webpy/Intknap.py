class intknap:

  
  def __init__(self,weights,values,c):
    self.weights=weights
    self.values=values
    self.table=[0]
    self.show=False
    for i in range(1,c+1):
      maxt=self.table[i-1]
      for t in range(len(self.weights)):
	if self.weights[t]<=i and self.table[i-self.weights[t]]+self.values[t]>maxt:
	  maxt=self.table[i-weights[t]]+values[t]
      self.table.append(maxt)
      
  