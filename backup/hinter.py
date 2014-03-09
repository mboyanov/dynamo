import re
class hinter:
  def hint(self,expr,level):
    out=""
    print "received",expr
    if len(expr)>300:
      return None
    commands=re.split('[\n\r]+',expr)
    if len(commands)>6:
      return None
    for i in commands:
      ok=self.check_input(i)
      if not ok:
	print "NOT OK",len(commands),'x'+i+'x'
	return None
      else:
	out+=self.hintline(i,level)+'\n'
    print "returning",out
    return out
  
  
  def check_input(self,expr):
    if '=' not in expr:
      return False
    return True
    
  def hintline(self,line,level):
    if level==0:
      return ''
    elif level==1:
      out=""
      left=0
      for i in line:
	if i=='=':
	  out+='=?'
	  break
	elif i=='[':
	  out+='['
	  left+=1
	  if left==1:
	    out+='?'
	elif i==']':
	  out+=']'
	  left-=1
	elif left==0:
	  out+=i
      return out
    elif level==2:
      out=""
      left=0
      for i in range(len(line)):
	if line[i:i+3]=='for':
	  out+='for ?'
	  break
	elif line[i]=='[':
	  out+='['
	  left+=1
	  if left==1:
	    out+='?'
	elif line[i]==']':
	  out+=']'
	  left-=1
	elif left==0:
	  out+=line[i]
      return out
    elif level==3:
	return line
    
a=hinter()
expr='T[0]=1'
expr1='T[i]=T[i-1]+1 for i in 1:N'
assert(a.hintline(expr,0)=='')
assert(a.hintline(expr,1)=='T[?]=?')
assert(a.hintline(expr1,2)=='T[?]=T[?]+1 for ?')
assert(a.hint(expr+'\n'+expr1,0)=='\n\n')
