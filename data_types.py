import random
import builtins

def uuid():
   return int_list(random.randrange(-(2**31),2**31) for _ in range(4))

def byte(b):
   return f"{builtins.int(b)}b"

TRUE = byte(1)
FALSE = byte(0)

def bool(b):
   return TRUE if b else FALSE

def short(s):
   return f"{builtins.int(s)}s"

def int(i):
   return str(builtins.int(i))

def float(f):
   return f"{builtins.float(f)}f"

def int_list(*ints):
   if len(ints) == 1 and hasattr(ints[0], '__iter__'):
      ints = ints[0]
   return f"[I;{','.join(int(i) for i in ints)}]"

def string(s):
   return f'"{s}"'

def auto(value):
   if isinstance(value, str):
      return string(value)
   if isinstance(value, bool):
      return bool(value)
   if isinstance(value, int):
      return int(value)
   if isinstance(value, float):
      return float(value)
   raise ValueError(f"Unable to determine a minecraft json type for {type(value)}")
