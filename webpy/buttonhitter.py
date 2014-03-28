import config
class buttonhitter:

    def __init__(self):
        self.db=config.getDB()

    def hitCommands(self):
        self.db.query("update buttonhits set count=count+1 where id=1")

    def hitMenus(self):
        self.db.query("update buttonhits set count=count+1 where id=2")

    def hitCorrectCommands(self):
        self.db.query("update buttonhits set count=count+1 where id=3")

    def hitCorrectMenus(self):
        self.db.query("update buttonhits set count=count+1 where id=4")

    def hitHints(self):
        self.db.query("update buttonhits set count=count+1 where id=5")