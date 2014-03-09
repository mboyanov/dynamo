from xhtml2pdf import pisa             # import python module
import web
import config
class pdfgenerator:
# Define your data
  def generateHtmlFromId(self,name,id):
    db = config.getDB()
    data={}
    data['id']=id
    achievementdata=db.select('achievements',data,where='id=$id')
    achievementdata=achievementdata[0]
    return self.generateHtml(name,achievementdata['title'],achievementdata['url'])
  
  
  def generateHtml(self,name,title,img):
    f=open('rewards.html','r')
    text=f.read().format(name,title,img)
    f.close()
    return text

  def convertHtmlToPdf(self,sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err





