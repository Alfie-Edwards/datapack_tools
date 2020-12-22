import copy
import re

DEFAULT_STACK = []


class Scope:
   def __init__(self, val, *, stack=DEFAULT_STACK):
      self._stack = stack
      self._val = val

   def __enter__(self):
      self._depth = len(self._stack)
      self._stack.append(self._val)
      return self._val

   def __exit__(self, exc_type, exc_val, exc_tb):
      if len(self._stack) > (self._depth + 1):
         raise Exception("Not all inner scopes have been closed")
      if len(self._stack) < (self._depth + 1):
         raise Exception("This scope has already been closed")
      self._stack.pop()
      return False


class Tag(Scope):
   def __init__(self, key, val, *, overwrite=True, stack=DEFAULT_STACK):
      if len(stack) < 1 or not isinstance(stack[-1], dict):
         raise Exception("Tag can only be used within a dictionary scope")
      if not overwrite and key in stack[-1]:
         Scope.__init__(self, stack[-1][key], stack=stack)
      else:
         stack[-1][key] = val
         Scope.__init__(self, val, stack=stack)


class ListItem(Scope):
   def __init__(self, val, *, index=None, pad=None, overwrite=True, stack=DEFAULT_STACK):
      if len(stack) < 1 or not isinstance(stack[-1], list):
         raise Exception("ListItem can only be used within a list scope")
      if index is None:
         if pad is not None:
            raise Exception("Pad is only valid when an index is specified")
         overwrite = False
         index = len(stack[-1])
      if index < len(stack[-1]):
         if overwrite:
            stack[-1][index] = val
            Scope.__init__(self, val, stack=stack)
         else:
            Scope.__init__(self, stack[-1][index], stack=stack)
      else:
         if pad is not None:
            for _ in range(index - len(stack[-1])):
               stack[-1].append(copy.deepcopy(pad))
         stack[-1].append(val)
         Scope.__init__(self, val, stack=stack)


class RelativeScope:
   def __init__(self, path, *, stack=DEFAULT_STACK):
      self._stack = stack
      self._tokens = re.findall(r'(\w+|\d*\])(\.|\[)', path)
      self._subscopes = []

   def __len__(self):
      return len(self._tokens)

   def __enter__(self):
      for identifier, type_indicator in self._tokens:
         if type_indicator == '.':
            default_value = {}
         elif type_indicator == '[':
            default_value = []
         else:
            raise Exception("Unknown type indicator: {}".format(type_indicator))
         if identifier.endswith(']'):
            index = identifier.strip('[]')
            if len(index) > 0:
               subscope = ListItem(default_value, index=int(index), pad=default_value, overwrite=False, stack=self._stack)
            else:
               subscope = ListItem(default_value, overwrite=False, stack=self._stack)
         else:
            subscope = Tag(identifier, default_value, overwrite=False, stack=self._stack)
         subscope.__enter__()
         self._subscopes.append(subscope)

      return self._stack[-1]

   def __exit__(self, exc_type, exc_val, exc_tb):
      for _ in range(len(self)):
         self._subscopes.pop().__exit__(exc_type, exc_val, exc_tb)
      return False
