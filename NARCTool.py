import sys
from NARC import *

if sys.argv[1].lower() == "extract":
  NARC_Unpack(sys.argv[2], sys.argv[3])
elif sys.argv[1].lower() == "compile":
  NARC_Pack(sys.argv[2], sys.argv[3])
