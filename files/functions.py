from subprocess import Popen, PIPE

def checkQuestion(file, inputValue, outputValue):
    proc = Popen(["python", "files/code/"+file+".py"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    try:
      stdout, stderr = proc.communicate(input=inputValue.encode('UTF-8'),timeout=2)
      if stderr.decode('UTF-8') != "":
        return [False,stderr.decode('UTF-8')]
      elif stdout.decode('UTF-8') == outputValue:
        return [True,stdout.decode('UTF-8')]
      else:
        return [False,"Wrong Output recieved: "+stdout.decode('UTF-8')[0:200]]
    except:
      return [False,"timed out too slow"]
