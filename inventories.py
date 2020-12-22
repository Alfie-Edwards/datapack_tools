import datapack_tools.data_types as dt
import datapack_tools.format as fm
from datapack_tools.scopes import *

class Inventory(list):
   def __init__(self):
      list.__init__(self)

def slot(slot, item):
   self = DEFAULT_STACK[-1]
   with Scope(item):
      Tag("Slot", dt.byte(slot))

   for i in range(len(self)):
      if self[i]["Slot"] == item["Slot"]:
         self[i] = item
         return
      elif self[i]["Slot"] > item["Slot"]:
         self.insert(i, item)
         return
   self.append(item)
