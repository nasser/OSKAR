import sys
import os
import io
import string
import random

# https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
def temp_name(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def usage():
  print("usage: python3 oskar.py in.osk out.scad")

# fail on less than two arguments, otherwise store as infile outfile
if len(sys.argv) < 3:
  usage()
  exit()
[_, infile, outfile] = sys.argv

# generate name to store generated python code
tempPythonFile = temp_name() + ".py"

# run compiler to generate python file
os.system("runhaskell oskar_to_python/oskar_compiler.hs %s %s" % (infile, tempPythonFile))

# run generated python
exec(open(tempPythonFile).read())

# output the file to outfile
# the scene variable is defined in the generated python
scene.generateCode(outfile)

# remove temp file
os.remove(tempPythonFile)