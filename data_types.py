import random
import builtins
import re

# Type test functions.

def _is_string_matching(x, pattern):
   return isinstance(x, builtins.str) and re.match(pattern, x)

def is_byte(x):
   return _is_string_matching(x, r"^\\d+[bB]$")

def is_short(x):
   return _is_string_matching(x, r"^\d+[sS]$")

def is_int(x):
   return _is_string_matching(x, r"^\d+$")

def is_long(x):
   return _is_string_matching(x, r"^\d+[lL]$")

def is_float(x):
   return _is_string_matching(x, r"^\d+[fF]$")

def is_double(x):
   return _is_string_matching(x, r"^\d+[dD]$")

def is_byte_array(x):
   return _is_string_matching(x, r"^\[B;((\d+[bB],)*\d+[bB])?\]$")

def is_short_array(x):
   return _is_string_matching(x, r"^\[S;((\d+[sS],)*\d+[sS])?\]$")

def is_int_array(x):
   return _is_string_matching(x, r"^\[I;((\d+,)*\d+)?\]$")

def is_long_array(x):
   return _is_string_matching(x, r"^\[L;((\d+[lL],)*\d+[lL])?\]$")

def is_string(x):
   return isinstance(x, builtins.str)

_TYPE_TEST_FUNCTIONS = [
   is_byte
   is_short
   is_int
   is_long
   is_float
   is_double
   is_byte_array
   is_short_array
   is_int_array
   is_long_array
   is_string
]

# Types.

def uuid():
   return int_array(random.randrange(-(2**31),2**31) for _ in range(4))

def byte(b):
   if is_byte(b):
      return b
   return f"{builtins.int(b)}b"

TRUE = byte(1)
FALSE = byte(0)

def bool(b):
   if is_byte(b):
      return b
   return TRUE if b else FALSE

def short(s):
   if is_short(s):
      return s
   return f"{builtins.int(s)}s"

def int(i):
   if is_int(i):
      return i
   return str(builtins.int(i))

def long(l):
   if is_long(l):
      return l
   return f"{builtins.int(l)}l"

def float(f):
   if is_float(f):
      return f
   return f"{builtins.float(f)}f"

def double(d):
   if is_double(d):
      return d
   return f"{builtins.float(d)}d"

def byte_array(*bytes):
   if len(bytes) == 1 and is_byte_array(bytes[0]):
      return bytes[0]
   if len(bytes) == 1 and hasattr(bytes[0], '__iter__'):
      bytes = bytes[0]
   return f"[B;{','.join(byte(b) for b in bytes)}]"

def short_array(*shorts):
   if len(shorts) == 1 and is_short_array(shorts[0]):
      return shorts[0]
   if len(shorts) == 1 and hasattr(shorts[0], '__iter__'):
      shorts = shorts[0]
   return f"[S;{','.join(short(s) for s in shorts)}]"

def int_array(*ints):
   if len(ints) == 1 and is_int_array(ints[0]):
      return ints[0]
   if len(ints) == 1 and hasattr(ints[0], '__iter__'):
      ints = ints[0]
   return f"[I;{','.join(int(i) for i in ints)}]"

def long_array(*longs):
   if len(longs) == 1 and is_long_array(longs[0]):
      return longs[0]
   if len(longs) == 1 and hasattr(longs[0], '__iter__'):
      longs = longs[0]
   return f"[L;{','.join(long(l) for l in longs)}]"

def string(s):
   return f'"{s}"'

def auto(value):
   if isinstance(value, builtins.bool):
      return bool(value)
   if isinstance(value, builtins.int):
      return int(value)
   if isinstance(value, builtins.float):
      return float(value)
   if any(f(value) for f in _TYPE_TEST_FUNCTIONS):
      return value
   raise ValueError(f"Unable to determine a minecraft json type for {type(value)}")

# Constants.

def _min_signed(bits):
   return -(2 ** (bits - 1))

def _max_signed(bits):
   return (2 ** (bits - 1)) - 1

MAX_LONG = _max_signed(64)
MIN_LONG = _min_signed(64)
MAX_INT = _max_signed(32)
MIN_INT = _min_signed(32)
MAX_SHORT = _max_signed(16)
MIN_SHORT = _min_signed(16)
MAX_BYTE = _max_signed(8)
MIN_BYTE = _min_signed(8)
