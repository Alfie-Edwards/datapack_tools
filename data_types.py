import random
import builtins

def uuid():
   return int_list(random.randrange(-(2**31),2**31) for _ in range(4))

def byte(b):
   return "{}b".format(builtins.int(b))

TRUE = byte(1)
FALSE = byte(0)

def bool(b):
   return TRUE if b else FALSE

def short(s):
   return "{}s".format(builtins.int(s))

def int(i):
   return str(builtins.int(i))

def float(f):
   return "{}f".format(builtins.float(f))

def int_list(*ints):
   if len(ints) == 1 and hasattr(ints[0], '__iter__'):
      ints = ints[0]
   return "[I;{}]".format(",".join(int(i) for i in ints))

def string(s):
   return '"{}"'.format(s)