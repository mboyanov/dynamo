class solutioninstance:
  def __init__(self,(table,path,answer)):
    self.show=False
    self.table=table
    self.path=path
    self.answer=answer
    if type(self.table)==type([]):
        self.length=len(self.table)
    else:
        self.length=len(self.table)*len(self.table[0])

    print type(self.table)