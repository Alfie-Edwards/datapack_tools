import random
import builtins

def uuid():
   return int_array(random.randrange(-(2**31),2**31) for _ in range(4))

def byte(b):
   return f"{builtins.int(b)}b"

def bool(b):
   return TRUE if b else FALSE

def short(s):
   return f"{builtins.int(s)}s"

def int(i):
   return str(builtins.int(i))

def long(l):
   return f"{builtins.int(s)}l"

def float(f):
   return f"{builtins.float(f)}f"

def double(d):
   return f"{builtins.float(d)}d"

def byte_array(*bytes):
   if len(bytes) == 1 and hasattr(bytes[0], '__iter__'):
      bytes = bytes[0]
   return f"[B;{','.join(byte(b) for b in bytes)}]"

def short_array(*shorts):
   if len(shorts) == 1 and hasattr(shorts[0], '__iter__'):
      shorts = shorts[0]
   return f"[S;{','.join(short(s) for s in shorts)}]"

def int_array(*ints):
   if len(ints) == 1 and hasattr(ints[0], '__iter__'):
      ints = ints[0]
   return f"[I;{','.join(int(i) for i in ints)}]"

def long_array(*longs):
   if len(longs) == 1 and hasattr(longs[0], '__iter__'):
      longs = longs[0]
   return f"[L;{','.join(long(l) for l in longs)}]"

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

# Constants

def _min_signed(bits):
   return -(2 ** (bits - 1))

def _max_signed(bits):
   return (2 ** (bits - 1)) - 1

TRUE = byte(1)
FALSE = byte(0)
MAX_INT = _max_signed(64)
MIN_INT = _min_signed(64)
MAX_INT = _max_signed(32)
MIN_INT = _min_signed(32)
MAX_SHORT = _max_signed(16)
MIN_SHORT = _min_signed(16)
MAX_BYTE = _max_signed(8)
MIN_BYTE = _min_signed(8)
