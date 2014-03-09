class problem:
  content=""
  lists={}
  constants={}
  def __init__(self, content,listpairs, constants,dimensions,solution,tableexplanation,hints=None,video=None):
    self.content=content
    self.lists={}
    self.lists=listpairs
    self.constants={}
    self.constants=constants
    self.tableexplanation=tableexplanation
    self.dimensions=dimensions
    self.solution=solution
    self.hints=hints
    self.video=video
  
